import sqlite3


def getDatabaseMetaData(conn):
    cursor = conn.cursor()

    # read db from sql file
    sql_file = open("././database/db.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

    meta_data = dict()

    # get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    result = cursor.fetchall()
    tables = set()
    for i in range(len(result)):
        tables.add(result[i][0])

    # get column names
    for table in tables:
        columns = set()
        cursor.execute("PRAGMA table_info('" + table + "')")
        result = cursor.fetchall()
        for i in range(len(result)):
            columns.add(result[i][1])
        meta_data[table] = columns

    return meta_data


def sql_generator_func():
    conn = sqlite3.connect(":memory:")
    return getDatabaseMetaData(conn)
