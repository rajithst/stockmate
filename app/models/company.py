from pydantic import BaseModel


class CompanyProfileRead(BaseModel):
    symbol: str
    company_name: str
