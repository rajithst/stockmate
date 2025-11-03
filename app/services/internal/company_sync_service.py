from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
from app.schemas.company import CompanyRead, CompanyWrite

logger = getLogger(__name__)


class CompanySyncService:
    """
    Service for synchronizing company data between external API and local database.

    This service handles the business logic for fetching company data from external
    sources and managing its persistence in the local database.
    """

    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        """
        Initialize CompanySyncService with required dependencies.

        Args:
            market_api_client: Client for external market data API
            session: Database session for persistence operations
        """
        self._market_api_client = market_api_client
        self._repository = CompanyRepository(session)

    def upsert_company(self, symbol: str) -> CompanyRead | None:
        """
        Fetch company data from external API and upsert it into the database.

        Implements hybrid pattern: Explicit API call + base helper reuse.
        Company profile doesn't require company_id injection (it IS the company).

        Args:
            symbol: Stock symbol of the company

        Returns:
            CompanyRead schema if successful, None if company not found

        Raises:
            Exception: If there's an error during API fetch or database operation
        """
        try:
            # Step 1: Fetch from API with explicit parameter control
            company_data = self._market_api_client.get_company_profile(symbol)

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
            logger.info(f"Successfully synced company profile for symbol: {symbol}")
            return result

        except Exception as e:
            logger.error(
                f"Failed to sync company profile for symbol: {symbol}, error: {e}"
            )
            raise
