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
	location_longitude DOUBLE,
	location_latitude DOUBLE,
	name VARCHAR(200) NOT NULL,
	users_id INTEGER REFERENCES users(id)
);

CREATE TABLE measurements(
	id SERIAL PRIMARY KEY,
	temperature DOUBLE,
	pressure DOUBLE,
	humidity DOUBLE,
	devices_id INTEGER REFERENCES devices(id)
);
