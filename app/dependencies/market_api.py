from app.clients.fmp import FMPClient
from app.clients.fmp.protocol import FMPClientProtocol
from app.clients.yfinance.yfinance_client import YFinanceClient
from app.clients.yfinance.protocol import YFinanceClientProtocol
from app.core.config import config


def get_fmp_client() -> FMPClientProtocol:
    """Dependency that provides an FMPClient instance."""
    return FMPClient(token=config.fmp_api_key)


def get_yfinance_client() -> YFinanceClientProtocol:
    """Dependency that provides a YFinanceClient instance."""
    return YFinanceClient()
