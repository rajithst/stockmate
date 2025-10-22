from logging import getLogger
from typing import Optional

from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.db.models import Company
from app.repositories.financial_repo import FinancialRepository
from app.schemas.balance_sheet import CompanyBalanceSheetRead, CompanyBalanceSheetWrite
from app.schemas.cashflow import (
    CompanyCashFlowStatementRead,
    CompanyCashFlowStatementWrite,
)
from app.schemas.income_statement import (
    CompanyIncomeStatementRead,
    CompanyIncomeStatementWrite,
)

logger = getLogger(__name__)


class FinancialSyncService:
    def __init__(self, market_api_client: FMPClientProtocol, session: Session) -> None:
        self._market_api_client = market_api_client
        self._repository = FinancialRepository(session)

    def get_balance_sheets(self, symbol: str) -> list[CompanyBalanceSheetRead]:
        balance_sheets = self._repository.get_balance_sheets_by_symbol(symbol)
        return [
            CompanyBalanceSheetRead.model_validate(bs.model_dump())
            for bs in balance_sheets
        ]

    def get_income_statements(self, symbol: str) -> list[CompanyIncomeStatementRead]:
        income_statements = self._repository.get_income_statements_by_symbol(symbol)
        return [
            CompanyIncomeStatementRead.model_validate(is_.model_dump())
            for is_ in income_statements
        ]

    def get_cash_flow_statements(
        self, symbol: str
    ) -> list[CompanyCashFlowStatementRead]:
        cash_flow_statements = self._repository.get_cash_flow_statements_by_symbol(
            symbol
        )
        return [
            CompanyCashFlowStatementRead.model_validate(cs.model_dump())
            for cs in cash_flow_statements
        ]

    def upsert_balance_sheet(self, symbol: str):
        balance_sheets_data = self._market_api_client.get_balance_sheets(symbol)
        if not balance_sheets_data:
            logger.info(f"No balance sheet data found for symbol: {symbol}")
            return None
        balance_sheets_in = [
            CompanyBalanceSheetWrite.model_validate(bs.model_dump())
            for bs in balance_sheets_data
        ]
        return self._repository.upsert_balance_sheets(balance_sheets_in)

    def upsert_income_statement(self, symbol: str):
        income_statements_data = self._market_api_client.get_income_statements(symbol)
        if not income_statements_data:
            logger.info(f"No income statement data found for symbol: {symbol}")
            return None
        income_statements_in = [
            CompanyIncomeStatementWrite.model_validate(is_.model_dump())
            for is_ in income_statements_data
        ]
        return self._repository.upsert_income_statement(income_statements_in)

    def upsert_cash_flow_statement(self, symbol: str):
        cash_flow_statements_data = self._market_api_client.get_cash_flow_statements(
            symbol
        )
        if not cash_flow_statements_data:
            logger.info(f"No cash flow statement data found for symbol: {symbol}")
            return None
        cash_flow_statements_in = [
            CompanyCashFlowStatementWrite.model_validate(cs.model_dump())
            for cs in cash_flow_statements_data
        ]
        return self._repository.upsert_cash_flow_statement(cash_flow_statements_in)

    def delete_balance_sheet(self, symbol: str, year: int) -> Optional[Company]:
        return self._repository.delete_balance_sheet(symbol, year)

    def delete_income_statement(self, symbol: str, year: int) -> Optional[Company]:
        return self._repository.delete_income_statement(symbol, year)

    def delete_cash_flow_statement(self, symbol: str, year: int) -> Optional[Company]:
        return self._repository.delete_cash_flow_statement(symbol, year)
