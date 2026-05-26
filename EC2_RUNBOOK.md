# EC2 Runbook

## Purpose

This runbook describes how the FastAPI trading toolkit coudl run on an EC2 linux server.

## Basic EC2 Deployment flow

1. SSH into the EC2 server.
2. Pull the latest code from Github.
3. Create or activate a python virtual environment.
4. Install dependencies from "requirements.txt".
5. Set production environemt variables.
6. Start the FastAPI application using Uvicorn or Gunicorn.
7. Confirm the app is running using the health endpoint.
8. Inspect logs if the app fails.

## Example Commands

```bash
git pull origin main
python -m venv .venv
source .venv/bin/activate
pip install -r 'requirements.txt'
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

## RDS Connection Notes

In local development, the FastAPI application connects to PostgreSQL running in Docker.

In a production-style EC2 setup, the application would connect to PostgreSQL hosted on Amazon RDS.

The application should not hardcode database credentials. Instead, it should read database settings from environment variables:

- DB_HOST
- DB_PORT
- DB_NAME
- DB_USER
- DB_PASSWORD

This allows the same application code to run in different environments by changing configuration rather than changing source code.

Local example:

- DB_HOST=localhost

Production example:

- DB_HOST=my-database.xxxxxx.eu-west-2.rds.amazonaws.com
