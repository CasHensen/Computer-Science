import re
# import pandas as pd
# import numpy as np


# Data cleaning of a string
def dataCleaningOfSingleString(string):
    string = string.lower()
    string = string.replace("inches", "inch")
    string = string.replace("hertz", "hz")
    string = re.sub(r"(\d+)( *)\"", r'\g<1>inch', string)
    string = re.sub('[(]?[)]?', "", string)
    string = re.sub(r':\s', ' ', string)
    string = re.sub(r'-inch', 'inch', string)
    string = re.sub(r' - ', ' ', string)
    string = re.sub(r'(?!<\d)[.](?!\d)', '', string)
    string = re.sub(' +', ' ', string)
    return string


# Calculate the q-gram similarity for strings q and r
def calcSim(q, r):
    all_q_grams_of_q = []
    all_q_grams_of_r = []
    length_q_gram = 3
    for i in range(len(q) - length_q_gram + 1):
        q_gram_of_q = q[i:i + length_q_gram]
        if q_gram_of_q not in all_q_grams_of_q:
            all_q_grams_of_q.append(q_gram_of_q)
    print(all_q_grams_of_q)
    intersection = []
    union = all_q_grams_of_q.copy()
    for i in range(len(r) - length_q_gram + 1):
        q_gram_of_r = r[i:i + length_q_gram]
        if q_gram_of_r not in all_q_grams_of_r:
            all_q_grams_of_r.append(q_gram_of_r)
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
    brands = ["akai", "alba", "apple", "arcam", "arise", "bang", "bpl", "bush", "cge", "changhong", "compal", "curtis", "durabrand", "element", "finlux", "fujitsu", "funai", "google", "haier", "hisense", "hitachi", "itel", "jensen", "jvc", "kogan", "konka", "lg", "loewe", "magnavox", "marantz", "memorex", "micromax", "metz", "onida", "panasonic", "pensonic", "philips", "planar", "proscan", "rediffusion", "saba", "salora", "samsung", "sansui", "sanyo", "seiki", "sharp", "skyworth", "sony", "tatung", "tcl", "telefunken", "thomson", "tpv", "tp vision", "vestel", "videocon", "vizio", "vu", "walton", "westinghouse", "xiaomi", "zenith"]
    if any(word in p_i["title"] for word in brands) & any(word in p_j["title"] for word in brands):
        for brand in brands:
            if p_i["title"].__contains__(brand) and p_j["title"].__contains__(brand):
                return False
            if p_i["title"].__contains__(brand) and not p_j["title"].__contains__(brand) or not p_i["title"].__contains__(brand) and p_j["title"].__contains__(brand):
                return True
        return True
    return False  # only different brands important


# Find the model words of a product (both in title and values)
def find_modelWordsOfaProduct(product):
    model_words = []
    for k in product.keys():
        if k == "featuresMap":
            for v in product[k].values():
                model_words_KVP = model_words + find_modelWordsOfaKVP(v)
                for word in model_words_KVP:
                    if word not in model_words:
                        model_words.append(word)
        if k != "url" and k != "featuresMap":
            model_words_string = model_words + find_modelWordsOfaString(product[k])
            for word in model_words_string:
                if word not in model_words:
                    model_words.append(word)
    return model_words


# Find the model words of an input string (helper method)
def find_modelWordsOfaString(string):
    string = dataCleaningOfSingleString(string)
    string_splitted = string.split()
    model_words = []
    for w in range(0, len(string_splitted)):
        if re.search(r"(\d+)[^0-9]+|[^0-9]+(\d+)", string_splitted[w]):
            model_words.append(string_splitted[w])
    return model_words


# Find the model words of a KVP (helper method)
def find_modelWordsOfaKVP(string):
    string = dataCleaningOfSingleString(string)
    string_splitted = string.split()
    model_words = []
    for w in range(0, len(string_splitted)):
        if re.search(r"(\d+)[^0-9]+|[^0-9]+(\d+)", string_splitted[w]):
            model_words.append(string_splitted[w])
    return model_words


# Percentage of matching model words from two sets of model words
def mw(C, D):
    intersection = C.intersection(D)
    union = C.union(D)
    return float(len(intersection))/float(len(union))

# The TMWM similarity between the products i and j using the parameters alpha and bete
# TODO: def TMWMSim(p_i, p_j , alpha, beta):

# The minimum of the number of product features that product i and j contain
# TODO: def minFeatures(p_i, p_j):

# Returns the clusters
# TODO: def hClustering(dist, epsilon):
