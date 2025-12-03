import json
import logging
from datetime import date as date_type, timedelta

from sqlalchemy.orm import Session

from app.repositories.company_repo import CompanyRepository
from app.repositories.quotes_repo import CompanyQuotesRepository
from app.schemas.quote import (
    CompanyEarningsCalendarRead,
    IndexQuoteRead,
    CompanyDividendRead,
)
from app.schemas.user import DashboardResponse, StockSymbol
from app.services.portfolio_service import PortfolioService

logger = logging.getLogger(__name__)


class DashboardService:
    """Service for dashboard-related operations."""

    def __init__(self, session: Session) -> None:
        self._session = session
        self._quotes_repo = CompanyQuotesRepository(session)
        self._portfolio_service = PortfolioService(session)
        self._company_repository = CompanyRepository(session)

    @staticmethod
    def _validate_models(schema_class, items):
        """Helper to validate a list of ORM models against a Pydantic schema."""
        if not items:
            return []
        return [schema_class.model_validate(item) for item in items]

    def get_dashboard_summary(self, user_id: int) -> DashboardResponse:
        """
        Get summary data for the user's dashboard.
        Returns a valid DashboardResponse even if there are errors retrieving individual components.
        """
        try:
            earnings_calendar_read = self._get_earnings_calendar()
            dividend_calendar_read = self._get_dividend_calendar()
            index_quotes_read = self._get_index_quotes()
            combined_portfolio = self._get_combined_portfolio(user_id)

            index_quotes_read = self._validate_models(IndexQuoteRead, index_quotes_read)
            return DashboardResponse(
                total_portfolios=combined_portfolio.get("total_portfolios", 0),
                total_invested=combined_portfolio.get("total_invested", 0.0),
                total_current_value=combined_portfolio.get("current_value", 0.0),
                total_profit_loss=combined_portfolio.get("profit_loss", 0.0),
                gain_loss_percentage=combined_portfolio.get(
                    "gain_loss_percentage", 0.0
                ),
                total_dividends=combined_portfolio.get("total_dividends", 0.0),
                earnings_calendar=earnings_calendar_read,
                dividends_calendar=dividend_calendar_read,
                index_quotes=index_quotes_read,
            )
        except Exception as e:
            logger.error(f"Error getting dashboard summary for user {user_id}: {e}")
            # Return a default DashboardResponse instead of None
            return DashboardResponse(
                total_portfolios=0,
                total_invested=0.0,
                total_current_value=0.0,
                total_profit_loss=0.0,
                gain_loss_percentage=0.0,
                total_dividends=0.0,
                earnings_calendar=[],
                dividends_calendar=[],
                index_quotes=[],
            )

    def get_all_stock_symbols(self) -> list[StockSymbol]:
        """Retrieve all stock symbols available in the system."""

        # Get all symbols in database for quick lookup
        db_companies = self._company_repository.get_all_companies()
        non_us_companies = self._company_repository.get_all_non_us_companies()
        db_symbols = {company.symbol for company in db_companies}
        non_us_symbols = {company[0] for company in non_us_companies}
        # Read from file
        us_stocks = []
        non_us_stocks = []
        with open("app/data/stocks.json", "r") as f:
            stocks = json.load(f)
            us_stocks = [
                StockSymbol(**stock, is_in_db=stock["symbol"] in db_symbols)
                for stock in stocks
            ]
        with open("app/data/jp_stocks.json", "r") as f:
            stocks = json.load(f)
            non_us_stocks = [
                StockSymbol(**stock, is_in_db=stock["symbol"] in non_us_symbols)
                for stock in stocks
            ]
        all_stocks = us_stocks + non_us_stocks
        return all_stocks

    def _get_earnings_calendar(self) -> list[CompanyEarningsCalendarRead]:
        """Retrieve earnings calendar entries within a date range."""
        week_ago = date_type.today() - timedelta(days=7)
        two_months_after = date_type.today() + timedelta(days=60)
        week_ago_str = week_ago.strftime("%Y-%m-%d")
        two_months_after_str = two_months_after.strftime("%Y-%m-%d")
        earnings_calendar = self._quotes_repo.get_earnings_calendar(
            from_date=week_ago_str, to_date=two_months_after_str
        )
        earnings_calendar_read = self._validate_models(
            CompanyEarningsCalendarRead, earnings_calendar
        )
        return earnings_calendar_read

    def _get_dividend_calendar(self) -> list[CompanyDividendRead]:
        """Retrieve dividend calendar entries within a date range."""
        week_ago = date_type.today() - timedelta(days=7)
        two_months_after = date_type.today() + timedelta(days=60)
        week_ago_str = week_ago.strftime("%Y-%m-%d")
        two_months_after_str = two_months_after.strftime("%Y-%m-%d")
        dividend_calendar = self._quotes_repo.get_dividend_calendar(
            from_date=week_ago_str, to_date=two_months_after_str
        )
        dividend_calendar_read = self._validate_models(
            CompanyDividendRead, dividend_calendar
        )
        return dividend_calendar_read

    def _get_index_quotes(self) -> list[IndexQuoteRead]:
        """Retrieve index quotes for major indices."""
        index_quotes = self._quotes_repo.get_index_quotes()
        index_quotes_read = self._validate_models(IndexQuoteRead, index_quotes)
        return index_quotes_read

    def _get_combined_portfolio(self, user_id: int) -> dict:
        """Retrieve combined portfolio data for the user."""
        # Placeholder for combined portfolio retrieval logic

        all_portfolios = self._portfolio_service.get_all_portfolios(user_id)
        total_invested = 0.0
        total_current_value = 0.0
        total_profit_loss = 0.0
        total_dividends = 0.0
        for portfolio in all_portfolios:
            portfolio_snapshot = self._portfolio_service.get_portfolio_snapshot(
                portfolio.id, user_id
            )
            if portfolio_snapshot:
                total_invested += portfolio_snapshot.total_invested
                total_current_value += portfolio_snapshot.total_value
                total_profit_loss += portfolio_snapshot.total_gain_loss
                total_dividends += portfolio_snapshot.dividends_received
        total_profit_loss_percent = (
            (total_profit_loss / total_invested) * 100 if total_invested > 0 else 0.0
        )
        combined_portfolio = {
            "total_portfolios": len(all_portfolios),
            "total_invested": total_invested,
            "current_value": total_current_value,
            "profit_loss": total_profit_loss,
            "gain_loss_percentage": total_profit_loss_percent,
            "total_dividends": total_dividends,
        }
        return combined_portfolio
