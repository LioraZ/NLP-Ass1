from collections import Counter
from itertools import islice
import sys


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
    return Counter(pairs), Counter(triplets), Counter(singles)


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def write_estimations(pairs1, tags, f_name):
    pairs = merge_two_dicts(pairs1, train_unknown(pairs1))
    with open(f_name, "w") as file:
        for i in pairs:
            file.write(join([i, '\t', str(pairs[i]), '\n', str(i.split(" ")[1]),
                             '\t', str(tags[i.split(" ")[1]]), '\n']))


def write_quantities(pairs, triplets, singles, f_name):
    with open(f_name, "w") as file:
        for key in triplets:
            pair_key = join([k for k in key.split()[:-1]])
            file.write(join([str(key), '\t', str(triplets[key]), '\n']))
            file.write(join([str(pair_key), '\t', str(pairs[pair_key]), '\n']))
        for key in pairs:
            single_key = join([k for k in key.split()[:-1]])



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


def get_q(t1, t2, t3, q_dic):
    tags = join([t1, t2, t3])
    if tags in q_dic:
        return q_dic[tags]
    return 0


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
        if float(count) is 0 or float(next_count) is 0: #might be better way for handling division by 0
            q_dict[tags] = 0
        else:
            prob = float(count) / float(next_count)
            q_dict[tags] = prob
            #e_dict[word_and_tag] = float(count) / float(next_count)
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
        if float(count) is 0 or float(next_count) is 0: #might be better way for handling division by 0
            e_dict[word_and_tag] = 0
        else:
            prob = float(count) / float(next_count)
            e_dict[word_and_tag] = prob
            #e_dict[word_and_tag] = float(count) / float(next_count)
    return e_dict


def get_e(w, t, e_dict):
    word_and_tag = join([w, t])
    if word_and_tag in e_dict.keys():
        return e_dict[word_and_tag]
    return 0


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


def my_counter(data):
    wordsCount = {}
    words = []  # list of words
    for word in data:
        if word[0] not in wordsCount:
            wordsCount[word[0]] = [0, ""]
        wordsCount[word[0]][0] += 1   
        wordsCount[word[0]][1] = word[1]
    return wordsCount


def train_unknown(data):
    """ data is dict of words and there tags -> there count """
    data1 = [[k.split()[0],k.split()[1]] for k in data]    
    data1 = my_counter(data1)
    data1 = [[k, data1[k][1]] for k in data1 if data1[k][0] is 1] #now data1 is list of words which appear only once and there tag [word, tag]
    dict_to_e = {} # dictionary of unknowns to add to e.mle
    for word, tag in data1:
        current_str = "unk"
        if (word[0].isupper()):
            current_str = "Unk"
        if (word[-3:] is "ing"):    
            current_str = current_str + "ing"
        elif (word[-2:] == 'ly'):
            current_str = current_str + "ly"
        elif (word[-4:] == 'tial'):
            current_str = current_str + "tial"  
        elif (word[-2:] == 'al'):
            current_str = current_str + "al"
        elif (word[-4:] == 'tion'):
            current_str = current_str + "tion"  
        elif (word[-4:] == 'ed'):
            current_str = current_str + "ed"  
        #maybe should add some more ifs..
        try:
            word = float(word)
            current_str =  'unk-num'
        except ValueError:
            pass  # it was a string, not an float

        current_str = current_str + " " + tag
        if current_str not in dict_to_e:
            dict_to_e[current_str] = 0
        dict_to_e[current_str] += 1
   # print (dict_to_e)
    return dict_to_e
    #return {**data, **dict_to_e}


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
    """
    print (tags)
    print (data)
    exit()
    """

    unknown_dict = train_unknown(data)
    create_possible_tags(tags)
    pairs, triplets, singles = counting_quantities(tags)
    write_quantities(pairs, triplets, singles, q_mle)
    write_estimations(Counter(data), Counter(tags), e_mle)
    


