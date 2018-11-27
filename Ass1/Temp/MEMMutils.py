import operator
import json
START_SYMBOL = 'start'
END_SYMBOL = 'end'


def argmax(dict_of_score):
    max_item = max(dict_of_score.items(), key=operator.itemgetter(1))
    return max_item[0], max_item[1]


def create_feature_vec(word_context, feature_map):
    res = []
    for k, v in word_context.items():
        s = k + "=" + v
        if s in feature_map:
            res.append(feature_map[s])
    return res


def get_tags_and_features_maps(feature_map_file):
    with open(feature_map_file) as f:
        data = json.load(f)
    tags_map = data["THIS_IS_THE_TAGLIST"]
    pruning_dict = data["PRUNED_WORDS_TAGS"]
    del data["THIS_IS_THE_TAGLIST"]
    del data["PRUNED_WORDS_TAGS"]
    return tags_map, data, pruning_dict


def get_features_of_word(word_details, rare_words=[]):
    features = {}
    word = word_details["word"]
    if (word in rare_words or rare_words == []):
        for i in range(1, min(5, len(word))):
            features['prefix' + str(i)] = word[:i]
        for i in range(1, min(5, len(word))):
            features['suffix' + str(i)] = word[-i:]
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
          'previous_word': sentence[i - 1] if i > 0 else START_SYMBOL,
          'pre_previous_word': sentence[i - 2] if i > 1 else START_SYMBOL,
          'next_word': sentence[i + 1] if i < len(sentence) - 1 else END_SYMBOL,
          'next_next_word': sentence[i + 2] if i < len(sentence) - 2 else END_SYMBOL,
          'previous_tag': pt,
          'pre_previous_tag': ppt}
    return get_features_of_word(dc)


def join(str_list):
    return " ".join(str_list)
