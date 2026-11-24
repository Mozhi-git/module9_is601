# Module 12 Reflection

In Module 12, I connected the User and Calculation models to FastAPI routes. I created routes for user registration and login, and I also created the calculation BREAD routes for Browse, Read, Edit, Add, and Delete.

I tested the user routes in Swagger. I confirmed that a new user could register, a user could log in with the correct password, and an incorrect password returned an error. Passwords are stored securely using hashing.

I also tested all of the calculation routes in Swagger. I was able to create, view, update, and delete calculations successfully.

One challenge was that my existing PostgreSQL database tables did not completely match the newer SQLAlchemy models. I backed up the database and updated the table structure so it matched the application. Another challenge was setting the correct `DATABASE_URL` for integration testing.

After fixing these issues, all 16 integration tests passed and the integration test run reached 92% code coverage. I also updated GitHub Actions for the `module12-routes` branch. The CI/CD workflow successfully ran the tests, built the Docker image, scanned it with Trivy, and pushed the image to Docker Hub.

This module helped me better understand how FastAPI routes, Pydantic schemas, SQLAlchemy, PostgreSQL, testing, Docker, and GitHub Actions work together in one application.
