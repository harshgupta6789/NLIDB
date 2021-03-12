import sqlite3
from google_trans_new import google_translator


def getDatabaseMetaData(conn):
    cursor = conn.cursor()

    # read db from sql file
    sql_file = open("././database/db.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

    meta_data = {}

    # get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    result = cursor.fetchall()
    tables = []
    for i in range(len(result)):
        tables.append(result[i][0])
    meta_data["tables"] = tables

    # get column names
    for table in tables:
        columns = []
        cursor.execute("PRAGMA table_info('" + table + "')")
        result = cursor.fetchall()
        for i in range(len(result)):
            columns.append(result[i][1])
        meta_data[table] = columns

    return meta_data


def select(table, columns, conn):
    cursor = conn.cursor()

    # read db from sql file
    sql_file = open("././database/db.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

    statement = "SELECT "
    for column in columns:
        statement = statement + column + ","
    statement = statement[:-1] + " FROM "
    statement = statement + table
    print(statement)

    cursor.execute(statement)
    result = cursor.fetchall()
    return result

def sql_generator_func(semantic_result):
    print(semantic_result)
    conn = sqlite3.connect(":memory:")
    meta_data = getDatabaseMetaData(conn)
    conn.close()

    if semantic_result["type"] != "select":
        return "to be implemented"

    hindi_table = semantic_result["table"]

    translator = google_translator()
    english_table = translator.translate('छात्र', lang_src='hindi')

    table = None

    for i in range(len(meta_data["tables"])):
        if meta_data["tables"][i].lower() == english_table.lower().strip():
            table = meta_data["tables"][i]
            break
    else:
        pass

    if table == None:
        return "could not find any matching data"

    columns = []
    for i in range(len(semantic_result["columns"])):
        semantic_result["columns"][i] = translator.translate(semantic_result["columns"][i], lang_src='hindi')

    for column in semantic_result["columns"]:
        for i in range(len(meta_data[table])):
            if meta_data[table][i].lower() == column.lower().strip():
                columns.append(meta_data[table][i])
                break
        else:
            pass
    print(columns)
    print(semantic_result["columns"])
    if len(columns) == 0:
        return "could not find any matching data"

    conn = sqlite3.connect(":memory:")
    data = select(table, columns, conn)
    return data
