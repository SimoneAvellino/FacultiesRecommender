# read from "faculties.json" and compose "objective_data.json"

import json
import math


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


def idf(documents: list[dict[str, any]]):
    idf = {}
    doc_count = len(documents)
    all_words = set([word for doc in documents for word in doc['description'].split()])
    for word in all_words:
        docs_with_word = 0
        for doc in documents:
            if word in doc['tf']:
                docs_with_word += 1
        idf[word] = 1 + math.log(doc_count / docs_with_word)
    return idf


with open('../data/faculties.json', 'r') as file:
    faculties = json.load(file)['faculties']
    # for faculty in faculties:
    #     print("Faculty:", faculty['name'])
    #     faculty['tf'] = tf(faculty['description'].split())
    #     print("TF:", faculty['tf'])
    # print(idf(faculties))
    # with open('../data/objective_data.json', 'w') as file:
    #     json.dump(faculties, file)