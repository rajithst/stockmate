from typing import Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.clients.yfinance.protocol import YFinanceClientProtocol
from app.core.config import config
from app.dependencies.db import get_db_session
from app.dependencies.market_api import get_fmp_client, get_yfinance_client
from app.repositories.company_repo import CompanyRepository
from app.services.internal.base_sync_service import BaseSyncService
from app.services.pubsub_handler import PubSubHandler
from app.services.pubsub_service import PubSubService
from app.services.cron_dispatcher import CronDispatcher
from app.services.internal.company_sync_service import CompanySyncService
from app.services.company_service import CompanyService

T = TypeVar("T", bound=BaseSyncService)


def create_sync_service_provider(
    service_class: Type[T],
) -> Callable[[FMPClientProtocol, Session], T]:
    """
    Factory function to create a dependency provider for any sync service.

    This eliminates boilerplate in API endpoint files by providing a generic
    way to inject sync services with all required dependencies.

    Note: CompanySyncService requires both FMP and YFinance clients,
    so use get_company_sync_service() instead.

    Usage:
        get_dcf_sync_service = create_sync_service_provider(DiscountedCashFlowSyncService)

        @router.get("/{symbol}/sync")
        def sync_endpoint(
            symbol: str,
            service: DiscountedCashFlowSyncService = Depends(get_dcf_sync_service)
        ):
            ...

    Args:
        service_class: The sync service class to create instances of

    Returns:
        A dependency provider function compatible with FastAPI's Depends()
    """

    def get_sync_service(
        fmp_client: FMPClientProtocol = Depends(get_fmp_client),
        db_session: Session = Depends(get_db_session),
    ) -> T:
        """
        Provides a sync service instance with required dependencies.

        Args:
            fmp_client: FMP API client (injected via Depends)
            db_session: Database session (injected via Depends)

        Returns:
            Initialized sync service instance
        """
        return service_class(market_api_client=fmp_client, session=db_session)

    return get_sync_service


def get_company_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    yfinance_client: YFinanceClientProtocol = Depends(get_yfinance_client),
    db_session: Session = Depends(get_db_session),
) -> CompanyService:
    """
    Provides a CompanyService instance for querying company data.

    Args:
        fmp_client: FMP API client for US company data (injected via Depends)
        yfinance_client: YFinance API client for non-US company data (injected via Depends)
        db_session: Database session for persistence operations (injected via Depends)

    Returns:
        Initialized CompanyService instance

    Usage:
        @router.get("/{symbol}")
        def get_company(
            symbol: str,
            service: CompanyService = Depends(get_company_service)
        ):
            result = service.get_company_page(symbol)
            ...
    """
    return CompanyService(
        session=db_session,
        fmp_client=fmp_client,
        yfinance_client=yfinance_client,
    )


def get_company_sync_service(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    yfinance_client: YFinanceClientProtocol = Depends(get_yfinance_client),
    db_session: Session = Depends(get_db_session),
) -> CompanySyncService:
    """
    Provides a CompanySyncService instance with both API clients.

    CompanySyncService is unique in requiring both FMP (for US stocks)
    and YFinance (for non-US stocks) API clients.

    Args:
        fmp_client: FMP API client for US company data (injected via Depends)
        yfinance_client: YFinance API client for non-US company data (injected via Depends)
        db_session: Database session for persistence operations (injected via Depends)

    Returns:
        Initialized CompanySyncService instance

    Usage:
        @router.post("/{symbol}/sync")
        def sync_company(
            symbol: str,
            service: CompanySyncService = Depends(get_company_sync_service)
        ):
            result = service.upsert_company_by_market(symbol)
            ...
    """
    return CompanySyncService(
        fmp_client=fmp_client,
        yfinance_client=yfinance_client,
        session=db_session,
    )


def get_pubsub_handler(
    company_sync_service: CompanySyncService = Depends(get_company_sync_service),
) -> PubSubHandler:
    """
    Provides a PubSubHandler instance with all required sync services.

    Args:
        company_sync_service: CompanySyncService instance (injected via Depends)

    Returns:
        Initialized PubSubHandler instance
    """
    return PubSubHandler(
        company_sync_service=company_sync_service,
    )


def get_pubsub_service() -> PubSubService:
    """
    Provides a PubSubService instance.

    Returns:
        Initialized PubSubService instance
    """
    return PubSubService(
        project_id=config.gcp_project_id,
    )


def get_cron_dispatcher(
    pubsub_service: PubSubService = Depends(get_pubsub_service),
    db_session: Session = Depends(get_db_session),
) -> CronDispatcher:
    """
    Provides a CronDispatcher instance with all required dependencies.

    Args:
        pubsub_service: PubSubService instance (injected)
        db_session: Database session (injected)

    Returns:
        Initialized CronDispatcher instance
    """
    company_repo = CompanyRepository(db=db_session)
    return CronDispatcher(
        pubsub_service=pubsub_service,
        company_repo=company_repo,
    )
