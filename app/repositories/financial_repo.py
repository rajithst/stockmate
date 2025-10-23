from sqlalchemy.orm import Session

from app.db.models.balance_sheet import CompanyBalanceSheet
from app.db.models.cashflow import CompanyCashFlowStatement
from app.db.models.income_statement import CompanyIncomeStatement
from app.schemas.balance_sheet import CompanyBalanceSheetWrite
from app.schemas.cashflow import CompanyCashFlowStatementWrite
from app.schemas.income_statement import CompanyIncomeStatementWrite
from app.util.map_model import map_model


class FinancialRepository:
    def __init__(self, session: Session):
        self._db = session

    def get_balance_sheets_by_symbol(self, symbol: str) -> list[CompanyBalanceSheet]:
        return (
            self._db.query(CompanyBalanceSheet)
            .filter(CompanyBalanceSheet.symbol == symbol)
            .all()
        )

    def get_income_statements_by_symbol(
        self, symbol: str
    ) -> list[CompanyIncomeStatement]:
        return (
            self._db.query(CompanyIncomeStatement)
            .filter(CompanyIncomeStatement.symbol == symbol)
            .all()
        )

    def get_cash_flow_statements_by_symbol(
        self, symbol: str
    ) -> list[CompanyCashFlowStatement]:
        return (
            self._db.query(CompanyCashFlowStatement)
            .filter(CompanyCashFlowStatement.symbol == symbol)
            .all()
        )

    def upsert_balance_sheets(
        self, balance_sheets: list[CompanyBalanceSheetWrite]
    ) -> list[CompanyBalanceSheet] | None:
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

    def upsert_income_statements(
        self, income_statements: list[CompanyIncomeStatementWrite]
    ) -> list[CompanyIncomeStatement] | None:
        records = []
        for income_statement in income_statements:
            existing = (
                self._db.query(CompanyIncomeStatement)
                .filter_by(symbol=income_statement.symbol, date=income_statement.date)
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

    def upsert_cash_flow_statements(
        self, cash_flow_statements: list[CompanyCashFlowStatementWrite]
    ) -> list[CompanyCashFlowStatement] | None:
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

    def delete_balance_sheet(self, symbol: str, year: int) -> None:
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

    def delete_income_statement(self, symbol: str, year: int) -> None:
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

    def delete_cash_flow_statement(self, symbol: str, year: int) -> None:
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
