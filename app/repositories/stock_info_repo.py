from sqlalchemy.orm import Session

from app.db.models.dividend import CompanyDividend
from app.db.models.stock import CompanyStockPeer, CompanyStockSplit
from app.schemas.dividend import CompanyDividendWrite
from app.schemas.stock import CompanyStockPeerWrite, CompanyStockSplitWrite
from app.util.model_mapper import map_model


class StockInfoRepository:
    def __init__(self, session: Session) -> None:
        self._db = session

    def get_dividends_by_symbol(self, symbol: str) -> list[CompanyDividend]:
        return (
            self._db.query(CompanyDividend)
            .filter(CompanyDividend.symbol == symbol)
            .all()
        )

    def get_stock_splits_by_symbol(self, symbol: str) -> list[CompanyStockSplit]:
        return (
            self._db.query(CompanyStockSplit)
            .filter(CompanyStockSplit.symbol == symbol)
            .all()
        )

    def get_stock_peers_by_symbol(self, symbol: str) -> list[CompanyStockPeer]:
        return (
            self._db.query(CompanyStockPeer)
            .filter(CompanyStockPeer.symbol == symbol)
            .all()
        )

    def upsert_dividends(
        self, dividends_data: list[CompanyDividendWrite]
    ) -> list[CompanyDividend] | None:
        dividend_records = []
        for dividend in dividends_data:
            existing = (
                self._db.query(CompanyDividend)
                .filter_by(symbol=dividend.symbol, date=dividend.date)
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
                .filter_by(symbol=split.symbol, date=split.date)
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
        self, peers_data: list[CompanyStockPeerWrite]
    ) -> list[CompanyStockPeer]:
        peer_records = []
        for peer in peers_data:
            existing = (
                self._db.query(CompanyStockPeer)
                .filter_by(symbol=peer.symbol, company_id=peer.company_id)
                .first()
            )
            if existing:
                peer_record = map_model(existing, peer)
            else:
                peer_record = CompanyStockPeer(**peer.model_dump(exclude_unset=True))
                self._db.add(peer_record)
            peer_records.append(peer_record)
        self._db.commit()
        for record in peer_records:
            self._db.refresh(record)
        return peer_records
