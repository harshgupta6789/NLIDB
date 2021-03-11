import numpy as np
import pandas as pd
import stanfordnlp

# Create A Text Pipeline
# stanfordnlp.download('hi')
nlp = stanfordnlp.Pipeline(lang="hi")


# extract lemma
def extract_lemma(doc):
    parsed_text = {'word': [], 'lemma': []}
    for sent in doc.sentences:
        for wrd in sent.words:
            # extract text and lemma
            parsed_text['word'].append(wrd.text)
            parsed_text['lemma'].append(wrd.lemma)
    # return a dataframe
    return pd.DataFrame(parsed_text), ' '.join(parsed_text['lemma'])


# dictionary that contains POS tags and their explanations
pos_dict = {
    'CC': 'coordinating conjunction', 'CD': 'cardinal digit', 'DT': 'determiner',
    'EX': 'existential there (like: \"there is\" ... think of it like \"there exists\")',
    'FW': 'foreign word', 'IN': 'preposition/subordinating conjunction', 'JJ': 'adjective \'big\'',
    'JJR': 'adjective, comparative \'bigger\'', 'JJS': 'adjective, superlative \'biggest\'',
    'LS': 'list marker 1)', 'MD': 'modal could, will', 'NN': 'noun, singular \'desk\'',
    'NNS': 'noun plural \'desks\'', 'NNP': 'proper noun, singular \'Harrison\'',
    'NNPS': 'proper noun, plural \'Americans\'', 'PDT': 'predeterminer \'all the kids\'',
    'POS': 'possessive ending parent\'s', 'PRP': 'personal pronoun I, he, she',
    'PRP$': 'possessive pronoun my, his, hers', 'RB': 'adverb very, silently,',
    'RBR': 'adverb, comparative better', 'RBS': 'adverb, superlative best',
    'RP': 'particle give up', 'TO': 'to go \'to\' the store.', 'UH': 'interjection errrrrrrrm',
    'VB': 'verb, base form take', 'VBD': 'verb, past tense took',
    'VBG': 'verb, gerund/present participle taking', 'VBN': 'verb, past participle taken',
    'VBP': 'verb, sing. present, non-3d take', 'VBZ': 'verb, 3rd person sing. present takes',
    'WDT': 'wh-determiner which', 'WP': 'wh-pronoun who, what', 'WP$': 'possessive wh-pronoun whose',
    'WRB': 'wh-abverb where, when', 'QF': 'quantifier, bahut, thoda, kam (Hindi)', 'VM': 'main verb',
    'PSP': 'postposition, common in indian langs', 'DEM': 'demonstrative, common in indian langs'
}


# extract parts of speech
def extract_pos(doc):
    parsed_text = {'word': [], 'pos': [], 'exp': []}
    for sent in doc.sentences:
        for wrd in sent.words:
            if wrd.pos in pos_dict.keys():
                pos_exp = pos_dict[wrd.pos]
            else:
                pos_exp = 'NA'
            parsed_text['word'].append(wrd.text)
            parsed_text['pos'].append(wrd.pos)
            parsed_text['exp'].append(pos_exp)
    # return a dataframe of pos and text
    return pd.DataFrame(parsed_text)


# Workflow

# Input Hindi Query
def syntactic_analyser(query):
    hindi_doc = nlp(query)

    # Tokenization
    tokens_object = hindi_doc.sentences[0].my_tokens()
    tokens = list()
    for token in tokens_object:
        tokens.append(token.words[0].text)

    # Lemmatization
    # call the function on doc
    df, query_lemma = extract_lemma(hindi_doc)

    hindi_doc_lemma = nlp(query_lemma)

    # POS Tagging
    pos = extract_pos(hindi_doc_lemma)

    # Print Dependencies
    dependencies = list()
    dep_edge = hindi_doc_lemma.sentences[0].my_dependencies()
    for dep in dep_edge:
        dependencies.append((dep[2].text, dep[0].index, dep[1]))

    # map to karaka relations
    return {
        "tokens": tokens,
        "query_lemma": query_lemma,
        "pos": pos,
        "dependencies": dependencies,
    }
