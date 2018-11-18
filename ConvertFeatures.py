from collections import Counter
from itertools import islice
import sys
import json


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
    
def get_featurs_map(featurs_list):
   fset = list(set(featurs_list))
   x =  dict((i , j + 1) for i,j in zip(fset, range(len(fset))))
   return (x)

def create_tags_map(tags):
   x =  dict((i , j + 1) for i,j in zip(tags, range(len(tags))))
   return (x)

def write_featurs_vecs(tags_map, feature_map, lines):
    f = open(feature_vecs_file, 'w')
    #print (lines)
    for line in lines:
        splited_feature_line = line.split(" ")
        tag_num = tags_map.get(splited_feature_line[0])
        s = []
        for feat in splited_feature_line[1:]:
          #  print (feat)
            s.append(str(feature_map.get(feat)))
        

        list1 = [int(x) for x in s]
        s = sorted(list1)
        s = [str(x) for x in s]
        #print (s)
        f.write(str(tag_num) + " ")
        f.write(":1 ".join(s))
        f.write(':1\n')
    f.close()

def write_featurs_map(feature_map):
    with open(feature_map_file, 'w') as file:
        file.write(json.dumps(feature_map))

def join(str_list):
    return " ".join(str_list)

if __name__ == '__main__':
    script_name, input_file, feature_vecs_file, feature_map_file = sys.argv
    tags, data, lines = reading_input(input_file)
    feat_map = get_featurs_map(data)
    tag_map = create_tags_map(tags)
    write_featurs_vecs(tag_map, feat_map, lines)
    write_featurs_map(feat_map)
    #get_featurs_map(data)
