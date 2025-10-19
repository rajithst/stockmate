from sqlalchemy.orm import Session

from app.repositories.company_repo import CompanyRepository
from app.repositories.news_repo import CompanyNewsRepository
from app.schemas.company import CompanyPageResponse, CompanyRead
from app.schemas.dcf import DiscountedCashFlowRead
from app.schemas.grading import CompanyGradingSummaryRead
from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyPriceTargetNewsRead,
)
from app.schemas.price_target import (
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
)
from app.schemas.quote import StockPriceChangeRead
from app.schemas.rating import CompanyRatingSummaryRead


class CompanyService:
    def __init__(self, session: Session):
        self._db = session

    def get_company_page(self, symbol: str) -> CompanyPageResponse | None:
        """Retrieve a company's profile by its stock symbol."""
        page_repo = CompanyRepository(self._db)
        response = page_repo.get_company_snapshot_by_symbol(symbol)
        if not response:
            return None
        company_read = CompanyRead.model_validate(response)
        grading_summary_read = CompanyGradingSummaryRead.model_validate(
            response.grading_summary
        )
        dcf_read = DiscountedCashFlowRead.model_validate(response.discounted_cash_flow)
        rating_summary_read = CompanyRatingSummaryRead.model_validate(
            response.rating_summary
        )
        price_target_read = CompanyPriceTargetRead.model_validate(response.price_target)
        price_target_summary_read = CompanyPriceTargetSummaryRead.model_validate(
            response.price_target_summary
        )
        price_change_read = StockPriceChangeRead.model_validate(response.price_change)

        news_repo = CompanyNewsRepository(self._db)
        general_news_read = [
            CompanyGeneralNewsRead.model_validate(news)
            for news in news_repo.get_general_news_by_symbol(symbol)
        ]
        price_target_news_read = [
            CompanyPriceTargetNewsRead.model_validate(news)
            for news in news_repo.get_price_target_news_by_symbol(symbol)
        ]
        grading_news_read = [
            CompanyGradingNewsRead.model_validate(news)
            for news in news_repo.get_grading_news_by_symbol(symbol)
        ]

        return CompanyPageResponse(
            company=company_read,
            grading_summary=grading_summary_read,
            rating_summary=rating_summary_read,
            price_target_summary=price_target_summary_read,
            dcf=dcf_read,
            price_target=price_target_read,
            price_change=price_change_read,
            price_target_news=price_target_news_read,
            general_news=general_news_read,
            grading_news=grading_news_read,
        )
