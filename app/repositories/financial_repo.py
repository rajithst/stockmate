import logging
from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.balance_sheet import CompanyBalanceSheet
from app.db.models.cashflow import CompanyCashFlowStatement
from app.db.models.financial_health import CompanyFinancialHealth
from app.db.models.income_statement import CompanyIncomeStatement
from app.schemas.balance_sheet import CompanyBalanceSheetWrite
from app.schemas.cashflow import CompanyCashFlowStatementWrite
from app.schemas.financial_health import CompanyFinancialHealthWrite
from app.schemas.income_statement import CompanyIncomeStatementWrite
from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)


class FinancialRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_balance_sheets_by_symbol(self, symbol: str) -> list[CompanyBalanceSheet]:
        """Get all balance sheets for a symbol, ordered by date descending."""
        return (
            self._db.query(CompanyBalanceSheet)
            .filter(CompanyBalanceSheet.symbol == symbol)
            .order_by(CompanyBalanceSheet.date.desc())
            .all()
        )

    def get_income_statements_by_symbol(
        self, symbol: str
    ) -> list[CompanyIncomeStatement]:
        """Get all income statements for a symbol, ordered by date descending."""
        return (
            self._db.query(CompanyIncomeStatement)
            .filter(CompanyIncomeStatement.symbol == symbol)
            .order_by(CompanyIncomeStatement.date.desc())
            .all()
        )

    def get_cash_flow_statements_by_symbol(
        self, symbol: str
    ) -> list[CompanyCashFlowStatement]:
        """Get all cash flow statements for a symbol, ordered by date descending."""
        return (
            self._db.query(CompanyCashFlowStatement)
            .filter(CompanyCashFlowStatement.symbol == symbol)
            .order_by(CompanyCashFlowStatement.date.desc())
            .all()
        )

    def get_financial_health_by_symbol(
        self, symbol: str
    ) -> list[CompanyFinancialHealth]:
        """Get all financial health records for a symbol."""
        return (
            self._db.query(CompanyFinancialHealth)
            .filter(CompanyFinancialHealth.symbol == symbol)
            .all()
        )

    def upsert_financial_health(
        self, financial_health: list[CompanyFinancialHealthWrite]
    ) -> list[CompanyFinancialHealth]:
        """Upsert financial health data for a company."""
        try:
            records = []
            for fh in financial_health:
                existing = (
                    self._db.query(CompanyFinancialHealth)
                    .filter_by(symbol=fh.symbol, section=fh.section, metric=fh.metric)
                    .first()
                )
                if existing:
                    record = map_model(existing, fh)
                else:
                    record = CompanyFinancialHealth(**fh.model_dump(exclude_unset=True))
                    self._db.add(record)
                records.append(record)
            self._db.commit()
            for record in records:
                self._db.refresh(record)
            return records
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error upserting financial health data: {e}")
            raise

    def upsert_balance_sheets(
        self, balance_sheets: list[CompanyBalanceSheetWrite]
    ) -> list[CompanyBalanceSheet]:
        """Upsert multiple balance sheets and return the database records."""
        try:
            records = []
            for balance_sheet in balance_sheets:
                existing = (
                    self._db.query(CompanyBalanceSheet)
                    .filter_by(symbol=balance_sheet.symbol, date=balance_sheet.date)
                    .first()
                )
                if existing:
                    record = map_model(existing, balance_sheet)
                else:
                    record = CompanyBalanceSheet(
                        **balance_sheet.model_dump(exclude_unset=True)
                    )
                    self._db.add(record)
                records.append(record)

            self._db.commit()
            for record in records:
                self._db.refresh(record)
            return records
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error upserting balance sheets: {e}")
            raise

    def upsert_income_statements(
        self, income_statements: list[CompanyIncomeStatementWrite]
    ) -> list[CompanyIncomeStatement]:
        """Upsert multiple income statements and return the database records."""
        try:
            records = []
            for income_statement in income_statements:
                existing = (
                    self._db.query(CompanyIncomeStatement)
                    .filter_by(
                        symbol=income_statement.symbol, date=income_statement.date
                    )
                    .first()
                )
                if existing:
                    record = map_model(existing, income_statement)
                else:
                    record = CompanyIncomeStatement(
                        **income_statement.model_dump(exclude_unset=True)
                    )
                    self._db.add(record)
                records.append(record)

            self._db.commit()
            for record in records:
                self._db.refresh(record)
            return records
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error upserting income statements: {e}")
            raise

    def upsert_cash_flow_statements(
        self, cash_flow_statements: list[CompanyCashFlowStatementWrite]
    ) -> list[CompanyCashFlowStatement]:
        """Upsert multiple cash flow statements and return the database records."""
        try:
            records = []
            for cash_flow_statement in cash_flow_statements:
                existing = (
                    self._db.query(CompanyCashFlowStatement)
                    .filter_by(
                        symbol=cash_flow_statement.symbol, date=cash_flow_statement.date
                    )
                    .first()
                )
                if existing:
                    record = map_model(existing, cash_flow_statement)
                else:
                    record = CompanyCashFlowStatement(
                        **cash_flow_statement.model_dump(exclude_unset=True)
                    )
                    self._db.add(record)
                records.append(record)

            self._db.commit()
            for record in records:
                self._db.refresh(record)
            return records
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error upserting cash flow statements: {e}")
            raise

    def delete_balance_sheet(
        self, symbol: str, year: int
    ) -> Optional[CompanyBalanceSheet]:
        """Delete balance sheet by symbol and fiscal year."""
        try:
            record = (
                self._db.query(CompanyBalanceSheet)
                .filter(
                    CompanyBalanceSheet.symbol == symbol,
                    CompanyBalanceSheet.fiscal_year == str(year),
                )
                .first()
            )
            if record:
                self._db.delete(record)
                self._db.commit()
                return record
            return None
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error deleting balance sheet for {symbol} year {year}: {e}")
            raise

    def delete_income_statement(
        self, symbol: str, year: int
    ) -> Optional[CompanyIncomeStatement]:
        """Delete income statement by symbol and fiscal year."""
        try:
            record = (
                self._db.query(CompanyIncomeStatement)
                .filter(
                    CompanyIncomeStatement.symbol == symbol,
                    CompanyIncomeStatement.fiscal_year == str(year),
                )
                .first()
            )
            if record:
                self._db.delete(record)
                self._db.commit()
                return record
            return None
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(
                f"Error deleting income statement for {symbol} year {year}: {e}"
            )
            raise

    def delete_cash_flow_statement(
        self, symbol: str, year: int
    ) -> Optional[CompanyCashFlowStatement]:
        """Delete cash flow statement by symbol and fiscal year."""
        try:
            record = (
                self._db.query(CompanyCashFlowStatement)
                .filter(
                    CompanyCashFlowStatement.symbol == symbol,
                    CompanyCashFlowStatement.fiscal_year == str(year),
                )
                .first()
            )
            if record:
                self._db.delete(record)
                self._db.commit()
                return record
            return None
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(
                f"Error deleting cash flow statement for {symbol} year {year}: {e}"
            )
            raise
