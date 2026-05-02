# Trading Toolkit

## Overview

A Python backend system with FastAPI that allows users to create and retrieve trade data through endpoints.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- psycopg2
- pytest
- Linux
- Docker

## Features

- Create trades via API
- Retrieve trades with limit parameter
- Input validation using Pydantic schemas
- Domain modelling with classes (OOP)
- Unit and API Testing

## How to Run

1. Start Docker (Postgres)
2. Activate virtual environment:
    python3 venv .venv
    source .venv/bin/activate
3. Run API:
    uvicorn src.main:app --reload

## Example Request

POST /trades
{
    "symbol" : "AAPL"
    "quantity" : 10,
    "price" : 100
}

## Architecture

The system is structured into three layers:

- API Layer (FastAPI): handles requests and validation
- Service Layer: contains business logic and database interaction
- Database Layer: stores market data

Data flows from the API through validation and restructured into doamin objects for better design and reusability, then into the sercie layer for processing and persistence into the DB.

## What I Learned

- Building a backend API using FastAPI
- Used Pydantic for validation
- Implemented OOP for domain modelling
- Added unit and API tests
- Managed dependencies using pip and requirements.txt