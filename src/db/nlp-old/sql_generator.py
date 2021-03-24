import sqlite3

from google_trans_new import google_translator
from nltk.corpus import wordnet


# nltk.download('wordnet')


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


def getTable(sql_tables, english_table):
    for i in range(len(sql_tables)):
        if sql_tables[i].lower() == english_table.lower().strip():
            return sql_tables[i]

    # check for synonyms
    syn = list()
    for synset in wordnet.synsets(english_table.lower().strip()):
        for lemma in synset.lemmas():
            for synonym in lemma.name().split('_'):
                syn.append(synonym)
    for i in range(len(sql_tables)):
        for synonym in syn:
            if sql_tables[i].lower() == synonym.lower().strip():
                return sql_tables[i]

    return None


def getColumns(sql_columns, semantic_columns):
    translator = google_translator()
    columns = []
    for i in range(len(semantic_columns)):
        columns.append(translator.translate(semantic_columns[i], lang_src='hindi'))

    result = []

    for column in columns:
        for i in range(len(sql_columns)):
            if sql_columns[i].lower() == column.lower().strip():
                result.append(sql_columns[i])
                break
        else:
            # check for synonyms
            syn = list()
            for synset in wordnet.synsets(column.lower().strip()):
                for lemma in synset.lemmas():
                    for synonym in lemma.name().split('_'):
                        syn.append(synonym)
            for synonym in syn:
                for i in range(len(sql_columns)):
                    if sql_columns[i].lower() == synonym.lower().strip():
                        result.append(sql_columns[i])
                        break
    return result


def sql_generator_func(semantic_result):
    # get database metadata
    conn = sqlite3.connect(":memory:")
    meta_data = getDatabaseMetaData(conn)
    conn.close()

    if semantic_result["type"] != "select":
        return "to be implemented"

    # find matching table
    hindi_table = semantic_result["table"]
    translator = google_translator()
    english_table = translator.translate(hindi_table, lang_src='hindi')

    table = getTable(meta_data["tables"], english_table)

    if table == None:
        return "could not find any matching data"

    # find matching columns
    columns = getColumns(meta_data[table], semantic_result["columns"])

    if len(columns) != len(semantic_result["columns"]):
        return "could not find any matching data"

    # run sql query
    conn = sqlite3.connect(":memory:")
    data = select(table, columns, conn)

    return {
        "table": table,
        "column": columns,
        "data": data
    }
