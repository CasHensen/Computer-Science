import json
import functions
import random
import numpy as np
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
boot = 5
adjusted_list = []
for i in tqdm(range(boot)):
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
F1 = []
matches_best = []
F1_best = -1
n = len(signature_matrix)
for i in range(2, n):
    matches = []
    if n % i == 0:
        b = i
        r = int(n/b)
        matches = functions.LSH(signature_matrix, b, r)
        print(len(matches[1]))
        F1_new = functions.F1_Score(matches, adjusted_list, len(signature_matrix[0]), b, r)
        F1.append(F1_new)
        if F1_best < F1_new:
            F1_best = F1_new
            matches_best = matches

# ---------------------------------------------------------------------------

# matches = functions.LSH(signature_matrix, b, r)

inf_distances = []  # store indexes of columns that respective row has infinite distance with (either different brand or same shop)
for item_i in range(0, len(adjusted_list)):
    temp_for_inf_distance = []
    for item_j in range(0, len(adjusted_list)):
        if item_i != item_j:
            if functions.sameShop(adjusted_list[item_i], adjusted_list[item_j]):
                temp_for_inf_distance.append(item_j)
            elif functions.diffBrand(adjusted_list[item_i], adjusted_list[item_j]):
                temp_for_inf_distance.append(item_j)
            elif not matches_best[item_i].__contains__(item_j):
                temp_for_inf_distance.append(item_j)
    inf_distances.append(temp_for_inf_distance)
print(inf_distances)
print()

# Clustering
number_of_items = len(signature_matrix[0])
dissimilarities = np.ones((number_of_items, number_of_items)) * np.inf
for item1 in range(number_of_items):
    for item2 in range(item1 + 1, number_of_items):
        if not inf_distances[item1].__contains__(item2):
            temp = functions.dissimilarity(item1, item2, adjusted_list)
            dissimilarities[item1][item2] = temp
            dissimilarities[item2][item1] = temp
print(dissimilarities)
print()

closest_item = np.ones((number_of_items, 3)) * np.inf  # bestaat ook index nul zodat duidelijk onderscheid is tussen index nul of geen
for item1 in range(number_of_items):
    index_of_closest = -1
    similarity_of_closest = -1
    for item2 in range(number_of_items):
        if item1 != item2 and not inf_distances[item1].__contains__(item2):
            if dissimilarities[item1][item2] > similarity_of_closest:
                index_of_closest = item2
                similarity_of_closest = dissimilarities[item1][item2]
    if index_of_closest == -1:
        closest_item[item1][0] = item1
    else:
        closest_item[item1][0] = item1
        closest_item[item1][1] = index_of_closest
        closest_item[item1][2] = dissimilarities[item1][index_of_closest]
print(closest_item)
print()

clusters = []
cluster = True
threshold = 1
while cluster:
    # Find minimum
    minimum = threshold  # Set to threshold
    dropped_item = 0
    merged_to_item = 0

    for item in range(len(closest_item)):
        if closest_item[item][2] > minimum and closest_item[item][2] != np.inf:
            minimum = closest_item[item][2]
            if closest_item[item][0] < closest_item[item][1]:       # merged_to always smallest number of the two
                merged_to_item = int(closest_item[item][0])
                dropped_item = int(closest_item[item][1])
            else:
                merged_to_item = int(closest_item[item][1])
                dropped_item = int(closest_item[item][0])

    if minimum == threshold:
        break

    dropped_row_of_item = -1
    merged_to_row_of_item = -1
    for row_nr in range(len(closest_item)):
        if closest_item[row_nr][1] == merged_to_item and closest_item[row_nr][0] == dropped_item:
            merged_to_row_of_item = row_nr
            dropped_row_of_item = row_nr
            break

    closest_item = np.delete(closest_item, dropped_row_of_item, 0)

    # Update clusters
    cluster_of_merged_to = next((tup for tup in clusters if merged_to_item in tup), None)
    cluster_of_dropped = next((tup for tup in clusters if dropped_item in tup), None)

    if cluster_of_merged_to is not None:
        if cluster_of_dropped is None:
            clusters.remove(cluster_of_merged_to)
            new_cluster_tuple = cluster_of_merged_to + (dropped_item,)
            clusters.append(new_cluster_tuple)
        elif cluster_of_dropped != cluster_of_merged_to:
            clusters.remove(cluster_of_merged_to)
            clusters.remove(cluster_of_dropped)
            new_cluster_tuple = cluster_of_merged_to + cluster_of_dropped
            clusters.append(new_cluster_tuple)
    elif cluster_of_dropped is not None:
        clusters.remove(cluster_of_dropped)
        new_cluster_tuple = cluster_of_dropped + (merged_to_item,)
        clusters.append(new_cluster_tuple)
    else:  # merged_to and dropped both not part of a cluster yet
        clusters.append(tuple((merged_to_item, dropped_item)))

    # Adjust new values
    new_min_merged = np.inf * -1
    for item in range(len(closest_item)):
        # Adjust new closest item for merged items
        if closest_item[item][0] == merged_to_item:
            closest_item[item][1] = np.inf
            closest_item[item][2] = np.inf
            for i in range(number_of_items):
                # Update the merged dissimilarities to the lowest value of the cluster (unless dropped had inf distance to item)
                if dissimilarities[merged_to_item][i] != np.inf and dissimilarities[merged_to_item][i] < dissimilarities[dropped_item][i]:
                    dissimilarities[merged_to_item][i] = dissimilarities[dropped_item][i]
                    dissimilarities[i][merged_to_item] = dissimilarities[dropped_item][i]
                # Update the new closest item for the merged items
                if dissimilarities[merged_to_item][i] != np.inf and dissimilarities[merged_to_item][i] > new_min_merged:  # and not inf_distances[dropped].__contains__(i): (nu al in vorige if)
                    new_min_merged = dissimilarities[merged_to_item][i]
                    closest_item[item][1] = i
                    closest_item[item][2] = new_min_merged
                # If merged had inf distance with i, dropped now also has inf distance with i
                if dissimilarities[dropped_item][i] != np.inf and dissimilarities[merged_to_item][i] == np.inf:
                    dissimilarities[dropped_item][i] = np.inf
                    dissimilarities[i][dropped_item] = np.inf
                    # Replace the item that is dropped by the newly merged item (one cluster) for items
        elif closest_item[item][1] == dropped_item:
            if dissimilarities[merged_to_item][item] == np.inf:
                closest_item[item][1] = np.inf
                closest_item[item][2] = np.inf
            if dissimilarities[merged_to_item][item] != np.inf:
                closest_item[item][1] = merged_to_item
        # Check whether the other product fall in the inf distance of the cluster, if so change their closest neighbour
        elif closest_item[item][1] == merged_to_item:
            closest_item[item][1] = np.inf
            closest_item[item][2] = np.inf
            if inf_distances[dropped_item].__contains__(closest_item[item][0]):
                new_min = np.inf * -1
                dissimilarities[closest_item[item][0]][merged_to_item] = np.inf
                dissimilarities[merged_to_item][closest_item[item][0]] = np.inf
                for i in range(number_of_items):
                    if dissimilarities[merged_to_item][i] != np.inf and dissimilarities[merged_to_item][i] > new_min:
                        new_min = dissimilarities[closest_item[item][0]][i]
                        closest_item[item][1] = i
                        closest_item[item][2] = new_min

print(clusters)
