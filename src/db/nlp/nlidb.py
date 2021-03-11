from .syntactic_analysis import syntactic_analyser
from .sql_generator import  sql_generator_func


def perform_nlidb(query):
    result_syntactic_analysis = syntactic_analyser(query)
    print(sql_generator_func())
    return result_syntactic_analysis
