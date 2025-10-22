from sqlalchemy.orm import Session

from app.db.models.dividend import CompanyDividend
from app.db.models.stock import CompanyStockPeer, CompanyStockSplit
from app.schemas.dividend import CompanyDividendWrite
from app.schemas.stock import CompanyStockPeerWrite, CompanyStockSplitWrite
from app.util.map_model import map_model


class StockInfoRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def get_dividends_by_symbol(self, symbol: str) -> list[CompanyDividend]:
        return (
            self._db.query(CompanyDividend)
            .filter(CompanyDividend.company_symbol == symbol)
            .all()
        )

    def get_stock_splits_by_symbol(self, symbol: str) -> list[CompanyStockSplit]:
        return (
            self._db.query(CompanyStockSplit)
            .filter(CompanyStockSplit.company_symbol == symbol)
            .all()
        )

    def get_stock_peers_by_symbol(self, symbol: str) -> list[CompanyStockPeer]:
        return (
            self._db.query(CompanyStockPeer)
            .filter(CompanyStockPeer.company_symbol == symbol)
            .all()
        )

    def upsert_dividends(
        self, dividends_data: list[CompanyDividendWrite]
    ) -> list[CompanyDividend] | None:
        dividend_records = []
        for dividend in dividends_data:
            existing = (
                self._db.query(CompanyDividend)
                .filter_by(company_symbol=dividend.symbol, date=dividend.date)
                .first()
            )
            if existing:
                dividend_record = map_model(existing, dividend)
            else:
                dividend_record = CompanyDividend(
                    **dividend.model_dump(exclude_unset=True)
                )
                self._db.add(dividend_record)
            dividend_records.append(dividend_record)
        self._db.commit()
        for record in dividend_records:
            self._db.refresh(record)
        return dividend_records

    def upsert_stock_splits(
        self, splits_data: list[CompanyStockSplitWrite]
    ) -> list[CompanyStockSplit] | None:
        split_records = []
        for split in splits_data:
            existing = (
                self._db.query(CompanyStockSplit)
                .filter_by(company_symbol=split.symbol, date=split.date)
                .first()
            )
            if existing:
                split_record = map_model(existing, split)
            else:
                split_record = CompanyStockSplit(**split.model_dump(exclude_unset=True))
                self._db.add(split_record)
            split_records.append(split_record)
        self._db.commit()
        for record in split_records:
            self._db.refresh(record)
        return split_records

    def upsert_stock_peers(
        self, symbol: str, peers_data: list[CompanyStockPeerWrite]
    ) -> list[CompanyStockPeer]:
        from app.db.models.stock import CompanyStockPeer

        # First, delete existing peers for the symbol
        self._db.query(CompanyStockPeer).filter_by(company_symbol=symbol).delete()

        peer_records = []
        for peer_symbol in peers_data:
            peer_record = CompanyStockPeer(
                company_symbol=symbol, peer_symbol=peer_symbol
            )
            self._db.add(peer_record)
            peer_records.append(peer_record)

        self._db.commit()
        for record in peer_records:
            self._db.refresh(record)
        return peer_records
