from collections import Counter
from itertools import islice
import sys

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'


def reading_input(fname):
    """ data is list of words and there tags (in one string)"""
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
    singles = [a for a in tags]
    pairs = [join([a, b]) for a, b in combinations(tags, 2)]
    triplets = [join([a, b, c]) for a, b, c in combinations(tags, 3)]
    return Counter(pairs), Counter(triplets), Counter(singles), len(tags)


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def write_estimations(pairs1, tags, f_name):
    pairs = merge_two_dicts(pairs1, train_unknown(pairs1))
    with open(f_name, "w") as file:
        for i in pairs:
            file.write(join([i, '\t', str(pairs[i]), '\n', str(i.split()[1]),
                             '\t', str(tags[i.split()[1]]), '\n']))


def write_quantities():
    with open(q_mle, "w") as file:
        for key in triplets:
            pair_key = join([k for k in key.split()[:-1]])
            file.write(join([str(key), '\t', str(triplets[key]), '\n']))
            file.write(join([str(pair_key), '\t', str(pairs[pair_key]), '\n']))
        for key in pairs:
            single_key = join([k for k in key.split()[:-1]])
            file.write(join([str(key), '\t', str(pairs[key]), '\n']))
            file.write(join([str(single_key), '\t', str(singles[single_key]), '\n']))
        for key in singles:
            file.write(join([str(key), '\t', str(singles[key]), '\n']))
            file.write(join(["All tags", '\t', str(tags_size), '\n']))


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


def get_q(t1, t2, t3, lambda_values, q_dic):
    l1, l2, l3 = lambda_values
    # print(lambda_values)
    # print(str(t1) + "    " + str(t2) + "   " + str(t3) + "\n")
    if t1 == START_SYMBOL:
        pred1 = 0
    else:
        pred1 = l1 * q_dic.get(join([t1, t2, t3]), 0)
    if t2 == START_SYMBOL:
        pred2 = 0
    else:
        pred2 = l2 * q_dic.get(join([t2, t3]), 0)
    if t3 == STOP_SYMBOL:
        pred3 = 0
    else:
        pred3 = l3 * q_dic.get(t3, 0)
    return pred1 + pred2 + pred3


def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def get_q_dict(f_name):
    with open(f_name, encoding="utf8") as file:
        lines = [line for line in file]
    q_dict = {}
    for line, next_line in zip(lines[::2], lines[1::2]):
        tags, count = line.split('\t')
        tags = tags[:-1]
        count = count.split("\n")[0]
        next_tags, next_count = next_line.split('\t')
        next_count = next_count.split("\n")[0]
        if float(count) is 0 or float(next_count) is 0:  # might be better way for handling division by 0
            q_dict[tags] = 0
        else:
            prob = float(count) / float(next_count)
            q_dict[tags] = prob
            # e_dict[word_and_tag] = float(count) / float(next_count)
    return q_dict


def get_e_dict(f_name):
    with open(f_name, encoding="utf8") as file:
        lines = [line for line in file]
    e_dict = {}
    for line, next_line in zip(lines[::2], lines[1::2]):
        word_and_tag, count = line.split('\t')
        word_and_tag = word_and_tag[:-1]
        count = count.split("\n")[0]
        next_tags, next_count = next_line.split('\t')
        next_count = next_count.split("\n")[0]
        if float(count) is 0 or float(next_count) is 0:  # might be better way for handling division by 0
            e_dict[word_and_tag] = 0
        else:
            prob = float(count) / float(next_count)
            e_dict[word_and_tag] = prob
            # e_dict[word_and_tag] = float(count) / float(next_count)
    return e_dict


def get_e(w, t, e_dict):
    return e_dict.get(join([w, t]), 0)


def get_unknown_e(w, t, e_dict):
    unk = classify_unknown(w)
    return e_dict.get(join([unk, t]), 1 / len(e_dict))


def create_possible_tags(tags_file, tags):
    tags_dict = Counter(tags)
    tags_list = sorted(tags_dict, key=tags_dict.get, reverse=True)
    with open(tags_file, "w") as file:
        for tag in tags_list:
            file.write(tag + '\n')


def get_possible_tags(tags_file):
    tags = []
    with open(tags_file, "r") as file:
        for line in file:
            tags.append(line.split("\n")[0])
    return tags


def my_counter(data):
    words_count = {}
    for word in data:
        if word[0] not in words_count:
            words_count[word[0]] = [0, ""]
        words_count[word[0]][0] += 1
        words_count[word[0]][1] = word[1]
    return words_count


def train_unknown(data):
    """ data is dict of words and there tags -> there count """
    data1 = [[k.split()[0], k.split()[1]] for k in data]
    data1 = my_counter(data1)
    data1 = [[k, data1[k][1]] for k in data1 if
             data1[k][0] is 1]  # now data1 is list of words which appear only once and there tag [word, tag]
    dict_to_e = {}  # dictionary of unknowns to add to e.mle
    for word, tag in data1:
        current_str = classify_unknown(word)
        """if current_str == "^unk":
            continue"""
        current_str = current_str + " " + tag
        if current_str not in dict_to_e:
            dict_to_e[current_str] = 0
        dict_to_e[current_str] += 1
        # dict_to_e[join(["^unk", "all"])] = 1
        # dict_to_e["all"] = len(data)
        # print (dict_to_e)
    return dict_to_e


def classify_unknown(word):
    suffix_1 = ["s"]
    suffix_2 = ["ly", "ed", "al", "ul", "er", "es", "ty", "en"]
    suffix_3 = ["ing", "ous", "age", "ies", "ive", "ery", "ers", "ity", "ist", "ent", "ian", "ism", "ary", "ory",
                "phy", "ate", "est"]
    suffix_4 = ["ness", "tial", "tion", "sion", "able", "ence", "ance"]

    current_str = "^unk"
    if word[0].isupper():
        current_str = "^Unk"

    if word[-4:] in suffix_4:
        current_str += word[-4:]
    elif word[-3:] in suffix_3:
        current_str += word[-3:]
    elif word[-2:] in suffix_2:
        current_str += word[-2:]
    elif word[-1:] in suffix_1:
        current_str += word[-1:]
    elif len(word.split("-")) >= 2:
        subs = word.split("-")
        for sub in subs:
            if is_number(sub):
                current_str += "-num"
            else:
                current_str += "-not_num"
    elif are_all_numbers(word, ":") or are_all_numbers(word, "/"):
        current_str += "time"
    elif are_all_numbers(word, ",") or are_all_numbers(word, "."):
        current_str += "num"
    elif "'" in word:
        current_str += "slang"
    return current_str


def are_all_numbers(str, delim):
    all_num = True
    subs = str.split(delim)
    for sub in subs:
        if not is_number(sub):
            all_num = False
    return all_num


def is_number(str):
    try:
        word = float(str)
        return True
    except ValueError:
        return False
        pass  # it was a string, not an float


if __name__ == '__main__':
    script_name, f_name, q_mle, e_mle = sys.argv
    tags, data = reading_input(f_name)
    create_possible_tags(tags)
    pairs, triplets, singles, tags_size = counting_quantities(tags)
    write_quantities()
    write_estimations(Counter(data), Counter(tags), e_mle)

