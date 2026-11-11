
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

---

## Module 10: Secure Users and CI/CD

### Overview
In Module 10, I extended my FastAPI calculator project with secure user data models, password hashing, PostgreSQL integration tests, and an automated CI/CD pipeline.

### New Features
- SQLAlchemy User model with unique usernames and emails.
- Password hashing using Argon2.
- Pydantic schemas for input validation.
- PostgreSQL database connection using SQLAlchemy.
- Separate test database to protect existing Module 9 data.

### Testing
The following tests passed locally:
- 30 unit tests.
- 8 integration tests.
- 3 end-to-end tests.

Unit tests:
python -m pytest tests/unit/

Integration tests:
python -m pytest tests/integration/

End-to-end tests:
python -m pytest tests/e2e/

PostgreSQL integration tests require DATABASE_URL to point to an initialized module10_test_db database.

### GitHub Actions CI/CD
GitHub Actions automatically:
1. Installs Python dependencies.
2. Starts a PostgreSQL test database.
3. Runs automated tests.
4. Builds the Docker image.
5. Scans the image using Trivy.
6. Pushes the image to Docker Hub after successful checks.

### Security
- Passwords are hashed using Argon2.
- Database credentials are not stored in source code.
- Environment files are excluded from Git and Docker builds.
- Trivy scans for HIGH and CRITICAL vulnerabilities.
- A verified false-positive pip inventory file is excluded from scanning.

### Docker Hub
Repository:
https://hub.docker.com/r/mozhdeh83/module10-calculator

Pull the published Docker image:
docker pull mozhdeh83/module10-calculator:module10-secure-users

Run the published image:
docker run --rm -p 127.0.0.1:8001:8000 mozhdeh83/module10-calculator:module10-secure-users

Open:
http://127.0.0.1:8001/docs

### Results
- All 41 local tests passed across the test suites.
- Docker image built and ran successfully.
- Trivy security scan passed under the configured policy.
- GitHub Actions completed successfully.
- Docker Hub image was published, pulled, and tested successfully.

