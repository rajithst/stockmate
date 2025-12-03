from enum import Enum
from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.clients.yfinance.protocol import YFinanceClientProtocol
from app.repositories.internal.company_sync_repo import CompanySyncRepository
from app.schemas.company import (
    CompanyRead,
    CompanyWrite,
    NonUSCompanyRead,
    NonUSCompanyWrite,
)

logger = getLogger(__name__)


class MarketType(str, Enum):
    """Enumeration of market types."""

    US = "US"
    NON_US = "NON_US"


class CompanySyncService:
    """
    Service for synchronizing company data between external APIs and local database.

    Supports dual API integration:
    - FMP API for US companies (stored in Company table)
    - YFinance API for non-US companies (stored in NonUSCompany table)

    Uses Strategy Pattern: Detects market type and routes to appropriate adapter.
    """

    def __init__(
        self,
        fmp_client: FMPClientProtocol,
        yfinance_client: YFinanceClientProtocol,
        session: Session,
    ) -> None:
        """
        Initialize CompanySyncService with both API clients.

        Args:
            fmp_client: FMP API client for US company data
            yfinance_client: YFinance API client for non-US company data
            session: Database session for persistence operations
        """
        self._fmp_client = fmp_client
        self._yfinance_client = yfinance_client
        self._repository = CompanySyncRepository(session)

    def upsert_company(self, symbol: str) -> CompanyRead | None:
        """
        Fetch US company data from FMP API and upsert to database.

        Args:
            symbol: US stock symbol (e.g., "AAPL", "MSFT")

        Returns:
            CompanyRead schema if successful, None if company not found

        Raises:
            Exception: If there's an error during API fetch or database operation
        """
        try:
            # Step 1: Fetch from FMP API
            company_data = self._fmp_client.get_company_profile(symbol)

            # Step 2: Validate API response
            if not company_data:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            # Step 3: Transform to write schema
            company_in = CompanyWrite.model_validate(company_data.model_dump())

            # Step 4: Persist to database
            persisted_company = self._repository.upsert_company(company_in)

            # Step 5: Map to read schema and log success
            result = CompanyRead.model_validate(persisted_company)
            logger.info(f"Successfully synced US company profile for symbol: {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync US company profile for symbol: {symbol}, error: {e}"
            )
            raise

    def upsert_non_us_company(self, symbol: str) -> NonUSCompanyRead | None:
        """
        Fetch non-US company data from YFinance API and upsert to database.

        Args:
            symbol: Non-US stock symbol (e.g., "8411.T", "0700.HK", "MC.PA")

        Returns:
            NonUSCompanyRead schema if successful, None if company not found

        Raises:
            Exception: If there's an error during API fetch or database operation
        """
        try:
            # Step 1: Fetch from YFinance API
            company_data = self._yfinance_client.get_company_profile(symbol)

            # Step 2: Validate API response
            if not company_data:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            # Step 3: Transform to write schema
            company_in = NonUSCompanyWrite.model_validate(company_data.model_dump())

            # Step 4: Persist to database
            persisted_company = self._repository.upsert_non_us_company(company_in)

            # Step 5: Map to read schema and log success
            result = NonUSCompanyRead.model_validate(persisted_company)
            logger.info(
                f"Successfully synced non-US company profile for symbol: {symbol}"
            )
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync non-US company profile for symbol: {symbol}, error: {e}"
            )
            raise
