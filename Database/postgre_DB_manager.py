from classes import Person, Race, Club, Record_Race_Person, Record_Club_Person
import psycopg2
from Database.postgre_DB import give_cursor as get_cursor
from Database.postgre_DB import close_connection

connection, cursor = get_cursor()
schema = "public"                                                                                                       # schema that is used

                                        ##      PERSON BLOCK        ##


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


def insert_person(runner: Person):
    try:
        postgres_insert_query = """ INSERT INTO """+schema+""".Person (account_name) VALUES(%s);"""
        cursor.execute(postgres_insert_query, (runner.name,))
        count = cursor.rowcount
        # print(count, "record inserted successfully into table Person (", runner.name,")")
        print("INSERT in PERSON")
    except psycopg2.IntegrityError:
        # print("Data already present in the Person Table ("+runner.name+")")
        connection.rollback()
    except (Exception, psycopg2.Error) as error:
        if cursor:
            pass
            # print("Failed to insert record into table Person", error)
    else:
        connection.commit()



def fetch_runner_by_name(name):
    tmp = 0
    try:
        postgres_insert_query = """SELECT * FROM """+schema+""".Person WHERE account_name = %s""" # todo fix it
        record_to_insert = (str(name))
        cursor.execute(postgres_insert_query, (record_to_insert,))
        count = cursor.rowcount

        if cursor.rowcount:
            for row in cursor:
                tmp = row[0]
        # print(str(count) + " account found with this name, id #"+str(tmp))
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to fetch record from table Person,\nERROR: ", error)
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


def update_runner_id(runner: Person):            # with this function we update the id of the runner
    tmp = None                                   # in the case we need it
    tmp = fetch_runner_by_name(runner.name)
    runner.set_id(tmp[1])


                                        ##      RACE BLOCK        ##


def insert_race(race: Race):
    try:
        postgres_insert_query = """INSERT INTO """+schema+""".Race (elevation, lenght, partecipants_number, race_date, race_name) VALUES(%s,%s,%s,%s,%s); """
        record_to_insert = (race.elevation, race.lenght, race.partecipants, race.date, race.name)
        cursor.execute(postgres_insert_query, record_to_insert)
        count = cursor.rowcount
        # print(count, "record inserted successfully into table Race (", race.name,")")
        print("INSERT in RACE")
    except psycopg2.IntegrityError:
        print("Data already present in the Race Table (" + race.name + ")")
        connection.rollback()
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to insert record into table Race", error)
    else:
        connection.commit()


def get_race_id(race:Race):
    try:
        postgres_insert_query = """SELECT * FROM """+schema+""".Race WHERE race_name = %s AND race_date = %s """
        record_to_insert = (race.name, race.date)
        cursor.execute(postgres_insert_query, record_to_insert)
        count = cursor.rowcount
        for row in cursor:
            id = row[0]
        print(count, "record fetched successfully from table Race (", race.name,")")
    except (Exception, psycopg2.Error) as error:
        print("Failed to fetch record into table Race", error)
        connection.rollback()
    else:
        return id


                                ##      CLUB BLOCK        ##


def insert_club(club: Club):
    try:
        postgres_insert_query = """INSERT INTO """+schema+""".Club (club_name) 
        VALUES(%s); """
        member_list = club.insert_list()
        record_to_insert = club.name
        cursor.execute(postgres_insert_query, (record_to_insert,))
        count = cursor.rowcount
        print(count, "record inserted successfully into table club (", club.name,")")
        print("INSERT in CLUB")
    except psycopg2.IntegrityError:
        # print("Data already present in the Club Table ("+club.name+")")
        connection.rollback()
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to insert record into table club", error)
    else:
        connection.commit()


def fetch_club_by_name(name):
    tmp = 0
    try:
        postgres_insert_query = """SELECT * FROM """+schema+""".Club WHERE club_name = """+"'"+str(name)+"'"+""""""
        record_to_insert = ()
        cursor.execute(postgres_insert_query, (record_to_insert,))
        count = cursor.rowcount
        print(count+" account found with this name")
        if cursor.rowcount:
            for row in cursor:
                print("id=", row[0], "name=", row[1])
                tmp = row[0]
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to fetch record from table Person", error)
    return tmp


def get_club_id(club: Club):
    try:
        postgres_insert_query = """SELECT club_id FROM """ + schema + """.Club WHERE club_name = %s;"""
        record_to_insert = (club.name)
        cursor.execute(postgres_insert_query, (record_to_insert,))
        count = cursor.rowcount
        for row in cursor:
            id = row[0]
        print(count, "record fetched successfully from table Club (", club.name,")")
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to fetch record from table Club", error)
    except UnboundLocalError:
        id = fetch_club_by_name(club.name)
    else:
       return id


                                ##      RECORD BLOCK        ##


def insert_record_race_person(record: Record_Race_Person):
    try:
        postgres_insert_query = """INSERT INTO """+schema+""".Record_Race_Person(category, person_id, race_id, score, time_race) VALUES(%s,%s,%s,%s,%s); """
        record_to_insert = (record.category, record.person_id, record.race_id, record.score, record.time)
        cursor.execute(postgres_insert_query, record_to_insert)
        count = cursor.rowcount
        print(count, "record inserted successfully into table Record_race_person")
    except psycopg2.IntegrityError:
        print("Data already present in the Record_Race_Person Table ("+str(record.person_id)+" , "+str(record.race_id)+")")
        connection.rollback()
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to insert record into table Record_race_person", error)
    else:
        connection.commit()



def insert_record_club_person(record: Record_Club_Person):
    try:
        postgres_insert_query = """INSERT INTO """+schema+""".Record_Club_Person(club_id, person_id) VALUES(%s,%s); """
        record_to_insert = (record.club_id, record.person_id)
        cursor.execute(postgres_insert_query, record_to_insert)
        count = cursor.rowcount
        print(count, "record inserted successfully into table Record_club_person")
    except psycopg2.IntegrityError:
        print("Data already present in the Record_Club_Person Table ("+str(record.club_id)+" , "+str(record.person_id)+")")
        connection.rollback()
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to insert record into table Record_club_person", error)
    else:
        connection.commit()


def drop1():                         # if we need to reset the db
    try:
        postgres_insert_query = """DROP TABLE """+schema+""".club CASCADE """
        cursor.execute(postgres_insert_query)
        print("record DROPPED successfully into table Record_race_person")
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to drop record into table Record_race_person", error)
def drop2():                         # if we need to reset the db
    try:
        postgres_insert_query = """DROP TABLE """+schema+""".person CASCADE """
        cursor.execute(postgres_insert_query)
        print("record DROPPED successfully into table Record_race_person")
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to drop record into table Record_race_person", error)
def drop3():                         # if we need to reset the db
    try:
        postgres_insert_query = """DROP TABLE """+schema+""".race CASCADE """
        cursor.execute(postgres_insert_query)
        print("record DROPPED successfully into table Record_race_person")
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to drop record into table Record_race_person", error)
def drop4():                         # if we need to reset the db
    try:
        postgres_insert_query = """DROP TABLE """+schema+""".record_club_person CASCADE """
        cursor.execute(postgres_insert_query)
        print("record DROPPED successfully into table Record_race_person")
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to drop record into table Record_race_person", error)
def drop5():                         # if we need to reset the db
    try:
        postgres_insert_query = """DROP TABLE """+schema+""".Record_Race_Person CASCADE """
        cursor.execute(postgres_insert_query)
        print("record DROPPED successfully into table Record_race_person")
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to drop record into table Record_race_person", error)
def drop():                                                                                                             # sometime is better to start again instead of fix :)
    drop1()
    drop2()
    drop3()
    drop4()
    drop5()
    finished()


def how_much_did_we_stored():
    names = ['Person','Race','Club','Record_Club_Person','Record_Race_Person']
    values = [0,0,0,0,0]
    for name in names:
        values[names.index(name)] = select(name)
    print(values)


def select(name):
    try:
        postgres_insert_query = """ SELECT * FROM """ + schema + """."""+str(name)+""";"""
        cursor.execute(postgres_insert_query, )
        count = cursor.rowcount
        print(count, "record fetched from into table ", name)
    except (Exception, psycopg2.Error) as error:
        if cursor:
            print("Failed to fetch record from table "+str(name)+" : ", error)
    finally:
        return count

how_much_did_we_stored()

def finished():
    close_connection(connection, cursor)






