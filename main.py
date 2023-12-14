import json
import functions
import random
from tqdm import tqdm
import numpy as np

# Load all data
with open("TVs-all-merged.json", "r") as file:
    data = json.load(file)

# Create list of all entries
list_adjusted = []
for v in data.values():
    for duplicate in v:
        list_adjusted.append(duplicate)

# Create different bootstraps
random.seed(0)
boot = 1  # 5
adjusted_list = []
for i in range(boot):
    adjusted_list = random.sample(list_adjusted, int(0.7*len(list_adjusted)))

    number_of_items = len(adjusted_list)
    duplicates = np.zeros((number_of_items, number_of_items))
    for index1 in range(number_of_items):
        item1 = adjusted_list[index1]
        for index2 in range(number_of_items):
            item2 = adjusted_list[index2]
            if not index1 == index2:
                if item1["modelID"] == item2["modelID"]:
                    duplicates[index1][index2] = 1

    # Store all model words
    all_model_words = []
    model_words_per_item = []
    for i in range(0, number_of_items):
        temp_mw = functions.find_modelWordsOfaProduct(adjusted_list[i])
        for word in temp_mw:
            if word not in all_model_words:
                all_model_words.append(word)
        model_words_per_item.append(temp_mw)

    binary_representation = []
    # Create binary representation
    for i in range(0, number_of_items):
        model_words_of_item_i = model_words_per_item[i]
        binary_model_words_of_i = []
        for element in range(0, len(all_model_words)):
            if model_words_of_item_i.__contains__(all_model_words[element]):
                binary_model_words_of_i.append(element)
        binary_representation.append(binary_model_words_of_i)

    signature_matrix = functions.minHashing(binary_representation, 1000, len(all_model_words))

    # ---------------------------------------------------------------------------
    # TODO: adjust
    F1 = []
    F1Star = []
    # F1_best = -1
    n = len(signature_matrix)
    for i in tqdm(range(2, n)):
        # matches = []
        if n % i == 0:
            b = i
            r = int(n/b)
            [matches, Nc, found] = functions.LSH(signature_matrix, b, r)

            F1Star.append(functions.F1_star_score(Nc, matches, adjusted_list, duplicates, found))

            # CLustering
            cluster = functions.clusterZELF(matches, adjusted_list, b)

            F1.append(functions.F1_score(Nc, cluster, adjusted_list, duplicates))
            # print(cluster.n_clusters_)
            # print(cluster.labels_)
            # print()

    print(F1Star)
    print(F1)

