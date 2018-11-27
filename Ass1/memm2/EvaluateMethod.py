import sys
from collections import defaultdict

first_file = sys.argv[1]
second_file = sys.argv[2]

with open(first_file, 'r') as first, open(second_file, 'r') as second:
    totals = defaultdict(int)
    for line1, line2 in zip(first, second):
        for word1, word2 in zip(line1.split(), line2.split()):
            if word1 == word2:
                totals['correct'] += 1
            totals['all'] += 1
t = str(totals['all'])
c = str(totals['correct'])
p = str(int(totals['correct'] / float(totals['all']) * 100))

print('Out of all words ({0}) there were {1} correct matches ({2}%)'.format(t,c,p))
