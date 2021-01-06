from classes.race import Race
from classes.club import Club
from database.connection import get_cursor, close_connection
from re import sub

connection, cursor = get_cursor()
schema = "public"


def fetch_runner_by_name(name):
    id = None
    name = sub("'", "''", name)
    query = "SELECT * FROM {}.Person WHERE account_name = '{}';".format(schema, name)
    cursor.execute(query)
    count = cursor.rowcount
    print(str(count)+" account found with this name")
    for row in cursor:
        id = row[0]
    return id


def fetch_races_by_runner(id):
    races = []
    query = ("SELECT * " +
                    "FROM {}.Race ".format(schema) +
                    "INNER JOIN {}.Record_race_person ON {}.Race.race_id = public.Record_race_person.race_id ".format(schema, schema) +
                    "WHERE person_id = {};".format(id))
    cursor.execute(query)
    print("Found {} races for runner with id {}".format(cursor.rowcount, id))
    for row in cursor:
        races.append(Race(row[0], row[1], row[2], row[3], row[4], row[5]))
    return races

def fetch_club_by_runner(id):
    clubs = []
    query = ("SELECT public.Club.club_id, club_name " +
                    "FROM {}.Club ".format(schema) +
                    "INNER JOIN {}.Record_club_person ON {}.Club.club_id = public.Record_club_person.club_id ".format(schema, schema) +
                    "WHERE person_id = {};".format(id))
    cursor.execute(query)
    print("Found {} clubs for runner with id {}".format(cursor.rowcount, id))
    for row in cursor:
        clubs.append(Club(row[0], row[1]))
    return clubs

def random_name():
    query = "SELECT account_name FROM {}.Person ORDER BY RANDOM() LIMIT 1".format(schema)
    cursor.execute(query)
    for row in cursor:
        print("Selected random runner : {}".format(row[0]))
        return row[0]

def finished():
    close_connection(connection, cursor)
