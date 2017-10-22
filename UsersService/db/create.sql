CREATE DATABASE users_prod;
CREATE DATABASE users_dev;
CREATE DATABASE users_test;

USE users_prod;
CREATE TABLE IF NOT EXISTS users
(
id SERIAL,
name TEXT NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL,
CONSTRAINT users_pkey PRIMARY KEY (id)
);

USE users_dev;
CREATE TABLE IF NOT EXISTS users
(
id SERIAL,
name TEXT NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL,
CONSTRAINT users_pkey PRIMARY KEY (id)
);

USE users_test;
CREATE TABLE IF NOT EXISTS users
(
id SERIAL,
name TEXT NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL,
CONSTRAINT users_pkey PRIMARY KEY (id)
);