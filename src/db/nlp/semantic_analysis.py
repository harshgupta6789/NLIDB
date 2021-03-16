from google_trans_new import google_translator
from nltk.corpus import wordnet


# Workflow
def semantic_analyser(syntactic_result):
    # query classification
    select_list = ["क्या", "कौन", "कहाँ", "कब", "कितना"]
    matches = [x for x in select_list if x in syntactic_result["query_lemma"]]
    if len(matches) == 0:
        return {"error": "to be implemented"}

    if "औसत" in syntactic_result["query_lemma"] or "माध्य" in syntactic_result["query_lemma"]:
        query_type = "select-avg"
    elif "कितना" in syntactic_result["query_lemma"]:
        query_type = "select-count"
    else:
        query_type = "select"

    # finding keywords and their synonyms
    keywords = []
    for dependency in syntactic_result["dependencies"]:
        if dependency[2] in ["nmod", "nsubj", "conj", "obj"]:
            keywords.append(dependency[0])

    for i in range(len(keywords)):
        translator = google_translator()
        temp = translator.translate(keywords[i], lang_src='hindi')
        keywords[i] = [temp.lower().strip()]
        for synset in wordnet.synsets(temp.lower().strip()):
            for lemma in synset.lemmas():
                for synonym in lemma.name().split('_'):
                    keywords[i].append(synonym.lower().strip())

    return {
        "query": syntactic_result["query"],
        "tokens": syntactic_result["tokens"],
        "query_lemma": syntactic_result["query_lemma"],
        "pos": syntactic_result["pos"],
        "dependencies": syntactic_result["dependencies"],
        "type": query_type,
        "keywords": keywords,
    }
