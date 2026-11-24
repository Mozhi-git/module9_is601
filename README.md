
# Module 9 - FastAPI and PostgreSQL

## Project Overview

This project demonstrates how to use PostgreSQL with a FastAPI calculator application in a Docker Compose environment.


In Module 9, I used PostgreSQL and pgAdmin to work with raw SQL. In Modules 10 and 11, I expanded the project using SQLAlchemy models and Pydantic schemas.


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


---

## Module 11: Calculation Model and Testing

### Overview
In Module 11, I extended my FastAPI calculator application by adding a Calculation model using SQLAlchemy, Pydantic validation, and a Factory Pattern.

### New Features
- SQLAlchemy Calculation model with id, a, b, type, result, and user_id.
- Foreign key connecting calculations to users.
- Pydantic CalculationCreate and CalculationRead schemas.
- Validation for invalid operation types, division by zero, and invalid input.
- Factory Pattern supporting Add, Sub, Multiply, and Divide.
- PostgreSQL integration tests.

### Running Tests Locally

Activate the Python virtual environment:

```bash
source .venv/bin/activate
```

Start PostgreSQL:

```bash
docker compose start db
```


Before running integration tests, set `DATABASE_URL` to the PostgreSQL `module10_test_db` database. The local Docker connection uses port 5433.

Example DATABASE_URL configuration:

```bash
export DATABASE_URL='postgresql+psycopg://postgres:YOUR_PASSWORD@127.0.0.1:5433/module10_test_db'
```

Replace YOUR_PASSWORD with the local PostgreSQL password. If the password contains special URL characters, they must be URL-encoded. Never commit actual database credentials to GitHub.


Run unit tests:

```bash
python -m pytest tests/unit -q
```

Run integration tests:

```bash
python -m pytest tests/integration -q
```

Run all tests:

```bash
python -m pytest -q -ra
```

### Test Results
- 54 unit tests passed.
- 13 integration tests passed.
- 3 end-to-end tests passed.
- 70 total tests passed locally.
- 98% overall code coverage.

### GitHub Actions CI/CD
The GitHub Actions workflow is configured to:
1. Start a PostgreSQL test database.
2. Install Python dependencies.
3. Create database tables using SQLAlchemy.
4. Run unit, integration, and E2E tests.
5. Build a Docker image.
6. Scan the image using Trivy.
7. Push the image to Docker Hub after successful checks.

### Docker Hub
Repository:
https://hub.docker.com/r/mozhdeh83/module10-calculator

The Module 11 workflow is configured to publish the Docker image with the tag:

`module11-calculations`

Pull command after successful CI/CD deployment:

```bash
docker pull mozhdeh83/module10-calculator:module11-calculations
```


### Security Scan Exception

The GitHub Actions workflow uses Trivy to scan the Docker image for HIGH and CRITICAL vulnerabilities.

The workflow excludes `**/pip/_vendor/bom.cdx.json`, a pip dependency inventory file. This exception was introduced during Module 10 troubleshooting.

The exception should be reviewed against the original scan findings and reconsidered whenever dependencies or the Docker base image change. It should be removed if it is no longer justified.

---

## Module 12: User and Calculation Routes + Integration Testing

### Overview

In Module 12, I connected the existing User and Calculation models to FastAPI routes. The application now supports user registration and login, as well as complete BREAD operations for calculations.

### User Routes

The following user endpoints were implemented:

- `POST /users/register` - Register a new user.
- `POST /users/login` - Authenticate a user by verifying the stored Argon2 password hash.

User responses do not expose passwords or password hashes.

### Calculation BREAD Routes

The following calculation endpoints were implemented:

- `GET /calculations` - Browse all calculations.
- `GET /calculations/{calculation_id}` - Read one calculation.
- `POST /calculations` - Add a new calculation.
- `PUT /calculations/{calculation_id}` - Edit an existing calculation.
- `DELETE /calculations/{calculation_id}` - Delete a calculation.

The calculation routes use the existing SQLAlchemy Calculation model, Pydantic schemas, and CalculationFactory.

### Manual Testing with OpenAPI

Start the FastAPI application:

```bash
.venv/bin/python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Open Swagger/OpenAPI:

```text
http://127.0.0.1:8000/docs
```

The following operations were manually verified:

- User registration returned `201 Created`.
- Successful login returned `200 OK`.
- Incorrect login returned `401 Unauthorized`.
- Browse calculations returned `200 OK`.
- Read calculation returned `200 OK`.
- Add calculation returned `201 Created`.
- Edit calculation returned `200 OK`.
- Delete calculation returned `204 No Content`.

### Running Integration Tests

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Set `DATABASE_URL` to the PostgreSQL test database:

```bash
export DATABASE_URL='postgresql+psycopg://postgres:YOUR_PASSWORD@127.0.0.1:5433/module10_test_db'
```

Replace `YOUR_PASSWORD` with the local PostgreSQL password. Do not commit database credentials to GitHub.

Run the Module 12 route tests:

```bash
pytest tests/integration/test_module12_routes.py -q
```

Run all integration tests:

```bash
pytest tests/integration -q
```

Local integration test result:

```text
16 passed
```

The integration test run reached 92% application code coverage.

### GitHub Actions CI/CD

The Module 12 GitHub Actions workflow successfully:

1. Starts a PostgreSQL 16 test database.
2. Creates the PostgreSQL test tables.
3. Runs automated tests.
4. Builds the Docker image.
5. Scans the Docker image using Trivy.
6. Logs in to Docker Hub.
7. Pushes the Docker image to Docker Hub.

### Docker Hub

Repository:

```text
https://hub.docker.com/r/mozhdeh83/module10-calculator
```

Module 12 image tag:

```text
module12-routes
```

Pull the Module 12 image:

```bash
docker pull mozhdeh83/module10-calculator:module12-routes
```

### Results

- User registration and login routes completed.
- All five Calculation BREAD routes completed.
- Manual Swagger/OpenAPI testing completed.
- 16 integration tests passed locally.
- 92% application code coverage during the integration test run.
- GitHub Actions CI/CD completed successfully.
- Docker image built successfully.
- Trivy security scan passed.
- Module 12 Docker image published successfully to Docker Hub.
