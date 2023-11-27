import re
import pandas as pd
import numpy as np

# Calculate the q-gram similarity for strings q and r
def calcSim(q, r):
    all_q_grams_of_q = []
    all_q_grams_of_r = []
    length_q_gram = 3
    for i in range(len(q) - length_q_gram + 1):
        q_gram_of_q = q[i:i + length_q_gram]
        if q_gram_of_q not in all_q_grams_of_q:
            all_q_grams_of_q.append(q_gram_of_q)
    intersection = []
    union = all_q_grams_of_q
    for i in range(len(r) - length_q_gram + 1):
        q_gram_of_r = r[i:i + length_q_gram]
        if q_gram_of_r not in all_q_grams_of_r:
            all_q_grams_of_r.append(q_gram_of_r)
            # print("appended to:", all_q_grams_of_r)
            if q_gram_of_r in all_q_grams_of_q:
                intersection.append(q_gram_of_r)
            if q_gram_of_r not in union:
                union.append(q_gram_of_r)
    return len(intersection) / len(union)


# True if shop is same for products i and j
def sameShop(p_i, p_j):
    if p_i["shop"] == p_j["shop"]:
        return True
    else:
        return False


# True if brands of products i and j are different
def diffBrand(p_i, p_j):
    brands = ["philips", "samsung"]
    if any(word in p_i["title"] for word in brands) & any(word in p_j["title"] for word in brands):
        for brand in brands:
            if p_i["title"].__contains__(brand) and p_j["title"].__contains__(brand):
                return False
            if p_i["title"].__contains__(brand) and not p_j["title"].__contains__(brand) or not p_i["title"].__contains__(brand) and p_j["title"].__contains__(brand):
                return True
        return True
    return False # only different brands important

# Find the model words of an input string
def find_modelWords(string):
    string_splitted = string.split()
    model_words = []
    for w in range(0, len(string_splitted)):
        if re.search(r"(\d+)[^0-9]+|[^0-9]+(\d+)", string_splitted[w]):
            model_words.append(string_splitted[w])
    return model_words

# The key from key-value pair (KVP) q; value(q) returns the value from KVP q
# TODO: def key(p):

# All model words from the values of the attributes from product p
def exMW(p):
    model_words = []
    for v in p["featuresMap"].values():
        words_splitted = v.split()
        for w in range(0, len(words_splitted)):
            if re.search(r"(\d+)[^0-9]+|[^0-9]+(\d+)", words_splitted[w]):
                model_words.append(words_splitted[w])
    return model_words

# Percentage of matching model words from two sets of model words
def mw(C, D):
    intersection = C.intersection(D)
    union = C.union(D)
    return float(len(intersection))/float(len(union))

# The TMWM similarity between the products i and j using the parameters α and β
# TODO: def TMWMSim(p_i, p_j , alpha, beta):

# The minimum of the number of product features that product i and j contain
# TODO: def minFeatures(p_i, p_j):

# Returns the clusters
# TODO: def hClustering(dist, epsilon):
