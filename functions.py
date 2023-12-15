import re
import random
import numpy as np
from random import randint
from tqdm import tqdm
from sklearn.cluster import AgglomerativeClustering


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
    q = dataCleaningOfSingleString(q)
    r = dataCleaningOfSingleString(r)

    length_q_gram = min(3, len(q), len(r))
    all_q_grams_of_q = []
    all_q_grams_of_r = []

    for i in range(len(q) - length_q_gram + 1):
        q_gram_of_q = q[i:i + length_q_gram]
        all_q_grams_of_q.append(q_gram_of_q)
    union = all_q_grams_of_q.copy()
    for i in range(len(r) - length_q_gram + 1):
        q_gram_of_r = r[i:i + length_q_gram]
        all_q_grams_of_r.append(q_gram_of_r)
        union.append(q_gram_of_r)
    intersection = np.intersect1d(all_q_grams_of_q, all_q_grams_of_r, assume_unique=False, return_indices=False)
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
    brands = ["akai", "alba", "apple", "arcam", "arise", "bang", "bpl", "bush", "cge", "changhong", "compal", "curtis", "durabrand", "element", "finlux", "fujitsu", "funai", "google", "haier", "hisense", "hitachi", "itel", "jensen", "jvc", "kogan", "konka", "lg", "loewe", "magnavox", "marantz", "memorex", "micromax", "metz", "onida", "panasonic", "pensonic", "philips", "planar", "proscan", "rediffusion", "saba", "salora", "samsung", "sansui", "sanyo", "seiki", "sharp", "skyworth", "sony", "tatung", "tcl", "telefunken", "thomson", "tpv", "tp vision", "vestel", "videocon", "vizio", "vu", "walton", "westinghouse", "xiaomi", "zenith"]
    if any(word in title_pi for word in brands) and any(word in title_pj for word in brands):
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
        if k == "title":
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


def minHashing(binary_data, number_of_hashes, number_of_mw):
    primes = [i for i in range(5, 100) if checkIfPrime(i)]              # which bounds?????????????????????
    parameters_of_hash_functions = []
    for i in range(0, number_of_hashes):
        a = randint(1, 21)                                      # which bounds?????????????????????
        b = randint(1, 21)                                      # which bounds?????????????????????
        p = random.choice(primes)
        parameters = np.array([a, b, p])
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

    def h(i, row):
        a = param_hash_functions[i][0]
        b = param_hash_functions[i][1]
        p = param_hash_functions[i][2]
        return (a + b * (row+1)) % p

    hash_functions = np.array([[h(i, row) for row in range(number_of_mw)] for i in range(number_of_hash_functions)])

    for col, indices in enumerate(tqdm(binary_data)):
        for row in indices:
            for hash_func in range(0, number_of_hash_functions):
                row_hash = hash_functions[hash_func, row]
                hash_results[hash_func, col] = np.min([hash_results[hash_func, col], row_hash])

    return hash_results


def LSH(signature_matrix, b, r):
    number_of_items = len(signature_matrix[0])
    found = np.zeros((number_of_items, number_of_items))
    # Generate buckets per band
    overall_result_dict = {}
    for band in range(b):
        band_result_dict = {}
        for item in range(number_of_items):
            key_of_col_in_band = '-'.join(
                map(str, [col[item] for col in signature_matrix[(band * r):((band + 1) * r)]]))

            if key_of_col_in_band not in band_result_dict:
                band_result_dict[key_of_col_in_band] = [item]
            else:
                band_result_dict[key_of_col_in_band].append(item)

        overall_result_dict[band] = band_result_dict

    number_of_candidates_found = 0
    # Find candidate pairs, meaning they are the same in at least one bucket
    candidate_pairs = {}
    for band_results in overall_result_dict.values():
        for values in band_results.values():
            if len(values) > 1:
                number_of_candidates_found += 1
                for item_index in values:
                    if item_index not in candidate_pairs:
                        candidate_pairs[item_index] = set(values)
                        found[item_index, values] = 1
                    else:
                        candidate_pairs[item_index].update(values)
                        found[item_index, values] = 1

    return candidate_pairs, number_of_candidates_found, found


def dissimilarity(item1, item2, adjusted_list):
    keys_item1_featuresMap = list(adjusted_list[item1]["featuresMap"].keys())
    keys_item2_featuresMap = list(adjusted_list[item2]["featuresMap"].keys())
    intersection_keys = np.intersect1d(keys_item1_featuresMap, keys_item2_featuresMap)

    dsim1 = 0
    for matching_key in intersection_keys:
        dsim1 += calcSim(adjusted_list[item1]["featuresMap"][matching_key], adjusted_list[item2]["featuresMap"][matching_key])

    unique_keys_item1 = np.setdiff1d(keys_item1_featuresMap, intersection_keys)
    unique_keys_item2 = np.setdiff1d(keys_item2_featuresMap, intersection_keys)

    model_words_item_1_non_matching_keys = []
    model_words_item_2_non_matching_keys = []

    for non_matching_key in unique_keys_item1:
        model_words_item_1_non_matching_keys.extend(find_modelWordsOfaString(adjusted_list[item1]["featuresMap"][non_matching_key]))

    for non_matching_key in unique_keys_item2:
        model_words_item_2_non_matching_keys.extend(find_modelWordsOfaString(adjusted_list[item2]["featuresMap"][non_matching_key]))

    dsim2 = 0
    if len(np.union1d(model_words_item_1_non_matching_keys, model_words_item_2_non_matching_keys)) != 0:
        dsim2 = len(np.intersect1d(model_words_item_1_non_matching_keys, model_words_item_2_non_matching_keys)) / len(np.union1d(model_words_item_1_non_matching_keys, model_words_item_2_non_matching_keys))

    model_words_item_1_title = find_modelWordsOfaString(adjusted_list[item1]["title"])
    model_words_item_2_title = find_modelWordsOfaString(adjusted_list[item2]["title"])

    dsim3 = 0
    if len(np.union1d(model_words_item_1_title, model_words_item_2_title)) != 0:
        dsim3 = len(np.intersect1d(model_words_item_1_title, model_words_item_2_title)) / len(np.union1d(model_words_item_1_title, model_words_item_2_title))

    weighted_dissimilarity = 1/3 * dsim1 + 1/3 * dsim2 + 1/3 * dsim3

    return 1 / weighted_dissimilarity if weighted_dissimilarity != 0 else 1000


def F1_score(Nc, matches, adjusted_list, number_of_duplicates):
    number_of_items = len(adjusted_list)

    # Number of duplicates found
    Df = 0

    for v in matches:
        for i in v:
            for j in v:
                if not j == i:
                    if adjusted_list[i]["modelID"] == adjusted_list[j]["modelID"]:
                        Df += 1
    Df = Df / 2

    Dn = number_of_duplicates

    PQ = 0
    if not Nc == 0:
        PQ = Df / Nc

    PC = 0
    if not Dn == 0:
        PC = Df / Dn

    F1 = 0
    if not PC + PQ == 0:
        F1 = (2 * PQ * PC) / (PC + PQ)

    return F1, PC, PQ


def F1_star_score(Nc, matches, adjusted_list, duplicates, found):
    number_of_items = len(adjusted_list)

    Df = sum(sum(found * duplicates))/2

    # Total number of duplicates
    Dn = sum(sum(duplicates))/2

    PQ = 0
    if not Nc == 0:
        PQ = Df / Nc

    PC = 0
    if not Dn == 0:
        PC = Df / Dn

    F1 = 0
    if not PC + PQ == 0:
        F1 = (2 * PQ * PC) / (PC + PQ)

    return F1, PC, PQ


def cluster(matches, adjusted_list, b):
    number_of_items = len(adjusted_list)
    distances = np.ones((number_of_items, number_of_items)) * np.inf
    for key, value in matches.items():
        for v in value:
            if not key == v:
                item1 = adjusted_list[key]
                item2 = adjusted_list[v]
                if not (sameShop(item1, item2) or diffBrand(item1, item2)):
                    temp = dissimilarity(key, v, adjusted_list)
                    distances[key][v] = temp
                    distances[v][key] = temp

    clusters = []
    continue_cluster = True
    threshold = 10
    while continue_cluster:
        # Find minimum
        minimum = np.min(distances)
        min_indices = np.unravel_index(np.argmin(distances), distances.shape)
        merged_to = np.min(min_indices)
        dropped = np.max(min_indices)

        if minimum > threshold:
            break

        # Update clusters
        cluster_of_merged_to = next((tup for tup in clusters if merged_to in tup), None)
        cluster_of_dropped = next((tup for tup in clusters if dropped in tup), None)

        if cluster_of_merged_to is not None:
            if cluster_of_dropped is None:
                clusters.remove(cluster_of_merged_to)
                new_cluster_tuple = cluster_of_merged_to + (dropped,)
                clusters.append(new_cluster_tuple)
            elif cluster_of_dropped != cluster_of_merged_to:
                clusters.remove(cluster_of_merged_to)
                clusters.remove(cluster_of_dropped)
                new_cluster_tuple = cluster_of_merged_to + cluster_of_dropped
                clusters.append(new_cluster_tuple)
        elif cluster_of_dropped is not None:
            clusters.remove(cluster_of_dropped)
            new_cluster_tuple = cluster_of_dropped + (merged_to,)
            clusters.append(new_cluster_tuple)
        else:  # merged_to and dropped both not part of a cluster yet
            clusters.append(tuple((merged_to, dropped)))

        distances[merged_to][dropped] = np.inf
        distances[dropped][merged_to] = np.inf

        # Adjust distance matrix
        # Update the merged dissimilarities to the lowest value of the cluster (unless dropped had inf distance to item)
        for i in range(number_of_items):
            # Update the merged dissimilarities to the lowest value of the cluster (unless dropped had inf distance to item)
            if distances[merged_to][i] != np.inf and distances[merged_to][i] > distances[dropped][i]:
                distances[merged_to][i] = distances[dropped][i]
                distances[i][merged_to] = distances[dropped][i]
            elif distances[merged_to][i] != np.inf and distances[merged_to][i] < distances[dropped][i]:
                distances[dropped][i] = distances[merged_to][i]
                distances[i][dropped] = distances[merged_to][i]
            # If merged had inf distance with i, dropped now also has inf distance with i
            elif distances[dropped][i] != np.inf and distances[merged_to][i] == np.inf:
                distances[dropped][i] = np.inf
                distances[i][dropped] = np.inf
            elif distances[dropped][i] == np.inf and distances[merged_to][i] != np.inf:
                distances[merged_to][i] = np.inf
                distances[i][merged_to] = np.inf

    print(clusters)
    print(f"The length of clusters for iteration with {b} is: {len(clusters)}")
    print()

    return clusters
