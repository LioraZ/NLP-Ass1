import sys
import MLETrain as mle


def read_input(f_name):
    with open(f_name, "r") as file:
        return [greedy_train(words) for line in file for words in line.split()]


def greedy_train(sentence):
    tags = mle.get_possible_tags()
    # MISSING START TAG!!!




if __name__ == '__main__':
    script_name, f_input, q_mle, e_mle, f_output, f_extra = sys.argv

