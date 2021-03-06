import math
import sys

import hmm2.HMMutils as utils
from hmm2.HMMutils import START_SYMBOL, join


TAG_FILE = "possible_tags_greedy"


def read_input():
    with open(f_input, "r") as file:
        return [[line, greedy_train(line)] for line in file]


def get_lambda_values():
    lambda_values = []
    with open(f_extra, "r") as file:
        for line in file:
            lambda_values = [float(lambda_val) for lambda_val in line.split(",")]
    return lambda_values


def greedy_train(sentence):
    tags = utils.get_possible_tags(TAG_FILE)
    lambda_values = get_lambda_values()
    preds = [START_SYMBOL, START_SYMBOL]

    for word in sentence.split():
        max_known = {'score': 0.0, 'tag': ""}
        max_unknown = {'score': 0.0, 'tag': ""}

        for tag in tags:
            e = utils.get_e(word, tag, e_dict)
            q = utils.get_q(preds[-2], preds[-1], tag, lambda_values, q_dict)

            max_known = update_max(e * q, tag, max_known)
            if e == 0:
                temp_score = q * utils.get_unknown_e(word, tag, e_dict)
                max_unknown = update_max(temp_score, tag, max_unknown)
        if max_known['score'] == 0:
            preds.append(max_unknown["tag"])
        else:
            preds.append(max_known["tag"])
        if preds[-1] == "":
            preds.append(tags[0])
    return preds[2::]


def greedy_log(sentence):
    LOG_PROB_OF_ZERO = -100

    def log(num):
        try:
            return math.log(num)
        except ValueError:
            return LOG_PROB_OF_ZERO

    tags = utils.get_possible_tags()
    lambda_values = get_lambda_values()
    preds = [START_SYMBOL, START_SYMBOL]

    for word in sentence.split():
        max_known = {'score': float("-Inf"), 'tag': ""}
        max_unknown = {'score': float("-Inf"), 'tag': ""}

        for tag in tags:
            e = mle.get_e(word, tag, e_dict)
            q = mle.get_q(preds[-2], preds[-1], tag, lambda_values, q_dict)

            max_known = update_max(log(e) + log(q), tag, max_known)
            if e == 0:
                temp_score = log(q) + log(mle.get_unknown_e(word, tag, e_dict))
                max_unknown = update_max(temp_score, tag, max_unknown)
        if max_known['score'] == 0:
            preds.append(max_unknown["tag"])
        else:
            preds.append(max_known["tag"])
        if preds[-1] == "":
            words_with_no_tag.append(word)
    return preds[2::]


def update_max(score, tag, max):
    if score > max["score"]:
        max["score"] = score
        max["tag"] = tag
    return max


def greedy_train_with_tag(num_epoch, sentence):
    print("Epoch: " + str(num_epoch) + "\n")
    tags = []
    data = []
    for word in sentence.split():
        items = word.split('/')
        tags.append(items[-1])
        data.append("/".join(items[:-1]))
    data = join(data)
    preds = greedy_train(data)
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


def write_predictions(preds):
    with open(f_output, "w") as file:
        for line_and_pred in preds:
            line = line_and_pred[0]
            pred = line_and_pred[1]
            output = [word + "/" + tag for word, tag in zip(line.split(), pred)]
            file.write(" ".join(output) + "\n")


def check_test():
    with open("../data/ass1-tagger-test", "r") as file:
        epoch_counter = all_good = all_bad = 0.0
        for line in file:
            epoch_counter += 1
            num_good, num_bad = greedy_train_with_tag(epoch_counter, line)
            all_good += num_good
            all_bad += num_bad
        print("Total Accuracy: " + str(100 * (all_good / (all_good + all_bad))) + "%\n")


if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv
    e_dict = utils.get_e_dict(e_mle)
    q_dict = utils.get_q_dict(q_mle)

    tag_probs = {k: v for k, v in q_dict.items() if len(k.split()) == 1}
    utils.create_possible_tags(tag_probs, TAG_FILE)
    #tags = utils.get_possible_tags(TAG_FILE)

    check_test()

    #all_preds = read_input(f_input)
    #write_predictions(f_output, all_preds)


