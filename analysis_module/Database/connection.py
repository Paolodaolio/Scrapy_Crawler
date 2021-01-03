import psycopg2


def get_cursor():
    try:
        connection = psycopg2.connect(user="postgres",
                                     password="postgres",
                                     host="localhost",
                                     port="5432",
                                     database="runners")
        cursor = connection.cursor()
    except (Exception, psycopg2.Error):
        print("posgre_db: error handling connection...")
        connection, cursor = None, None
    return connection, cursor


def close_connection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
