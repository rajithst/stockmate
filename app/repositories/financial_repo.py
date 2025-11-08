import logging
from sqlalchemy.orm import Session

from app.db.models.financial_statements import CompanyBalanceSheet
from app.db.models.financial_statements import CompanyCashFlowStatement
from app.db.models.financial_health import CompanyFinancialHealth
from app.db.models.financial_statements import CompanyIncomeStatement
from app.repositories.base_repo import BaseRepository
from app.schemas.financial_statements import CompanyBalanceSheetWrite
from app.schemas.financial_statements import CompanyCashFlowStatementWrite
from app.schemas.financial_health import CompanyFinancialHealthWrite
from app.schemas.financial_statements import CompanyIncomeStatementWrite

logger = logging.getLogger(__name__)


class FinancialRepository(BaseRepository):
    """Repository for managing financial records."""

    def __init__(self, session: Session):
        super().__init__(session)

    def get_balance_sheets_by_symbol(self, symbol: str) -> list[CompanyBalanceSheet]:
        """Get all balance sheets for a symbol, ordered by date descending."""
        return self._get_by_filter(
            CompanyBalanceSheet,
            {"symbol": symbol},
            order_by_desc=CompanyBalanceSheet.date,
        )

    def get_income_statements_by_symbol(
        self, symbol: str
    ) -> list[CompanyIncomeStatement]:
        """Get all income statements for a symbol, ordered by date descending."""
        return self._get_by_filter(
            CompanyIncomeStatement,
            {"symbol": symbol},
            order_by_desc=CompanyIncomeStatement.date,
        )

    def get_cash_flow_statements_by_symbol(
        self, symbol: str
    ) -> list[CompanyCashFlowStatement]:
        """Get all cash flow statements for a symbol, ordered by date descending."""
        return self._get_by_filter(
            CompanyCashFlowStatement,
            {"symbol": symbol},
            order_by_desc=CompanyCashFlowStatement.date,
        )

    def get_financial_health_by_symbol(
        self, symbol: str
    ) -> list[CompanyFinancialHealth]:
        """Get all financial health records for a symbol."""
        return self._get_by_filter(CompanyFinancialHealth, {"symbol": symbol})

    def upsert_financial_health(
        self, financial_health: list[CompanyFinancialHealthWrite]
    ) -> list[CompanyFinancialHealth]:
        """Upsert financial health data using base class pattern."""
        return self._upsert_records(
            financial_health,
            CompanyFinancialHealth,
            lambda fh: {
                "symbol": fh.symbol,
                "section": fh.section,
                "metric": fh.metric,
            },
            "upsert_financial_health",
        )

    def upsert_balance_sheets(
        self, balance_sheets: list[CompanyBalanceSheetWrite]
    ) -> list[CompanyBalanceSheet]:
        """Upsert multiple balance sheets using base class pattern."""
        return self._upsert_records(
            balance_sheets,
            CompanyBalanceSheet,
            lambda bs: {"symbol": bs.symbol, "date": bs.date},
            "upsert_balance_sheets",
        )

    def upsert_income_statements(
        self, income_statements: list[CompanyIncomeStatementWrite]
    ) -> list[CompanyIncomeStatement]:
        """Upsert multiple income statements using base class pattern."""
        return self._upsert_records(
            income_statements,
            CompanyIncomeStatement,
            lambda is_: {"symbol": is_.symbol, "date": is_.date},
            "upsert_income_statements",
        )

    def upsert_cash_flow_statements(
        self, cash_flow_statements: list[CompanyCashFlowStatementWrite]
    ) -> list[CompanyCashFlowStatement]:
        """Upsert multiple cash flow statements using base class pattern."""
        return self._upsert_records(
            cash_flow_statements,
            CompanyCashFlowStatement,
            lambda cfs: {"symbol": cfs.symbol, "date": cfs.date},
            "upsert_cash_flow_statements",
        )
