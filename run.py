import math
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

    if x == '`':
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


def key_word_frequency_reduce(array, value):
    if array and array[-1][0] == value.word:
        array[-1] = array[-1][0], array[-1][1] + 1
    else:
        array.append((value.word, 1))
    return array


def flatten_list_reduce(acc, x):
    acc = acc + reduce(lambda z, y: z + [y], x, [])
    return acc


def calculate_tf(file_path):
    with open(file_path) as my_file:
        file_text = my_file.read()

        # region Splitting
        word_split = reduce(word_reduce, file_text, [])  # creates list of all words
        word_list = reduce(length_reduce, word_split, [])  # removes words with less than 4 letters
        # endregion

        # region Mapping
        mapper = map(lambda key: (key, 1), word_list)  # just change list to tuple ("word" -> ("word", 1))
        # endregion

        # region Shuffling
        mapper_sort = sorted(mapper, key=lambda x: x[0])  # creates sorted group for reducer
        # endregion

        # region Reducing
        mapper_reducer = reduce(key_reduce, mapper_sort, [])  # reduce to [("word1", 3), ("word2", 4)]
        # endregion

        # region Final result
        word_count = reduce(lambda acc_len, y: acc_len + 1, word_list, 0)  # calculate number of words
        word_frequency_list = starmap(lambda key, value: WordFrequency(file_path, key, value / word_count),
                                      mapper_reducer)
        # endregion
        return word_frequency_list


def calculate_tf_sum(file_paths):
    word_frequency_list = map(calculate_tf, file_paths)
    return reduce(flatten_list_reduce, word_frequency_list, [])


def calculate_idf_value(word_tf_list):
    document_count = reduce(lambda acc, y: acc + 1, config_file_paths, 0)
    word_tf_sorted = sorted(word_tf_list, key=lambda x: x.word)
    word_idf_counter = reduce(key_word_frequency_reduce, word_tf_sorted, [])
    word_idf_values = starmap(lambda key, value: (key, math.log10(document_count / value)), word_idf_counter)
    return list(word_idf_values)


def create_new_array_tf_idf(acc, value):
    check = reduce(lambda acc2, y2: y2[1] * acc2 if value.word == y2[0] else acc2, word_idf, value.frequency)
    acc.append((value.word, value.file_id, check))
    return acc


def calculate_tf_idf_value(word_tf_list, word_idf_list):
    result = reduce(create_new_array_tf_idf, word_tf_list, [])
    return sorted(result, key=lambda x: (x[1], x[2]))


if __name__ == "__main__":
    calculate_tf("sample_data/sample01.csv")  # calculate tf for each word from specific file
    config_yaml = yaml.safe_load(open('config.yaml'))  # get all files from config
    config_file_paths = config_yaml['file_paths']
    word_tf = calculate_tf_sum(config_file_paths)  # calculate tf for each word from all files
    word_idf = calculate_idf_value(word_tf)  # calculate idf for each word from word_tf
    print(calculate_tf_idf_value(word_tf, word_idf))  # calculate tf-idf values
