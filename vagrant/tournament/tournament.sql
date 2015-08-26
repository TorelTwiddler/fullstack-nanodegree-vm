-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create database tournament;

\c tournament;

create table players(
	id			SERIAL PRIMARY KEY,
	username	varchar(40) NOT NULL,
	CONSTRAINT unique_username UNIQUE(username)
);

create table matches(
	id 			SERIAL PRIMARY KEY,
	winner		integer REFERENCES players(id),
	loser		integer REFERENCES players(id)
);
