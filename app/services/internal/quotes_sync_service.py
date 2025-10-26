from logging import getLogger

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.repositories.company_repo import CompanyRepository
from app.repositories.quotes_repo import QuotesRepository
from app.schemas.quote import StockPriceChangeRead, StockPriceChangeWrite

logger = getLogger(__name__)


class QuotesSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = QuotesRepository(session)
        self._company_repository = CompanyRepository(session)

    def upsert_price_change(self, symbol: str) -> StockPriceChangeRead | None:
        try:
            # Get company to retrieve company_id
            company = self._company_repository.get_company_by_symbol(symbol)
            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            # Fetch price change data from external API client
            price_change_data = self._market_api_client.get_price_change_quote(symbol)
            if not price_change_data:
                logger.warning(f"No price change data found for symbol: {symbol}")
                return None
            price_change_in = StockPriceChangeWrite.model_validate(
                {**price_change_data.model_dump(), "company_id": company.id}
            )
            price_change = self._repository.upsert_price_change(price_change_in)
            return StockPriceChangeRead.model_validate(price_change)
        except Exception as e:
            logger.error(f"Error upserting price changes for symbol {symbol}: {e}")
            return None
