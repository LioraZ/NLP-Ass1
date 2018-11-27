import math
import sys
import hmm2.HMMutils as utils
from hmm2.HMMutils import START_SYMBOL, join

LOG_PROB_OF_ZERO = -100
MIN_VALUE = float("-Inf")
TAG_FILE = "possible_tags"


def read_input():
    with open(f_input, "r") as file:
        return [[line, get_viterbi_output(line)] for line in file]


def get_viterbi_output(sentence):
    words = sentence.split()
    pi = viterbi(words)
    preds = backtrack_viterbi_output(pi, len(words))
    return preds


def update_max(score, tag, max):
    if score > max["score"]:
        max["score"] = score
        max["tag"] = tag
    return max


def viterbi(words):
    pi = {}
    default = [0.0, '']
    pi[(0, START_SYMBOL, START_SYMBOL)] = default
    prev_prev_tags = [START_SYMBOL]
    prev_tags = [START_SYMBOL]
    n = len(words)
    for k in range(1, n + 1):
        word = words[k - 1]
        possible_tags_for_word = pruned_words.get(word, None)
        if possible_tags_for_word == None:
            possible_tags_for_word = pruned_words.get(utils.classify_unknown(word), tags)
        for v in possible_tags_for_word:
            for u in prev_tags:
                unknown_score = max_score = MIN_VALUE
                unknown_tag = max_tag = ""
                for w in prev_prev_tags:
                    prev_v = pi.get((k - 1, w, u), default)[0]
                    q = log(utils.get_q(w, u, v, lambda_values, q_dict))
                    e = utils.get_e(word, v, e_dict)
                    if e != 0:
                        score = (prev_v + q + 3 * log(e)) / 3
                        if score > max_score:
                            max_score = score
                            max_tag = w
                    elif utils.get_unknown_e(word, v, e_dict) != 0:
                        score = (prev_v + q + 3 * log(utils.get_unknown_e(word, v, e_dict))) / 3
                        if score > unknown_score:
                            unknown_score = score
                            unknown_tag = w
                if max_score == MIN_VALUE:
                    pi[(k, u, v)] = [unknown_score, unknown_tag]
                else:
                    pi[(k, u, v)] = [max_score, max_tag]
        prev_prev_tags = prev_tags
        prev_tags = possible_tags_for_word
    return pi


def backtrack_viterbi_output(pi, n):
    default = [0.0, '']
    max_score = MIN_VALUE
    u_max, v_max = "", ""
    for pair in pruned_tags_pairs:
        u, v = pair.split()
        if (n, u, v) not in pi:
            continue
        score = pi.get((n, u, v), default)[0]
        if score > max_score:
            max_score = score
            u_max = u
            v_max = v

    tagset = []
    tagset.append(v_max)
    tagset.append(u_max)

    for i, k in enumerate(range(n - 2, 0, -1)):
        tagset.append(pi[(k + 2, tagset[i + 1], tagset[i])][1])
    tagset.reverse()
    tagged = tagset
    return tagged


def log(num):
    try:
        return math.log(num)
    except ValueError:
        return LOG_PROB_OF_ZERO


def write_predictions(preds):
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
    print("Epoch: " + str(num_epoch) + "\n")
    tags = []
    data = []
    for word in sentence.split():
        items = word.split('/')
        tags.append(items[-1])
        data.append("/".join(items[:-1]))
    data = join(data)
    preds = get_viterbi_output(data)
    good = bad = 0.0
    print("\t".join(tags) + "\n")
    print("\t".join(preds) + "\n")
    for tag, pred in zip(tags, preds):
        if tag == pred:
            good += 1
        else:
            bad += 1
    print("Accuracy: " + str((good / (good + bad)) * 100) + "%" + "\n\n")
    return good, bad


def check_test():
    with open("../data/ass1-tagger-test", "r") as file:
        epoch_counter = all_good = all_bad = 0.0
        for line in file:
            epoch_counter += 1
            num_good, num_bad = viterbi_with_tag(epoch_counter, line)
            all_good += num_good
            all_bad += num_bad
        print("Total Accuracy: " + str(100 * (all_good / (all_good + all_bad))) + "%\n")


def get_pruning_dicts():
    tags = {k: v for k, v in q_dict.items() if len(k.split()) == 1}
    triplets = [key for key in q_dict.keys() if len(key.split()) == 3]
    new_dict = {}
    for item in triplets:
        key = join(item.split()[1:])
        if key in new_dict.keys():
            new_dict[key].append(item.split()[0])
        else:
            new_dict[key] = [item.split()[0]]
    word_to_tags = {}
    for item in e_dict:
        word, tag = item.split()
        if word in word_to_tags:
            word_to_tags[word].append(tag)
        else:
            word_to_tags[word] = [tag]

    return tags, new_dict, word_to_tags


if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv
    e_dict = utils.get_e_dict(e_mle)
    q_dict = utils.get_q_dict(q_mle)
    tag_probs, pruned_tags_pairs, pruned_words = get_pruning_dicts()
    utils.create_possible_tags(tag_probs, TAG_FILE)
    tags = utils.get_possible_tags(TAG_FILE)
    lambda_values = get_lambda_values()
    #check_test()
    all_preds = read_input()
    write_predictions(all_preds)

