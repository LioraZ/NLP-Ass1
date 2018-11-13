import sys
import MLETrain as mle
from MLETrain import join, START_SYMBOL



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
    viterbi(words, size - 1, tags_dict)
    return tags_dict



def viterbi(words, i, tags_dict):
    if i == 0:
        return tags_dict[join([str(i), START_SYMBOL, START_SYMBOL])]
    for t in tags:
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
            tags_dict[join([str(i), t, r])] = [best_tag, max_score]



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


if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv
    e_dict = mle.get_e_dict(e_mle)
    q_dict = mle.get_q_dict(q_mle)
    tags = mle.get_possible_tags()
    lambda_values = get_lambda_values()
    check_test()
    """all_preds = read_input(f_input)
    write_predictions(f_output, all_preds)"""

