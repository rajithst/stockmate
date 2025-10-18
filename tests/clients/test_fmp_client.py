# import pytest
# from unittest.mock import Mock, patch, MagicMock
# import requests
# from typing import Any, Dict

# from app.clients.fmp.fmp_client import FMPClient
# from app.clients.fmp.models.company import FMPCompanyProfile
# from app.clients.fmp.models.stock import FMPStockScreenResult, FMPStockPeer
# from app.clients.fmp.models.dividend import FMPDividend


# class TestFMPClient:
#     """Test suite for FMPClient."""

#     @pytest.fixture
#     def client(self):
#         """Create FMP client instance for testing."""
#         return FMPClient(token="test_api_key")

#     @pytest.fixture
#     def mock_company_profile_data(self):
#         """Mock company profile response data."""
#         return {
#             "symbol": "AAPL",
#             "companyName": "Apple Inc.",
#             "price": 150.25,
#             "marketCap": 2500000000000,
#             "currency": "USD",
#             "exchangeShortName": "NASDAQ",
#             "industry": "Consumer Electronics",
#             "website": "https://www.apple.com",
#             "description": "Apple Inc. designs and manufactures consumer electronics.",
#             "sector": "Technology",
#             "country": "US",
#             "phone": "1-408-996-1010",
#             "address": "One Apple Park Way",
#             "city": "Cupertino",
#             "state": "CA",
#             "zip": "95014",
#             "image": "https://financialmodelingprep.com/image-stock/AAPL.png"
#         }

#     @pytest.fixture
#     def mock_stock_screener_data(self):
#         """Mock stock screener response data."""
#         return [
#             {
#                 "symbol": "AAPL",
#                 "companyName": "Apple Inc.",
#                 "marketCap": 2500000000000,
#                 "sector": "Technology",
#                 "industry": "Consumer Electronics",
#                 "beta": 1.2,
#                 "price": 150.25,
#                 "volume": 50000000,
#                 "exchange": "NASDAQ"
#             },
#             {
#                 "symbol": "GOOGL",
#                 "companyName": "Alphabet Inc.",
#                 "marketCap": 1800000000000,
#                 "sector": "Communication Services",
#                 "industry": "Internet Content & Information",
#                 "beta": 1.1,
#                 "price": 125.50,
#                 "volume": 25000000,
#                 "exchange": "NASDAQ"
#             }
#         ]

#     def test_init(self):
#         """Test FMPClient initialization."""
#         token = "test_api_key"
#         client = FMPClient(token=token)

#         assert client.token == token
#         assert client.BASE_URL == "https://financialmodelingprep.com/stable"
#         assert client.timeout == 10

#     @patch('app.clients.fmp.fmp_client.fmpsdk.stock_screener')
#     def test_get_stock_screeners_success(self, mock_screener, client, mock_stock_screener_data):
#         """Test successful stock screener request."""
#         # Arrange
#         mock_screener.return_value = mock_stock_screener_data
#         params = {
#             "market_cap_more_than": 1000000000,
#             "sector": "Technology",
#             "limit": 10
#         }

#         # Act
#         result = client.get_stock_screeners(params)

#         # Assert
#         assert len(result) == 2
#         assert all(isinstance(stock, FMPStockScreenResult) for stock in result)
#         assert result[0].symbol == "AAPL"
#         assert result[1].symbol == "GOOGL"

#         # Verify the API was called with correct parameters
#         mock_screener.assert_called_once_with(
#             market_cap_more_than=1000000000,
#             market_cap_lower_than=None,
#             beta_more_than=None,
#             beta_lower_than=None,
#             volume_more_than=None,
#             volume_lower_than=None,
#             price_more_than=None,
#             price_lower_than=None,
#             dividend_more_than=None,
#             dividend_lower_than=None,
#             is_actively_trading=None,
#             exchange=None,
#             sector="Technology",
#             industry=None,
#             country=None,
#             limit=10,
#             apikey="test_api_key"
#         )

#     @patch('app.clients.fmp.fmp_client.fmpsdk.stock_screener')
#     def test_get_stock_screeners_empty_response(self, mock_screener, client):
#         """Test stock screener with empty response."""
#         # Arrange
#         mock_screener.return_value = []
#         params = {"limit": 10}

#         # Act
#         result = client.get_stock_screeners(params)

#         # Assert
#         assert result == []

#     @patch('app.clients.fmp.fmp_client.fmpsdk.stock_screener')
#     def test_get_stock_screeners_none_response(self, mock_screener, client):
#         """Test stock screener with None response."""
#         # Arrange
#         mock_screener.return_value = None
#         params = {"limit": 10}

#         # Act
#         result = client.get_stock_screeners(params)

#         # Assert
#         assert result == []

#     @patch.object(FMPClient, '_FMPClient__get_by_url')
#     def test_get_company_profile_success(self, mock_get_by_url, client, mock_company_profile_data):
#         """Test successful company profile retrieval."""
#         # Arrange
#         mock_get_by_url.return_value = [mock_company_profile_data]

#         # Act
#         result = client.get_company_profile("AAPL")

#         # Assert
#         assert isinstance(result, FMPCompanyProfile)
#         assert result.symbol == "AAPL"
#         assert result.companyName == "Apple Inc."
#         assert result.price == 150.25

#         mock_get_by_url.assert_called_once_with(
#             endpoint="profile",
#             params={"symbol": "AAPL"}
#         )

#     @patch.object(FMPClient, '_FMPClient__get_by_url')
#     def test_get_company_profile_empty_response(self, mock_get_by_url, client):
#         """Test company profile with empty response."""
#         # Arrange
#         mock_get_by_url.return_value = []

#         # Act
#         result = client.get_company_profile("INVALID")

#         # Assert
#         assert result is None

#     @patch.object(FMPClient, '_FMPClient__get_by_url')
#     def test_get_company_profile_none_response(self, mock_get_by_url, client):
#         """Test company profile with None response."""
#         # Arrange
#         mock_get_by_url.return_value = None

#         # Act
#         result = client.get_company_profile("INVALID")

#         # Assert
#         assert result is None

#     @patch('app.clients.fmp.fmp_client.fmpsdk.company_valuation.stock_peers')
#     def test_get_stock_peer_companies_success(self, mock_peers, client):
#         """Test successful peer companies retrieval."""
#         # Arrange
#         mock_peer_data = [
#             {"symbol": "MSFT", "companyName": "Microsoft Corporation"},
#             {"symbol": "GOOGL", "companyName": "Alphabet Inc."}
#         ]
#         mock_peers.return_value = mock_peer_data

#         # Act
#         result = client.get_stock_peer_companies("AAPL")

#         # Assert
#         assert len(result) == 2
#         assert all(isinstance(peer, FMPStockPeer) for peer in result)
#         assert result[0].symbol == "MSFT"
#         assert result[1].symbol == "GOOGL"

#         mock_peers.assert_called_once_with(symbol="AAPL", apikey="test_api_key")

#     @patch('app.clients.fmp.fmp_client.fmpsdk.company_valuation.stock_peers')
#     def test_get_stock_peer_companies_empty_response(self, mock_peers, client):
#         """Test peer companies with empty response."""
#         # Arrange
#         mock_peers.return_value = []

#         # Act
#         result = client.get_stock_peer_companies("INVALID")

#         # Assert
#         assert result == []

#     @patch('requests.get')
#     def test_private_get_by_url_success(self, mock_get, client):
#         """Test private __get_by_url method success."""
#         # Arrange
#         mock_response = Mock()
#         mock_response.json.return_value = {"test": "data"}
#         mock_response.raise_for_status.return_value = None
#         mock_get.return_value = mock_response

#         # Act
#         result = client._FMPClient__get_by_url("test-endpoint", {"param": "value"})

#         # Assert
#         assert result == {"test": "data"}
#         mock_get.assert_called_once_with(
#             f"{client.BASE_URL}/test-endpoint",
#             params={"param": "value", "apikey": "test_api_key"},
#             timeout=10
#         )
#         mock_response.raise_for_status.assert_called_once()

#     @patch('requests.get')
#     def test_private_get_by_url_timeout(self, mock_get, client):
#         """Test __get_by_url with timeout exception."""
#         # Arrange
#         mock_get.side_effect = requests.Timeout("Request timed out")

#         # Act & Assert
#         with pytest.raises(requests.Timeout):
#             client._FMPClient__get_by_url("test-endpoint")

#     @patch('requests.get')
#     def test_private_get_by_url_http_error(self, mock_get, client):
#         """Test __get_by_url with HTTP error."""
#         # Arrange
#         mock_response = Mock()
#         mock_response.raise_for_status.side_effect = requests.HTTPError("404 Not Found")
#         mock_get.return_value = mock_response

#         # Act & Assert
#         with pytest.raises(requests.HTTPError):
#             client._FMPClient__get_by_url("test-endpoint")

#     @patch('requests.get')
#     def test_private_get_by_url_connection_error(self, mock_get, client):
#         """Test __get_by_url with connection error."""
#         # Arrange
#         mock_get.side_effect = requests.ConnectionError("Connection failed")

#         # Act & Assert
#         with pytest.raises(requests.ConnectionError):
#             client._FMPClient__get_by_url("test-endpoint")

#     @patch('requests.get')
#     def test_private_get_by_url_json_decode_error(self, mock_get, client):
#         """Test __get_by_url with JSON decode error."""
#         # Arrange
#         mock_response = Mock()
#         mock_response.json.side_effect = ValueError("Invalid JSON")
#         mock_response.raise_for_status.return_value = None
#         mock_get.return_value = mock_response

#         # Act & Assert
#         with pytest.raises(ValueError):
#             client._FMPClient__get_by_url("test-endpoint")

#     def test_get_stock_screeners_with_all_params(self, client):
#         """Test stock screener with all possible parameters."""
#         with patch('app.clients.fmp.fmp_client.fmpsdk.stock_screener') as mock_screener:
#             # Arrange
#             mock_screener.return_value = []
#             params = {
#                 "market_cap_more_than": 1000000000,
#                 "market_cap_lower_than": 5000000000000,
#                 "beta_more_than": 0.5,
#                 "beta_lower_than": 2.0,
#                 "volume_more_than": 1000000,
#                 "volume_lower_than": 100000000,
#                 "price_more_than": 10.0,
#                 "price_lower_than": 500.0,
#                 "dividend_more_than": 0.01,
#                 "dividend_lower_than": 0.10,
#                 "is_actively_trading": True,
#                 "exchange": "NASDAQ",
#                 "sector": "Technology",
#                 "industry": "Software",
#                 "country": "US",
#                 "limit": 50
#             }

#             # Act
#             result = client.get_stock_screeners(params)

#             # Assert
#             mock_screener.assert_called_once_with(
#                 market_cap_more_than=1000000000,
#                 market_cap_lower_than=5000000000000,
#                 beta_more_than=0.5,
#                 beta_lower_than=2.0,
#                 volume_more_than=1000000,
#                 volume_lower_than=100000000,
#                 price_more_than=10.0,
#                 price_lower_than=500.0,
#                 dividend_more_than=0.01,
#                 dividend_lower_than=0.10,
#                 is_actively_trading=True,
#                 exchange="NASDAQ",
#                 sector="Technology",
#                 industry="Software",
#                 country="US",
#                 limit=50,
#                 apikey="test_api_key"
#             )
#             assert result == []

#     @pytest.mark.parametrize("invalid_symbol", ["", "   ", None])
#     def test_get_company_profile_invalid_symbols(self, client, invalid_symbol):
#         """Test company profile with invalid symbols."""
#         with patch.object(FMPClient, '_FMPClient__get_by_url') as mock_get:
#             # This would likely cause an error in real implementation
#             # but we test the behavior as-is
#             client.get_company_profile(invalid_symbol)
#             mock_get.assert_called_once_with(
#                 endpoint="profile",
#                 params={"symbol": invalid_symbol}
#             )
