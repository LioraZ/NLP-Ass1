from collections import Counter
from itertools import islice


def reading_input(fname):
    tags = []
    with open(fname, encoding="utf8") as file:
        data = [word for line in file for word in line.split()]
        for word in data:
            item = word.split('/')
            tags.append(item[-1])
    return tags


def counting_quantities(tags):
    pairs = [a + " " + b for a, b in combinations(tags, 2)]
    triplets = [a + " " + b + " " + c for a, b, c in combinations(tags, 3)]
    return Counter(pairs), Counter(triplets)


def write_quantities(pairs, triplets):
    with open("q.mle", "w") as file:
        for key in triplets:
            pair_key = " ".join([k for k in key.split()[:-1]])
            file.write(str(key) + '\t' + str(triplets[key]) + '\n')
            file.write(str(pair_key) + '\t' + str(pairs[pair_key]) + '\n')



def combinations(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


if __name__ == '__main__':
    pairs, triplets = counting_quantities(reading_input("data/ass1-tagger-train"))
    write_quantities(pairs, triplets)