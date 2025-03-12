# Python Image
FROM python:3.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app/

# Install system-level dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    && apt-get clean

# Install pip / upgrade pip and other dependencies from requirements.txt
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . /app/

# Static files
RUN python manage.py collectstatic --noinput

# Make port 8700 available to the world outside this container
EXPOSE 8700

# Connect to PostgreSQL as the default user
CMD ["psql -U postgres"]

# Create Database
CMD ["CREATE DATABASE LuablaDB;"]

# Create new Postgresql user and grant all privileges to this new user for the taget database.
CMD ["CREATE USER defaultuser WITH PASSWORD defaultpassword;"]
CMD ["GRANT ALL PRIVILEGES ON DATABASE LuablaDB TO defaultuser ;"]
CMD ["\q"]
CMD ["psql -U defaultuser -d LuablaDB"]

# Migrate Django models to the database using the default created user.
CMD ["python", "manage.py", "makemigrations", "Authentication"]
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate", "Authentication"]
CMD ["python", "manage.py", "migrate"]
# Run Django Server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8700"]
