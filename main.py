import json
import functions
import random
from tqdm import tqdm

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

    # ---------------------------------------------------------------------------
    # TODO: adjust
    # F1 = []
    # F1_best = -1
    n = len(signature_matrix)
    for i in tqdm(range(2, n)):
        # matches = []
        if n % i == 0:
            b = i
            r = int(n/b)
            matches = functions.LSH(signature_matrix, b, r)

            # F1_new = functions.F1_Score(matches, adjusted_list, len(signature_matrix[0]), b, r)
            # F1.append(F1_new)
            # if F1_best < F1_new:
            #     F1_best = F1_new

            # CLustering
            cluster = functions.clusterZELF(matches, adjusted_list, b)
            # print(cluster.n_clusters_)
            # print(cluster.labels_)
            # print()

