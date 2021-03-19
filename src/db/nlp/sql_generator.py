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
        columns = {}
        cursor.execute("PRAGMA table_info('" + table + "')")
        result = cursor.fetchall()
        for i in range(len(result)):
            temp = result[i][1]
            columns[temp] = []
            cursor.execute("SELECT DISTINCT " + temp + " FROM " + table)
            result2 = cursor.fetchall()
            for i in range(len(result2)):
                columns[temp].append(result2[i][0])
        meta_data[table] = columns
    return meta_data


def check_tables(synonyms, sql_data):
    for synonym in synonyms:
        for table in sql_data["tables"]:
            if synonym == table.lower().strip():
                return table
    return None


def check_columns(synonyms, sql_data):
    for synonym in synonyms:
        for table in sql_data["tables"]:
            for column in sql_data[table].keys():
                if synonym == column.lower().strip():
                    return column, table
    return None, None


def check_values(synonyms, sql_data):
    for synonym in synonyms:
        for table in sql_data["tables"]:
            for column in sql_data[table].keys():
                for value in sql_data[table][column]:
                    if str(value).lower().strip() == synonym:
                        return value, column, table
    return None, None, None


def select(query_type, semantic_result, meta_data, conn):
    tables = []
    columns = {}
    temp_columns = []
    where = {}
    for i in range(len(semantic_result["keywords"])):
        if type(semantic_result['keywords'][i]) == str:
            continue
        table = check_tables(semantic_result["keywords"][i], meta_data)
        # print("check table", table)
        if table is not None:
            if table not in tables:
                tables.append(table)
            continue
        column, table = check_columns(semantic_result["keywords"][i], meta_data)
        # print("check column", column, table)
        if column is not None:
            columns[column] = table
            if table not in tables:
                tables.append(table)
            if column not in temp_columns:
                temp_columns.append(column)
            continue
        value, column, table = check_values(semantic_result["keywords"][i], meta_data)
        # print("check value", value, column, table)
        if value is not None:
            where[value] = []
            where[value].append(column)
            where[value].append(table)
            if table not in tables:
                tables.append(table)
            continue
        # return None

    if len(tables) == 0:
        return None
    
    cursor = conn.cursor()

    # read db from sql file
    sql_file = open("././database/db.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)

    statement = "SELECT "
    if query_type == "select-count":
        statement = statement + 'COUNT('
    if query_type == "select-avg":
        statement = statement + 'AVG('
    if query_type == "select-max":
        statement = statement + 'MAX('
    if query_type == "select-min":
        statement = statement + 'MIN('
    if len(columns.keys()) == 0:
        statement = statement + "*"
    else:
        for column in columns.keys():
            statement = statement + columns[column] + "." + column + ","
        statement = statement[:-1]
    if query_type in ["select-count", "select-avg", "select-min", "select-max"]:
        statement = statement + ")"

    statement = statement + " FROM "

    for table in tables:
        statement = statement + table + " NATURAL JOIN "
    statement = statement[:-13]

    if len(where.keys()) != 0:
        statement = statement + "WHERE "
        for value in where.keys():
            statement = statement + "LOWER(" + where[value][1] + "." + where[value][0] + ") LIKE '%" + value + "%' OR "
        statement = statement[:-4]

    print(statement)
    cursor.execute(statement)
    result = cursor.fetchall()
    tables = list(tables)
    if len(temp_columns) == 0:
        for table in list(tables):
            for column in meta_data[table].keys():
                if column not in temp_columns:
                    temp_columns.append(column)

    return list(tables), list(temp_columns), statement, result


def sql_generator_func(semantic_result):
    # get database metadata
    conn = sqlite3.connect(":memory:")
    meta_data = getDatabaseMetaData(conn)
    conn.close()

    # get data
    conn = sqlite3.connect(":memory:")

    execute = select(semantic_result["type"], semantic_result, meta_data, conn)
    if execute is None:
        return {"error": "no matching data found"}
    tables, columns, statement, result = execute
    is_aggregate = semantic_result["type"] in ["select-count", "select-avg", "select-min", "select-max"]

    return {
        "query": semantic_result["query"],
        "tables": tables,
        "columns": columns,
        "statement": statement,
        "data": result,
        "is_aggregate": is_aggregate
    }
