#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import contextlib
from collections import namedtuple

Standing = namedtuple("Standing", ['id', 'username', 'wins', 'matches'])
Pairing = namedtuple("Pairing", ['id1', 'username1', 'id2', 'username2'])


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


@contextlib.contextmanager
def with_cursor():
    """
    Yields a cursor connected to our database. The connection
    will commit after leaving the yield without errors. Both
    the cursor and the connection will always close regardless
    of errors.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        yield cur
    except:
        raise
    else:
        conn.commit()
    finally:
        cur.close()
        conn.close()


def deleteMatches():
    """Remove all the match records from the database."""
    with with_cursor() as cursor:
        cursor.execute("TRUNCATE matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    with with_cursor() as cursor:
        cursor.execute("TRUNCATE players CASCADE;")


def countPlayers():
    """Returns the number of players currently registered.

    @return: the number of players in the players table
    @rtype: long
    """
    with with_cursor() as cursor:
        cursor.execute("SELECT count(*) FROM players;")
        return cursor.fetchone()[0]


def registerPlayer(username):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.

    Args:
      username: the player's username (MUST be unique). May contain spaces.
    """
    with with_cursor() as cursor:
        cursor.execute("INSERT INTO players (username) VALUES (%s);", [username])


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with with_cursor() as cursor:
        # Dear person reveiwing code: I would like to know if
        # this select statement could be optimized. Is there
        # a better way to do the counts or the join here?
        cursor.execute("""SELECT
    p.id,
    p.username,
    count(CASE WHEN p.id = m.winner THEN 1 END) as win_count,
    count(CASE WHEN p.id = m.winner OR p.id = m.loser THEN 1 END) as match_count
FROM
    players p
    LEFT JOIN matches m on p.id=m.winner OR p.id=m.loser
GROUP BY
    p.id,
    p.username
ORDER BY
    win_count desc;
""")
        return map(lambda x: Standing(*x), cursor.fetchall())


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with with_cursor() as cursor:
        cursor.execute("INSERT INTO matches (winner, loser) " \
            "VALUES (%s, %s);", [winner, loser])


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()

    # If we have an odd number of players, remove one person
    # that has the most number of matches (so one person doens't
    # keep getting left out).
    if len(standings) % 2 == 1:
        most_matches = max((x.matches for x in standings))
        for standing in standings:
            if standing.matches == most_matches:
                break
        standings.remove(standing)

    # We should always have an even number of players now
    assert len(standings) % 2 == 0

    pairings = []
    while standings:
        player1 = standings.pop()
        player2 = standings.pop()
        pairings.append(Pairing(player1.id, player1.username,
                                player2.id, player2.username))
    return pairings
