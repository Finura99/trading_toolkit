#!/usr/bin/env bash

set -e

if [ ! -f .env ]; then
  echo ".env file not found. Run this script from the project root."
  exit 1
fi

source .env

echo "Using database:"
echo "Host: $DB_HOST"
echo "Port: $DB_PORT"
echo "Name: $DB_NAME"
echo "User: $DB_USER"

if [ -z "${DB_PASSWORD:-}" ]; then
    echo "DB_PASSWORD is not set. Check your .env file."
    exit 1
fi

export PGPASSWORD="$DB_PASSWORD"

echo "Applying schema to $DB_NAME on $DB_HOST:$DB_PORT..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f db/schema.sql

echo "Applying seed data"
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f db/seed.sql

echo "Database setup complete"
