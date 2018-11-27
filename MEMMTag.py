import math
import sys
import operator
import liblin as lbln
import MEMMutils as utils
from MEMMutils import START_SYMBOL, join


def read_input():
    with open(input_file_name, "r") as file:
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


def get_tags_for_first_word(i, sentence, w, u):
    max_list = []
    context = utils.get_sentence_context(i, sentence, w, u)
    feature_indexes = utils.create_feature_vec(context, feature_map)
    tags_with_prob = llp.predict(feature_indexes)
    for tag, prob in tags_with_prob.items():
        max_tag = inv_tag_map[int(tag)]
        max_list = max_add(prob, max_tag, max_list)
    return max_list
    """
    r, score = utils.argmax(tags_with_prob)
    max_tag = inv_tag_map[int(r)]
    max_list = max_add(score, max_tag, max_list)"""


def viterbi(words):
    pi = {}
    default = [0.0, '']
    pi[(0, START_SYMBOL, START_SYMBOL)] = [0, ""]
    prev_prev_tags = [START_SYMBOL]
    prev_tags = [START_SYMBOL]
    n = len(words)
    tags = [tag for tag in tag_map.keys()]

    for k in range(1, n + 1):
        possible_tags_for_word = pruning_dict.get(words[k - 1], tags)
        for v in possible_tags_for_word:
            for u in prev_tags:
                max_score = 0.0
                max_tag = ""
                for w in prev_prev_tags:
                    context = utils.get_sentence_context(k - 1, words, w, u)
                    feature_indexes = utils.create_feature_vec(context, feature_map)
                    tags_with_prob = llp.predict(feature_indexes)
                    r, score = utils.argmax(tags_with_prob)
                    score = (score + pi.get((k - 1, w, u), default)[0]) / 2
                    if score > max_score:
                        max_score = score
                        max_tag = w
                pi[(k, u, v)] = [max_score, max_tag]
        prev_prev_tags = prev_tags
        prev_tags = possible_tags_for_word
    return pi


def get_max_from_list(max_list):
    max_item = max(max_list, key=operator.itemgetter(0))
    return max_item[0], max_item[1]


def max_add(score, tag, max_list):
    for item in max_list:
        if tag == item[1] and score <= item[0]:
            return max_list
    max_list.append((score, tag))
    temp_list = sorted(max_list, key=lambda tup: tup[0])
    return temp_list[:8]


def backtrack_viterbi_output(pi, n):
    default = [0.0, '']
    max_score = 0.0
    u_max, v_max = "", ""
    tags = [tag for tag in tag_map.keys()]
    for u in tags:
        for v in tags:
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


def write_predictions(preds):
    with open(out_file_name, "w") as file:
        for line_and_pred in preds:
            line = line_and_pred[0]
            pred = line_and_pred[1]
            output = [word + "/" + tag for word, tag in zip(line.split(), pred)]
            file.write(" ".join(output) + "\n")


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
    with open("data/ass1-tagger-test", "r") as file:
        epoch_counter = all_good = all_bad = 0.0
        for line in file:
            epoch_counter += 1
            num_good, num_bad = viterbi_with_tag(epoch_counter, line)
            all_good += num_good
            all_bad += num_bad
        print("Total Accuracy: " + str(100 * (all_good / (all_good + all_bad))) + "%\n")


if __name__ == '__main__':
    script_name, input_file_name, modelname, feature_map_file, out_file_name = sys.argv
    llp = lbln.LiblinearLogregPredictor(modelname)
    tag_map, feature_map, pruning_dict = utils.get_tags_and_features_maps(feature_map_file)
    inv_tag_map = {v: k for k, v in tag_map.items()}
    check_test()
    """all_preds = read_input()
    write_predictions(all_preds)"""

