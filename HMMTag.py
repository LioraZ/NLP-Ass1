import sys
import MLETrain as mle


def read_input(f_name):
    with open(f_name, "r") as file:
        return [[line, viterbi_alg(line)] for line in file]
        #return [greedy_train(words) for line in file for words in line.split()]


def viterbi_alg(sentence):
    tags = mle.get_possible_tags()
    preds = ["", ""]
    e_dict = mle.get_e_dict(e_mle)
    q_dict = mle.get_q_dict(q_mle)
    v = [{("s","s") : 1}]
    bp = []
    for word,i in zip(sentence.split(), range(len(sentence.split()))):
        min_score = 0
        best_tag = ""
        max_probs = dict()
        max_tag = dict()
        for t,m in v[i]: #tags:
            for r in tags:
                """
                for t_tag in tags:
                    e = mle.get_e(word, r, e_dict)
                    q = mle.get_q(t_tag, t, r, q_dict)
                 """             
#                for t_tag in tags:
#                    if (v[i][t_tag][t] * mle.get_q(t_tag, t,r) * mle.get_e(word, r, e_dict) > )
                node = max_on_tags_list([[v[i][(t_tag[0], t)] * mle.get_q(t_tag, t, r, q_dict) * mle.get_e(word, r, e_dict), t_tag] for t_tag in v[i]])
                max_probs[(t, r)] = node[0]
                max_tag[(t, r)] = node[1]
        v.append(maxProb)   
        bp.append(max_tag)
    print (v)                     

#ls is in this format: [[val0, tag0], [val1, tag1] ... ]
def max_on_tags_list(ls):
    curr_max = ls[0][0]
    max_node = ls[0]
    for i in ls:
        if (i[0] > curr_max):
            curr_max = i[0]
            max_node = i
    return max_node

def write_predictions(f_output, preds):
    with open(f_output, "w") as file:
        for line_and_pred in preds:
            line = line_and_pred[0]
            pred = line_and_pred[1]
            output = [word + "/" + tag for word, tag in zip(line.split(), pred)]
            file.write(" ".join(output) + "\n")





if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv
    # all_preds = read_input(f_input)
    # write_predictions(f_output, all_preds)
    #with open(e_mle, encoding="utf8") as file:
    #    input_data = [word for line in file for word in line.split()]
    print(mle.get_possible_tags())
    all_preds = read_input(f_input)
    write_predictions(f_output, all_preds)

