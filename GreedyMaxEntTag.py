from collections import Counter
import liblin as lbln
import MLETrain as mle
import math
#from MLETrain import START_SYMBOL
from itertools import islice
import sys


START_SYMBOL = '*'

def read_input(f_name):
    with open(f_name, "r") as file:
        return [[line, greedy_train(line)] for line in file]

def update_max(score, tag, max):
    if score > max["score"]:
        max["score"] = score
        max["tag"] = tag
    return max

def greedy_train(sentence):
    tags = mle.get_possible_tags()
    #lambda_values = get_lambda_values()
    preds = [START_SYMBOL, START_SYMBOL]

    print (sentence)
    exit()
    for word in sentence.split():
        max_known = {'score': 0, 'tag': ""}
        max_unknown = {'score': 0, 'tag': ""}

        for tag in tags:
            #e = mle.get_e(word, tag, e_dict)
            #q = mle.get_q(preds[-2], preds[-1], tag, lambda_values, q_dict)

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

def get_sentence_context(i, sentence, pt, ppt):
    dc = { 'word': sentence[i][0],
 'previous_word': sentence[i - 1][0] if i > 0 else 'start',
 'pre_previous_word': sentence[i - 2][0] if i > 1 else 'start',
 'next_word': sentence[i + 1][0] if i < len(sentence) - 1 else 'end',
 'next_next_word': sentence[i + 2][0] if i < len(sentence) - 2 else 'end',
 'tag': sentence[i][1],
 'previous_tag': pt
 'pre_previous_tag': ppt  }
    return dc

if __name__ == '__main__':

    script_name, input_file_name, modelname, feature_map_file, out_file_name = sys.argv
    llp = lbln.LiblinearLogregPredictor(modelname)
    read_input(input_file_name)
