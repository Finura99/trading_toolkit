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
