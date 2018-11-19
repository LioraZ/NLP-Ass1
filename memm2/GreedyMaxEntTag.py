import sys
import math
import re
import time
from collections import defaultdict
from liblin import LiblinearLogregPredictor

# Constants
START = 'start'
STRIP_REGEX = '[^a-zA-Z0-9]'


def load_model_file(filename):
    return LiblinearLogregPredictor(filename)


def load_features_file(filename):
    tag_map = {}
    feature_map = {}
    with open(filename, 'r') as file_ref:
        for line in file_ref:
            print (line)
            words = line.split()
            if line.startswith('*'):
                tag_map[words[1]] = words[0][1:]
            # We don't do pruning here
            elif line.startswith('%'):
                pass
            else:
                feature_map[words[0]] = int(words[1])
    return (tag_map, feature_map)


def append_feature(feature_map, return_vec, feature_name, feature_val):
    full_feature = feature_name + "=" + str(feature_val)
    if full_feature in feature_map:
        return_vec.append(int(feature_map[full_feature]))


def create_vector(word, prev_tags, prev_words, next_words, feature_map):
    return_vec = []
    form_feature = 'form=' + word
    if form_feature in feature_map:
        return_vec.append(int(feature_map[form_feature]))
    else:
        append_feature(feature_map, return_vec, 'caps', any([letter.isupper() for letter in word]))
        append_feature(feature_map, return_vec, 'hyph', '-' in word)
        append_feature(feature_map, return_vec, 'digit', any([letter.isdigit() for letter in word]))
        if len(word) > 5:
            for n in range(3):
                n1 = n + 1
                strn = str(n1)
                append_feature(feature_map, return_vec, 'suff' + strn, word[-1 * n1:])
                append_feature(feature_map, return_vec, 'pref' + strn, word[:n1])
    # Check if previous words exist
    if prev_words[-1] != '':
        append_feature(feature_map, return_vec, 'p_word', prev_words[-1])
        if prev_words[-2] != '':
            append_feature(feature_map, return_vec, 'pp_word', prev_words[-2])
    # Check if next words exist
    if next_words[0] != '':
        append_feature(feature_map, return_vec, 'n_word', next_words[0])
        if next_words[1] != '':
            append_feature(feature_map, return_vec, 'nn_word', next_words[1])
    # Previous tags always exist
    append_feature(feature_map, return_vec, 'p_tag', prev_tags[-1])
    pp_tags = '|'.join(prev_tags[-2:])
    append_feature(feature_map, return_vec, 'pp_tags', pp_tags)
    return_vec.sort()
    return return_vec

# Main #

t0 = time.time()
input_filename = sys.argv[1]
modelname = sys.argv[2]
feature_map_file = sys.argv[3]
output_filename = sys.argv[4]

word_predict = load_model_file(modelname)
tag_map, feature_map = load_features_file(feature_map_file)
print(tag_map)

with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
    for line in infile:
        prev_tags = [START, START]
        prev_words = ['', '']
        decided_tags = []
        words = line.split()
        max_words = len(words) - 1
        for i, word in enumerate(words):
            next_words = ['', '']
            next_words[0] = words[i + 1] if i + 1 <= max_words else ''
            next_words[1] = words[i + 2] if i + 2 <= max_words else ''
            
            features_vector = create_vector(word, prev_tags, prev_words, next_words, feature_map)
            results_vector = word_predict.predict(features_vector)
            max_tag = max(results_vector, key=results_vector.get)
            print (tag_map)
            max_tag_word = tag_map[max_tag]

            prev_tags.append(max_tag_word)
            prev_words.append(word)
            decided_tags.append((word, max_tag_word))
        outstr = ''
        for word, tag in decided_tags:
            outstr += '/'.join([word, tag]) + ' '
        outstr = outstr[:-1] + '\n'
        outfile.write(outstr)

            
t1 = time.time()
print('Runtime = ' + str(t1 - t0) + ' seconds')
