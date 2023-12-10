from functools import reduce
from itertools import starmap

import yaml

BANNED_CHARACTERS = [',', '.', '!', '?', '\n', '"', '\'', '“', '(', ')', '#', '$', '@']


class WordFrequency:
    def __init__(self, file_id, word, frequency):
        self.file_id = file_id
        self.word = word
        self.frequency = frequency

    def __str__(self):
        return self.file_id + " " + self.word + " " + str(self.frequency)

    def __repr__(self):
        return self.file_id + " " + self.word + " " + str(self.frequency)


def length_reduce(acc, x):
    if reduce(lambda acc_len, y: acc_len + 1, x, 0) > 3:
        return acc + [x]
    return acc


def word_reduce(acc, x):
    if x in BANNED_CHARACTERS:
        return acc

    if not acc:
        acc = ['']

    if x in '`':
        x = ' '

    if x != ' ':
        acc[-1] += x.lower()
        return acc

    if acc[-1] != '':
        return acc + ['']

    return acc


def key_reduce(array, value):
    if array and array[-1][0] == value[0]:
        array[-1] = array[-1][0], array[-1][1] + value[1]
    else:
        array.append(value)
    return array


def calculate_tf(file_path):
    with open(file_path) as my_file:
        file_text = my_file.read()

        word_split = reduce(word_reduce, file_text, [])  # creates list of all words
        word_list = reduce(length_reduce, word_split, [])  # removes words with less than 4 letters
        word_count = reduce(lambda acc_len, y: acc_len + 1, word_list, 0)

        mapper = map(lambda key: (key, 1), word_list)
        mapper_sort = sorted(mapper, key=lambda x: x[0])  # creates sorted group for reducer
        mapper_reducer = reduce(key_reduce, mapper_sort, [])

        word_frequency_list = starmap(lambda key, value: WordFrequency(file_path, key, value/word_count),
                                      mapper_reducer)
        return word_frequency_list


def flatten_list_reduce(acc, x):
    acc = acc + reduce(lambda z, y: z + [y], x, [])
    return acc


def calculate_tf_sum(file_paths):
    word_frequency_list = map(calculate_tf, file_paths)
    result = reduce(flatten_list_reduce, word_frequency_list, [])
    return result


if __name__ == "__main__":
    calculate_tf("sample_data/sample01.csv")
    config_yaml = yaml.safe_load(open('config.yaml'))
    config_file_paths = config_yaml['file_paths']
    print(calculate_tf_sum(config_file_paths))
