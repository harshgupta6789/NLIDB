from .semantic_analysis import semantic_analyser
from .sql_generator import sql_generator_func
from .syntactic_analysis import syntactic_analyser


def perform_nlidb(query):
    result_syntactic_analysis = syntactic_analyser(query)
    result_semantic_analysis = semantic_analyser(result_syntactic_analysis)
    result_sql_generator_analysis = sql_generator_func(result_semantic_analysis)
    return result_sql_generator_analysis
