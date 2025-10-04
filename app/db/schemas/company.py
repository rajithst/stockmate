from sqlalchemy import String, Float
from sqlalchemy.orm import Mapped, mapped_column

from app.db.engine import Base


class Company(Base):
    __tablename__ = "company"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    symbol: Mapped[str] = mapped_column(String(250), nullable=False)
    company_name: Mapped[str] = mapped_column(String(250), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    market_cap: Mapped[float] = mapped_column(Float, nullable=False)
    currency: Mapped[str] = mapped_column(String(50), nullable=False)
    exchange_full_name: Mapped[str] = mapped_column(String(250), nullable=False)
    exchange: Mapped[str] = mapped_column(String(250), nullable=False)
    industry: Mapped[str] = mapped_column(String(250), nullable=True)
    website: Mapped[str] = mapped_column(String(250), nullable=True)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    sector: Mapped[str] = mapped_column(String(250), nullable=True)
    country: Mapped[str] = mapped_column(String(250), nullable=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=True)
    address: Mapped[str] = mapped_column(String(250), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(100), nullable=True)
    zip: Mapped[str] = mapped_column(String(20), nullable=True)
    image: Mapped[str] = mapped_column(String(250), nullable=True)
    ipo_date: Mapped[str] = mapped_column(String(50), nullable=True)
