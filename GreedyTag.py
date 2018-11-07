import sys
import MLETrain as mle
#from MLETrain import join


def read_input(f_name):
    with open(f_name, "r") as file:
        return [[line, greedy_train(line)] for line in file]
        #return [greedy_train(words) for line in file for words in line.split()]


def greedy_train(sentence):
    tags = mle.get_possible_tags()
    preds = ["", ""]
    e_dict = mle.get_e_dict(e_mle)
    for word in sentence.split():
        max_score = 0
        best_tag = ""
        #best_tag = {"", 0}
        for tag in tags:
            e = mle.get_e(word, tag, e_mle)
            q = mle.get_q(preds[-2], preds[-1], tag, q_mle)
            #best_tag =
            if q * e >= max_score:
                best_tag = tag
        preds.append(best_tag)
    return preds


def write_predictions(f_output, preds):
    with open(f_output, "w") as file:
        for line_and_pred in preds:
            line = line_and_pred[0]
            pred = line_and_pred[1]
            output = [word + "/" + tag for word, tag in zip(line.split(), pred)]
            file.write(" ".join(output) + "\n")


if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv
    all_preds = read_input(f_input)
    write_predictions(f_output, all_preds)


