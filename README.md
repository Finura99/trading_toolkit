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