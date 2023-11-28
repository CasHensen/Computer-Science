import json
import functions
import re

# Load all data
with open("TVs-all-merged.json", "r") as file:
    data = json.load(file)

# Create list of all entries
adjusted_list = []
for v in data.values():
    for duplicate in v:
        adjusted_list.append(duplicate)

# Clean titles by removing all common characters (e.g., commas, slashes, white spaces), uppercase to lowercase and consistent unit representation of inch and hertz
for i in range(0, len(adjusted_list)):
    adjusted_list[i]["title"] = adjusted_list[i]["title"].lower()
    adjusted_list[i]["title"] = adjusted_list[i]["title"].replace("inches", "inch")
    adjusted_list[i]["title"] = adjusted_list[i]["title"].replace("hertz", "hz")
    adjusted_list[i]["title"] = re.sub(r"(\d+)( *)\"", r'\g<1>inch', adjusted_list[i]["title"])
    adjusted_list[i]["title"] = re.sub('[(]?[)]?', "", adjusted_list[i]["title"])
    adjusted_list[i]["title"] = re.sub(r':\s', ' ', adjusted_list[i]["title"])
    adjusted_list[i]["title"] = re.sub(r'-inch', 'inch', adjusted_list[i]["title"])
    adjusted_list[i]["title"] = re.sub(r' - ', ' ', adjusted_list[i]["title"])
    adjusted_list[i]["title"] = re.sub(r'(?!<\d)[.](?!\d)', '', adjusted_list[i]["title"])
    adjusted_list[i]["title"] = re.sub(' +', ' ', adjusted_list[i]["title"])

inf_distances = []  # store indexes of columns that respective row has infinite distance with (either different brand or same  shop)
for i in range(0, len(adjusted_list)):
    temp_for_inf_distance = []
    for j in range(0, len(adjusted_list)):
        if i != j and functions.sameShop(adjusted_list[i], adjusted_list[j]) or functions.diffBrand(adjusted_list[i], adjusted_list[j]):
            temp_for_inf_distance.append(j)
    inf_distances.append(temp_for_inf_distance)
print(inf_distances)
