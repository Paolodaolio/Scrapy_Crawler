import psycopg2


def give_cursor():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="Puffirossi1",
                                      host="localhost",
                                      port="5432",
                                      database="postgres")
        cursor = connection.cursor()

    except (Exception, psycopg2.Error) as error:
        print("posgre_db: error handling connection...", error)
        connection.close()
    finally:
        return connection, cursor


def close_connection(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
