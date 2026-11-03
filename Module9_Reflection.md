# Module 9 Reflection

In Module 9, I learned how to use PostgreSQL, pgAdmin, and Docker Compose with a FastAPI calculator application. I learned how a database stores information and how SQL commands can create, insert, retrieve, update, and delete records.

I created two tables called users and calculations. I used a foreign key to connect them and learned how one user can have multiple calculations. I also practiced using JOIN to retrieve information from both tables.

One challenge was setting up Docker in Ubuntu. At first, Docker was not working correctly, but I fixed the WSL integration. Another challenge was that my FastAPI container showed an unhealthy status. I discovered that the health check used curl, which was not installed. I changed the health check to use Python, and all three containers became healthy.

I also learned how to organize SQL scripts and document my results with screenshots.

Overall, this assignment helped me better understand databases, Docker Compose, and SQL. I now feel more comfortable working with PostgreSQL and managing database records.