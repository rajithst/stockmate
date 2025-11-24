"""
Generic sync service dependency providers for API endpoints.

This module provides a reusable factory pattern to create sync service instances
with all required dependencies, eliminating boilerplate in endpoint files.
"""

from typing import Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.core.config import config
from app.dependencies.db import get_db_session
from app.dependencies.market_api import get_fmp_client
from app.repositories.company_repo import CompanyRepository
from app.services.internal.base_sync_service import BaseSyncService
from app.services.pubsub_handler import PubSubHandler
from app.services.pubsub_service import PubSubService
from app.services.cron_dispatcher import CronDispatcher
from app.services.internal.company_sync_service import CompanySyncService
from app.services.internal.market_data_sync_service import MarketDataSyncService
from app.services.internal.financial_statements_sync_service import (
    FinancialStatementsSyncService,
)
from app.services.internal.financial_health_sync_service import FinancialHealthSyncService
from app.services.internal.company_metrics_sync_service import CompanyMetricsSyncService

T = TypeVar("T", bound=BaseSyncService)


def create_sync_service_provider(
    service_class: Type[T],
) -> Callable[[FMPClientProtocol, Session], T]:
    """
    Factory function to create a dependency provider for any sync service.

    This eliminates boilerplate in API endpoint files by providing a generic
    way to inject sync services with all required dependencies.

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


def get_pubsub_handler(
    fmp_client: FMPClientProtocol = Depends(get_fmp_client),
    db_session: Session = Depends(get_db_session),
) -> PubSubHandler:
    """
    Provides a PubSubHandler instance with all required sync services.

    Args:
        fmp_client: FMP API client (injected via Depends)
        db_session: Database session (injected via Depends)

    Returns:
        Initialized PubSubHandler instance
    """
    company_sync_service = CompanySyncService(
        market_api_client=fmp_client, session=db_session
    )
    market_data_sync_service = MarketDataSyncService(
        market_api_client=fmp_client, session=db_session
    )
    financial_statements_sync_service = FinancialStatementsSyncService(
        market_api_client=fmp_client, session=db_session
    )
    financial_health_sync_service = FinancialHealthSyncService(
        market_api_client=fmp_client, session=db_session
    )
    company_metrics_sync_service = CompanyMetricsSyncService(
        market_api_client=fmp_client, session=db_session
    )

    return PubSubHandler(
        company_sync_service=company_sync_service,
        market_data_sync_service=market_data_sync_service,
        financial_statements_sync_service=financial_statements_sync_service,
        financial_health_sync_service=financial_health_sync_service,
        company_metrics_sync_service=company_metrics_sync_service,
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
    company_repo = CompanyRepository(session=db_session)
    return CronDispatcher(
        pubsub_service=pubsub_service,
        company_repo=company_repo,
    )
