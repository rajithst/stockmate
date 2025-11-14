import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.dividend import CompanyDividend
from app.db.models.quote import CompanyStockPrice, CompanyStockPriceChange
from app.db.models.stock import CompanyStockPeer, CompanyStockSplit
from app.db.models.technical_indicators import CompanyTechnicalIndicator
from app.schemas.quote import (
    CompanyDividendWrite,
    CompanyStockPeerWrite,
    CompanyStockSplitWrite,
    CompanyTechnicalIndicatorWrite,
    StockPriceChangeWrite,
    StockPriceWrite,
)
from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)


class CompanyQuoteSyncRepository:
    """Repository for quote and stock info entities (price change, daily price, stock splits, stock peers)."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def upsert_price_change(
        self, price_change: StockPriceChangeWrite
    ) -> CompanyStockPriceChange:
        """Upsert price change record by symbol."""
        try:
            # Find existing record
            existing = (
                self._db.query(CompanyStockPriceChange)
                .filter_by(symbol=price_change.symbol)
                .first()
            )

            if existing:
                # Update existing
                result = map_model(existing, price_change)
            else:
                # Create new
                result = CompanyStockPriceChange(
                    **price_change.model_dump(exclude_unset=True)
                )
                self._db.add(result)

            self._db.commit()
            self._db.refresh(result)

            logger.info(f"Upserted price change for symbol {price_change.symbol}")
            return result
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_price_change: {e}")
            raise

    def upsert_daily_price(self, daily_price: StockPriceWrite) -> CompanyStockPrice:
        """Bulk upsert daily price records by symbol and date."""
        try:
            # Find existing record
            existing = (
                self._db.query(CompanyStockPrice)
                .filter_by(symbol=daily_price.symbol, date=daily_price.date)
                .first()
            )

            if existing:
                # Update existing
                result = map_model(existing, daily_price)
            else:
                # Create new
                result = CompanyStockPrice(**daily_price.model_dump(exclude_unset=True))
                self._db.add(result)

            self._db.commit()
            self._db.refresh(result)

            logger.info(f"Upserted daily price for symbol {daily_price.symbol}")
            return result
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_daily_price: {e}")
            raise

    def upsert_stock_splits(
        self, splits_data: list[CompanyStockSplitWrite]
    ) -> list[CompanyStockSplit]:
        """Bulk upsert stock split records by symbol and date."""
        try:
            results = []
            for split_in in splits_data:
                # Find existing record
                existing = (
                    self._db.query(CompanyStockSplit)
                    .filter_by(symbol=split_in.symbol, date=split_in.date)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, split_in)
                else:
                    # Create new
                    result = CompanyStockSplit(
                        **split_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} stock split records")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_stock_splits: {e}")
            raise

    def upsert_stock_peers(
        self, peers_data: list[CompanyStockPeerWrite]
    ) -> list[CompanyStockPeer]:
        """Bulk upsert stock peer records by symbol and company_id."""
        try:
            results = []
            for peer_in in peers_data:
                # Find existing record
                existing = (
                    self._db.query(CompanyStockPeer)
                    .filter_by(symbol=peer_in.symbol, company_id=peer_in.company_id)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, peer_in)
                else:
                    # Create new
                    result = CompanyStockPeer(**peer_in.model_dump(exclude_unset=True))
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} stock peer records")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_stock_peers: {e}")
            raise

    def upsert_dividends(
        self, dividends_data: list[CompanyDividendWrite]
    ) -> list[CompanyDividend]:
        """Upsert multiple dividend records."""
        try:
            results = []
            for dividend_in in dividends_data:
                # Find existing record
                existing = (
                    self._db.query(CompanyDividend)
                    .filter_by(symbol=dividend_in.symbol, date=dividend_in.date)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, dividend_in)
                else:
                    # Create new
                    result = CompanyDividend(
                        **dividend_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} dividend records")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_dividends: {e}")
            raise

    def upsert_technical_indicators(
        self, technical_indicators_in: list[CompanyTechnicalIndicatorWrite]
    ) -> list[CompanyTechnicalIndicator]:
        """Upsert multiple technical indicator records."""
        try:
            results = []
            for indicator_in in technical_indicators_in:
                # Find existing record
                existing = (
                    self._db.query(CompanyTechnicalIndicator)
                    .filter_by(symbol=indicator_in.symbol, date=indicator_in.date)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, indicator_in)
                else:
                    # Create new
                    result = indicator_in.__class__(
                        **indicator_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} technical indicator records")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_technical_indicators: {e}")
            raise
