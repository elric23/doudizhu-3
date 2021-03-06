--   mysql --user=user --password=pwd --database=ddz < schema.sql

CREATE DATABASE IF NOT EXISTS ddz DEFAULT CHARSET utf8 COLLATE utf8_general_ci;

CREATE TABLE IF NOT EXISTS account (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(16) NOT NULL UNIQUE,
    username VARCHAR(10) NOT NULL,
    password VARCHAR(32) NOT NULL,
    coin INT default 4000,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS session (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    u_id INT NOT NULL REFERENCES account(id),
    slug VARCHAR(100) NOT NULL UNIQUE,
    markdown MEDIUMTEXT NOT NULL,
    published DATETIME NOT NULL,
    updated TIMESTAMP NOT NULL,
    KEY (published)
);

