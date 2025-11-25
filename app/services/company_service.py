from enum import Enum
from logging import getLogger

from sqlalchemy.orm import Session

from app.repositories.company_metrics_repo import CompanyMetricsRepository
from app.repositories.company_repo import CompanyRepository
from app.repositories.financial_health_repo import CompanyFinancialHealthRepository
from app.repositories.financial_statements_repo import (
    CompanyFinancialStatementsRepository,
)
from app.repositories.market_data_repo import (
    CompanyMarketDataRepository,
    CompanyNewsType,
)
from app.repositories.quotes_repo import CompanyQuotesRepository
from app.schemas.company import (
    CompanyFinancialHealthResponse,
    CompanyFinancialResponse,
    CompanyInsightsResponse,
    CompanyPageResponse,
    CompanyRead,
)
from app.schemas.company_metrics import (
    CompanyDiscountedCashFlowRead,
    CompanyKeyMetricsRead,
    CompanyAnalystEstimateRead,
)
from app.schemas.financial_health import CompanyFinancialHealthRead
from app.schemas.financial_statements import (
    CompanyBalanceSheetRead,
    CompanyCashFlowStatementRead,
    CompanyFinancialRatioRead,
    CompanyIncomeStatementRead,
)
from app.schemas.market_data import (
    CompanyGeneralNewsRead,
    CompanyGradingNewsRead,
    CompanyGradingRead,
    CompanyGradingSummaryRead,
    CompanyPriceTargetNewsRead,
    CompanyPriceTargetRead,
    CompanyPriceTargetSummaryRead,
    CompanyRatingSummaryRead,
)
from app.schemas.quote import (
    CompanyDividendRead,
    CompanyTechnicalIndicatorRead,
    StockPriceChangeRead,
    StockPriceRead,
)

logger = getLogger(__name__)


class FinancialHealthSectorsEnum(Enum):
    PROFITABILITY_ANALYSIS = "Profitability Analysis"
    EFFICIENCY_ANALYSIS = "Efficiency and Productivity Analysis"
    LIQUIDITY_AND_SHORT_TERM_SOLVENCY = "Liquidity and Short-Term Solvency"
    LEVERAGE_AND_CAPITAL_STRUCTURE = "Leverage and Capital Structure"
    VALUATION_AND_MARKET_MULTIPLES = "Valuation and Market Multiples"
    CASHFLOW_STRENGTH = "Cash Flow Strength"
    ASSET_QUALITY_AND_CAPITAL_EFFICIENCY = "Asset Quality and Capital Efficiency"
    DIVIDEND_AND_SHAREHOLDER_RETURNS = "Dividend and Shareholder Returns"
    PER_SHARE_PERFORMANCE = "Per Share Performance"
    TAX_AND_COST_STRUCTURE = "Tax and Cost Structure Analysis"


class CompanyService:
    def __init__(self, session: Session):
        self._db = session
        self._company_repository = CompanyRepository(session)
        self._market_data_repository = CompanyMarketDataRepository(session)
        self._financial_statements_repository = CompanyFinancialStatementsRepository(
            session
        )
        self._metrics_repository = CompanyMetricsRepository(session)
        self._financial_health_repository = CompanyFinancialHealthRepository(session)
        self._quotes_repository = CompanyQuotesRepository(session)

    @staticmethod
    def _validate_models(schema_class, items):
        """Helper to validate a list of ORM models against a Pydantic schema."""
        if not items:
            return []
        return [schema_class.model_validate(item) for item in items]

    @staticmethod
    def _validate_single(schema_class, item):
        """Helper to validate a single ORM model, returning None if item is None."""
        return schema_class.model_validate(item) if item else None

    @staticmethod
    def _group_financial_health_by_section(
        financial_health_items: list,
    ) -> dict[str, list]:
        """Group financial health metrics by their section."""
        grouped = {section.value: [] for section in FinancialHealthSectorsEnum}

        for item in financial_health_items:
            for section in FinancialHealthSectorsEnum:
                if item.section == section.value:
                    grouped[section.value].append(
                        CompanyFinancialHealthRead.model_validate(item)
                    )
                    break

        return grouped

    def get_company_page(self, symbol: str) -> CompanyPageResponse | None:
        """Retrieve a company's profile by its stock symbol."""
        response = self._company_repository.get_company_snapshot_by_symbol(symbol)
        if not response:
            return None

        # Validate company - from_attributes=True will call property methods automatically
        company_read = CompanyRead.model_validate(response)

        grading_summary_read = self._validate_single(
            CompanyGradingSummaryRead, response.grading_summary
        )
        dcf_read = self._validate_single(
            CompanyDiscountedCashFlowRead, response.discounted_cash_flow
        )
        rating_summary_read = self._validate_single(
            CompanyRatingSummaryRead, response.rating_summary
        )
        price_target_read = self._validate_single(
            CompanyPriceTargetRead, response.price_target
        )
        price_target_summary_read = self._validate_single(
            CompanyPriceTargetSummaryRead, response.price_target_summary
        )
        price_change_read = self._validate_single(
            StockPriceChangeRead, response.stock_price_change
        )

        # Use repository methods for collections
        latest_gradings = self._validate_models(
            CompanyGradingRead,
            self._market_data_repository.get_gradings(symbol, limit=6),
        )

        general_news_read = self._validate_models(
            CompanyGeneralNewsRead,
            self._market_data_repository.get_company_news(
                symbol, CompanyNewsType.GENERAL
            ),
        )
        price_target_news_read = self._validate_models(
            CompanyPriceTargetNewsRead,
            self._market_data_repository.get_company_news(
                symbol, CompanyNewsType.PRICE_TARGET
            ),
        )
        grading_news_read = self._validate_models(
            CompanyGradingNewsRead,
            self._market_data_repository.get_company_news(
                symbol, CompanyNewsType.GRADING
            ),
        )

        daily_prices_read = self._validate_models(
            StockPriceRead, self._quotes_repository.get_daily_prices(symbol)
        )

        analyst_estimates_read = self._validate_models(
            CompanyAnalystEstimateRead,
            self._metrics_repository.get_analyst_estimates(symbol),
        )

        return CompanyPageResponse(
            company=company_read,
            grading_summary=grading_summary_read,
            rating_summary=rating_summary_read,
            price_target_summary=price_target_summary_read,
            dcf=dcf_read,
            price_target=price_target_read,
            stock_prices=daily_prices_read,
            price_change=price_change_read,
            latest_gradings=latest_gradings,
            analyst_estimates=analyst_estimates_read,
            price_target_news=price_target_news_read,
            general_news=general_news_read,
            grading_news=grading_news_read,
        )

    def get_company_financials(self, symbol: str) -> CompanyFinancialResponse | None:
        """Retrieve a company's financials by its stock symbol."""
        try:
            balance_sheets_read = self._validate_models(
                CompanyBalanceSheetRead,
                self._financial_statements_repository.get_balance_sheets(symbol),
            )
            income_statements_read = self._validate_models(
                CompanyIncomeStatementRead,
                self._financial_statements_repository.get_income_statements(symbol),
            )
            cash_flow_statements_read = self._validate_models(
                CompanyCashFlowStatementRead,
                self._financial_statements_repository.get_cash_flow_statements(symbol),
            )
            financial_ratios_read = self._validate_models(
                CompanyFinancialRatioRead,
                self._financial_statements_repository.get_financial_ratios(symbol),
            )
            key_metrics_read = self._validate_models(
                CompanyKeyMetricsRead,
                self._metrics_repository.get_key_metrics(symbol),
            )

            dividends_read = self._validate_models(
                CompanyDividendRead,
                self._quotes_repository.get_dividends(symbol),
            )

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
            company = self._company_repository.get_company_by_symbol(symbol)

            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            company_read = CompanyRead.model_validate(company)
            financial_health_items = (
                self._financial_health_repository.get_financial_health(symbol)
            )

            # Group financial health metrics by section with single iteration
            grouped = self._group_financial_health_by_section(financial_health_items)

            return CompanyFinancialHealthResponse(
                company=company_read,
                profitability_analysis=grouped[
                    FinancialHealthSectorsEnum.PROFITABILITY_ANALYSIS.value
                ],
                efficiency_analysis=grouped[
                    FinancialHealthSectorsEnum.EFFICIENCY_ANALYSIS.value
                ],
                liquidity_and_short_term_solvency=grouped[
                    FinancialHealthSectorsEnum.LIQUIDITY_AND_SHORT_TERM_SOLVENCY.value
                ],
                leverage_and_capital_structure=grouped[
                    FinancialHealthSectorsEnum.LEVERAGE_AND_CAPITAL_STRUCTURE.value
                ],
                valuation_and_market_multiples=grouped[
                    FinancialHealthSectorsEnum.VALUATION_AND_MARKET_MULTIPLES.value
                ],
                cashflow_strength=grouped[
                    FinancialHealthSectorsEnum.CASHFLOW_STRENGTH.value
                ],
                asset_quality_and_capital_efficiency=grouped[
                    FinancialHealthSectorsEnum.ASSET_QUALITY_AND_CAPITAL_EFFICIENCY.value
                ],
                dividend_and_shareholder_returns=grouped[
                    FinancialHealthSectorsEnum.DIVIDEND_AND_SHAREHOLDER_RETURNS.value
                ],
                per_share_performance=grouped[
                    FinancialHealthSectorsEnum.PER_SHARE_PERFORMANCE.value
                ],
                tax_and_cost_structure=grouped[
                    FinancialHealthSectorsEnum.TAX_AND_COST_STRUCTURE.value
                ],
            )
        except Exception as e:
            logger.error(f"Error retrieving financial health for {symbol}: {str(e)}")
            raise

    def get_company_technical_indicators(
        self, symbol: str
    ) -> list[CompanyTechnicalIndicatorRead] | None:
        """Retrieve a company's technical indicators by its stock symbol."""
        try:
            company = self._company_repository.get_company_by_symbol(symbol)

            if not company:
                logger.warning(f"Company not found for symbol: {symbol}")
                return None

            indicators = self._quotes_repository.get_technical_indicators(symbol)

            if not indicators:
                logger.info(f"No technical indicators found for symbol: {symbol}")
                return None

            return self._validate_models(CompanyTechnicalIndicatorRead, indicators)
        except Exception as e:
            logger.error(
                f"Error retrieving technical indicators for {symbol}: {str(e)}"
            )
            raise

    def get_company_insights(self, symbol: str) -> CompanyInsightsResponse:
        """Retrieve various insights for a company by its stock symbol."""
        try:
            # Retrieve raw financial data
            income_statements = (
                self._financial_statements_repository.get_income_statements(
                    symbol,
                )
            )
            balance_sheets = self._financial_statements_repository.get_balance_sheets(
                symbol,
            )
            cash_flow_statements = (
                self._financial_statements_repository.get_cash_flow_statements(
                    symbol,
                )
            )
            financial_ratios = (
                self._financial_statements_repository.get_financial_ratios(
                    symbol,
                )
            )
            key_metrics = self._metrics_repository.get_key_metrics(symbol)

            # Transform raw data into insights
            inc_statement_insights = self._transform_income_statement_data(
                income_statements
            )
            bal_sheet_insights = self._transform_balance_sheet_data(balance_sheets)
            cf_statement_insights = self._transform_cash_flow_statement_data(
                cash_flow_statements
            )
            fr_insights = self._transform_financial_ratio_data(financial_ratios)
            km_insights = self._transform_key_metrics_data(key_metrics)

            return CompanyInsightsResponse(
                net_income=inc_statement_insights["net_income"],
                ebita=inc_statement_insights["ebita"],
                eps=inc_statement_insights["eps"],
                eps_diluted=inc_statement_insights["eps_diluted"],
                weighted_average_shs_out=inc_statement_insights[
                    "weighted_average_shs_out"
                ],
                total_debt=bal_sheet_insights["total_debt"],
                free_cash_flow=cf_statement_insights["free_cash_flow"],
                operating_cash_flow=cf_statement_insights["operating_cash_flow"],
                gross_profit_margin=fr_insights["gross_profit_margin"],
                operating_profit_margin=fr_insights["operating_profit_margin"],
                debt_to_equity_ratio=fr_insights["debt_to_equity_ratio"],
                dividend_yield=fr_insights["dividend_yield"],
                return_on_equity=km_insights["return_on_equity"],
                market_cap=km_insights["market_cap"],
            )
        except Exception as e:
            logger.error(f"Error retrieving insights for {symbol}: {str(e)}")
            raise

    def _transform_income_statement_data(
        self, income_statements
    ) -> dict[str, list[dict[str, float]]]:
        """Transform income statement records into structured insights.

        Returns:
            Dictionary with keys: revenue, net_income, ebita, eps, eps_diluted, weighted_average_shs_out
        """
        insights = {
            "revenue": [],
            "net_income": [],
            "ebita": [],
            "eps": [],
            "eps_diluted": [],
            "weighted_average_shs_out": [],
        }
        for inc_stmt in income_statements:
            year = inc_stmt.fiscal_year
            quarter = inc_stmt.period

            insights["revenue"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": inc_stmt.revenue,
                }
            )
            insights["net_income"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": inc_stmt.net_income,
                }
            )
            insights["ebita"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": inc_stmt.ebitda,
                }
            )
            insights["eps"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": inc_stmt.eps,
                }
            )
            insights["eps_diluted"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": inc_stmt.eps_diluted,
                }
            )
            insights["weighted_average_shs_out"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": inc_stmt.weighted_average_shs_out,
                }
            )
        return insights

    def _transform_balance_sheet_data(
        self, balance_sheets
    ) -> dict[str, list[dict[str, float]]]:
        """Transform balance sheet records into structured insights.

        Returns:
            Dictionary with key: total_debt
        """
        insights = {
            "total_debt": [],
        }
        for bal_sheet in balance_sheets:
            year = bal_sheet.fiscal_year
            quarter = bal_sheet.period

            insights["total_debt"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": bal_sheet.total_debt,
                }
            )
        return insights

    def _transform_cash_flow_statement_data(
        self, cash_flow_statements
    ) -> dict[str, list[dict[str, float]]]:
        """Transform cash flow statement records into structured insights.

        Returns:
            Dictionary with keys: free_cash_flow, operating_cash_flow
        """
        insights = {
            "free_cash_flow": [],
            "operating_cash_flow": [],
        }
        for cf_stmt in cash_flow_statements:
            year = cf_stmt.fiscal_year
            quarter = cf_stmt.period

            insights["free_cash_flow"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": cf_stmt.free_cash_flow,
                }
            )
            insights["operating_cash_flow"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": cf_stmt.operating_cash_flow,
                }
            )
        return insights

    def _transform_financial_ratio_data(
        self, financial_ratios
    ) -> dict[str, list[dict[str, float]]]:
        """Transform financial ratio records into structured insights.

        Returns:
            Dictionary with keys: gross_profit_margin, operating_profit_margin, debt_to_equity_ratio, dividend_yield
        """
        insights = {
            "gross_profit_margin": [],
            "operating_profit_margin": [],
            "debt_to_equity_ratio": [],
            "dividend_yield": [],
        }
        for fr in financial_ratios:
            year = fr.fiscal_year
            quarter = fr.period

            insights["gross_profit_margin"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": fr.gross_profit_margin,
                }
            )
            insights["operating_profit_margin"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": fr.operating_profit_margin,
                }
            )
            insights["debt_to_equity_ratio"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": fr.debt_to_equity_ratio,
                }
            )
            insights["dividend_yield"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": fr.dividend_yield,
                }
            )
        return insights

    def _transform_key_metrics_data(
        self, key_metrics
    ) -> dict[str, list[dict[str, float]]]:
        """Transform key metrics records into structured insights.

        Returns:
            Dictionary with keys: return_on_equity, market_cap
        """
        insights = {
            "return_on_equity": [],
            "market_cap": [],
        }
        for km in key_metrics:
            year = km.fiscal_year
            quarter = km.period

            insights["return_on_equity"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": km.return_on_equity,
                }
            )
            insights["market_cap"].append(
                {
                    "year": year,
                    "quarter": quarter,
                    "value": km.market_cap,
                }
            )
        return insights
