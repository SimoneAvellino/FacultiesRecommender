# Scan the faculties.json file:
# - remove all stopwords and special characters
# - lowercase the text
# - lemmatize the words
# - keep only nouns
# - calculate the term frequency for each word in the description
# - calculate the inverse document frequency for each word in the description
# - save the result to a file

import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import math

lemmatizer = WordNetLemmatizer()

db = {
    'faculties': [],
    'idf': {}
}

def clean_text(text: str) -> str:
    # lowercase the text
    text = text.lower()
    # tokenize the text
    words = word_tokenize(text)
    # remove stopwords
    words = [word for word in words if word not in stopwords.words('english')]
    # remove special characters
    words = [word for word in words if word.isalnum()]
    # lemmatize the words
    words = [lemmatizer.lemmatize(word) for word in words]
    # keep only nouns
    words = [word for word in words if wordnet.synsets(word) and wordnet.synsets(word)[0].pos() == 'n']

    # join the words
    return ' '.join(words)

def tf(words: list[str]) -> dict[str, float]:
    tf = {}
    for word in words:
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1
    total_words = len(words)
    for word in tf:
        tf[word] /= total_words
    return tf


def idf(faculties: list[dict[str, any]]):
    idf = {}
    doc_count = len(faculties)
    all_words = set([word for doc in faculties for word in doc['description'].split()])
    for word in all_words:
        docs_with_word = 0
        for doc in faculties:
            if word in doc['tf']:
                docs_with_word += 1
        idf[word] = 1 + math.log(doc_count / docs_with_word)
    return idf

with open('../data/faculties.json', 'r') as file:
    faculties = json.load(file)['faculties']
    for faculty in faculties:
        f = {}
        f['code'] = faculty['code']
        f['name'] = faculty['name']
        f['description'] = clean_text(faculty['description']) + clean_text(faculty['goals']) + clean_text(faculty['jobs'])
        f['tf'] = tf(f['description'].split())
        print(f)
        db['faculties'].append(f.copy())

    db['idf'] = idf(db['faculties'])

# save the db to a file
with open('../data/objective_data.json', 'w') as file:
    json.dump(db, file)


