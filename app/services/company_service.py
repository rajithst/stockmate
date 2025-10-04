from sqlalchemy.orm import Session

from app.db.schemas.company import Company


class CompanyService:
    def __init__(self, session: Session):
        self._db = session

    def get_company_profile(self, symbol: str) -> Company | None:
        return self._db.query(Company).filter(Company.symbol == symbol).first()