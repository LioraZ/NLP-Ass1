from collections import Counter

def reading_input(fname):
    tags = []
    data = []

    with open(fname, encoding="utf8") as file:
        data = [word for line in file for word in line.split()]

        for word in data:
            item = word.split('/')
            tags.append(item[-1])

        for i in range(len(data)):
            data[i] = data[i].replace("/", " ")

    return tags, data



def write_estimations(pairs, tags):
    with open("e.mle", "w") as file:
        for i in pairs:
            print (i, pairs[i])
            print (i.split(" ")[1],tags[i.split(" ")[1]])
            file.write(i + '\t' + str(pairs[i]) + '\n' + str(i.split(" ")[1]) + '\t' + str(tags[i.split(" ")[1]]) + '\n')


x , y = reading_input("data/ass1-tagger-train")
write_estimations(Counter(y), Counter(x))
