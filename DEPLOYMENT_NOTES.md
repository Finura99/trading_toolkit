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

## Basic Production Flow

1. Code is pushed to Github.
2. The FastAPI app is packaged into a docker image
3. The docker image is then stored in ECR
4. The app runs on EC2 or ECS
5. The app connects to Postgres hosted on RDS
6. A load balancer is added to route heavy traffic to the running app (ELB)

## EC2 Deployment Model

EC2 is a virtual linux server that can run the FastAPI application outside of my local machine.

A simple EC2 deployment could work as follows:

1. Provision an EC2 Linux Server (instance)
2. SSH into the instance
3. Clone the Github Repository
4. Set environment variables for production configuration
5. Install dependencies or run docker container
6. Start FastAPI app using Uvicorn/Gunicorn
7. Connect the app to PostgreSQL thats hosted on RDS

EC2 gives more direct control to the server/instance, but also requires more manual setup and maintenance compared with ECS. (Will approach it initally with the instance and see how ECS makes a difference)

## RDS Deployment Model

Amazon RDS can host PostgreSQL as a managed production database.

In local development, PostgreSQL runs inside Docker. In a production-style AWS setup, the application would connect to PostgreSQL hosted on RDS instead.

A basic RDS setup would work as follows:

1. Create an RDS PostgreSQL database.
2. Store the RDS host, port, database name, username, and password as environment variables.
3. Configure the FastAPI application to read those values from the environment.
4. The FastAPI app connects to RDS instead of local Docker PostgreSQL.
5. RDS handles database persistence, backups, storage, and managed database operations.

RDS is useful because production databases need reliable persistence and operational management, while Docker is better suited for local development or running stateless application containers.

## ECR Deployment Model

Amazon ECR is a container image registry used to store Docker images.

In a production-style setup, the FastAPI application could be packaged into a Docker image and pushed to ECR. EC2 or ECS could then pull that image and run the application.

A basic ECR flow would work as follows:

1. Write a Dockerfile for the FastAPI application.
2. Build the Docker image locally or through a CI/CD pipeline.
3. Push the image to Amazon ECR.
4. EC2 or ECS pulls the image from ECR.
5. The application runs from the same packaged image across environments.

ECR helps make deployments more reproducible because the application, dependencies, and startup command are packaged together inside the Docker image

## Load balancer

Today I completed the ALB route:
Laptop → ALB → EC2 FastAPI container → RDS PostgreSQL.

The target group became healthy after fixing security group rules.

Main lesson:
Load balancer port 80 is the public entry point.
EC2 port 8000 is the backend app port.
RDS port 5432 is the database port.
