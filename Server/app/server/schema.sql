DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

SET timezone TO 'Europe/Warsaw';

CREATE TABLE users(
	id SERIAL PRIMARY KEY ,
	email VARCHAR(200) NOT NULL UNIQUE,
	password VARCHAR(200) NOT NULL,
	admin BOOLEAN NOT NULL,
	name VARCHAR(200) NOT NULL UNIQUE
);

CREATE TABLE devices(
	id SERIAL PRIMARY KEY ,
	location_longitude DECIMAL(9,6),
	location_latitude DECIMAL(9,6),
	name VARCHAR(200) NOT NULL,
	token VARCHAR(200) NOT NULL UNIQUE,
	users_id INTEGER REFERENCES users(id)
);

CREATE TABLE measurements(
	id SERIAL PRIMARY KEY,
	temperature DECIMAL(9,6),
	pressure DECIMAL(9,6),
	humidity DECIMAL(9,6),
	devices_id INTEGER REFERENCES devices(id)
);
