import sys
import json
import liblin as lbln
import TempMLETrain as mle

START_SYMBOL = '*'

def read_input():
    with open(input_file_name, "r") as file:
        return [[line, greedy_train(line)] for line in file]


def update_max(score, tag, max):
    if score > max["score"]:
        max["score"] = score
        max["tag"] = tag
    return max


def greedy_train(sentence, feature_map, tag_map):
   # tags = mle.get_possible_tags()
    final_line_tags = []
    words = sentence.split()
    for i, word in enumerate(words):
        maxProb = float("-Inf")
        maxTag = {}
        pt = "start"
        ppt = "start"
        context = get_sentence_context(i, words, pt, ppt)
        feature_indexes = create_feature_vec(context, feature_map)
        #print (feature_indexes)
        tags_with_prob = llp.predict(feature_indexes)
        #print (feature_indexes)
        #print (tag_map)
        for r in tag_map:   #possible pruning here
            if maxProb < tags_with_prob[str(tag_map[r])]:
                maxProb = tags_with_prob[str(tag_map[r])]
                maxTag = r
        ppt = pt
        pt = maxTag
        #tags.append(maxTag)        
        final_line_tags.append(maxTag)
    return final_line_tags         


def create_feature_vec(word_context, feature_map):
    res = []
    for k, v in word_context.items():
        s = k + "=" + v
        if s in feature_map:
            res.append(feature_map[s])
    return res


def get_tags_and_features_maps():
    data = {}
    tags_map = {}
    with open(feature_map_file) as f:
        data = json.load(f)
    tags_map = data["THISISTHETAGLIST"]
    del data["THISISTHETAGLIST"]
    return tags_map, data


def get_features_of_word(word_details, rear_words = []):
    
    features = {}
    word = word_details["word"]
    if (word in rear_words or rear_words == []):
        for i in range(1, min(5, len(word))):
            features['prefix'+str(i)] = word[:i]
        for i in range(1, min(5, len(word))):
            features['suffix'+str(i)] = word[-i:]
        if any(x.isdigit() for x in word):
            features['has_number'] = 'has_number'
        if any(x.isupper() for x in word):
            features['has_upper'] = 'has_upper'
        if '-' in word:
           features['contains_hyphen'] = 'contains_hyphen'

    features["form"] = word_details["word"]
    features["ptag"] = word_details["previous_tag"]
    features["pptag"] = word_details["pre_previous_tag"]
    features["pword"] = word_details["previous_word"]
    features["ppword"] = word_details["pre_previous_word"]
    features["nword"] = word_details["next_word"]
    features["nnword"] = word_details["next_next_word"]
    return features    


def get_sentence_context(i, sentence, pt, ppt):
    dc = {'word': sentence[i],
    'previous_word': sentence[i - 1] if i > 0 else 'start',
    'pre_previous_word': sentence[i - 2] if i > 1 else 'start',
    'next_word': sentence[i + 1] if i < len(sentence) - 1 else 'end',
    'next_next_word': sentence[i + 2] if i < len(sentence) - 2 else 'end',
    'previous_tag': pt,
    'pre_previous_tag': ppt}
    return get_features_of_word(dc)


def join(str_list):
    return " ".join(str_list)

def greedy_train_with_tag(num_epoch, sentence, tag_map, feature_map):
    print("Epoch: " + str(num_epoch) + "\n")
    tags = []
    data = []
    for word in sentence.split():
        items = word.split('/')
        tags.append(items[-1])
        data.append("/".join(items[:-1]))
    data = join(data)
    preds = greedy_train(data, feature_map, tag_map)
    good = bad = 0.0
    print("\t".join(tags) + "\n")
    print("\t".join(preds) + "\n")
    for tag, pred in zip(tags, preds):
        if tag == pred:
            good += 1
        else:
            bad += 1
    print("Accuracy: " + str((good / (good + bad)) * 100) + "%" + "\n\n")
    return good, bad


def check_test():
    epoch_count = good = bad = 0.0
    with open("data/ass1-tagger-test", "r") as file:
        for line in file:
            epoch_count += 1
            g, b = greedy_train_with_tag(epoch_count, line, tag_map, feature_map)
            good = good + g
            bad = bad + b

    print("Accuracy: " + str((good / (good + bad)) * 100) + "%" + "\n\n")


if __name__ == '__main__':
    script_name, input_file_name, modelname, feature_map_file, out_file_name = sys.argv
    llp = lbln.LiblinearLogregPredictor(modelname)
    tag_map, feature_map = get_tags_and_features_maps()
    check_test()
    #read_input(input_file_name)







