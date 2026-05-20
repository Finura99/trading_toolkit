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
