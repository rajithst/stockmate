from app.clients.fmp.fmp_client import FMPClient
from app.clients.fmp.protocol import FMPClientProtocol
from app.core.config import config


def get_fmp_client() -> FMPClientProtocol:
    return FMPClient(token=config.fmp_api_key)
