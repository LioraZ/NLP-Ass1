from collections import Counter
from itertools import islice
import sys


def reading_input(fname):
    tags = []
    with open(fname, encoding="utf8") as file:
        data = [word for line in file for word in line.split()]
        for word in data:
            item = word.split('/')
            tags.append(item[-1])
        for i in range(len(data)):
            data[i] = data[i].replace("/", " ")
    return tags, data


def counting_quantities(tags):
    pairs = [a + " " + b for a, b in combinations(tags, 2)]
    triplets = [a + " " + b + " " + c for a, b, c in combinations(tags, 3)]
    return Counter(pairs), Counter(triplets)


def write_estimations(pairs, tags, f_name):
    with open(f_name, "w") as file:
        for i in pairs:
            file.write(i + '\t' + str(pairs[i]) + '\n' + str(i.split(" ")[1]) + '\t' + str(tags[i.split(" ")[1]]) + '\n')


def write_quantities(pairs, triplets, f_name):
    with open(f_name, "w") as file:
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
    script_name, f_name, q_mle, e_mle = sys.argv
    tags, data = reading_input(f_name)
    write_estimations(Counter(data), Counter(tags), e_mle)
    pairs, triplets = counting_quantities(tags)
    write_quantities(pairs, triplets, q_mle)
