CREATE TABLE IF NOT EXISTS team (
    fifa_code   VARCHAR(3)  PRIMARY KEY,
    name        VARCHAR(50) NOT NULL UNIQUE,
    group_name  VARCHAR(10) NOT NULL
);