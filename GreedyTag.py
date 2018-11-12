import sys
import MLETrain as mle
import math
#from MLETrain import join


def read_input(f_name):
    with open(f_name, "r") as file:
        return [[line, greedy_train(line)] for line in file]
        #return [greedy_train(words) for line in file for words in line.split()]


def get_lambda_values():
    lambda_values = []
    with open(f_extra, "r") as file:
        for line in file:
            lambda_values = [float(lambda_val) for lambda_val in line.split(",")]
    return lambda_values


def greedy_train(sentence):
    tags = mle.get_possible_tags()
    lambda_values = get_lambda_values()
    preds = [None, None]

    for word in sentence.split():
        max_score = 0
        best_tag = ""
        best_unknown_score = 0
        best_unknown_tag = ""
        #best_tag = {"", 0}
        for tag in tags:
            e = mle.get_e(word, tag, e_dict)
            q = mle.get_q(preds[-2], preds[-1], tag, lambda_values, q_dict)
            #best_tag =
            # till we do interpolation and assign non zero values
            """if q is not 0:
                q = - math.log(q)
            if e is not 0:
                e = - math.log(e)"""
            if e * q > max_score:
                max_score = e * q
                best_tag = tag
            if e == 0:
                temp_score = q * mle.get_unknown_e(word, tag, e_dict)
                if temp_score > best_unknown_score:
                    best_unknown_score = temp_score
                    best_unknown_tag = tag
        if max_score == 0:
            best_tag = best_unknown_tag
        preds.append(best_tag)
    return preds[2::]


def greedy_train_with_tag(num_epoch, sentence):
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



def write_predictions(f_output, preds):
    with open(f_output, "w") as file:
        for line_and_pred in preds:
            line = line_and_pred[0]
            pred = line_and_pred[1]
            output = [word + "/" + tag for word, tag in zip(line.split(), pred)]
            file.write(" ".join(output) + "\n")



def check_test():
    with open("data/ass1-tagger-test", "r") as file:
        epoch_counter = 0.0
        for line in file:
            epoch_counter = epoch_counter + 1
            greedy_train_with_tag(epoch_counter, line)


if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv
    e_dict = mle.get_e_dict(e_mle)
    q_dict = mle.get_q_dict(q_mle)
    check_test()
    #all_preds = read_input(f_input)
    #write_predictions(f_output, all_preds)


