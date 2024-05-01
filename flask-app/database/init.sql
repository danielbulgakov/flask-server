-- Delete all tables before creating
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS auth CASCADE;
DROP TABLE IF EXISTS records CASCADE;

-- Table to save users meta info
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100),
    gender VARCHAR(10),
    age INTEGER,
    weight FLOAT,
    date_of_birth DATE
);

-- Table to save users auth data
CREATE TABLE IF NOT EXISTS auth (
    id SERIAL PRIMARY KEY,
    login VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES Users(id)
);

-- Table to save users ECG records
CREATE TABLE IF NOT EXISTS records (
    id SERIAL PRIMARY KEY,
    reading_date DATE NOT NULL,
    time_interval INTERVAL NOT NULL,
    readings_data JSONB
);
