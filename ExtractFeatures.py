from collections import Counter
import sys

START_TAG = "start"
END_TAG = "end"


def reading_input():
    """tagged is list of sentences which eche sentence is a list of (word, tag)"""
    with open(input_file, encoding="utf8") as file:
        lines = [line for line in file]
    tags = [[("/".join(word.split("/")[:-1]), word.split("/")[-1]) for word in sentence.split()] for sentence in lines]
    words = ["/".join(word.split("/")[:-1]) for sentence in lines for word in sentence.split()]
    return tags, words


def get_features_of_word(word_details):
    features = {}
    features[""] = word_details["tag"]
    word = word_details["word"]
    if word in rare_words:
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
    else:
        features["form"] = word_details["word"]

    features["ptag"] = word_details["previous_tag"]
    features["pptag"] = word_details["pre_previous_tag"]
    features["pword"] = word_details["previous_word"]
    features["ppword"] = word_details["pre_previous_word"]
    features["nword"] = word_details["next_word"]
    features["nnword"] = word_details["next_next_word"]
    return features


def write_res(wt):
    s = ""
    with open(output_file, 'w') as f:
        for ls in wt:
            for i, val in enumerate(ls):
                dct = get_sentence_context(i, ls)
                s = " ".join("{}={}".format(k, v) for k, v in get_features_of_word(dct).items())
                f.write(s[1:] + "\n")


def get_sentence_context(i, sentence):
    dc = {'word': sentence[i][0],
    'previous_word': sentence[i - 1][0] if i > 0 else START_TAG,
    'pre_previous_word': sentence[i - 2][0] if i > 1 else START_TAG,
    'next_word': sentence[i + 1][0] if i < len(sentence) - 1 else END_TAG,
    'next_next_word': sentence[i + 2][0] if i < len(sentence) - 2 else END_TAG,
    'tag': sentence[i][1],
    'previous_tag': sentence[i - 1][1] if i > 0 else START_TAG,
    'pre_previous_tag': sentence[i - 2][1] if i > 1 else START_TAG}
    return dc


if __name__ == '__main__':
    script_name, input_file, output_file = sys.argv
    wt1, words1 = reading_input()
    words_count = Counter(words1)
    rare_words = set([word for word, appear in words_count.items() if appear <= 4])
    write_res(wt1)
