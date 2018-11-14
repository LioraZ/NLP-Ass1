import sys
import MLETrain as mle
import math
from MLETrain import join, START_SYMBOL, STOP_SYMBOL

LOG_PROB_OF_ZERO = -1000

def read_input(f_name):
    with open(f_name, "r") as file:
        t = tags[0]
        r = tags[1]
        return [[line, train_viterbi(line)] for line in file]
        #return [greedy_train(words) for line in file for words in line.split()]


def train_viterbi(sentence):
    words = sentence.split()
    size = len(words)
    t = tags[0]
    r = tags[1]
    tags_dict = {}
    tags_dict[join([str(0), START_SYMBOL, START_SYMBOL])] = 1
    preds = viterbi(words, 0, tags_dict)
    return preds


def update_max(score, tag, max):
    if score > max["score"]:
        max["score"] = score
        max["tag"] = tag
    return max


def viterbi(words, i, tags_dict):
    preds = []
    t_and_r_tags =[]
    """if i == 0:
        return tags_dict[join([str(i), START_SYMBOL, START_SYMBOL])]"""
    while i < len(words):
        for pair in pruned_tags:
            t, r = pair.split()
            max_known = {'score': float('-Inf'), 'tag': ""}
            max_unknown = {'score': float('-Inf'), 'tag': ""}
            e = mle.get_e(words[i], r, e_dict)
            max_q = {'score': 0.0, 'tag': ""}
            prev_viterbi = 1
            if i == 0:
                t = START_SYMBOL
                q = mle.get_q(START_SYMBOL, t, r, lambda_values, q_dict)
                max_q = update_max(q, START_SYMBOL, max_q)
            elif i == 1:
                q = mle.get_q(START_SYMBOL, t, r, lambda_values, q_dict)
                max_q = update_max(q, START_SYMBOL, max_q)
                prev_viterbi = tags_dict.get(join([str(i - 1), max_q["tag"], t]), [0])[0]
            else:
                for t_tag in pruned_tags[pair]:
                    q = mle.get_q(t_tag, t, r, lambda_values, q_dict)
                    max_q = update_max(q, t_tag, max_q)
                prev_viterbi = tags_dict.get(join([str(i - 1), max_q["tag"], t]), [0])[0]

                """if q > max_q:
                    q = max_q"""
            """if e != 0:
                score = e * q * prev_viterbi
                max_known = update_max(score, t_tag, max_known)
            else:
                score = mle.get_unknown_e(words[i], r, e_dict) * q * prev_viterbi
                max_unknown = update_max(score, t_tag, max_unknown)"""
                #prev_viterbi = tags_dict.get(join([str(i - 1), max_q["tag"], t]), [0])[0]
            if e == 0:
                e = mle.get_unknown_e(words[i], r, e_dict)
            """if e != 0:
                print(e)"""
            tags_dict[join([str(i), t, r])] = [prev_viterbi * max_q["score"] * e, max_q["tag"]]
        i += 1

        """if max_known["score"] != 0:
            tags_dict[join([str(i), t, r])] = [max_known["score"], max_known["tag"]]
        else:
            tags_dict[join([str(i), t, r])] = [max_unknown["score"], max_unknown["tag"]]

        t_and_r_tags.append(more_viterbi(tags_dict, len(words)))"""
        #preds.append(tags_dict[join([str(i - 1), t_tag, r_tag])]["tag"])
        #preds.append(t_tag)
        #preds.append(r_tag)
    size = len(words) - 1
    max_score = {'score': 0.0, 'tag': ""}
    LAST_SYMBOL = "."
   # last_tags = [[v, k.split()[0]] for k, value in tags_dict.items() if k.split()[1] == LAST_SYMBOL for v in value]
    """for t_tag, t in inv_pruned_tags[LAST_SYMBOL]:
        q = mle.get_q(t_tag, t, LAST_SYMBOL, lambda_values, q_dict)
        score = tags_dict[join([str(size), t_tag, t])] * q
        max_q = update_max(score, t, max_score)
     preds.append(max_score["tag"])"""
    for k in range(size, 0, -1):
        for t, r in inv_pruned_tags[LAST_SYMBOL]:
            #t_tag, t = item[0], item[1]
            #q = mle.get_q(t_tag, t, LAST_SYMBOL, lambda_values, q_dict)
            entry = tags_dict[join([str(k), r, LAST_SYMBOL])]
            max_score = update_max(entry[0], entry[1], max_score)
        """if i == size:
            preds.append(max_score["tag"][1])"""
        preds.append(max_score["tag"][0])
        LAST_SYMBOL = preds[-1]
    return reversed(preds)

    """ counter = len(words) - 1
    for t_tag, r_tag in t_and_r_tags:
        temp = tags_dict[join([str(counter), t_tag, r_tag])][1]
        preds.append(tags_dict[join([str(counter), t_tag, r_tag])][1])
        counter -= 1
    for k in range(len(words) - 1, 0, -1):
        preds.append(tags_dict[join([str(k), t_tag, r_tag])]["tag"])"""



def more_viterbi(tags_dict, size):
    t_max, r_max = "", ""
    #max_score = float('-Inf')
    max_known = {'score': float('-Inf'), 'tag': [t_max, r_max]}

    for pair in pruned_tags:
        t, r = pair.split()
        #max_unknown = {'score': float('-Inf'), 'tag': ""}
        q = mle.get_q(t, r, STOP_SYMBOL, lambda_values, q_dict)
        """if q == 0:
            q = LOG_PROB_OF_ZERO"""
        score = tags_dict.get(join([str(size - 1), t, r]), [0])[0] + q
        max_known = update_max(score, [t, r], max_known)
    return max_known["tag"]
    #preds.append()


    """for u in S(n - 1):
        for v in S(n):
            score = pi.get((n, u, v), LOG_PROB_OF_ZERO) + \
                    q_values.get((u, v, STOP_SYMBOL), LOG_PROB_OF_ZERO)
            if score > max_score:
                max_score = score
                u_max = u
                v_max = v

    tags = deque()
    tags.append(v_max)
    tags.append(u_max)"""


def log(num):
    try:
        return math.log(num)
    except ValueError:
        return LOG_PROB_OF_ZERO
        pass
    """if num == 0 or num == float('-Inf'):
        return LOG_PROB_OF_ZERO
    return math.log(num)"""


    """for t in tags:
        for r in tags:
            best_tag = ""
            max_score = 0
            for t_tag in tags:
                q = mle.get_q(t_tag, t, r, lambda_values, q_dict)
                e = mle.get_e(words[i], r, e_dict)
                if join([str(i - 1), t, r]) not in tags_dict:
                    viterbi(words, i - 1, tags_dict)
                curr_score = tags_dict.get(join([str(i - 1), t, r])) * q * e
                if curr_score > max_score:
                    max_score = curr_score
                    best_tag = t_tag
            tags_dict[join([str(i), t, r])] = [best_tag, max_score]"""


def write_predictions(f_output, preds):
    with open(f_output, "w") as file:
        for line_and_pred in preds:
            line = line_and_pred[0]
            pred = line_and_pred[1]
            output = [word + "/" + tag for word, tag in zip(line.split(), pred)]
            file.write(" ".join(output) + "\n")


def get_lambda_values():
    lambda_values = []
    with open(f_extra, "r") as file:
        for line in file:
            lambda_values = [float(lambda_val) for lambda_val in line.split(",")]
    return lambda_values


def viterbi_with_tag(num_epoch, sentence):
    if int(num_epoch) == 1:
        print("yay")
    print("Epoch: " + str(num_epoch) + "\n")
    tags = []
    data = []
    for word in sentence.split():
        items = word.split('/')
        tags.append(items[-1])
        data.append("/".join(items[:-1]))
    data = mle.join(data)
    preds = train_viterbi(data)
    good = bad = 0.0
    print("\t".join(tags) + "\n")
    print("\t".join(preds) + "\n")
    for tag, pred in zip(tags, preds):
        if tag == pred:
            good += 1
        else:
            bad += 1
    print("Accuracy: " + str((good / (good + bad)) * 100) + "%" + "\n\n")


def check_test():
    with open("data/ass1-tagger-test", "r") as file:
        epoch_counter = 0.0
        for line in file:
            epoch_counter = epoch_counter + 1
            viterbi_with_tag(epoch_counter, line)


def get_pairs_of_possible_q():
    triplets = [key for key in q_dict.keys() if len(key.split()) == 3]
    new_dict = {}
    for item in triplets:
        key = join(item.split()[1:])
        if key in new_dict.keys():
            new_dict[key].append(item.split()[0])
        else:
            new_dict[key] = [item.split()[0]]
    last_tags = {}
    for item in triplets:
        key, v1, v2 = item.split()
        if key in last_tags.keys():
            last_tags[key].append([v1, v2])
        else:
            last_tags[key] = []
            last_tags[key].append([v1, v2])
    #last_tags = {k.split()[1]: join([v, k.split()[0]]) for k, value in new_dict.items() for v in value}
    return new_dict, last_tags
    #return {join(item.split()[1:]): [item.split()[0]] for item in triplets}


if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv
    e_dict = mle.get_e_dict(e_mle)
    q_dict = mle.get_q_dict(q_mle)
    pruned_tags, inv_pruned_tags = get_pairs_of_possible_q()
    tags = mle.get_possible_tags()
    lambda_values = get_lambda_values()
    check_test()
    """all_preds = read_input(f_input)
    write_predictions(f_output, all_preds)"""

