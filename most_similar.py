import csv

items = []

with open("similarities.csv", "r") as similarities_file:
    reader = csv.reader(similarities_file, delimiter = ",")
    for row in reader:
        lst = list(row)
        lst[4] = float(lst[4])
        items.append(tuple(lst))

by_similarity = sorted(items, key = lambda x: x[4], reverse = True)

for similar_item in [item for item in by_similarity if 0.5 < item[4] < 0.99]:
    print similar_item
