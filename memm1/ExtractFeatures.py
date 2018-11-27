import sys
from collections import defaultdict

START = 'start'

input_file = sys.argv[1]
output_file = sys.argv[2]

'''
The definition and use of 'rare' words is defined in:
A Maximum Entropy Model for Part-Of-Speech Tagging
By Adwait Ratnaparkhi
'''
def is_rare(word, word_counts):
    return word_counts[word] < 5

def write_res(wt, get_sentence_context, get_features_of_word):
    s = ""
    with open(output_file, 'w') as f:
        for ls in wt:
            for i, val in enumerate(ls):
                dct = get_sentence_context(i, ls)
                s = " ".join("{}={}".format(k, v) for k, v in get_features_of_word(dct).items())
                f.write(s[1:] + "\n")


def calc_rare_features(word, features):
    features['caps'] = any([letter.isupper() for letter in word])
    features['hyph'] = '-' in word
    features['digit'] = any([letter.isdigit() for letter in word])
    if len(word) > 5:
        for n in range(3):
            n1 = n + 1
            strn = str(n1)
            features['suff' + strn] = word[-1 * n1:]
            features['pref' + strn] = word[:n1]
    

with open(input_file, 'r') as input_file:
    word_counts = defaultdict(int)
    all_words = []
    for count, line in enumerate(input_file):
        prev_tags = [START, START]
        word_pairs = line.split()
        for word_pair in word_pairs:
            word, tag = word_pair.rsplit('/', 1)
            all_words.append((word, tag))
            word_counts[word] += 1

prev_tags = [START, START]
prev_words = ['', '']

with open(output_file, 'w') as output:
    last_word = len(all_words) - 1
	# Loop through every word
    for count, word_pair in enumerate(all_words):
        features = {}
        word, tag = word_pair
		# Collect features for the words (depending if they are rare or not)
        if (is_rare(word, word_counts)):
            calc_rare_features(word, features)
        else:
			# The form of the word is only held if it isn't rare
            features['form'] = word
		# We save previous words/tags as specified in the article
        features['p_tag'] = prev_tags[-1]
        features['pp_tags'] = '|'.join([prev_tags[-2], prev_tags[-1]])
        if prev_words[-1] != '':
            features['p_word'] = prev_words[-1]
            if prev_words[-2] != '':
                features['pp_word'] = prev_words[-2]
        if count + 1 <= last_word - 1:
            features['n_word'] = all_words[count + 1][0]
            if count + 2 <= last_word:
                features['nn_word'] = all_words[count + 2][0]
        
        prev_tags.append(tag)
        prev_words.append(word)

        outstr = tag + ' '
        for feature in features:
            outstr += feature + "=" + str(features[feature]) + ' '
        output.write(outstr[:-1] + '\n')
    
