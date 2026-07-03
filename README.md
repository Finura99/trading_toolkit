# Trading Toolkit

## Overview

Trading Toolkit is a simplified internal trading backend built with FastAPI, PostgreSQL and Python.

It models trade capture, portfolio summaries, position calculation and exposure reporting for a finance-style backend system. The project focuses on backend engineering fundamentals including API design, service-layer structure, database integration, testing, logging, readiness checks, Docker-based local development and cloud deployment practice.

## Business Use Case

In a trading environment, individual trades are recorded as events, while positions represent the net result of those trades.

This project models a simplified internal tool where completed BUY and SELL trades can be stored, queried and aggregated into portfolio and position views. The API could be used by an internal dashboard, reporting process, analyst tool or another backend service.

Example:

- A BUY trade increases the net position.
- A SELL trade decreases the net position.
- Exposure is calculated from net quantity and market price.

```text
BUY 10 AAPL
SELL 4 AAPL

Net position = 6 AAPL
Market price = 150
Exposure = 900
```

## Technology Used

- Python
- FastAPI
- Pydantic
- PostgreSQL
- psycopg2
- pytest
- Linux
- Docker
- Git / Github

## Core Features

- Create trades via REST API endpoints
- Retrieve trades with a limit parameter
- Retrieve trades by symbol
- Validate input using Pydantic schemas
- Model BUY and SELL trade events
- Calculate notional trade value
- Aggregate trades into portfolio summaries
- Calculate net positions and exposure by symbol
- Structure backend logic across API, service, domain and database layers

## Production-Oriented Features

- Health check endpoint for uptime monitoring
- Readiness endpoint for database availability checks
- Middleware request logging with request IDs
- Service-level logging and timing decorator
- PostgreSQL connection pooling
- Database connection context manager for safe resource cleanup
- .env configuration for local environment variables
- Unit, service, API and utility tests

## Architecture / Data Flow

```text
Client / API Consumer
        ↓
FastAPI Endpoint
        ↓
Pydantic Validation
        ↓
Domain / Service Layer
        ↓
PostgreSQL Database
        ↓
API Response
```

The API layer handles HTTP requests and response models. The service layer contains the business/database logic, while the database layer manages PostgreSQL connections through a connection pool and context manager.

## API Endpoints

|Method|Endpoint|Description|
|---|---|---|
|GET|`/health`|Basic service health check|
|GET|`/readiness`|Checks whether the API can reach the database|
|GET|`/trades?limit=5`|Returns recent trades|
|GET|`/trades/{symbol}`|Returns trades for a specific symbol|
|POST|`/trades`|Creates a new trade|
|GET|`/portfolio`|Returns portfolio summary data|
|GET|`/portfolio/{symbol}`|Returns portfolio data for a specific symbol|
|GET|`/positions`|Returns net positions and exposure by symbol|

## Finance Domain Model

This project models a simplified trading workflow:

- Trades are individual BUY or SELL events.
- Positions are derived from trades by aggregating quantities per symbol.
- BUY trades increase the net position.
- SELL trades decrease the net position.
- Exposure is calculated as:

```text
net_quantity * market_price

EX: BUY 10 AAPL
    SELL 4 AAPL

    Net position = 6 AAPL
    Market price = 150
    Exposure = 900
```

## Testing

The project includes tests across multiple layers:

- Domain tests for trade objects, validation and business calculations
- Service tests for portfolio and position logic
- API tests using FastAPI TestClient
- Readiness tests using mocking/patching
- Utility tests for decorators and logging behaviour
- Database context manager tests using mocked connection pools

Run the test suite:

```bash
python -m pytest -v
```

## Local Setup

Start the local PostgreSQL container:

```bash
docker start postgres-toolkit-local
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Initialise the local database:

```bash
scripts/init_local_db.sh
```

Run the API:

```bash
python -m uvicorn src.main:app --reload
```

## What I Learned

- Building backend APIs with FastAPI
- Using Pydantic for request and response validation
- Modelling trade and portfolio concepts using OOP
- Structuring code into API, service, domain and database layers
- Connecting a Python backend to PostgreSQL
- Using Docker for local database development
- Writing unit, service and API tests with PyTest
- Using mocking and patching to isolate external dependencies
- Managing database connections with connection pools and context managers
- Adding logging, request IDs and readiness checks for basic observability

## Future Improvements

- Add authentication and user-level access control
- Improve transaction handling and structured error responses
- Add richer market price simulation
- Add more integration tests using a real PostgreSQL container
- Add a simple frontend or dashboard for portfolio and position views
- Build a separate Java/Spring Boot trade execution simulator that can submit simulated filled trades  into this trading toolkit
