from datetime import date as date_type, datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
    func,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship, object_session

from app.db.engine import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class TradeType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CAD = "CAD"
    AUD = "AUD"
    CHF = "CHF"
    CNY = "CNY"
    INR = "INR"


class Portfolio(Base):
    __tablename__ = "portfolios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    currency: Mapped[Currency] = mapped_column(nullable=False, default=Currency.USD)
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User", back_populates="portfolios", foreign_keys=[user_id], lazy="select"
    )
    holding_performances: Mapped[list["PortfolioHoldingPerformance"]] = relationship(
        "PortfolioHoldingPerformance",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    trading_histories: Mapped[list["PortfolioTradingHistory"]] = relationship(
        "PortfolioTradingHistory",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    dividend_histories: Mapped[list["PortfolioDividendHistory"]] = relationship(
        "PortfolioDividendHistory",
        back_populates="portfolio",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    @property
    def total_invested(self) -> float:
        """Calculate total amount invested across all holdings."""
        return sum(holding.total_invested for holding in self.holding_performances)

    @property
    def total_value(self) -> float:
        """Calculate current total value of all holdings."""
        return sum(holding.current_value for holding in self.holding_performances)

    @property
    def total_gain_loss(self) -> float:
        """Calculate total gain/loss across all holdings."""
        return self.total_value - self.total_invested

    @property
    def dividends_received(self) -> float:
        """Calculate total dividends received."""
        return sum(dividend.dividend_amount for dividend in self.dividend_histories)

    @property
    def total_return_percentage(self) -> float:
        """Calculate total return percentage including dividends."""
        if self.total_invested == 0:
            return 0.0
        return (
            (self.total_value + self.dividends_received - self.total_invested)
            / self.total_invested
        ) * 100

    def __repr__(self):
        return f"<Portfolio(name={self.name}, user_id={self.user_id})>"


class PortfolioHoldingPerformance(Base):
    __tablename__ = "portfolio_holding_performances"
    __table_args__ = (
        UniqueConstraint("portfolio_id", "symbol", name="uq_portfolio_holding"),
        Index("ix_holding_portfolio_symbol", "portfolio_id", "symbol"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    currency: Mapped[Currency] = mapped_column(nullable=False, default=Currency.USD)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio",
        back_populates="holding_performances",
        foreign_keys=[portfolio_id],
        lazy="select",
    )

    def _get_trades_by_type(
        self, trade_type: TradeType
    ) -> list["PortfolioTradingHistory"]:
        """Helper method to get trades for this holding by trade type."""
        return [
            trade
            for trade in self.portfolio.trading_histories
            if trade.symbol == self.symbol and trade.trade_type == trade_type
        ]

    @property
    def buy_trades(self) -> list["PortfolioTradingHistory"]:
        """Get all buy trades for this holding."""
        return self._get_trades_by_type(TradeType.BUY)

    @property
    def sell_trades(self) -> list["PortfolioTradingHistory"]:
        """Get all sell trades for this holding."""
        return self._get_trades_by_type(TradeType.SELL)

    @property
    def total_shares(self) -> float:
        """Calculate total shares from trading history."""
        shares_bought = sum(trade.shares for trade in self.buy_trades)
        shares_sold = sum(trade.shares for trade in self.sell_trades)
        return shares_bought - shares_sold

    @property
    def adjusted_total_cost(self) -> float:
        """Compute adjusted total cost (average cost method)."""
        buy_total = sum(trade.net_total for trade in self.buy_trades)
        buy_shares = sum(trade.shares for trade in self.buy_trades)
        if buy_shares == 0:
            return 0.0

        avg_cost = buy_total / buy_shares

        # Subtract the cost basis for sold shares
        shares_sold = sum(trade.shares for trade in self.sell_trades)
        cost_sold = shares_sold * avg_cost

        return max(buy_total - cost_sold, 0.0)

    @property
    def average_cost_per_share(self) -> float:
        """Calculate average cost per share from buy transactions."""
        total_shares = self.total_shares
        if total_shares <= 0:
            return 0.0
        return self.adjusted_total_cost / total_shares

    @property
    def total_invested(self) -> float:
        """
        Calculate the current cost basis of held shares using average cost method.
        This represents the invested capital in currently held shares.
        """
        return self.adjusted_total_cost

    def set_current_price(self, price: float) -> None:
        """Set the current price (pre-loaded to avoid N+1 queries)."""
        self._current_price = price

    def _get_current_price(self) -> float:
        """Fetch the latest stock price from the database."""
        # Return pre-loaded price if available (set by service for bulk loading)
        if hasattr(self, "_current_price"):
            return self._current_price

        session = object_session(self)
        if not session:
            return 0.0

        from app.db.models.quote import StockPrice

        # Get the most recent stock price for this symbol
        stmt = (
            select(StockPrice)
            .where(StockPrice.symbol == self.symbol)
            .order_by(StockPrice.date.desc())
            .limit(1)
        )

        result = session.execute(stmt).scalar_one_or_none()

        if result:
            return result.close_price
        return 0.0

    @property
    def current_price(self) -> float:
        """Get the current/latest price for this stock."""
        return self._get_current_price()

    @property
    def current_value(self) -> float:
        """Calculate current value of this holding based on latest price."""
        price = self.current_price
        if price == 0.0:
            return self.total_invested
        return self.total_shares * price

    @property
    def realized_gain_loss(self) -> float:
        """Total realized gain/loss from all sell trades (average cost method)."""
        buy_total = sum(trade.net_total for trade in self.buy_trades)
        buy_shares = sum(trade.shares for trade in self.buy_trades)
        if buy_shares == 0:
            return 0.0

        avg_cost = buy_total / buy_shares
        realized_gain = 0.0

        for trade in self.sell_trades:
            proceeds = trade.net_total
            cost_basis = trade.shares * avg_cost
            realized_gain += proceeds - cost_basis

        return realized_gain

    @property
    def unrealized_gain_loss(self) -> float:
        """Gain/loss for shares still held (unrealized)."""
        current_value = self.current_value
        total_cost = self.adjusted_total_cost
        return current_value - total_cost

    @property
    def total_gain_loss(self) -> float:
        """Combined realized + unrealized gain/loss."""
        return self.realized_gain_loss + self.unrealized_gain_loss

    @property
    def gain_loss_percentage(self) -> float:
        """Percentage gain/loss based on total cost invested."""
        invested = self.adjusted_total_cost
        if invested == 0:
            return 0.0
        return (self.unrealized_gain_loss / invested) * 100

    @property
    def allocation_percentage(self) -> float:
        """Calculate allocation percentage of this holding in the portfolio."""
        portfolio_total = self.portfolio.total_invested
        if portfolio_total == 0:
            return 0.0
        return (self.total_invested / portfolio_total) * 100

    def __repr__(self):
        return f"<PortfolioHoldingPerformance(portfolio_id={self.portfolio_id}, symbol={self.symbol})>"


class PortfolioTradingHistory(Base):
    __tablename__ = "portfolio_trading_histories"
    __table_args__ = (
        Index("ix_portfolio_symbol_trade_date", "portfolio_id", "symbol", "trade_date"),
        CheckConstraint("shares > 0", name="check_positive_trade_shares"),
        CheckConstraint("price_per_share >= 0", name="check_positive_price"),
        CheckConstraint("commission >= 0", name="check_positive_commission"),
        CheckConstraint("fees >= 0", name="check_positive_fees"),
        CheckConstraint("tax >= 0", name="check_positive_tax"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), index=True, nullable=False
    )
    trade_type: Mapped[TradeType] = mapped_column(nullable=False)
    currency: Mapped[Currency] = mapped_column(nullable=False, default=Currency.USD)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    shares: Mapped[float] = mapped_column(nullable=False)
    price_per_share: Mapped[float] = mapped_column(nullable=False)
    total_value: Mapped[float] = mapped_column(nullable=False)
    commission: Mapped[float] = mapped_column(nullable=False, default=0.0)
    fees: Mapped[float] = mapped_column(nullable=False, default=0.0)
    tax: Mapped[float] = mapped_column(nullable=False, default=0.0)
    net_total: Mapped[float] = mapped_column(nullable=False)
    notes: Mapped[str | None] = mapped_column(String(500), nullable=True, default=None)
    trade_date: Mapped[date_type] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio",
        back_populates="trading_histories",
        foreign_keys=[portfolio_id],
        lazy="select",
    )

    def __repr__(self):
        return f"<PortfolioTradingHistory(portfolio_id={self.portfolio_id}, symbol={self.symbol}, trade_type={self.trade_type})>"


class PortfolioDividendHistory(Base):
    __tablename__ = "portfolio_dividend_histories"
    __table_args__ = (
        Index(
            "ix_portfolio_symbol_payment_date", "portfolio_id", "symbol", "payment_date"
        ),
        CheckConstraint("shares >= 0", name="check_positive_dividend_shares"),
        CheckConstraint("dividend_per_share >= 0", name="check_positive_dps"),
        CheckConstraint("dividend_amount >= 0", name="check_positive_dividend_amount"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.id", ondelete="CASCADE"), index=True, nullable=False
    )
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    shares: Mapped[float] = mapped_column(nullable=False, default=0.0)
    dividend_per_share: Mapped[float] = mapped_column(nullable=False, default=0.0)
    dividend_amount: Mapped[float] = mapped_column(nullable=False, default=0.0)
    currency: Mapped[Currency] = mapped_column(nullable=False, default=Currency.USD)
    declaration_date: Mapped[date_type] = mapped_column(Date, nullable=False)
    payment_date: Mapped[date_type] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    portfolio: Mapped["Portfolio"] = relationship(
        "Portfolio",
        back_populates="dividend_histories",
        foreign_keys=[portfolio_id],
        lazy="select",
    )

    def __repr__(self):
        return f"<PortfolioDividendHistory(portfolio_id={self.portfolio_id}, symbol={self.symbol}, dividend_amount={self.dividend_amount})>"
