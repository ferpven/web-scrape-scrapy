CREATE DATABASE IF NOT EXISTS petlebi;

USE petlebi;

CREATE TABLE IF NOT EXISTS petlebi (
    UrL varchar(255),
    Name varchar(255),
    Category varchar(255),
    Barcode varchar(255),
    Price varchar(255),
    Images varchar(255),
    Sku varchar(255),
    Description mediumtext,
    Brand varchar(255)
);

SHOW FULL TABLES;
SHOW COLUMNS FROM petlebi;