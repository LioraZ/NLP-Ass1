from collections import Counter
from itertools import islice

START_SYMBOL = "*"
STOP_SYMBOL = "STOP"


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


def get_q_dict(q_mle):
    with open(q_mle, encoding="utf8") as file:
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
    return q_dict


def get_e_dict(e_mle):
    with open(e_mle, encoding="utf8") as file:
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
    return e_dict


def get_e(w, t, e_dict):
    return e_dict.get(join([w, t]), 0)


def get_unknown_e(w, t, e_dict):
    unk = classify_unknown(w)
    return e_dict.get(join([unk, t]), 1 / len(e_dict))


def create_possible_tags(tags, f_name):
    tags_dict = Counter(tags)
    tags_list = sorted(tags_dict, key=tags_dict.get, reverse=True)
    with open(f_name, "w") as file:
        for tag in tags_list:
            file.write(tag + '\n')


def get_possible_tags(f_name):
    tags = []
    with open(f_name, "r") as file:
        for line in file:
            tags.append(line.split("\n")[0])
    return tags


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


