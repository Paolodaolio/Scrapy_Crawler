from classes import Runner, Race, Club
import psycopg2
from postgre_DB import give_cursor as get_cursor
from postgre_DB import close_connection

connection, cursor = get_cursor()
schema = "public"

                                        ##      RUNNER/PERSON BLOCK        ##


def fetch_all_runner():
    try:
        postgres_insert_query = """ SELECT * FROM """+schema+""".Person;"""
        cursor.execute(postgres_insert_query,)
        count = cursor.rowcount
        print(count, "record fetched successfully into table Person ")
        for row in cursor:
            print(row[0], row[1])
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to fetch record into table Person", error)


def insert_person(runner: Runner):
    try:
        postgres_insert_query = """ INSERT INTO """+schema+""".Person (account_name) VALUES(%s);"""
        cursor.execute(postgres_insert_query, (runner.name,))
        count = cursor.rowcount
        print(count, "record inserted successfully into table Person (", runner.name, ")")
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to insert record into table Person", error)


def fetch_runner_by_name(name):
    tmp = (0,0)
    try:
        postgres_insert_query = """SELECT * FROM """+schema+""".Person WHERE account_name = """+"'"+str(name)+"'"+""""""
        record_to_insert = ()
        cursor.execute(postgres_insert_query, (record_to_insert,))
        count = cursor.rowcount
        print(count+" account found with this name")
        if cursor.rowcount:
            for row in cursor:
                print("id=", row[0], "name=", row[1])
            tmp = (row[0], row[1])
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to fetch record from table Person", error)
    return tmp


def fetch_runner_by_id(id):
    try:
        postgres_insert_query = """ SELECT * FROM """+schema+""".Person WHERE  person_id = """+str(id)+""" """
        record_to_insert = ()
        cursor.execute(postgres_insert_query, (record_to_insert,))
        if cursor:
            for row in cursor:
                print(row[0], row[1])
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to fetch record from table Person", error)


def update_runner_id(runner: Runner):            # with this function we update the id of the runner
    tmp = None                                   # in the case we need it
    tmp = fetch_runner_by_name(runner.name)
    runner.set_id(tmp[1])


def insert_race(race: Race):
    try:
        postgres_insert_query = """INSERT INTO """+schema+""".Race (elevation, lenght, partecipants, race_date, race_name) 
        VALUES(%d,%d,%d,%date,%s); """  # TODO fix %date
        record_to_insert = (race.elevation, race.lenght, race.partecipants, race.date, race.name)
        cursor.execute(postgres_insert_query, (record_to_insert,))
        count = cursor.rowcount
        print(count, "record inserted successfully into table Race (", race.name, ")")
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to insert record into table Race", error)


def insert_club(club: Club):
    try:
        postgres_insert_query = """INSERT INTO """+schema+""".Club (club_name, members) 
        VALUES(%s); """
        member_list = club.insert_list()
        record_to_insert = (club.name, member_list)          # TODO try if this works
        cursor.execute(postgres_insert_query, (record_to_insert,))
        count = cursor.rowcount
        print(count, "record inserted successfully into table Race (", club.name, ")")
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to insert record into table club", error)


def finished():
    close_connection(connection, cursor)













