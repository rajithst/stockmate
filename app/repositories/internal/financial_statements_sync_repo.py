import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models.financial_statements import (
    CompanyBalanceSheet,
    CompanyCashFlowStatement,
    CompanyFinancialRatio,
    CompanyIncomeStatement,
)
from app.schemas.financial_statements import (
    CompanyBalanceSheetWrite,
    CompanyCashFlowStatementWrite,
    CompanyFinancialRatioWrite,
    CompanyIncomeStatementWrite,
)
from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)


class CompanyFinancialStatementsSyncRepository:
    """Repository for financial statements entities (income, balance sheet, cash flow)."""

    def __init__(self, session: Session) -> None:
        self._db = session

    def upsert_income_statements(
        self, income_statements: list[CompanyIncomeStatementWrite]
    ) -> list[CompanyIncomeStatement]:
        """Bulk upsert income statements by symbol and date."""
        try:
            results = []
            for statement_in in income_statements:
                # Find existing record
                existing = (
                    self._db.query(CompanyIncomeStatement)
                    .filter_by(symbol=statement_in.symbol, date=statement_in.date)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, statement_in)
                else:
                    # Create new
                    result = CompanyIncomeStatement(
                        **statement_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} income statements")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_income_statements: {e}")
            raise

    def upsert_balance_sheets(
        self, balance_sheets: list[CompanyBalanceSheetWrite]
    ) -> list[CompanyBalanceSheet]:
        """Bulk upsert balance sheets by symbol and date."""
        try:
            results = []
            for sheet_in in balance_sheets:
                # Find existing record
                existing = (
                    self._db.query(CompanyBalanceSheet)
                    .filter_by(symbol=sheet_in.symbol, date=sheet_in.date)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, sheet_in)
                else:
                    # Create new
                    result = CompanyBalanceSheet(
                        **sheet_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} balance sheets")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_balance_sheets: {e}")
            raise

    def upsert_cash_flow_statements(
        self, cash_flow_statements: list[CompanyCashFlowStatementWrite]
    ) -> list[CompanyCashFlowStatement]:
        """Bulk upsert cash flow statements by symbol and date."""
        try:
            results = []
            for statement_in in cash_flow_statements:
                # Find existing record
                existing = (
                    self._db.query(CompanyCashFlowStatement)
                    .filter_by(symbol=statement_in.symbol, date=statement_in.date)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, statement_in)
                else:
                    # Create new
                    result = CompanyCashFlowStatement(
                        **statement_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} cash flow statements")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_cash_flow_statements: {e}")
            raise

    def upsert_financial_ratios(
        self, financial_ratios: list[CompanyFinancialRatioWrite]
    ) -> list[CompanyFinancialRatio]:
        """Upsert financial ratios using the base class pattern."""
        try:
            results = []
            for ratio_in in financial_ratios:
                # Find existing record
                existing = (
                    self._db.query(CompanyFinancialRatio)
                    .filter_by(symbol=ratio_in.symbol, date=ratio_in.date)
                    .first()
                )

                if existing:
                    # Update existing
                    result = map_model(existing, ratio_in)
                else:
                    # Create new
                    result = CompanyFinancialRatio(
                        **ratio_in.model_dump(exclude_unset=True)
                    )
                    self._db.add(result)

                results.append(result)

            # Commit all changes
            self._db.commit()

            # Refresh all records
            for result in results:
                self._db.refresh(result)

            logger.info(f"Upserted {len(results)} financial ratios")
            return results
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error during upsert_financial_ratios: {e}")
            raise
