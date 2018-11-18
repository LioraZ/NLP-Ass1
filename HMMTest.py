import sys
import MLETrain as mle
import math
from MLETrain import join, START_SYMBOL

LOG_PROB_OF_ZERO = -100
MIN_VALUE = float("-Inf")

def read_input(f_name):
    with open(f_name, "r") as file:
        return [[line, train_viterbi(line)] for line in file]


def train_viterbi(sentence):
    words = sentence.split()
    preds = new_viterbi(words)
    #tags_dict = viterbi(words, 1)
    #preds = extract_preds_from_dict(tags_dict, len(words))
    return preds


def update_max(score, tag, max):
    if score > max["score"]:
        max["score"] = score
        max["tag"] = tag
    return max


def get_tagset(i):
    if i == 1:
        return [join([START_SYMBOL, t]) for t in tags]
    return pruned_tags_pairs


def new_viterbi(words):
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
            possible_tags_for_word = pruned_words.get(mle.classify_unknown(word), tags)
        for v in possible_tags_for_word:
            for u in prev_tags:
                unknown_score = max_score = MIN_VALUE
                unknown_tag = max_tag = ""
                for w in prev_prev_tags:
                    prev_v = pi.get((k - 1, w, u), default)[0]
                    q = log(mle.get_q(w, u, v, lambda_values, q_dict))
                    e = mle.get_e(word, v, e_dict)
                    if e != 0:
                        score = (prev_v + q + 3 * log(e)) / 3
                        if score > max_score:
                            max_score = score
                            max_tag = w
                    elif mle.get_unknown_e(word, v, e_dict) != 0:
                        score = prev_v + q + 3 * log(mle.get_unknown_e(word, v, e_dict))
                        if score > unknown_score:
                            unknown_score = score / 3
                            unknown_tag = w
                if max_score == MIN_VALUE:
                    pi[(k, u, v)] = [unknown_score, unknown_tag]
                else:
                    pi[(k, u, v)] = [max_score, max_tag]
        prev_prev_tags = prev_tags
        prev_tags = possible_tags_for_word

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


def viterbi(words, i):
    tags_dict = {}
    tags_dict[join([str(0), START_SYMBOL, START_SYMBOL])] = 1
    while i <= len(words):
        for pair in pruned_tags:
            t, r = pair.split()
            e = mle.get_e(words[i - 1], r, e_dict)
            #max_q = {'score': float("-Inf"), 'tag': ""}
            max_q = {'score': 0.0, 'tag': ""}
            prev_viterbi = 1
            if i == 1:
                t = START_SYMBOL
                q = mle.get_q(START_SYMBOL, t, r, lambda_values, q_dict)
                max_q = update_max(q, START_SYMBOL, max_q)
            elif i == 0:
                q = mle.get_q(START_SYMBOL, t, r, lambda_values, q_dict)
                max_q = update_max(q, START_SYMBOL, max_q)
                #prev_viterbi = tags_dict.get(join([str(i - 1), max_q["tag"], t]), [0])[0]
            else:
                for t_tag in pruned_tags[pair]:
                    q = mle.get_q(t_tag, t, r, lambda_values, q_dict)
                    max_q = update_max(q, t_tag, max_q)
                prev_viterbi = tags_dict.get(join([str(i - 1), max_q["tag"], t]), [0])[0]
            if e == 0:
                e = mle.get_unknown_e(words[i - 1], r, e_dict)
            tags_dict[join([str(i), t, r])] = [prev_viterbi * max_q["score"] * e, max_q["tag"]]
            print("i= " + str(i), "e= " + str(e), "prev_viterbi= " + str(prev_viterbi),
                  "q= " + str(q) ,"Dict= " + str(tags_dict[join([str(i), t, r])]))
        i += 1
    return tags_dict


def extract_preds_from_dict(tags_dict, size):
    preds = []
    #max_score = float("-Inf")
    max_score = 0.0
    max_t = max_r = max_t_tag = ""
    for pair in pruned_tags:
        t, r = pair.split()
        score = tags_dict.get(join([str(size), t, r]))
        if score[0] > max_score:
            max_score = score[0]
            max_r = r
            max_t = t
            max_t_tag = score[1]
    preds.append(max_r)
    preds.append(max_t)
    # preds.append(max_t_tag)

    for k in range(size - 2, 0, -1):
        max_tag = tags_dict.get(join([str(k + 1), preds[-2], preds[-1]]), ["", ""])[1]
        preds.append(max_tag)
    preds = [item for item in reversed(preds)]
    return preds


def log(num):
    try:
        return math.log(num)
    except ValueError:
        return LOG_PROB_OF_ZERO


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


def get_pairs_of_possible_q():
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
        """if word[:-4] == "^unk" or word[:-4] == "^Unk":
            continue"""""
        """unk_word = mle.classify_unknown(word)
        if len(word)"""
        if word in word_to_tags:
            word_to_tags[word].append(tag)
        else:
            word_to_tags[word] = [tag]
    tag_dict = {}
    for pair in new_dict:
        u, v = pair.split()
        if v not in tag_dict:
            tag_dict[v] = {}
        tag_dict[v].update({u: new_dict[pair]})

    return new_dict, tag_dict, word_to_tags
    #return {join(item.split()[1:]): [item.split()[0]] for item in triplets}


if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv
    e_dict = mle.get_e_dict(e_mle)
    q_dict = mle.get_q_dict(q_mle)
    pruned_tags_pairs, pruned_tags_dict, pruned_words = get_pairs_of_possible_q()
    tags = mle.get_possible_tags()
    lambda_values = get_lambda_values()
    check_test()
    """all_preds = read_input(f_input)
    write_predictions(f_output, all_preds)"""

