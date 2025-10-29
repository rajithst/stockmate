import datetime

from pydantic import BaseModel, ConfigDict


class CompanyTechnicalIndicator(BaseModel):
    company_id: int
    symbol: str
    date: str
    simple_moving_average: float | None = None
    exponential_moving_average: float | None = None
    weighted_moving_average: float | None = None
    double_exponential_moving_average: float | None = None
    triple_exponential_moving_average: float | None = None
    relative_strength_index: float | None = None
    standard_deviation: float | None = None
    williams_percent_r: float | None = None
    average_directional_index: float | None = None

    model_config = ConfigDict(from_attributes=True)


class CompanyTechnicalIndicatorWrite(CompanyTechnicalIndicator):
    model_config = ConfigDict(from_attributes=True)


class CompanyTechnicalIndicatorRead(CompanyTechnicalIndicator):
    id: int
    created_at: datetime.datetime | None = None
    updated_at: datetime.datetime | None = None

    model_config = ConfigDict(from_attributes=True)
