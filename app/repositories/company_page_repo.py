from typing import Optional, Tuple

from sqlalchemy.orm import Session

from app.db.models import Company, CompanyGrading


class CompanyPageRepository:
    def __init__(self, db: Session):
        self._db = db

    def get_company_profile_snapshot(
        self, symbol: str
    ) -> Optional[Tuple[Company, CompanyGrading]]:
        # Get company and its latest grading
        company_with_grading = (
            self._db.query(Company, CompanyGrading)
            .outerjoin(CompanyGrading, Company.id == CompanyGrading.company_id)
            .filter(Company.symbol == symbol)
            .first()
        )

        if not company_with_grading:
            return None

        company, grading = company_with_grading
        return company, grading
