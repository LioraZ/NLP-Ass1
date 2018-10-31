from itertools import combinations
from collections import Counter

def reading_input(fname):
    tags = []
    with open(fname, encoding="utf8") as file:
        data = [word for line in file for word in line.split()]
        for word in data:
            item = word.split('/')
            tags.append(item[1])
    return tags


def counting_quantities(tags):
    for pair in combinations(tags, 2):
        a, b = pair
        print(a, b, pair)
        print(a + " " + b)

    pairs = [a + " " + b for pair in combinations(tags, 2) for a, b in pair]
    triplets = [a + " " + b + " " + c for triplet in combinations(tags, 3) for a, b, c in triplet]
    return Counter(pairs), Counter(triplets)


def write_quantities(pairs, triplets):
    with open("q.mle", "w") as file:
        file.write(pair.key() + '\t' + str(pair.value) + '\n' for pair in pairs)
        file.write(triplet.key() + '\t' + str(triplet.value) + '\n' for triplet in triplets)
        """
        for pair in pairs:
            file.write(pair.key() + '\t' + str(pair.value) + '\n')
        for triplet in triplets:
            file.write(triplet.key() + '\t' + str(triplet.value) + '\n')
        """


if __name__ == '__main__':
    write_quantities(counting_quantities(reading_input("data/ass1-tagger-train")))

