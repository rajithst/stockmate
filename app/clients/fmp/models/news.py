from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class FMPNews(BaseModel):
    symbol: Optional[str] = None
    published_date: datetime = Field(..., alias="publishedDate")
    publisher: str
    title: str
    image: HttpUrl
    site: str
    text: str
    url: HttpUrl

    model_config = ConfigDict(populate_by_name=True)
