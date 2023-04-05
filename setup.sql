CREATE DATABASE 449_db;
USE 449_db;
CREATE TABLE user
(
    id INT NOT NULL
    AUTO_INCREMENT, username VARCHAR
    (255) NOT NULL, password_salt VARCHAR
    (255) NOT NULL, password_hash VARCHAR
    (255) NOT NULL, PRIMARY KEY
    (id), UNIQUE
    (username));
