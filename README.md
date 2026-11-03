
# Module 9 - FastAPI and PostgreSQL

## Project Overview

This project demonstrates how to use PostgreSQL with a FastAPI calculator application in a Docker Compose environment.

The database is managed through pgAdmin using raw SQL commands.

## Technologies Used

- Python and FastAPI
- PostgreSQL 16
- pgAdmin 4
- Docker and Docker Compose
- SQL
- Git and GitHub

## Project Structure

- `main.py` - FastAPI application
- `app/` - Calculator application code
- `tests/` - Application tests
- `Dockerfile` - FastAPI container configuration
- `docker-compose.yml` - Docker services
- `requirements.txt` - Python dependencies
- `sql/` - SQL scripts for database operations

## Running the Application

1. Install Docker Desktop and enable WSL integration if using Ubuntu on Windows.
2. Create a `.env` file with the following variables:

   - `POSTGRES_PASSWORD`
   - `PGADMIN_EMAIL`
   - `PGADMIN_PASSWORD`

3. Start the containers:

   `docker compose up --build -d`

4. Verify the services:

   `docker compose ps`

## Application Access

- FastAPI: http://localhost:8000/docs
- pgAdmin: http://localhost:5050

## PostgreSQL Connection

In pgAdmin, register a PostgreSQL server using:

- Host: `db`
- Port: `5432`
- Database: `fastapi_db`
- Username: `postgres`
- Password: Value of `POSTGRES_PASSWORD`

## Database Tables

The database contains two tables:

1. `users` - Stores usernames, emails, and timestamps.
2. `calculations` - Stores calculator operations and links each calculation to a user.

The tables demonstrate a one-to-many relationship through a foreign key.

## SQL Operations

The SQL scripts are organized into four files:

1. `01_create_tables.sql` - Creates database tables.
2. `02_insert_records.sql` - Inserts sample records.
3. `03_query_data.sql` - Retrieves and joins records.
4. `04_update_delete.sql` - Updates and deletes records.

Run the scripts in numerical order on a new, empty database. The INSERT script creates the sample records used by the later scripts.

## Database Persistence

Docker uses a named volume to preserve PostgreSQL data when containers restart.

## Security

Database passwords are stored in a local `.env` file.

The `.env` file is excluded from Git using `.gitignore`.

## Assignment Documentation

Screenshots demonstrate successful SQL commands and Docker Compose services.

A separate report and reflection document the assignment results and learning experience.
