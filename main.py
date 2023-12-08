import json
import functions
import random
# import re

# Load all data
with open("TVs-all-merged.json", "r") as file:
    data = json.load(file)

# Create list of all entries
adjusted_list = []
for v in data.values():
    for duplicate in v:
        adjusted_list.append(duplicate)

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

random.seed(1)
minhash = functions.minHashing(binary_representation, int(len(binary_representation)/2), len(all_model_words))

# inf_distances = []  # store indexes of columns that respective row has infinite distance with (either different brand or same shop)
# for i in range(0, len(adjusted_list)):
#     temp_for_inf_distance = []
#     for j in range(0, len(adjusted_list)):
#         if i != j and functions.sameShop(adjusted_list[i], adjusted_list[j]) or functions.diffBrand(adjusted_list[i], adjusted_list[j]):
#             temp_for_inf_distance.append(j)
#     inf_distances.append(temp_for_inf_distance)
# print(inf_distances)

# TODO: use calcSim(q, r) for q-gram similarity (but check function first!!)
# TODO: use mw(C, D) for percentage of matching model words from two sets of model words

# test_str = "aaaaa"
# bla = "aaa"
# print(functions.calcSim(test_str, bla))
# functions.calcSim(test_str, test_str2) # IS NOT RIGHT
