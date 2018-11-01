import sys
import MLETrain as mle


def read_input(f_name):
    with open(f_name, "r") as file:
        return [greedy_train(words) for line in file for words in line.split()]


def greedy_train(sentence):
    tags = mle.get_possible_tags()
    for t1, t2, t3 in mle.combinations(tags, 3):
        max_tag = 0
        for word in sentence:
            # MISSING START TAG!!!
            e = mle.get_e(word, t3, e_mle)
            q = mle.get_q(t1, t2, t3, q_mle)
            if e * q >= max_tag: # might need to make in minimum log
                max_tag = e * q



if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv

