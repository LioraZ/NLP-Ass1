import sys
import MLETrain as mle
import math
from MLETrain import START_SYMBOL


def read_input(f_name):
    with open(f_name, "r") as file:
        return [[line, greedy_train(line)] for line in file]


def get_lambda_values():
    lambda_values = []
    with open(f_extra, "r") as file:
        for line in file:
            lambda_values = [float(lambda_val) for lambda_val in line.split(",")]
    return lambda_values


def greedy_train(sentence):
    tags = mle.get_possible_tags()
    lambda_values = get_lambda_values()
    preds = [START_SYMBOL, START_SYMBOL]

    for word in sentence.split():
        max_known = {'score': 0, 'tag': ""}
        max_unknown = {'score': 0, 'tag': ""}

        for tag in tags:
            e = mle.get_e(word, tag, e_dict)
            q = mle.get_q(preds[-2], preds[-1], tag, lambda_values, q_dict)

            # till we do interpolation and assign non zero values
            """if q is not 0:
                q = - math.log(q)
            if e is not 0:
                e = - math.log(e)"""
            max_known = update_max(e * q, tag, max_known)
            if e == 0:
                temp_score = q * mle.get_unknown_e(word, tag, e_dict)
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
    data = mle.join(data)
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


def write_predictions(f_output, preds):
    with open(f_output, "w") as file:
        for line_and_pred in preds:
            line = line_and_pred[0]
            pred = line_and_pred[1]
            output = [word + "/" + tag for word, tag in zip(line.split(), pred)]
            file.write(" ".join(output) + "\n")



def check_test():
    with open("data/ass1-tagger-test", "r") as file:
        epoch_counter = all_good = all_bad = 0.0
        for line in file:
            epoch_counter += 1
            num_good, num_bad = greedy_train_with_tag(epoch_counter, line)
            all_good += num_good
            all_bad += num_bad
        print("Total Accuracy: " + str(100 * (all_good / (all_good + all_bad))) + "%\n")


if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv
    e_dict = mle.get_e_dict(e_mle)
    q_dict = mle.get_q_dict(q_mle)

    words_with_no_tag = []
    check_test()
    with open("unk-words.txt", "w") as file:
        for word in words_with_no_tag:
            file.write(word + "\n")

    #all_preds = read_input(f_input)
    #write_predictions(f_output, all_preds)


