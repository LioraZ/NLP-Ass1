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
            return symbol
        else:
            expansion = self.random_expansion(symbol)
            # print expansion
            # return " ".join("(" + symbol +", "+ self.gen(s) + ")" for s in expansion)
            gen = " ".join(self.gen(s) for s in expansion)
            if is_tree:
                gen = '(' + symbol + ' ' + gen + ')'
            return gen

    def random_sent(self):
        return self.gen("ROOT")

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        # print self._rules[symbol]
        for r, w in self._rules[symbol]:
            p = p - w
            if p < 0: return r
        return r


def get_args():
    num_of_sen = 1
    tree = False
    # print (sys.argv)
    try:
        x = sys.argv[2]
        #   print x
        if (sys.argv[2] == "-n"):
            #       print "in"
            try:
                num_of_sen = int(sys.argv[3])
            except:
                print("the nmber of sentence is illegal")
            try:
                if (sys.argv[4] == '-t'):
                    tree = True
            except:
                pass
        else:
            #      print ("in")
            tree = True
            try:
                if (sys.argv[3] == "-n"):
                    num_of_sen = int(sys.argv[4])
            except:
                pass
    except:
        #   print ("jdkvhsdkfjl")
        pass
    return num_of_sen, tree


if __name__ == '__main__':

    num_of_sen, is_tree = get_args()
    pcfg = PCFG.from_file(sys.argv[1])
    for i in range(num_of_sen):
        print(pcfg.random_sent())





