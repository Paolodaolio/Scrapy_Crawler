from classes.race import Race
from database.connection import get_cursor, close_connection

connection, cursor = get_cursor()
schema = "public"


def fetch_runner_by_name(name):
    id = None
    postgres_insert_query = "SELECT * FROM {}.Person WHERE account_name = '{}';".format(schema, name)
    cursor.execute(postgres_insert_query)
    count = cursor.rowcount
    print(str(count)+" account found with this name")
    for row in cursor:
        id = row[0]
    return id


def fetch_races_by_runner(id):
    races = []
    select_query = ("SELECT * " +
                    "FROM {}.Race ".format(schema) +
                    "INNER JOIN {}.Record_race_person ON {}.Race.race_id = public.Record_race_person.race_id ".format(schema, schema) +
                    "WHERE person_id = {};".format(id))
    cursor.execute(select_query)
    print("Found {} races for runner with id {}".format(cursor.rowcount, id))
    for row in cursor:
        races.append(Race(row[0], row[1], row[2], row[3], row[4], row[5]))
    return races

def finished():
    close_connection(connection, cursor)
