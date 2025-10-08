from app.clients.fmp import FMPClient
from app.clients.fmp.protocol import FMPClientProtocol
from app.core.config import config


def get_fmp_client() -> FMPClientProtocol:
    """Dependency that provides an FMPClient instance."""
    return FMPClient(token=config.fmp_api_key)
