from google_trans_new import google_translator
from nltk.corpus import wordnet


# Workflow
def semantic_analyser(syntactic_result):
    # query classification
    select_list = ["क्या", "कौन", "कहाँ", "कब", "कितना"]
    matches = [x for x in select_list if x in syntactic_result["query_lemma"]]
    if len(matches) == 0:
        return {"error": "To Be Implemented"}

    if "औसत" in syntactic_result["query_lemma"] or "माध्य" in syntactic_result["query_lemma"]:
        query_type = "select-avg"
    elif "अधिकतम" in syntactic_result['query_lemma']:
        query_type = "select-max"
    elif "न्यूनतम" in syntactic_result['query_lemma']:
        query_type = "select-min"
    elif "कितना" in syntactic_result["query_lemma"]:
        query_type = "select-count"
    else:
        query_type = "select"

    # finding keywords and their synonyms
    keywords = []
    for i in range(len(syntactic_result["dependencies"])):
        if syntactic_result['dependencies'][i][2] in ["nmod", "nsubj", "conj", "obj", "obl", "root"]:  # and
            # syntactic_result[
            # 'pos']['pos'][i] != 'PROPN':
            keywords.append(syntactic_result['tokens'][i])

    for i in range(len(keywords)):
        translator = google_translator()
        hindi_temp = keywords[i]
        temp = translator.translate(hindi_temp, lang_src='hindi')
        keywords[i] = []
        keywords[i].append(hindi_temp)
        keywords[i].append(temp.lower().strip())
        for synset in wordnet.synsets(temp.lower().strip()):
            for lemma in synset.lemmas():
                for synonym in lemma.name().split('_'):
                    keywords[i].append(synonym.lower().strip())

    # for i in range(len(syntactic_result['pos'])):
    #     if syntactic_result['pos']['pos'][i] == 'PROPN':
    #         keywords.append(syntactic_result['pos']['word'][i])

    return {
        "query": syntactic_result["query"],
        "tokens": syntactic_result["tokens"],
        "query_lemma": syntactic_result["query_lemma"],
        "pos": syntactic_result["pos"],
        "dependencies": syntactic_result["dependencies"],
        "type": query_type,
        "keywords": keywords,
    }
