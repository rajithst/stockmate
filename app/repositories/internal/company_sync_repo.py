import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models import Company
from app.db.models.company import NonUSCompany
from app.schemas.company import CompanyWrite, NonUSCompanyWrite
from app.util.model_mapper import map_model

logger = logging.getLogger(__name__)


class CompanySyncRepository:
    def __init__(self, db: Session):
        self._db = db

    def upsert_company(self, company_data: CompanyWrite) -> Company:
        """Insert or update a company record based on the provided data."""
        try:
            # Check if company exists by symbol
            existing = (
                self._db.query(Company).filter_by(symbol=company_data.symbol).first()
            )

            if existing:
                # Update existing company
                map_model(existing, company_data)
                logger.info(f"Updated company {company_data.symbol}")
            else:
                # Create new company
                existing = Company(**company_data.model_dump(exclude_unset=True))
                self._db.add(existing)
                logger.info(f"Created new company {company_data.symbol}")

            self._db.commit()
            self._db.refresh(existing)
            return existing
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error upserting company {company_data.symbol}: {e}")
            raise

    def upsert_non_us_company(self, company_data: NonUSCompanyWrite) -> NonUSCompany:
        """Insert or update a non-US company record based on the provided data."""
        try:
            # Check if company exists by symbol
            existing = (
                self._db.query(NonUSCompany)
                .filter_by(symbol=company_data.symbol)
                .first()
            )

            if existing:
                # Update existing non-US company
                map_model(existing, company_data)
                logger.info(f"Updated non-US company {company_data.symbol}")
            else:
                # Create new non-US company
                existing = NonUSCompany(**company_data.model_dump(exclude_unset=True))
                self._db.add(existing)
                logger.info(f"Created new non-US company {company_data.symbol}")

            self._db.commit()
            self._db.refresh(existing)
            return existing
        except SQLAlchemyError as e:
            self._db.rollback()
            logger.error(f"Error upserting non-US company {company_data.symbol}: {e}")
            raise
