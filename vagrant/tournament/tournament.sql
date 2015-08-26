-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE DATABASE tournament;

\c tournament;

CREATE TABLE players(
	id			SERIAL PRIMARY KEY,
	username	VARCHAR(40) NOT NULL,
	CONSTRAINT unique_username UNIQUE(username)
);

CREATE TABLE matches(
	id 			SERIAL PRIMARY KEY,
	winner		INTEGER REFERENCES players(id),
	loser		INTEGER REFERENCES players(id)
);

-- Dear code reviewer: Is there a better way to structure these
-- counts and join statements? Is this standard/optimized well?
-- Thanks in advance!
CREATE VIEW standings AS
SELECT
    p.id,
    p.username,
    COUNT(CASE WHEN p.id = m.winner THEN 1 END) AS win_count,
    COUNT(CASE WHEN p.id = m.winner OR p.id = m.loser THEN 1 END) AS match_count
FROM
    players p
    LEFT JOIN matches m ON p.id=m.winner OR p.id=m.loser
GROUP BY
    p.id,
    p.username;
