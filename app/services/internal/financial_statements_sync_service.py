import logging

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.internal.financial_statements_sync_repo import (
    CompanyFinancialStatementsSyncRepository,
)
from app.schemas.financial_statements import (
    CompanyBalanceSheetRead,
    CompanyBalanceSheetWrite,
    CompanyCashFlowStatementRead,
    CompanyCashFlowStatementWrite,
    CompanyFinancialRatioRead,
    CompanyFinancialRatioWrite,
    CompanyIncomeStatementRead,
    CompanyIncomeStatementWrite,
)
from app.services.internal.base_sync_service import BaseSyncService

logger = logging.getLogger(__name__)


class CompanyFinancialStatementsSyncService(BaseSyncService):
    """Service for syncing company financial statements data from FMP API."""

    def __init__(self, market_api_client: FMPClientProtocol, session: Session):
        super().__init__(session)
        self._market_api_client = market_api_client
        self._repository = CompanyFinancialStatementsSyncRepository(session)

    def upsert_balance_sheets(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyBalanceSheetRead] | None:
        """
        Fetch and upsert balance sheets for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted balance sheet records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call with known parameters
            api_data = self._market_api_client.get_balance_sheets(
                symbol, period=period, limit=limit
            )
            if not api_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyBalanceSheetWrite
            )
            persisted_records = self._repository.upsert_balance_sheets(
                records_to_persist
            )
            result = self._map_schema_list(persisted_records, CompanyBalanceSheetRead)

            logger.info(f"Successfully synced balance sheets for {symbol}")
            return result

        except Exception as e:
            logger.error(f"Failed to sync balance sheets for {symbol}: {e}")
            raise

    def upsert_income_statements(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyIncomeStatementRead] | None:
        """
        Fetch and upsert income statements for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted income statement records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call with known parameters
            api_data = self._market_api_client.get_income_statements(
                symbol, period=period, limit=limit
            )
            if not api_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyIncomeStatementWrite
            )
            persisted_records = self._repository.upsert_income_statements(
                records_to_persist
            )
            result = self._map_schema_list(
                persisted_records, CompanyIncomeStatementRead
            )

            logger.info(f"Successfully synced income statements for {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync income statements for {symbol}: {e}", exc_info=True
            )
            raise

    def upsert_cash_flow_statements(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyCashFlowStatementRead] | None:
        """
        Fetch and upsert cash flow statements for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted cash flow statement records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call with known parameters
            api_data = self._market_api_client.get_cash_flow_statements(
                symbol, period=period, limit=limit
            )
            if not api_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                api_data, company.id, CompanyCashFlowStatementWrite
            )
            persisted_records = self._repository.upsert_cash_flow_statements(
                records_to_persist
            )
            result = self._map_schema_list(
                persisted_records, CompanyCashFlowStatementRead
            )

            logger.info(f"Successfully synced cash flow statements for {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync cash flow statements for {symbol}: {e}", exc_info=True
            )
            raise

    def upsert_financial_ratios(
        self, symbol: str, limit: int, period: str = "annual"
    ) -> list[CompanyFinancialRatioRead] | None:
        """
        Fetch and upsert financial ratios for a company.

        Args:
            symbol: Stock symbol
            limit: Number of records to fetch
            period: Period type (annual/quarter)

        Returns:
            List of upserted financial ratio records or None if not found
        """
        try:
            company = self._get_company_or_fail(symbol)
            if not company:
                return None

            # Explicit control over API call with known parameters
            financial_ratios_data = self._market_api_client.get_financial_ratios(
                symbol, period=period, limit=limit
            )
            if not financial_ratios_data:
                return None

            records_to_persist = self._add_company_id_to_records(
                financial_ratios_data, company.id, CompanyFinancialRatioWrite
            )
            financial_ratios = self._repository.upsert_financial_ratios(
                records_to_persist
            )
            result = self._map_schema_list(financial_ratios, CompanyFinancialRatioRead)

            logger.info(f"Successfully synced financial ratios for {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync financial ratios for {symbol}: {e}", exc_info=True
            )
            raise
