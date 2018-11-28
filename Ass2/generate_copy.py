from collections import defaultdict
import random
import sys


class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._sums = defaultdict(float)

    def add_rule(self, lhs, rhs, weight):
        assert (isinstance(lhs, str))
        assert (isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w, l, r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l, r, w)
        return grammar

    def is_terminal(self, symbol):
        return symbol not in self._rules

    def gen(self, symbol):
        if self.is_terminal(symbol):
            #print(symbol + "\t")
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            # print expansion
            #print(symbol + "\t" + " ".join(expansion))
            return " ".join(self.gen(s) for s in expansion)

    def random_sent(self):
        return self.gen("ROOT")

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r, w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r


def gen_grammar_2():
    """for i in range(num_sentences):
        print(pcfg.random_sent())"""
    with open("grammar2.gen", "w") as f:
        for i in range(num_sentences):
            s = pcfg.random_sent()
            f.write(s + "\n")


def get_args():
    if len(sys.argv) == 1:
        return sys.argv[1], 0
    if sys.argv[2] == "-n":
        return sys.argv[1], int(sys.argv[3])
    return sys.argv[1], 0


if __name__ == '__main__':
    grammar_file, num_sentences = get_args()
    pcfg = PCFG.from_file(grammar_file)
    gen_grammar_2()
    """for i in range(num_sentences):
        print(pcfg.random_sent())"""
