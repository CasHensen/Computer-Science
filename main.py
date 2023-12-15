import json
import functions
import random
# from tqdm import tqdm
import numpy as np
import pandas as pd

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
boot = 5
adjusted_list = []
for bootstrap in range(boot):
    adjusted_list = random.sample(list_adjusted, int(0.63*len(list_adjusted)))

    number_of_items = len(adjusted_list)
    duplicates = np.zeros((number_of_items, number_of_items))
    number_of_duplicates = 0
    for index1 in range(len(adjusted_list)):
        item1 = adjusted_list[index1]
        for index2 in range(len(adjusted_list)):
            item2 = adjusted_list[index2]
            if not index1 == index2:
                if item1["modelID"] == item2["modelID"]:
                    duplicates[index1][index2] = 1
                    number_of_duplicates += 1
    number_of_duplicates = int(number_of_duplicates/2)

    # Store all model words
    all_model_words = []
    model_words_per_item = []
    for i in range(0, len(adjusted_list)):
        temp_mw = functions.find_modelWordsOfaProduct(adjusted_list[i])
        for word in temp_mw:
            if word not in all_model_words:
                all_model_words.append(word)
        model_words_per_item.append(temp_mw)

    binary_representation = []
    # Create binary representation
    for i in range(0, len(adjusted_list)):
        model_words_of_item_i = model_words_per_item[i]
        binary_model_words_of_i = []
        for element in range(0, len(all_model_words)):
            if model_words_of_item_i.__contains__(all_model_words[element]):
                binary_model_words_of_i.append(element)
        binary_representation.append(binary_model_words_of_i)

    signature_matrix = functions.minHashing(binary_representation, 1000, len(all_model_words))

    F1 = []
    F1Star = []
    PCStar = []
    PQStar = []
    PC = []
    PQ = []
    NcStar = []
    Nc = []
    n = len(signature_matrix)
    # for i in tqdm(range(2, n)):
    for i in range(2, n):
        # matches = []
        if n % i == 0:
            b = i
            r = int(n / b)
            [matches, Nc_value_star, found] = functions.LSH(signature_matrix, b, r)

            [F1_value_Star, PC_value_Star, PQ_value_Star] = functions.F1_star_score(Nc_value_star, duplicates, found)
            F1Star.append(F1_value_Star)
            PCStar.append(PC_value_Star)
            PQStar.append(PQ_value_Star)
            NcStar.append(Nc_value_star)

            # Clustering
            [cluster, Nc_value] = functions.cluster(matches, adjusted_list, b)

            [F1_value, PC_value, PQ_value] = functions.F1_score(Nc_value, cluster, adjusted_list, number_of_duplicates)
            F1.append(F1_value)
            PC.append(PC_value)
            PQ.append(PQ_value)
            Nc.append(Nc_value)

    print("-----------------------------------------------------------------------------------------------------")
    print(F1Star, PCStar, PQStar, NcStar)
    print(F1, PC, PQ, Nc)
    print("-----------------------------------------------------------------------------------------------------")
    print()

    str_value = "Results_Computer_Science"
    str_value = str_value + str(bootstrap)
    str_value = str_value + ".xlsx"
    df = pd.DataFrame(data=[F1Star, F1, PCStar, PC, PQStar, PQ, NcStar, Nc])

    df.to_excel(str_value, index=False)
