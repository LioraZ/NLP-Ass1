from collections import Counter
from itertools import islice
import sys


def reading_input(fname):
    tags = []
    data = []
    with open(fname, encoding="utf8") as file:
        input_data = [word for line in file for word in line.split()]
    for word in input_data:
        items = word.split('/')
        tags.append(items[-1])
        data.append(join(["/".join(items[:-1]), items[-1]]))
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


def get_q(t1, t2, t3, q_dic, f_name):
    with open(f_name, encoding="utf8") as file:
        lines = [line for line in file]
    for line, next_line in zip(lines[::2], lines[1::2]):
        tags, count = line.split('\t')
        count = count.split("\n")[0]
        if tags is join([t1, t2, t3]):
            next_tags, next_count = next_line.split('\t')
            return float(count) / float(next_count)
    return 0
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
        return None"""


def get_e_dict(f_name):
    with open(f_name, encoding="utf8") as file:
        lines = [line for line in file]
    e_dict = {}
    for line, next_line in zip(lines[::2], lines[1::2]):
        word_and_tag, count = line.split('\t')
        count = count.split("\n")[0]
        next_tags, next_count = next_line.split('\t')
        next_count = next_count.split("\n")[0]
        if float(count) is 0 or float(next_count) is 0: #might be better way for handling division by 0
            e_dict[word_and_tag] = 0
        else:
            prob = float(count) / float(next_count)
            e_dict[word_and_tag] = prob
            #e_dict[word_and_tag] = float(count) / float(next_count)
    return e_dict


def get_e(w, t, e_dict):
    word_and_tag = join([w, t])
    if word_and_tag in e_dict:
        return e_dict[word_and_tag]
    return 0
    """with open(f_name, encoding="utf8") as file:
        lines = [line for line in file]
    for line, next_line in zip(lines[::2], lines[1::2]):
        word_and_tag, count = line.split('\t')
        count = count.split("\n")[0]
        temp = join([w, t])
        if word_and_tag is join([w, t]):
            # next_line = next(line)
            next_tags, next_count = next_line.split('\t')
            return float(count) / float(next_count)"""
    #return 0


def create_possible_tags(tags):
    tags = set(tags)
    with open("possible_tags", "w") as file:
        for tag in tags:
            file.write(tag + '\n')


def get_possible_tags():
    tags = []
    with open("possible_tags", "r") as file:
        for line in file:
            tags.append(line.split("\n")[0])
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
