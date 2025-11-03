"""
Generic sync service dependency providers for API endpoints.

This module provides a reusable factory pattern to create sync service instances
with all required dependencies, eliminating boilerplate in endpoint files.
"""

from typing import Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from app.clients.fmp.protocol import FMPClientProtocol
from app.dependencies.db import get_db_session
from app.dependencies.market_api import get_fmp_client
from app.services.internal.base_sync_service import BaseSyncService

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
