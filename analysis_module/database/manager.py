from classes.race import Race
from classes.club import Club
from database.connection import get_cursor, close_connection
from re import sub

connection, cursor = get_cursor()
schema = "public"


def fetch_runner_by_name(name):
    id = None
    name = sub("'", "''", name)
    query = "SELECT * FROM public.Person WHERE account_name = '{}';".format(name)
    cursor.execute(query)
    count = cursor.rowcount
    for row in cursor:
        id = row[0]
    return id


def fetch_races_by_runner(id):
    races = []
    query = ("SELECT public.race.race_id, race_name, lenght, race_date, elevation, partecipants_number " +
             "FROM public.Race " +
             "INNER JOIN public.Record_race_person ON public.Race.race_id = public.Record_race_person.race_id " +
             "WHERE person_id = {};".format(id))
    cursor.execute(query)
    for row in cursor:
        races.append(Race(row[0], row[1], row[2], row[3], row[4], row[5]))
    return races

def fetch_club_by_runner(id):
    clubs = []
    query = ("SELECT public.Club.club_id, club_name " +
                    "FROM public.Club " +
                    "INNER JOIN public.Record_club_person ON public.Club.club_id = public.Record_club_person.club_id " +
                    "WHERE person_id = {};".format(id))
    cursor.execute(query)
    for row in cursor:
        clubs.append(Club(row[0], row[1]))
    return clubs

def random_name():
    query = "SELECT account_name FROM public.Person ORDER BY RANDOM() LIMIT 1"
    cursor.execute(query)
    for row in cursor:
        return row[0]

def random_linked_names():
    names = []
    query = ("SELECT account_name " + 
             "FROM (public.person INNER JOIN public.record_club_person ON public.person.person_id = public.record_club_person.person_id) " +
             "WHERE club_id IN (SELECT club_id FROM public.record_club_person GROUP BY club_id HAVING COUNT(*) > 2 ORDER BY RANDOM() LIMIT 1) " +
             "ORDER BY RANDOM() LIMIT 2;")
    cursor.execute(query)
    for row in cursor:
        names.append(row[0])
    return names

def potentially_linked_to_runner(id):
    names = []
    query = ("SELECT DISTINCT account_name " +
             "FROM (public.person " +
             "INNER JOIN public.record_race_person " +
             "ON public.person.person_id = public.record_race_person.person_id) " +
             "WHERE race_id IN (SELECT race_id FROM public.record_race_person WHERE person_id = {});".format(id))
    cursor.execute(query)
    for row in cursor:
        names.append(row[0])
    return names


def finished():
    close_connection(connection, cursor)
