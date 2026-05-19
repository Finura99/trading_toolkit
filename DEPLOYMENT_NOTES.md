# Deployment Notes

## Local Setup

- FastAPI application runs locally using Uvicorn
- PostgreSQL runs locally in docker
- Environment variables are loaded from '.env'
- General configuration is loaded from 'config.yaml'

## Possible AWS Production Setup

- FastAPI application could be containerised with Docker
- Docker image could be stored in Amazon ECR
- Application could run on EC2 or ECS
- PostgreSQl could be hosted using Amazon RDS
- A load balancer could route traffic to the application
- Environment variables would store production secrets and configuration

## Why this matters

This seperates the application code from infrastructure concerns and helps the system move from local development towards a production-style deployment

## AWS service mapping

/ Local component / AWS Production Equivalent / Purpose /
/---/---/---/
/ FastAPI app on local machine / EC2 or ECS / Runs the backend application
/ Docker image / ECR / Stores the application container image
/ Local Docker for PostgreSQL / RDS PostgreSQL / Manage production database
/ '.env' file / Environment variables / stores, handles configurations and secrets
/ curl or Postman testing / health checks and monitoring / Confirms the service is alive or healthy
/ Load file/reports / S3 / Stores exported files, reports, or objects /

### Basic Production Flow

1. Code is pushed to Github.
2. The FastAPI app is packaged into a docker image.
3. The docekr image is then stored in ECR.
4. The app runs on EC2 or ECS.
5. The app connects to Postgres thats on RDS.
6. A load balancer is added to route heavy traffic to the running app.
