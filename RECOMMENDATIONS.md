# StockMate - Actionable Recommendations

This document provides specific, actionable steps to improve the StockMate codebase based on the comprehensive code review.

---

## 🔴 Critical Fixes (Do This Week)

### 1. Fix Pydantic v2 Deprecation Warnings

**Problem**: 20 deprecation warnings from Pydantic v1 syntax that will break in v3.

**Files to Update:**
- `app/clients/fmp/models/analyst_estimates.py`
- `app/clients/fmp/models/company.py`
- `app/clients/fmp/models/discounted_cashflow.py`
- `app/clients/fmp/models/dividend.py`
- `app/clients/fmp/models/earnings.py`
- `app/clients/fmp/models/financial_ratios.py`
- `app/clients/fmp/models/financial_statements.py`
- `app/clients/fmp/models/news.py`
- `app/clients/fmp/models/stock.py`

**How to Fix:**
```python
# Before
class FMPCompanyProfile(BaseModel):
    class Config:
        allow_population_by_field_name = True

# After
from pydantic import ConfigDict

class FMPCompanyProfile(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
```

**Estimated Time**: 2 hours

---

### 2. Fix Critical Bugs in FMP Client

**Location**: `app/clients/fmp/fmp_client.py`

**Bug 1 (Line 98):**
```python
# Current - WRONG
return [FMPDividend(**dividend) for dividend in calendar] if dividend_calendar else []

# Fixed
return [FMPDividend(**dividend) for dividend in calendar] if calendar else []
```

**Bug 2 (Line 164):**
```python
# Current - WRONG
return [FMPKeyMetrics(**metric) for metric in key_metrics_data] if key_metrics else []

# Fixed
return [FMPKeyMetrics(**metric) for metric in key_metrics_data] if key_metrics_data else []
```

**Estimated Time**: 15 minutes

---

### 3. Add Configuration Validation

**Location**: `app/core/config.py`

**Implementation:**
```python
from pydantic import field_validator, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    app_name: str = "StockMate"
    debug: bool = False

    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 3306
    db_name: str
    fmp_api_key: str
    openai_api_key: str

    @field_validator('db_user', 'db_password', 'db_name', 'fmp_api_key')
    @classmethod
    def validate_required_fields(cls, v: str, info) -> str:
        if not v or v.strip() == "":
            raise ValueError(f"{info.field_name} is required and cannot be empty")
        return v

    @property
    def db_url(self) -> str:
        safe_password = quote_plus(self.db_password)
        return (
            f"mysql+pymysql://{self.db_user}:{safe_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

# Add startup validation
try:
    config = Config()
except ValidationError as e:
    print(f"Configuration error: {e}")
    raise
```

**Estimated Time**: 30 minutes

---

### 4. Add Basic README

**Location**: `README.md`

**Content:**
```markdown
# StockMate

A FastAPI-based stock market data aggregation platform that fetches and stores financial data from Financial Modeling Prep (FMP) API.

## Features

- Company profile management
- Financial statements (Income, Balance Sheet, Cash Flow)
- Stock ratings and analyst grades
- Dividend and stock split tracking
- News aggregation (general, price targets, grading)
- RESTful API with automatic documentation

## Tech Stack

- **Framework**: FastAPI 0.117+
- **Database**: MySQL (via SQLAlchemy 2.0)
- **Migrations**: Alembic
- **External API**: Financial Modeling Prep (FMP)
- **Testing**: Pytest
- **Python**: 3.12+

## Quick Start

### Prerequisites

- Python 3.12+
- MySQL 8.0+
- FMP API Key (get from https://financialmodelingprep.com/)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/rajithst/stockmate.git
cd stockmate
```

2. Install dependencies:
```bash
pip install alembic fastapi[standard] fmpsdk pydantic-settings pymysql pytest python-dotenv sqlalchemy uvicorn
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

Required environment variables:
```
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=stockmate
FMP_API_KEY=your_fmp_api_key
OPENAI_API_KEY=your_openai_api_key
DEBUG=false
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the application:
```bash
uvicorn app.main:app --reload
```

6. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Public API (`/api/v1`)

- `GET /api/v1/company/{symbol}` - Get company profile

### Internal API (`/internal`)

- `GET /internal/company/{symbol}/sync` - Sync company data from FMP

## Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=app --cov-report=html
```

## Project Structure

```
stockmate/
├── alembic/              # Database migrations
├── app/
│   ├── api/             # API routes
│   │   ├── internal/   # Internal endpoints
│   │   └── v1/         # Public API v1
│   ├── clients/        # External API clients
│   │   └── fmp/       # FMP client
│   ├── core/          # Core configuration
│   ├── db/            # Database models and engine
│   ├── dependencies/  # FastAPI dependencies
│   ├── repositories/  # Data access layer
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── util/          # Utilities
└── tests/             # Test suite
```

## Development

### Code Quality

```bash
# Format code
black app/ tests/

# Lint
ruff check app/ tests/

# Type check
mypy app/
```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Add your license here]

## Support

For issues and questions, please open a GitHub issue.
```

**Estimated Time**: 1 hour

---

### 5. Add Authentication to Internal Endpoints

**Location**: `app/api/internal/company_data.py`

**Implementation:**
```python
from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

router = APIRouter(prefix="/company")

# Add API Key header
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify internal API key"""
    from app.core.config import config
    if api_key != config.internal_api_key:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

@router.get("/{symbol}/sync", response_model=CompanyRead)
def sync_company_profile(
    symbol: str, 
    service: CompanySyncService = Depends(get_company_sync_service),
    api_key: str = Depends(verify_api_key)  # Add this
):
    company = service.upsert_company(symbol)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company
```

Add to `.env`:
```
INTERNAL_API_KEY=your-secure-random-key-here
```

**Estimated Time**: 30 minutes

---

## 🟡 High Priority (Do This Sprint)

### 6. Improve Error Handling and Logging

**Locations**: Multiple files

**Create Logging Utility** (`app/util/logging.py`):
```python
import logging
import sys
from typing import Optional

def setup_logger(name: str, level: Optional[int] = None) -> logging.Logger:
    """Create a configured logger instance"""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    if level:
        logger.setLevel(level)
    
    return logger
```

**Update FMP Client** (`app/clients/fmp/fmp_client.py`):
```python
from app.util.logging import setup_logger

logger = setup_logger(__name__)

class FMPClient:
    def __get_by_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
        if params is None:
            params = {}
        params["apikey"] = self.token

        internal_url = f"{self.BASE_URL}/{endpoint}"

        try:
            logger.info(f"Calling FMP API: {endpoint}")
            response = requests.get(internal_url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.Timeout as e:
            logger.error(f"Timeout calling {endpoint}: {e}")
            raise
        except requests.HTTPError as e:
            logger.error(f"HTTP error calling {endpoint}: {e.response.status_code}")
            raise
        except requests.RequestException as e:
            logger.error(f"Request error calling {endpoint}: {e}", exc_info=True)
            raise
```

**Update API Endpoints** (`app/api/v1/company.py`):
```python
from app.util.logging import setup_logger

logger = setup_logger(__name__)

@router.get("/{symbol}", response_model=CompanyRead)
def get_company_profile(symbol: str, service: CompanyService = Depends(get_company_service)):
    logger.info(f"Fetching company profile for: {symbol}")
    try:
        company = service.get_company_profile(symbol)
        if not company:
            logger.warning(f"Company not found: {symbol}")
            raise HTTPException(status_code=404, detail=f"Company not found: {symbol}")
        logger.info(f"Successfully retrieved company: {symbol}")
        return company
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error fetching company {symbol}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
```

**Estimated Time**: 3 hours

---

### 7. Add Database Constraints and Fix Types

**Create New Migration**:
```bash
alembic revision -m "add_constraints_and_fix_types"
```

**Migration File**:
```python
def upgrade() -> None:
    # Add unique constraint on company.symbol
    op.create_unique_constraint('uq_company_symbol', 'company', ['symbol'])
    
    # Add unique constraints on financial statements
    op.create_unique_constraint(
        'uq_balance_sheet_symbol_date_period',
        'company_balance_sheets',
        ['symbol', 'date', 'period']
    )
    
    op.create_unique_constraint(
        'uq_income_statement_symbol_date_period',
        'company_income_statements',
        ['symbol', 'date', 'period']
    )
    
    op.create_unique_constraint(
        'uq_cashflow_symbol_date_period',
        'company_cash_flow_statements',
        ['symbol', 'date', 'period']
    )

def downgrade() -> None:
    op.drop_constraint('uq_company_symbol', 'company', type_='unique')
    op.drop_constraint('uq_balance_sheet_symbol_date_period', 'company_balance_sheets', type_='unique')
    op.drop_constraint('uq_income_statement_symbol_date_period', 'company_income_statements', type_='unique')
    op.drop_constraint('uq_cashflow_symbol_date_period', 'company_cash_flow_statements', type_='unique')
```

**Estimated Time**: 2 hours

---

### 8. Increase Test Coverage

**Create Test Structure**:
```bash
mkdir -p tests/unit tests/integration
mkdir -p tests/unit/clients tests/unit/services tests/unit/repositories
```

**Add FMP Client Tests** (`tests/unit/clients/test_fmp_client.py`):
```python
import pytest
from unittest.mock import Mock, patch
from app.clients.fmp import FMPClient

class TestFMPClient:
    @pytest.fixture
    def client(self):
        return FMPClient(token="test_token")
    
    @patch('requests.get')
    def test_get_company_profile_success(self, mock_get, client):
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = [{
            "symbol": "AAPL",
            "companyName": "Apple Inc.",
            "price": 150.0,
            "marketCap": 2500000000000,
            # ... other fields
        }]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Act
        result = client.get_company_profile("AAPL")
        
        # Assert
        assert result is not None
        assert result.symbol == "AAPL"
        mock_get.assert_called_once()
    
    @patch('requests.get')
    def test_get_company_profile_timeout(self, mock_get, client):
        # Arrange
        mock_get.side_effect = requests.Timeout()
        
        # Act & Assert
        with pytest.raises(requests.Timeout):
            client.get_company_profile("AAPL")
    
    def test_get_income_statement_invalid_period(self, client):
        # Act & Assert
        with pytest.raises(ValueError, match="Period must be"):
            client.get_income_statement("AAPL", period="invalid")
```

**Add Repository Tests** (`tests/unit/repositories/test_company_repo.py`):
```python
from app.repositories.company_repo import CompanyRepository
from app.schemas.company import CompanyIn
from tests.data.company_test_data import create_company

class TestCompanyRepository:
    def test_get_company_by_symbol_found(self, db_session):
        # Arrange
        create_company(db_session, symbol="AAPL")
        repo = CompanyRepository(db_session)
        
        # Act
        result = repo.get_company_by_symbol("AAPL")
        
        # Assert
        assert result is not None
        assert result.symbol == "AAPL"
    
    def test_upsert_company_creates_new(self, db_session):
        # Arrange
        repo = CompanyRepository(db_session)
        company_data = CompanyIn(
            symbol="MSFT",
            company_name="Microsoft",
            # ... other fields
        )
        
        # Act
        result = repo.upsert_company(company_data)
        
        # Assert
        assert result.id is not None
        assert result.symbol == "MSFT"
    
    def test_upsert_company_updates_existing(self, db_session):
        # Arrange
        existing = create_company(db_session, symbol="GOOGL", price=100.0)
        repo = CompanyRepository(db_session)
        company_data = CompanyIn(
            symbol="GOOGL",
            price=150.0,  # Updated price
            # ... other fields
        )
        
        # Act
        result = repo.upsert_company(company_data)
        
        # Assert
        assert result.id == existing.id  # Same record
        assert result.price == 150.0  # Updated
```

**Target**: 80% code coverage

**Estimated Time**: 8 hours

---

### 9. Standardize Table Naming

**Create Migration**:
```bash
alembic revision -m "rename_company_table_to_companies"
```

**Migration**:
```python
def upgrade() -> None:
    op.rename_table('company', 'companies')
    
    # Update foreign key references
    op.drop_constraint('company_balance_sheets_company_id_fkey', 'company_balance_sheets')
    op.create_foreign_key(
        'company_balance_sheets_company_id_fkey',
        'company_balance_sheets', 'companies',
        ['company_id'], ['id'],
        ondelete='CASCADE'
    )
    # Repeat for other tables...

def downgrade() -> None:
    op.rename_table('companies', 'company')
    # Reverse foreign keys...
```

**Update Model** (`app/db/models/company.py`):
```python
class Company(Base):
    __tablename__ = "companies"  # Changed from "company"
```

**Estimated Time**: 2 hours

---

### 10. Add Input Validation Enums

**Create Enums File** (`app/util/enums.py`):
```python
from enum import Enum

class Period(str, Enum):
    """Financial statement period types"""
    QUARTER = "quarter"
    ANNUAL = "annual"
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"
    FY = "FY"

class Exchange(str, Enum):
    """Stock exchanges"""
    NYSE = "NYSE"
    NASDAQ = "NASDAQ"
    AMEX = "AMEX"
    # Add more as needed

class Sector(str, Enum):
    """Market sectors"""
    TECHNOLOGY = "Technology"
    HEALTHCARE = "Healthcare"
    FINANCIAL = "Financial Services"
    # Add more as needed
```

**Update FMP Client**:
```python
from app.util.enums import Period

def get_income_statement(
    self, 
    symbol: str, 
    period: Period = Period.ANNUAL, 
    limit: int = 5
) -> list[FMPCompanyIncomeStatement]:
    # No validation needed - Pydantic handles it
    income_statements = fmpsdk.income_statement(
        symbol=symbol, 
        period=period.value,  # Use .value 
        limit=limit, 
        apikey=self.token
    )
    return [FMPCompanyIncomeStatement(**stmt) for stmt in income_statements] if income_statements else []
```

**Estimated Time**: 2 hours

---

## 🟢 Medium Priority (Next Sprint)

### 11. Implement Caching

**Install Redis Client**:
```bash
pip install redis
```

**Create Cache Utility** (`app/util/cache.py`):
```python
import json
import redis
from typing import Optional, Any
from app.core.config import config

redis_client = redis.Redis(
    host=config.redis_host,
    port=config.redis_port,
    db=0,
    decode_responses=True
)

def cache_get(key: str) -> Optional[Any]:
    """Get value from cache"""
    value = redis_client.get(key)
    return json.loads(value) if value else None

def cache_set(key: str, value: Any, ttl: int = 3600):
    """Set value in cache with TTL in seconds"""
    redis_client.setex(key, ttl, json.dumps(value))

def cache_delete(key: str):
    """Delete key from cache"""
    redis_client.delete(key)
```

**Update Service with Caching**:
```python
from app.util.cache import cache_get, cache_set

class CompanyService:
    def get_company_profile(self, symbol: str) -> CompanyRead | None:
        # Check cache first
        cache_key = f"company:{symbol}"
        cached = cache_get(cache_key)
        if cached:
            return CompanyRead(**cached)
        
        # Fetch from database
        repository = CompanyRepository(self._db)
        company = repository.get_company_by_symbol(symbol)
        
        if company:
            result = CompanyRead.model_validate(company, from_attributes=True)
            # Cache for 1 hour
            cache_set(cache_key, result.model_dump(), ttl=3600)
            return result
        
        return None
```

**Estimated Time**: 4 hours

---

### 12. Add Rate Limiting

**Install slowapi**:
```bash
pip install slowapi
```

**Update main.py**:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/v1/company/{symbol}")
@limiter.limit("10/minute")  # 10 requests per minute
def get_company(symbol: str, request: Request):
    # ...
```

**Estimated Time**: 2 hours

---

### 13. Split FMP Client into Domain Clients

**New Structure**:
```
app/clients/fmp/
├── __init__.py
├── base.py              # Base client with __get_by_url
├── company_client.py    # Company operations
├── financial_client.py  # Financial statements
├── market_client.py     # Market data & screening
└── news_client.py       # News operations
```

**Example** (`app/clients/fmp/company_client.py`):
```python
from app.clients.fmp.base import BaseFMPClient
from app.clients.fmp.models.company import FMPCompanyProfile

class CompanyClient(BaseFMPClient):
    def get_profile(self, symbol: str) -> Optional[FMPCompanyProfile]:
        profile = self._get_by_url(endpoint="profile", params={"symbol": symbol})
        if profile and isinstance(profile, list):
            return FMPCompanyProfile.model_validate(profile[0])
        return None
    
    def get_peers(self, symbol: str) -> list[FMPStockPeer]:
        # ...
```

**Estimated Time**: 6 hours

---

### 14. Add API Documentation

**Update main.py**:
```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="StockMate API",
        version="1.0.0",
        description="""
        StockMate provides comprehensive stock market data aggregation and analysis.
        
        ## Features
        
        * **Company Profiles**: Access detailed company information
        * **Financial Statements**: Historical income, balance sheets, cash flows
        * **Market Data**: Stock prices, ratings, analyst estimates
        * **News**: Company news, price targets, analyst upgrades/downgrades
        
        ## Authentication
        
        Internal endpoints require an API key via the `X-API-Key` header.
        """,
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

**Add Response Examples to Endpoints**:
```python
@router.get(
    "/{symbol}", 
    response_model=CompanyRead,
    summary="Get company profile",
    description="Retrieve detailed company profile by stock symbol",
    responses={
        200: {
            "description": "Company found",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "symbol": "AAPL",
                        "company_name": "Apple Inc.",
                        "price": 150.25,
                        # ...
                    }
                }
            }
        },
        404: {"description": "Company not found"}
    }
)
def get_company_profile(...):
    # ...
```

**Estimated Time**: 3 hours

---

### 15. Configure Database Connection Pooling

**Update** (`app/db/engine.py`):
```python
from app.core.config import config

pool_settings = {
    "pool_size": config.db_pool_size or 10,
    "max_overflow": config.db_max_overflow or 20,
    "pool_recycle": config.db_pool_recycle or 3600,
    "pool_pre_ping": True,
}

# Only add pool settings for MySQL (not SQLite)
if not config.db_url.startswith("sqlite"):
    engine = create_engine(
        config.db_url,
        connect_args=connect_args,
        **pool_settings
    )
else:
    engine = create_engine(
        config.db_url,
        connect_args=connect_args,
    )
```

**Add to config.py**:
```python
class Config(BaseSettings):
    # ...
    db_pool_size: int = 10
    db_max_overflow: int = 20
    db_pool_recycle: int = 3600
```

**Estimated Time**: 1 hour

---

## 🔵 Low Priority (Technical Debt)

### 16. Add Pre-commit Hooks

**Install**:
```bash
pip install pre-commit
```

**Create** `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
  
  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
  
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.9.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

**Setup**:
```bash
pre-commit install
```

**Estimated Time**: 1 hour

---

### 17. Add Circuit Breaker Pattern

**Install**:
```bash
pip install tenacity
```

**Update FMP Client**:
```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import requests

class FMPClient:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.Timeout, requests.ConnectionError))
    )
    def __get_by_url(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
        # existing implementation
```

**Estimated Time**: 2 hours

---

### 18. Add Monitoring

**Install Prometheus Client**:
```bash
pip install prometheus-client
```

**Add Metrics** (`app/util/metrics.py`):
```python
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

# Middleware
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    http_request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response

# Metrics endpoint
@app.get("/metrics")
def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
```

**Estimated Time**: 3 hours

---

## Summary

| Priority | Task | Time | Impact |
|----------|------|------|--------|
| 🔴 Critical | Fix Pydantic deprecations | 2h | High |
| 🔴 Critical | Fix FMP client bugs | 0.25h | Critical |
| 🔴 Critical | Add config validation | 0.5h | High |
| 🔴 Critical | Add README | 1h | High |
| 🔴 Critical | Add authentication | 0.5h | High |
| 🟡 High | Improve error handling | 3h | High |
| 🟡 High | Add DB constraints | 2h | Medium |
| 🟡 High | Increase test coverage | 8h | High |
| 🟡 High | Standardize table naming | 2h | Low |
| 🟡 High | Add validation enums | 2h | Medium |
| 🟢 Medium | Implement caching | 4h | High |
| 🟢 Medium | Add rate limiting | 2h | Medium |
| 🟢 Medium | Split FMP client | 6h | Medium |
| 🟢 Medium | Add API docs | 3h | Medium |
| 🟢 Medium | Configure pooling | 1h | Medium |
| 🔵 Low | Add pre-commit | 1h | Low |
| 🔵 Low | Circuit breaker | 2h | Low |
| 🔵 Low | Add monitoring | 3h | Medium |

**Total Estimated Time**: 43.25 hours (~1 sprint for 1 developer)

---

## Getting Started

**This Week** (🔴 Critical - 4.25 hours):
1. Fix Pydantic deprecations
2. Fix FMP client bugs
3. Add config validation
4. Write README
5. Add authentication

**This Sprint** (🟡 High - 19 hours):
1. Improve error handling and logging
2. Add database constraints
3. Write comprehensive tests
4. Standardize naming
5. Add validation enums

**Next Sprint** (🟢 Medium - 19 hours):
1. Caching layer
2. Rate limiting
3. Refactor FMP client
4. API documentation
5. Connection pooling

---

## Questions or Issues?

For clarifications on any recommendations, please open a GitHub issue or discussion.
