from app.schemas.company import CompanyPageResponse
from tests.common.mock_company_data import MockCompanyDataBuilder
from tests.common.mock_company_grading_data import (
    MockCompanyGradingSummaryBuilder,
)
from tests.common.mock_company_news_data import MockCompanyNewsDataBuilder
from tests.common.mock_company_rating_data import MockCompanyRatingSummaryBuilder
from tests.common.mock_dcf_data import MockDiscountedCashFlowDataBuilder
from tests.common.mock_price_change_data import MockStockPriceChangeDataBuilder
from tests.common.mock_price_target_data import (
    MockPriceTargetDataBuilder,
    MockPriceTargetSummaryDataBuilder,
)


class MockCompanyPageDataBuilder:
    @staticmethod
    def company_page_response(**overrides) -> CompanyPageResponse:
        """Build complete CompanyPageResponse test data."""
        defaults = {
            "company": MockCompanyDataBuilder.company_read(),
            "grading_summary": MockCompanyGradingSummaryBuilder.company_grading_summary_read(),
            "rating_summary": MockCompanyRatingSummaryBuilder.company_rating_summary_read(),
            "dcf": MockDiscountedCashFlowDataBuilder.discounted_cash_flow_read(),
            "price_target": MockPriceTargetDataBuilder.price_target_read(),
            "price_change": MockStockPriceChangeDataBuilder.stock_price_change_read(),
            "price_target_summary": MockPriceTargetSummaryDataBuilder.price_target_summary_read(),
            "general_news": [MockCompanyNewsDataBuilder.general_news_read()],
            "price_target_news": [MockCompanyNewsDataBuilder.price_target_news_read()],
            "grading_news": [MockCompanyNewsDataBuilder.grading_news_read()],
        }
        return CompanyPageResponse(**(defaults | overrides))
