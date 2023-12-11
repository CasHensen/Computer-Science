import json
import functions
import random
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
boot = 5
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
# print(binary_representation)

signature_matrix = functions.minHashing(binary_representation, 1000, len(all_model_words))
print(signature_matrix)
print()

# ---------------------------------------------------------------------------
# TODO: adjust
b = 0
r = 0
for i in range(2, 10):
    if int(len(binary_representation)) % (10-i) == 0:
        b = i
        r = int(int(len(binary_representation)) / i)
        break
# ---------------------------------------------------------------------------

matches = functions.LSH(signature_matrix, b, r)
# print(matches)
# print()

inf_distances = []  # store indexes of columns that respective row has infinite distance with (either different brand or same shop)
for item_i in range(0, len(adjusted_list)):
    temp_for_inf_distance = []
    for item_j in range(0, len(adjusted_list)):
        if item_i != item_j:
            if functions.sameShop(adjusted_list[item_i], adjusted_list[item_j]):
                temp_for_inf_distance.append(item_j)
            elif functions.diffBrand(adjusted_list[item_i], adjusted_list[item_j]):
                temp_for_inf_distance.append(item_j)
            elif not matches[item_i].__contains__(item_j):
                temp_for_inf_distance.append(item_j)
    inf_distances.append(temp_for_inf_distance)
print(inf_distances)
print()

number_of_items = len(signature_matrix[0])
dissimilarities = np.ones((number_of_items, number_of_items)) * np.inf
closest_item = np.zeros((number_of_items, 2))
for col1 in range(number_of_items):
    index_of_closest = 0
    for col2 in range(col1+1, number_of_items):
        if not inf_distances[col1].__contains__(col2):
            # dissimilarities[col1][col2] = functions.dissimilarity()
            if dissimilarities[col1][col2] < dissimilarities[col1][index_of_closest]:
                index_of_closest = col2
    closest_item[col1][0] = index_of_closest
    closest_item[col1][1] = dissimilarities[col1][index_of_closest]
