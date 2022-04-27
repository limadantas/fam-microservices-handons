-- heroku pg:psql

CREATE TABLE accounts (
	user_id serial PRIMARY KEY,
	username VARCHAR ( 50 ) UNIQUE NOT NULL,
	password VARCHAR ( 50 ) NOT NULL,
	email VARCHAR ( 255 ) UNIQUE NOT NULL
);

CREATE TABLE posts (
	post_id serial PRIMARY KEY,
	id_user INTEGER,
	title VARCHAR ( 50 ) NOT NULL,
	body VARCHAR ( 500 ) NOT NULL
);