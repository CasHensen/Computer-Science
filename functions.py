import re
import random
# import pandas as pd
import numpy as np
from random import randint
from math import ceil, sqrt
from itertools import permutations


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
    title_pi = dataCleaningOfSingleString(p_i["title"])
    title_pj = dataCleaningOfSingleString(p_j["title"])
    print(title_pi)
    print(title_pj)
    brands = ["akai", "alba", "apple", "arcam", "arise", "bang", "bpl", "bush", "cge", "changhong", "compal", "curtis", "durabrand", "element", "finlux", "fujitsu", "funai", "google", "haier", "hisense", "hitachi", "itel", "jensen", "jvc", "kogan", "konka", "lg", "loewe", "magnavox", "marantz", "memorex", "micromax", "metz", "onida", "panasonic", "pensonic", "philips", "planar", "proscan", "rediffusion", "saba", "salora", "samsung", "sansui", "sanyo", "seiki", "sharp", "skyworth", "sony", "tatung", "tcl", "telefunken", "thomson", "tpv", "tp vision", "vestel", "videocon", "vizio", "vu", "walton", "westinghouse", "xiaomi", "zenith"]
    if any(word in title_pi for word in brands) & any(word in title_pj for word in brands):
        for brand in brands:
            if title_pi.__contains__(brand) and title_pj.__contains__(brand):
                return False
            if title_pi.__contains__(brand) and not title_pj.__contains__(brand) or not title_pi.__contains__(brand) and title_pj.__contains__(brand):
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


def minHashing(binary_data, number_of_hashes, number_of_mw):
    primes = [i for i in range(5, 100) if checkIfPrime(i)]              # which bounds?????????????????????
    parameters_of_hash_functions = []
    for i in range(0, number_of_hashes):
        a = randint(0, 20)                                      # which bounds?????????????????????
        b = randint(0, 20)                                      # which bounds?????????????????????
        p = random.choice(primes)
        parameters = [a, b, p]
        parameters_of_hash_functions.append(parameters)
    return apply_hashes(binary_data, parameters_of_hash_functions, number_of_mw)


def checkIfPrime(value):
    if value >= 2:
        for n in range(2, value):
            if (value % n) == 0:
                return False
        return True
    else:
        return False


def apply_hashes(binary_data, param_hash_functions, number_of_mw):  # param_hash_functions = [[a0, b0, p0], [a1, b1, p1], ...]
    number_of_hash_functions = len(param_hash_functions)
    number_of_items = len(binary_data)
    hash_results = np.ones((number_of_hash_functions, number_of_items)) * np.inf  # initialize with infinity

    for col in range(0, number_of_mw):
        for hash_func in range(0, number_of_hash_functions):
            a = param_hash_functions[hash_func][0]
            b = param_hash_functions[hash_func][1]
            p = param_hash_functions[hash_func][2]
            hash_value = (a + b * (col+1)) % p

            for i in range(0, number_of_items):
                if binary_data[i].__contains__(col):
                    if hash_value < hash_results[hash_func][i]:
                        hash_results[hash_func][i] = hash_value

    return hash_results


def LSH(signature_matrix, b, r, length):
    number_of_items = len(signature_matrix[0])
    index = 0
    buckets = np.zeros((b, number_of_items))

    for band in range(b):
        total_col_sum = 0
        for row in range(r):
            index = band * r + row
            total_col_sum += signature_matrix[index]
        buckets[band] = hashBucket(np.array(total_col_sum), sqrt(length))

    matches = []
    for col1 in range(number_of_items):
        matches_per_col = []  # at least one band same value
        for col2 in range(number_of_items):
            for buck_row in range(b):
                if buckets[buck_row, col1] == buckets[buck_row, col2] and col1 != col2 and not matches_per_col.__contains__(col2):
                    matches_per_col.append(col2)
        matches.append(matches_per_col)

    return matches


def hashBucket(array, length):
    results = []
    range_of_a_bucket = length
    for c in range(len(array)):
        for k in range(1, 10):
            if k == 9:
                results.append(k)
                break
            elif array[c] < range_of_a_bucket * k:
                results.append(k)
                break

    return results


# The TMWM similarity between the products i and j using the parameters alpha and bete
# TODO: def TMWMSim(p_i, p_j , alpha, beta):

# The minimum of the number of product features that product i and j contain
# TODO: def minFeatures(p_i, p_j):

# Returns the clusters
# TODO: def hClustering(dist, epsilon):