from app.schemas.quote import StockPriceChangeRead
from app.db.models.quote import StockPriceChange


class MockStockPriceChangeDataBuilder:
    @staticmethod
    def stock_price_change_read(**overrides) -> StockPriceChangeRead:
        """Build StockPriceChangeRead test data."""
        defaults = {
            "id": 1,
            "company_id": 1,
            "symbol": "AAPL",
            "one_day": 2.5,
            "five_day": 3.0,
            "one_month": 5.0,
            "three_month": 7.5,
            "six_month": 10.0,
            "ytd": 12.0,
            "one_year": 15.0,
            "three_year": 25.0,
            "five_year": 40.0,
            "ten_year": 80.0,
            "created_at": "2023-10-01T00:00:00Z",
            "updated_at": "2023-10-01T00:00:00Z",
        }
        return StockPriceChangeRead(**(defaults | overrides))

    @staticmethod
    def save_stock_price_change(db_session, **overrides) -> StockPriceChange:
        """Save StockPriceChangeRead test data to the database."""
        defaults = {
            "company_id": 1,
            "symbol": "AAPL",
            "one_day": 2.5,
            "five_day": 3.0,
            "one_month": 5.0,
            "three_month": 7.5,
            "six_month": 10.0,
            "ytd": 12.0,
            "one_year": 15.0,
            "three_year": 25.0,
            "five_year": 40.0,
            "ten_year": 80.0,
        }
        price_change_data = {**defaults, **overrides}
        stock_price_change = StockPriceChange(**price_change_data)
        db_session.add(stock_price_change)
        db_session.commit()
        db_session.refresh(stock_price_change)
        return stock_price_change
