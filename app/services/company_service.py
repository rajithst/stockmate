from enum import Enum
from logging import getLogger

from sqlalchemy.orm import Session

from app.repositories.company_repo import CompanyRepository
from app.repositories.financial_repo import FinancialRepository
from app.repositories.grading_repo import GradingRepository
from app.repositories.metrics_repo import MetricsRepository
from app.repositories.news_repo import CompanyNewsRepository
from app.repositories.stock_info_repo import StockInfoRepository
from app.repositories.technical_indicator_repo import TechnicalIndicatorRepository
from app.schemas.balance_sheet import CompanyBalanceSheetRead
from app.schemas.cashflow import CompanyCashFlowStatementRead
from app.schemas.company import (
    CompanyFinancialHealthResponse,
    CompanyFinancialResponse,
    CompanyPageResponse,
    CompanyRead,
)
from app.schemas.dcf import DiscountedCashFlowRead
from app.schemas.dividend import CompanyDividendRead
from app.schemas.financial_health import CompanyFinancialHealthRead
from app.schemas.financial_ratio import CompanyFinancialRatioRead
from app.schemas.grading import CompanyGradingRead, CompanyGradingSummaryRead
from app.schemas.income_statement import CompanyIncomeStatementRead
from app.schemas.key_metrics import CompanyKeyMetricsRead
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
from app.schemas.technical_indicator import CompanyTechnicalIndicatorRead

logger = getLogger(__name__)


class FinancialHealthSectorsEnum(Enum):
    PROFITABILITY = "Profitability"
    EFFICIENCY = "Efficiency"
    LIQUIDITY_AND_SOLVENCY = "Liquidity & Solvency"
    CASHFLOW_STRENGTH = "Cash Flow Strength"
    VALUATION = "Valuation"
    GROWTH_AND_INVESTMENT = "Growth & Investment"
    DIVIDEND_AND_SHAREHOLDER_RETURN = "Dividend & Shareholder Return"


class CompanyService:
    def __init__(self, session: Session):
        self._db = session

    def get_company_page(self, symbol: str) -> CompanyPageResponse | None:
        """Retrieve a company's profile by its stock symbol."""
        page_repo = CompanyRepository(self._db)

        response = page_repo.get_company_snapshot_by_symbol(symbol)
        if not response:
            return None
        news_repo = CompanyNewsRepository(self._db)
        grading_repo = GradingRepository(self._db)

        company_read = CompanyRead.model_validate(response)
        grading_summary_read = (
            CompanyGradingSummaryRead.model_validate(response.grading_summary)
            if response.grading_summary
            else None
        )
        dcf_read = (
            DiscountedCashFlowRead.model_validate(response.discounted_cash_flow)
            if response.discounted_cash_flow
            else None
        )
        rating_summary_read = (
            CompanyRatingSummaryRead.model_validate(response.rating_summary)
            if response.rating_summary
            else None
        )
        price_target_read = (
            CompanyPriceTargetRead.model_validate(response.price_target)
            if response.price_target
            else None
        )
        price_target_summary_read = (
            CompanyPriceTargetSummaryRead.model_validate(response.price_target_summary)
            if response.price_target_summary
            else None
        )
        price_change_read = (
            StockPriceChangeRead.model_validate(response.price_change)
            if response.price_change
            else None
        )
        latest_gradings = [
            CompanyGradingRead.model_validate(grading)
            for grading in grading_repo.get_gradings_by_symbol(symbol, limit=6)
        ]

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
            latest_gradings=latest_gradings,
            price_target_news=price_target_news_read,
            general_news=general_news_read,
            grading_news=grading_news_read,
        )

    def get_company_financials(self, symbol: str) -> CompanyFinancialResponse | None:
        """Retrieve a company's financials by its stock symbol."""
        try:
            financials_repo = FinancialRepository(self._db)
            metrics_repo = MetricsRepository(self._db)
            stock_info_repo = StockInfoRepository(self._db)

            balance_sheets_read = [
                CompanyBalanceSheetRead.model_validate(bs)
                for bs in financials_repo.get_balance_sheets_by_symbol(symbol)
            ]
            income_statements_read = [
                CompanyIncomeStatementRead.model_validate(is_)
                for is_ in financials_repo.get_income_statements_by_symbol(symbol)
            ]
            cash_flow_statements_read = [
                CompanyCashFlowStatementRead.model_validate(cs)
                for cs in financials_repo.get_cash_flow_statements_by_symbol(symbol)
            ]
            key_metrics_read = [
                CompanyKeyMetricsRead.model_validate(km)
                for km in metrics_repo.get_key_metrics_by_symbol(symbol)
            ]
            financial_ratios_read = [
                CompanyFinancialRatioRead.model_validate(fr)
                for fr in metrics_repo.get_financial_ratios_by_symbol(symbol)
            ]
            dividends_read = [
                CompanyDividendRead.model_validate(div)
                for div in stock_info_repo.get_dividends_by_symbol(symbol)
            ]

            return CompanyFinancialResponse(
                balance_sheets=balance_sheets_read,
                income_statements=income_statements_read,
                cash_flow_statements=cash_flow_statements_read,
                key_metrics=key_metrics_read,
                financial_ratios=financial_ratios_read,
                dividends=dividends_read,
            )
        except Exception as e:
            logger.error(f"Error retrieving financials for {symbol}: {str(e)}")
            raise

    def get_company_financial_health(
        self, symbol: str
    ) -> CompanyFinancialHealthResponse | None:
        """Retrieve a company's financial health data by its stock symbol."""
        try:
            financials_repo = FinancialRepository(self._db)
            company_repo = CompanyRepository(self._db)
            company = company_repo.get_company_by_symbol(symbol)

            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            company_read = CompanyRead.model_validate(company)

            financial_health_read = [
                CompanyFinancialHealthRead.model_validate(fh)
                for fh in financials_repo.get_financial_health_by_symbol(symbol)
            ]
            profitability = [
                CompanyFinancialHealthRead.model_validate(fh)
                for fh in financial_health_read
                if fh.section == FinancialHealthSectorsEnum.PROFITABILITY.value
            ]
            efficiency = [
                CompanyFinancialHealthRead.model_validate(fh)
                for fh in financial_health_read
                if fh.section == FinancialHealthSectorsEnum.EFFICIENCY.value
            ]
            liquidity_and_solvency = [
                CompanyFinancialHealthRead.model_validate(fh)
                for fh in financial_health_read
                if fh.section == FinancialHealthSectorsEnum.LIQUIDITY_AND_SOLVENCY.value
            ]
            cashflow_strength = [
                CompanyFinancialHealthRead.model_validate(fh)
                for fh in financial_health_read
                if fh.section == FinancialHealthSectorsEnum.CASHFLOW_STRENGTH.value
            ]
            valuation = [
                CompanyFinancialHealthRead.model_validate(fh)
                for fh in financial_health_read
                if fh.section == FinancialHealthSectorsEnum.VALUATION.value
            ]
            growth_and_investment = [
                CompanyFinancialHealthRead.model_validate(fh)
                for fh in financial_health_read
                if fh.section == FinancialHealthSectorsEnum.GROWTH_AND_INVESTMENT.value
            ]
            dividend_and_shareholder_return = [
                CompanyFinancialHealthRead.model_validate(fh)
                for fh in financial_health_read
                if fh.section
                == FinancialHealthSectorsEnum.DIVIDEND_AND_SHAREHOLDER_RETURN.value
            ]

            return CompanyFinancialHealthResponse(
                company=company_read,
                profitability=profitability,
                efficiency=efficiency,
                liquidity_and_solvency=liquidity_and_solvency,
                cashflow_strength=cashflow_strength,
                valuation=valuation,
                growth_and_investment=growth_and_investment,
                dividend_and_shareholder_return=dividend_and_shareholder_return,
            )
        except Exception as e:
            logger.error(f"Error retrieving financial health for {symbol}: {str(e)}")
            raise

    def get_company_technical_indicators(
        self, symbol: str
    ) -> list[CompanyTechnicalIndicatorRead] | None:
        """Retrieve a company's technical indicators by its stock symbol."""
        try:
            company_repo = CompanyRepository(self._db)
            company = company_repo.get_company_by_symbol(symbol)

            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            technical_indicators = TechnicalIndicatorRepository(self._db)
            indicators = technical_indicators.get_technical_indicators_by_symbol(symbol)
            if not indicators:
                logger.info(f"No technical indicators found for symbol: {symbol}")
                return None

            return [
                CompanyTechnicalIndicatorRead.model_validate(indicator)
                for indicator in indicators
            ]
        except Exception as e:
            logger.error(
                f"Error retrieving technical indicators for {symbol}: {str(e)}"
            )
            raise
