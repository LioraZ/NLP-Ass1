import sys
import time
from liblin import LiblinearLogregPredictor

START = 'start'

def load_model_file(filename):
    return LiblinearLogregPredictor(filename)


def update_max(score, tag, max):
    if score > max["score"]:
        max["score"] = score
        max["tag"] = tag
    return max


def get_tags_for_first_word(i, sentence, w, u, utils, llp):
    max_list = []
    max_add = []
    inv_tag_map = []
    context = utils.get_sentence_context(i, sentence, w, u)
    feature_indexes = utils.create_feature_vec(context, feature_map)
    tags_with_prob = llp.predict(feature_indexes)
    for tag, prob in tags_with_prob.items():
        max_tag = inv_tag_map[int(tag)]
        max_list = max_add(prob, max_tag, max_list)
    return max_list
    """
    r, score = utils.argmax(tags_with_prob)
    max_tag = inv_tag_map[int(r)]
    max_list = max_add(score, max_tag, max_list)"""




def load_features_file(filename):
    tag_map = {}
    feature_map = {}
    tagged_words = {}
    with open(filename, 'r') as file_ref:
        for line in file_ref:
            words = line.split()
            if line.startswith('*'):
                tag_map[words[1]] = words[0][1:]
            elif line.startswith('%'):
                tagged_words[words[0][1:]] = words[1:] 
            else:
                feature_map[words[0]] = int(words[1])
    return (tag_map, feature_map, tagged_words)

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

def get_viterbi_output(sentence):
    backtrack_viterbi_output = []
    viterbi = []
    words = sentence.split()
    pi = viterbi(words)
    preds = backtrack_viterbi_output(pi, len(words))
    return preds




# Main #

t0 = time.time()
input_filename = sys.argv[1]
modelname = sys.argv[2]
output_filename = sys.argv[4]
feature_map_file = sys.argv[3]

word_predict = load_model_file(modelname)
tag_map, feature_map, tagged_words = load_features_file(feature_map_file)

tag_list = list(tag_map.values())
#print (tag_list)
tag_list.insert(0, START)

with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:    
    for count, line in enumerate(infile):
        # V holds the dynamic programming array, bp holds dictionaries of the backpointers
        V = [{}]
        bp = [{}]
        for tag in tag_list:
            # Initialize position 0
            V[0][tag] = {}
            for inner_tag in tag_list:
                V[0][tag][inner_tag] = 0

        words = line.split()
        # The initial tag sets are only start
        V[0][START][START] = 1
        pp_tag_set = [START]
        p_tag_set = [START]
        prev_words = ['', '']
        next_words = ['', '']
        max_words = len(words) - 1

        
        for i, word in enumerate(words):
            # Pruning (choosing the correct tag set for the word)
            if word in tagged_words:
                all_tags = tagged_words[word]
            elif any(letter.isdigit() for letter in word):
                all_tags = tagged_words['*DIGIT*']
            else:
                all_tags = tagged_words['*UNK*']

            V.append({})
            bp.append({})

            # The essential loop, checks every 1-prev tag and finds max 2-prev
            for p_tag in p_tag_set:
                V[i + 1][p_tag] = {}
                bp[i + 1][p_tag] = {}
                for tag in all_tags:
                    tag_num = list(tag_map.keys())[list(tag_map.values()).index(tag)]
                    double_back = {}
                    # Loop through all potential double-backs and find the max element
                    for pp_tag in pp_tag_set:
                        prev_tags = [pp_tag, p_tag]
                        next_words[0] = words[i + 1] if i + 1 <= max_words else ''
                        next_words[1] = words[i + 2] if i + 2 <= max_words else ''

                        features_vector = create_vector(word, prev_tags, prev_words, next_words, feature_map)
                        results_vector = word_predict.predict(features_vector)
                        double_back[pp_tag] = V[i][pp_tag][p_tag] * results_vector[tag_num]
                    max_key = max(double_back, key=double_back.get)
                    # Save it and its back pointer
                    bp[i + 1][p_tag][tag] = max_key
                    V[i + 1][p_tag][tag] = double_back[max_key]

            pp_tag_set = p_tag_set
            p_tag_set = all_tags
            prev_words.append(word)

        # Now do the backtrace on the word
        last_word = len(words) - 1
        bp = bp[1:]
        V = V[1:]
        final_col = []
        final_max = []
        
        for item in V[last_word].values():
            final_col.append(item.values())
            final_max.append(max(item.values()))
        max_item_index = final_max.index(max(final_max))
        max_pp = list(V[last_word].keys())[max_item_index]
        max_p = max(V[last_word][max_pp], key=V[last_word][max_pp].get)

        # Loop through the backpointers
        backtrace = {}
        backtrace[last_word] = max_p
        backtrace[last_word -1] = max_pp

        for i in range(last_word - 2, -1, -1):
            backtrace[i] = bp[i + 2][backtrace[i + 1]][backtrace[i + 2]]
        
        output = ''
        for i in range(len(words)):
            output += ' ' + words[i] + '/' + backtrace[i]
        output += '\n'
        outfile.write(output[1:])
t1 = time.time()
print ('Runtime = ' + str(t1 - t0) + ' seconds')


    
