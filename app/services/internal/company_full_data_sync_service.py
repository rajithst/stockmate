"""Comprehensive company data sync service for syncing all company data at once."""

import logging
import time
from datetime import datetime

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
from app.services.internal.company_sync_service import CompanySyncService
# from app.services.internal.dcf_sync_service import DiscountedCashFlowSyncService
# from app.services.internal.financial_sync_service import FinancialSyncService
# from app.services.internal.grading_sync_service import GradingSyncService
# from app.services.internal.metrics_sync_service import MetricsSyncService
# from app.services.internal.price_target_sync_service import PriceTargetSyncService
# from app.services.internal.quotes_sync_service import QuotesSyncService
# from app.services.internal.rating_sync_service import RatingSyncService
# from app.services.internal.stock_info_sync_service import StockInfoSyncService

logger = logging.getLogger(__name__)

# Sleep time between API calls (in seconds) to respect rate limits
DEFAULT_SLEEP_TIME = 0.5


class CompanyFullDataSyncService:
    """Service for syncing all company data from FMP to database."""

    def __init__(
        self,
        market_api_client: FMPClientProtocol,
        session: Session,
        sleep_time: float = DEFAULT_SLEEP_TIME,
    ) -> None:
        self._session = session
        self._sleep_time = sleep_time
        self._company_repo = CompanyRepository(session)

        # Initialize all sync services
        self._company_sync = CompanySyncService(market_api_client, session)
        # self._quotes_sync = QuotesSyncService(market_api_client, session)
        # self._price_target_sync = PriceTargetSyncService(market_api_client, session)
        # self._rating_sync = RatingSyncService(market_api_client, session)
        # self._grading_sync = GradingSyncService(market_api_client, session)
        # self._dcf_sync = DiscountedCashFlowSyncService(market_api_client, session)
        # self._metrics_sync = MetricsSyncService(market_api_client, session)
        # self._financials_sync = FinancialSyncService(market_api_client, session)
        # self._stock_info_sync = StockInfoSyncService(market_api_client, session)

    def _sleep(self, reason: str = "") -> None:
        """Sleep to respect API rate limits."""
        if self._sleep_time > 0:
            logger.debug(f"Sleeping {self._sleep_time}s {reason}")
            time.sleep(self._sleep_time)

    def sync_all_company_data(
        self,
        symbol: str,
        financial_limit: int = 40,
        metrics_limit: int = 40,
        include_news: bool = False,
    ) -> dict:
        """
        Sync all company data from FMP.

        Syncs in this order:
        1. Company profile
        2. Price change
        3. Price targets
        4. Ratings
        5. Gradings
        6. DCF valuation
        7. Key metrics
        8. Financial ratios
        9. Income statements
        10. Balance sheets
        11. Cash flow statements
        12. Stock peers
        13. Stock splits
        14. Grading summary
        15. Price target summary
        16. Financial Health

        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            financial_limit: Number of financial records to fetch
            metrics_limit: Number of metric records to fetch
            include_news: Whether to sync company news (slower)

        Returns:
            Dictionary with sync results and timing information
        """
        start_time = datetime.now()
        results = {
            "symbol": symbol,
            "status": "in_progress",
            "steps": {},
            "total_api_calls": 0,
            "total_time_seconds": 0,
        }

        try:
            # Step 1: Company Profile
            logger.info(f"[1/13] Syncing company profile for {symbol}")
            try:
                self._company_sync.upsert_company(symbol)
                results["steps"]["company_profile"] = "success"
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync company profile: {e}")
                results["steps"]["company_profile"] = f"failed: {str(e)}"
            self._sleep("after company profile")

            # Step 2: Price Change
            logger.info(f"[2/13] Syncing price change for {symbol}")
            try:
                self._quotes_sync.upsert_price_change(symbol)
                results["steps"]["price_change"] = "success"
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync price change: {e}")
                results["steps"]["price_change"] = f"failed: {str(e)}"
            self._sleep("after price change")

            # Step 3: Price Targets
            logger.info(f"[3/13] Syncing price targets for {symbol}")
            try:
                targets = self._price_target_sync.upsert_price_target(symbol)
                results["steps"]["price_targets"] = (
                    f"success ({1 if targets else 0} records)"
                )
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync price targets: {e}")
                results["steps"]["price_targets"] = f"failed: {str(e)}"
            self._sleep("after price targets")

            # Step 4: Ratings
            logger.info(f"[4/13] Syncing ratings for {symbol}")
            try:
                self._rating_sync.upsert_rating_summary(symbol)
                results["steps"]["ratings"] = "success"
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync ratings: {e}")
                results["steps"]["ratings"] = f"failed: {str(e)}"
            self._sleep("after ratings")

            # Step 5: Gradings
            logger.info(f"[5/13] Syncing gradings for {symbol}")
            try:
                gradings = self._grading_sync.upsert_gradings(symbol)
                results["steps"]["gradings"] = (
                    f"success ({len(gradings) if gradings else 0} records)"
                )
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync gradings: {e}")
                results["steps"]["gradings"] = f"failed: {str(e)}"
            self._sleep("after gradings")

            # Step 6: DCF Valuation
            logger.info(f"[6/13] Syncing DCF valuation for {symbol}")
            try:
                self._dcf_sync.upsert_discounted_cash_flow(symbol)
                results["steps"]["dcf"] = "success"
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync DCF: {e}")
                results["steps"]["dcf"] = f"failed: {str(e)}"
            self._sleep("after DCF")

            # Step 7: Key Metrics
            logger.info(f"[7/13] Syncing key metrics for {symbol}")
            try:
                metrics = self._metrics_sync.upsert_key_metrics(
                    symbol, metrics_limit, "annual"
                )
                results["steps"]["key_metrics"] = (
                    f"success ({len(metrics) if metrics else 0} records)"
                )
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync key metrics: {e}")
                results["steps"]["key_metrics"] = f"failed: {str(e)}"
            self._sleep("after key metrics")

            # Step 8: Financial Ratios
            logger.info(f"[8/13] Syncing financial ratios for {symbol}")
            try:
                ratios = self._metrics_sync.upsert_financial_ratios(
                    symbol, metrics_limit, "annual"
                )
                results["steps"]["financial_ratios"] = (
                    f"success ({len(ratios) if ratios else 0} records)"
                )
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync financial ratios: {e}")
                results["steps"]["financial_ratios"] = f"failed: {str(e)}"
            self._sleep("after financial ratios")

            # Step 9: Income Statements
            logger.info(f"[9/13] Syncing income statements for {symbol}")
            try:
                statements = self._financials_sync.upsert_income_statements(
                    symbol, financial_limit, "annual"
                )
                results["steps"]["income_statements"] = (
                    f"success ({len(statements) if statements else 0} records)"
                )
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync income statements: {e}")
                results["steps"]["income_statements"] = f"failed: {str(e)}"
            self._sleep("after income statements")

            # Step 10: Balance Sheets
            logger.info(f"[10/13] Syncing balance sheets for {symbol}")
            try:
                sheets = self._financials_sync.upsert_balance_sheets(
                    symbol, financial_limit, "annual"
                )
                results["steps"]["balance_sheets"] = (
                    f"success ({len(sheets) if sheets else 0} records)"
                )
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync balance sheets: {e}")
                results["steps"]["balance_sheets"] = f"failed: {str(e)}"
            self._sleep("after balance sheets")

            # Step 11: Cash Flow Statements
            logger.info(f"[11/13] Syncing cash flow statements for {symbol}")
            try:
                flows = self._financials_sync.upsert_cash_flow_statements(
                    symbol, financial_limit, "annual"
                )
                results["steps"]["cash_flow_statements"] = (
                    f"success ({len(flows) if flows else 0} records)"
                )
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync cash flow statements: {e}")
                results["steps"]["cash_flow_statements"] = f"failed: {str(e)}"
            self._sleep("after cash flow statements")

            # Step 12: Stock Peers
            logger.info(f"[12/13] Syncing stock peers for {symbol}")
            try:
                peers = self._stock_info_sync.upsert_stock_peers(symbol)
                results["steps"]["stock_peers"] = (
                    f"success ({len(peers) if peers else 0} records)"
                )
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync stock peers: {e}")
                results["steps"]["stock_peers"] = f"failed: {str(e)}"
            self._sleep("after stock peers")

            # Step 13: Stock Splits
            logger.info(f"[13/13] Syncing stock splits for {symbol}")
            try:
                splits = self._stock_info_sync.upsert_stock_splits(symbol)
                results["steps"]["stock_splits"] = (
                    f"success ({len(splits) if splits else 0} records)"
                )
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync stock splits: {e}")
                results["steps"]["stock_splits"] = f"failed: {str(e)}"

            logger.info(f"[14/14] Syncing grading summary for {symbol}")
            try:
                self._grading_sync.upsert_grading_summary(symbol)
                results["steps"]["grading_summary"] = "success"
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync grading summary: {e}")
                results["steps"]["grading_summary"] = f"failed: {str(e)}"
            self._sleep("after grading summary")

            logger.info(f"[15/15] Syncing price target summary for {symbol}")
            try:
                self._price_target_sync.upsert_price_target_summary(symbol)
                results["steps"]["price_target_summary"] = "success"
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync price target summary: {e}")
                results["steps"]["price_target_summary"] = f"failed: {str(e)}"
            self._sleep("after price target summary")

            logger.info(f"[16/16] Syncing financial health for {symbol}")
            try:
                self._financials_sync.upsert_financial_health(symbol)
                results["steps"]["financial_health"] = "success"
                results["total_api_calls"] += 1
            except Exception as e:
                logger.error(f"Failed to sync financial health: {e}")
                results["steps"]["financial_health"] = f"failed: {str(e)}"
            self._sleep("after financial health")

            # Calculate total time
            end_time = datetime.now()
            total_seconds = (end_time - start_time).total_seconds()
            results["total_time_seconds"] = total_seconds
            results["status"] = "success"

            logger.info(
                f"Completed full sync for {symbol} in {total_seconds:.2f}s "
                f"({results['total_api_calls']} API calls)"
            )

            return results

        except Exception as e:
            logger.error(
                f"Fatal error during full data sync for {symbol}: {e}", exc_info=True
            )
            end_time = datetime.now()
            total_seconds = (end_time - start_time).total_seconds()
            results["total_time_seconds"] = total_seconds
            results["status"] = "failed"
            results["error"] = str(e)
            return results
