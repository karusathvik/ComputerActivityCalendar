CREATE DATABASE IF NOT EXISTS trackerdb;
USE trackerdb;

CREATE TABLE IF NOT EXISTS login (
    id int AUTO_INCREMENT PRIMARY KEY,
    username varchar(255) NOT NULL UNIQUE,
    password varchar(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS activities (
    id int AUTO_INCREMENT PRIMARY KEY,
    user_id int NOT NULL,
    recorded_at DATETIME NOT NULL,
    app varchar(255) NOT NULL,
    title varchar(255),
    FOREIGN KEY (user_id) REFERENCES login(id),
    INDEX (user_id, recorded_at)
);