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
matches = []

n = len(signature_matrix)
for i in range(n):
    if i%n == 0:
        b = i
        r = n/b
        matches.append(functions.LSH(signature_matrix, b, r))

# ---------------------------------------------------------------------------

#matches = functions.LSH(signature_matrix, b, r)
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
closest_item = np.zeros((number_of_items, 3))
for item1 in range(number_of_items):
    index_of_closest = 0
    for item2 in range(item1 + 1, number_of_items):
        if not inf_distances[item1].__contains__(item2):
            temp = functions.dissimilarity(item1, item2, adjusted_list)
            dissimilarities[item1][item2] = temp
            dissimilarities[item2][item1] = temp
            if temp < dissimilarities[item1][index_of_closest]:
                index_of_closest = item2
    closest_item[item1][0] = item1
    closest_item[item1][1] = index_of_closest
    closest_item[item1][2] = dissimilarities[item1][index_of_closest]

clusters = []
cluster = True
threshold = 6
while cluster:
    #find minimum
    minimum = threshold #set to threshold
    dropped = 0
    merged = 0
    for item in range(closest_item):
        if closest_item[item][2] < minimum:
            minimum = closest_item[item][2]
            dropped = closest_item[item][1]
            merged = closest_item[item][0]

    if minimum == threshold:
        break

    closest_item = np.delete(closest_item, dropped, 0)
    clusters = clusters.append(tuple((merged, dropped)))

    #adjust new values
    new_min_merged = np.inf

    for item in range(closest_item):
        if closest_item[item][0] == merged:
            for i in range(number_of_items):
                if dissimilarities[merged][i] < new_min_merged and not nf_distances[dropped].__contains__(i):
                    new_min_merged = dissimilarities[merged][i]
                    closest_item[item][1] = i
                    closest_item[item][2] = new_min_merged
        elif closest_item[item][1] == dropped:
            closest_item[item][1] = merged
        elif closest_item[item][1] == merged:
            if inf_distances[dropped].__contains__(closest_item[item][0]):
                new_min = np.inf
                dissimilarities[closest_item[item][0]][merged] = np.inf
                dissimilarities[merged][closest_item[item][0]] = np.inf
                for i in range(number_of_items):
                    if dissimilarities[merged][i] < new_min:
                        new_min = dissimilarities[closest_item[item][0]][i]
                        closest_item[item][1] = i
                        closest_item[item][2] = new_min



