# PostgreSQL Common Commands

## Connecting to PostgreSQL
```sh
# Connect to PostgreSQL as the default user
psql -U postgres

# Connect to a specific database
psql -U username -d database_name

# Exit psql
\q
```

## Database Management
```sh
# List all databases
\l

# Create a new database
CREATE DATABASE database_name;

# Drop a database
DROP DATABASE database_name;
```

## User and Role Management
```sh
# List all users
\du

# Create a new user
CREATE USER username WITH PASSWORD 'password';

# Grant privileges to a user
GRANT ALL PRIVILEGES ON DATABASE database_name TO username;

# Alter a user's password
ALTER USER username WITH PASSWORD 'new_password';
```

## Table and Data Management
```sh
# List all tables in the current database
\dt

# Create a new table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE
);

# Insert data into a table
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');

# Select data from a table
SELECT * FROM users;

# Delete a table
DROP TABLE users;
```

## Backup and Restore
```sh
# Backup a database
pg_dump -U username -d database_name -F c -f backup_file.dump

# Restore a database
pg_restore -U username -d database_name -F c backup_file.dump
```

## Performance and Monitoring
```sh
# Show running queries
SELECT * FROM pg_stat_activity;

# Check database size
SELECT pg_size_pretty(pg_database_size('database_name'));
```