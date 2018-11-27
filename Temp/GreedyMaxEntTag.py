import sys
import liblin as lbln
import MEMMutils as utils
from MEMMutils import START_SYMBOL


def read_input():
    with open(input_file_name, "r") as file:
        return [[line, greedy_train(line)] for line in file]


def update_max(score, tag, max):
    """"updating the max as needed"""
    if score > max["score"]:
        max["score"] = score
        max["tag"] = tag
    return max


def greedy_train(sentence):
    final_line_tags = [START_SYMBOL, START_SYMBOL]
    words = sentence.split()
    for i, word in enumerate(words):
        context = utils.get_sentence_context(i, words, final_line_tags[-2], final_line_tags[-1])
        feature_indexes = utils.create_feature_vec(context, feature_map)
        tags_with_prob = llp.predict(feature_indexes)
        r = utils.argmax(tags_with_prob)[0]
        max_tag = inv_tag_map[int(r)]
        final_line_tags.append(max_tag)
    return final_line_tags[2:]


def join(str_list):
    return " ".join(str_list)


def greedy_train_with_tag(num_epoch, sentence):
    print("Epoch: " + str(num_epoch) + "\n")
    tags = []
    data = []
    for word in sentence.split():
        items = word.split('/')
        tags.append(items[-1])
        data.append("/".join(items[:-1]))
    data = join(data)
    preds = greedy_train(data)
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
            g, b = greedy_train_with_tag(epoch_count, line)
            good = good + g
            bad = bad + b

    print("Accuracy: " + str((good / (good + bad)) * 100) + "%" + "\n\n")


if __name__ == '__main__':
    script_name, input_file_name, modelname, feature_map_file, out_file_name = sys.argv
    llp = lbln.LiblinearLogregPredictor(modelname)
    tag_map, feature_map, pruning_map = utils.get_tags_and_features_maps(feature_map_file)
    inv_tag_map = {v: k for k, v in tag_map.items()}
    check_test()
    #read_input(input_file_name)







