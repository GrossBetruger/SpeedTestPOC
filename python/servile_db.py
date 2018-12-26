import psycopg2
from os import environ

DB_PASS_ENV_VAR = "DB_PASS"

HOST = "caseyellow.cgqzew4kdsmr.eu-central-1.rds.amazonaws.com"

USER = "dango"

DB = "caseyellow"


def connect(db_name, user, host, password):
    conn = psycopg2.connect("""
                                dbname='{}' 
                                user='{}'
                                host='{}'
                                password='{}'
                            """.format(db_name, user, host, password))
    return conn.cursor()


def read_password():
    try:
        return environ[DB_PASS_ENV_VAR].strip()
    except KeyError:
        print("Missing Environment Variable: '{}', please supply it...".format(DB_PASS_ENV_VAR))
        quit()


if __name__ == "__main__":
    cur = connect(DB, USER, HOST, read_password())
    cur.execute("select 'dango  0' from user_details")
    for row in cur.fetchall():
        print(row)