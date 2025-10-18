from sqlalchemy.orm import Session

from app.repositories.company_page_repo import CompanyPageRepository
from app.repositories.news_repo import CompanyNewsRepository
from app.schemas.company import CompanyPageResponse, CompanyRead
from app.schemas.grading import CompanyGradingRead
from app.schemas.news import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyPriceTargetNewsRead,
)


class CompanyPageService:
    def __init__(self, session: Session):
        self._db = session

    def get_company_page(self, symbol: str) -> CompanyPageResponse | None:
        """Retrieve a company's profile by its stock symbol."""
        page_repo = CompanyPageRepository(self._db)
        response = page_repo.get_company_profile_snapshot(symbol)
        if not response:
            return None
        company, grading_summary = response
        company_read = CompanyRead.model_validate(company)
        grading_summary_read = CompanyGradingRead.model_validate(grading_summary)

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
            price_target_news=price_target_news_read,
            general_news=general_news_read,
            grading_news=grading_news_read,
        )
