Swiss Tournament Pairings
=============

This repo holds a Vagrant VM running Python and PostgresQL to run a simple [Swiss Tournament Pairings](https://en.wikipedia.org/wiki/Swiss-system_tournament) program.


### Structure
After launching the VM (`vagrant up`), you can view the files in the following directory:

```
+ /
|--+ vagrant/
   |--+ tournament/
      |--+ tournament.py
      |--+ tournament_test.py
      |--+ tournament.sql
```

### Execution
To run the tests:

```
python /vagrant/tournament/tournament_test.py
```

which has this output:

```
vagrant@vagrant-ubuntu-trusty-32:~$ python /vagrant/tournament/tournament_test.py
0. Cursor connection works.
1. Old matches can be deleted.
2. Player records can be deleted.
3. After deleting, countPlayers() returns zero.
4. After registering a player, countPlayers() returns 1.
5. Players can be registered and deleted.
6. Newly registered players appear in the standings with no matches.
7. After a match, players have updated standings.
8. After one match, players with one win are paired.
9. Odd number of players works too!
Success!  All tests pass!
vagrant@vagrant-ubuntu-trusty-32:~$
```
