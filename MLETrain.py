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
    pairs = [join([a, b]) for a, b in combinations(tags, 2)]
    triplets = [join([a, b, c]) for a, b, c in combinations(tags, 3)]
    return Counter(pairs), Counter(triplets)


def write_estimations(pairs, tags, f_name):
    with open(f_name, "w") as file:
        for i in pairs:
            file.write(join([i, '\t', str(pairs[i]), '\n', str(i.split(" ")[1]),
                             '\t', str(tags[i.split(" ")[1]]), '\n']))


def write_quantities(pairs, triplets, f_name):
    with open(f_name, "w") as file:
        for key in triplets:
            pair_key = join([k for k in key.split()[:-1]])
            file.write(join([str(key), '\t', str(triplets[key]), '\n']))
            file.write(join([str(pair_key), '\t', str(pairs[pair_key]), '\n']))


def join(str_list):
    return " ".join(str_list)


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


def get_q(t1, t2, t3, f_name):
    """
    REMEMBER TO MAKE INTERPOLATION, BECAUSE CAN HAVE ZERO VALUE!!!
    :param t1:
    :param t2:
    :param t3:
    :return:
    """
    with open(f_name, encoding="utf8") as file:
        for line in file:
            tags, count = line.split('\t')
            if tags is join([t1, t2, t3]):
                next_line = next(line)
                next_tags, next_count = next_line.split('\t')
                return float(count) / float(next_count)
            else:
                next(line)
        return None


def get_e(w, t, f_name):
    with open(f_name, encoding="utf8") as file:
        for line in file:
            word_and_tag, count = line.split('\t')
            if word_and_tag is join([w, t]):
                next_line = next(line)
                next_tags, next_count = next_line.split('\t')
                return float(count) / float(next_count)
            else:
                next(line)
    return None


def create_possible_tags(tags):
    tags = set(tags)
    with open("possible_tags", "w") as file:
        for tag in tags:
            file.write(tag + '\n')


def get_possible_tags():
    tags = []
    with open("possible_tags", "w") as file:
        for line in file:
            tags.append(line)
    return tags


def train_unknown(word, data):
    data = [k for k, v in data.items() if v is 1]
    for key in data:
        word = key.split()[0] # only if needed
        pred = classify_unknown(word)


def classify_unknown(word):
    if word[-3:] is "ing":
        return unk_type
    # word contains a number
    # word contains an upper-case letter
    # word contains a hyphen
    # word is all upper-case
    # word contains a particular prefix (up to length 4)
    # word contains a particular suffix (up to length 4)
    # word is upper-case and has a digit and and a dash
    return "NN"


if __name__ == '__main__':
    script_name, f_name, q_mle, e_mle = sys.argv
    tags, data = reading_input(f_name)
    create_possible_tags(tags)
    pairs, triplets = counting_quantities(tags)
    write_quantities(pairs, triplets, q_mle)
    write_estimations(Counter(data), Counter(tags), e_mle)
