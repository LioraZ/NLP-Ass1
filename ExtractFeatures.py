from collections import Counter
from itertools import islice
import sys

def reading_input(fname):
    """tagged is list of sentences which eche sentence is a list of (word, tag)"""
    tags = []
    data = []
    with open(fname, encoding="utf8") as file:
        #input_data = [word for line in file for word in line.split()]
        lines = [line for line in file]
    tagged = []
    words = []
    for sentence in lines:
        ls = []
        for wordtag in sentence.split(' '):
             items = wordtag.split('/')
             tag = items[-1].strip()
             word = "/".join(items[:-1])
             words.append(word)
             ls.append((word, tag))
        tagged.append(ls)
    return tagged, words 


def get_features_of_word(word_details, rear_words):
    
    features = {}
    features[""] = word_details["tag"] #the word tag
    word = word_details["word"]
    if (word in rear_words):
        for i in range(1, min(5, len(word))):
            features['prefix'+str(i)] = word[:i]
        for i in range(1, min(5, len(word))):
            features['suffix'+str(i)] = word[-i:]
        if any(x.isdigit() for x in word):
            features['has_number'] = 'has_number'
        if any(x.isupper() for x in word):
            features['has_upper'] = 'has_upper'
            #features.append('has_upper')
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

def write_res(fname, wt, rear_words):
    s = ""
    f = open(fname, 'w')
    for ls in wt:
        for i, val in enumerate(ls):
            dct = get_sentence_context(i,ls)
            s = " ".join("{}={}".format(k, v) for k, v in get_features_of_word(dct, rear_words).items())
           # print (s)
            s = s[1:] # cut the '=' from the string to feet the requseted format
           # print (s)
            f.write(s)
            f.write("\n")
    f.close()

def get_sentence_context(i, sentence):
    dc = { 'word': sentence[i][0],
 'previous_word': sentence[i - 1][0] if i > 0 else 'start',
 'pre_previous_word': sentence[i - 2][0] if i > 1 else 'start',
 'next_word': sentence[i + 1][0] if i < len(sentence) - 1 else 'end',
 'next_next_word': sentence[i + 2][0] if i < len(sentence) - 2 else 'end',
 'tag': sentence[i][1],
 'previous_tag': sentence[i - 1][1] if i > 0 else 'start',
 'pre_previous_tag': sentence[i - 2][1] if i > 1 else 'start'  }
    return dc

if __name__ == '__main__':
  script_name, input_file , output_file = sys.argv
  wt1, words1 =  reading_input(input_file)
  wordscount = Counter(words1)
  rear_words =  set([word for word, appear in wordscount.items() if appear <= 3])
  #print (rear_words)
  write_res(output_file, wt1, rear_words)
