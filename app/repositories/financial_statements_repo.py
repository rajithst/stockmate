import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.financial_statements import (
    CompanyBalanceSheet,
    CompanyCashFlowStatement,
    CompanyFinancialRatio,
    CompanyIncomeStatement,
)

logger = logging.getLogger(__name__)


class CompanyFinancialStatementsRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_income_statements(
        self, symbol: str, limit: int = 50
    ) -> list[CompanyIncomeStatement]:
        """Retrieve income statements for a company."""
        try:
            return (
                self._db.query(CompanyIncomeStatement)
                .filter(CompanyIncomeStatement.symbol == symbol)
                .order_by(
                    CompanyIncomeStatement.date.desc(),
                    CompanyIncomeStatement.fiscal_year.desc(),
                )
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting income statements for {symbol}: {e}")
            raise

    def get_balance_sheets(
        self, symbol: str, limit: int = 50
    ) -> list[CompanyBalanceSheet]:
        """Retrieve balance sheets for a company."""
        try:
            return (
                self._db.query(CompanyBalanceSheet)
                .filter(CompanyBalanceSheet.symbol == symbol)
                .order_by(
                    CompanyBalanceSheet.date.desc(),
                    CompanyBalanceSheet.fiscal_year.desc(),
                )
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting balance sheets for {symbol}: {e}")
            raise

    def get_cash_flow_statements(
        self, symbol: str, limit: int = 50
    ) -> list[CompanyCashFlowStatement]:
        """Retrieve cash flow statements for a company."""
        try:
            return (
                self._db.query(CompanyCashFlowStatement)
                .filter(CompanyCashFlowStatement.symbol == symbol)
                .order_by(
                    CompanyCashFlowStatement.date.desc(),
                    CompanyCashFlowStatement.fiscal_year.desc(),
                )
                .limit(limit)
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting cash flow statements for {symbol}: {e}")
            raise

    def get_financial_ratios(self, symbol: str) -> list[CompanyFinancialRatio]:
        """Retrieve financial ratios for a company."""
        try:
            return (
                self._db.query(CompanyFinancialRatio)
                .filter(CompanyFinancialRatio.symbol == symbol)
                .order_by(
                    CompanyFinancialRatio.date.desc(),
                    CompanyFinancialRatio.fiscal_year.desc(),
                )
                .all()
            )
        except SQLAlchemyError as e:
            logger.error(f"Error getting financial ratios for {symbol}: {e}")
            raise
