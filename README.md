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