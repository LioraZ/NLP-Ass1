import sys
from collections import defaultdict

def add_mapped_element(element, element_map):
    if element not in element_map:
        # For the solvers, features must start at 1 (not 0, this
        # appears to be a bug in line 307 of Train.java, they should
        # initialize from -1)
        element_map[element] = len(element_map) + 1

def reading_input(fname):
    """ data is list of words and there tags (in one string)"""
    tags = []
    featurs_list = []
    with open(fname, encoding="utf8") as file:
        input_feat = [line[:-1] for line in file]

    for feature_line in input_feat:
        splited_feature_line = feature_line.split(" ")
        tags.append(splited_feature_line[0])
        for feature in splited_feature_line[1:]:
            featurs_list.append(feature)
    return list(set(tags)), featurs_list, input_feat



features_file = sys.argv[1]
output_vec_file = sys.argv[2]
output_map_file = sys.argv[3]

features_map = defaultdict(int)
labels_map = defaultdict(int)
num_lines = sum(1 for line in open(features_file, 'r'))




with open(features_file, 'r') as input_file, open(output_vec_file, 'w') as output:
    word_tag_dict = defaultdict(set)
    for count, line in enumerate(input_file):
        one_feature_set = {}
        features = line.split()
        
        label = features[0]
        add_mapped_element(label, labels_map)

        feature_number_list = []
        for feature in features[1:]:
            add_mapped_element(feature, features_map)
            feature_number_list.append(features_map[feature])
        # For the solver the list needs to be sorted
        feature_number_list.sort()
        output_line = str(labels_map[label])
        for feature in feature_number_list:
            output_line += ' ' + str(feature) + ':1'
        output.write(output_line + '\n')

        # Word training / UNK training
        find_form = [ form for form in features[1:] if form.startswith('form') ]
        for word in find_form:
            word = word.split('=')[1]        
            if count < num_lines * 0.7:
                word_tag_dict[word].add(label)
            else:
                if word not in word_tag_dict:
                    word_tag_dict['*UNK*'].add(label)
                if any(letter.isdigit() for letter in word):
                    word_tag_dict['*DIGIT*'].add(label)

with open(output_map_file, 'w') as output:
    for label in labels_map:
        output.write('*' + label + ' ' + str(labels_map[label]) + '\n')
    for word in word_tag_dict:
        output.write('%' + word + ' ' + ' '.join(word_tag_dict[word]) + '\n')
    for feature in features_map:
        output.write(feature + ' ' + str(features_map[feature]) + '\n')
        
            
            

