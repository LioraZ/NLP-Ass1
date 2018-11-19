import math
import sys
import operator
import liblin as lbln
import MEMMutils as utils
from MEMMutils import START_SYMBOL, join
T = 8


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


def viterbi(words):
    pi = {}
    default = [0.0, '']
    pi[(0, START_SYMBOL, START_SYMBOL)] = default
    prev_prev_tags = [START_SYMBOL]
    prev_tags = [START_SYMBOL]
    #max_r = [0.0]
    #max_tag = ""
    max_list = [(0, tag) for tag in tag_map.keys()]
    n = len(words)
    #possible_tags_for_word = [tag for tag in tag_map.keys()]
    for k in range(1, n + 1):
        possible_tags_for_word = [tag for score, tag in max_list]
        max_list = []
        for v in possible_tags_for_word:
            for u in prev_tags:
                for w in prev_prev_tags:
                    context = utils.get_sentence_context(k - 1, words, w, u)
                    feature_indexes = utils.create_feature_vec(context, feature_map)
                    tags_with_prob = llp.predict(feature_indexes)
                    r, score = utils.argmax(tags_with_prob)
                    score += pi.get((k - 1, w, u), default)[0]
                    max_tag = inv_tag_map[int(r)]
                    max_list = max_add(score, max_tag, max_list)
                max_score, max_tag = get_max_from_list(max_list)
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
    return temp_list[:T]


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
    script_name, input_file_name, modelname, feature_map_file, out_file_name = sys.argv
    llp = lbln.LiblinearLogregPredictor(modelname)
    tag_map, feature_map = utils.get_tags_and_features_maps(feature_map_file)
   # tag_probs, pruned_tags_pairs, pruned_words = get_pruning_dicts()
    inv_tag_map = {v: k for k, v in tag_map.items()}
    check_test()
    """llp = lbln.LiblinearLogregPredictor(modelname)
    tag_map, feature_map = get_tags_and_features_maps()
    inv_tag_map = {v: k for k, v in tag_map.items()}
    check_test()
    tag_probs, pruned_tags_pairs, pruned_words = get_pruning_dicts()
    utils.create_possible_tags(tag_probs, TAG_FILE)
    tags = utils.get_possible_tags(TAG_FILE)
    lambda_values = get_lambda_values()
    #check_test()
    all_preds = read_input()
    write_predictions(all_preds)"""

