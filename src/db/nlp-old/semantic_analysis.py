
# Workflow

def semantic_analyser(syntactic_result):

    select_list = ["क्या", "कौन", "कितने", ""]
    matches = [x for x in select_list if x in syntactic_result["query_lemma"]]
    if len(matches):
        is_select = True
    else:
        is_select = False

    if not is_select:
        return "to be implemented"

    table = None
    columns = []

    for dependency in syntactic_result["dependencies"] :
        if dependency[2] == "nmod":
            table = dependency[0]
        elif dependency[2] == "nsubj" or dependency[2] == "conj":
            columns.append(dependency[0])

    return {
        "type": "select",
        "table": table,
        "columns": columns,
        "where": "to be implemented"
    }
