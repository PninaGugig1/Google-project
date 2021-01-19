import json


def read_from_text():
    data = 'file1.txt'
    with open(data, 'r') as file:
        list_ = [line.split() for line in file]
    return [[" ".join(l), f' ({data}, {i})'] for i, l in enumerate(list_) if l]


def write_to_json():
    with open('data.json', 'w') as f:
        list_ = read_from_text()
        list_.sort()
        data = {}
        for i, str in enumerate(list_):
            data[i] = str
        json.dump(data, f)


def get_json():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data


def remove_unnecessary(string, command):
    tmp = string.split(command)
    res = [word for word in tmp if word != '']
    return " ".join(res)


def perfect_str(string):
    string = remove_unnecessary(string, " ")
    string = remove_unnecessary(string, ",")
    string = remove_unnecessary(string, ".")
    return string


def score(user_str, data):
    points = len(user_str) * 2
    if user_str in data:
        return points
    index = data.find(user_str[0])
    i, j, diff = 0, index, 0
    while i < min(len(user_str) - 1, len(data) - 1):
        if user_str[i] != data[j]:
            diff += 1
            if user_str[i + 1] != data[j + 1]:
                points -= max(5 - i, 1)
            elif (user_str[i] != data[j + 1] and user_str[i + 1] != data[j]) or diff > 1:
                points = 0
                break
            elif user_str[i] == data[j + 1]:  # The user forgot character
                points -= max(10 - 2 * i, 2)
                j += 1
            elif user_str[i + 1] == data[j]:  # The user has added an unnecessary character
                points -= max(10 - 2 * i, 2)
                i += 1
            elif user_str[i + 1] == data[j + 1]:  # one different character
                points -= 2
                i += 1
                j += 1
        i += 1
        j += 1

        if user_str[i] != data[j]:
            diff += 1
            if diff > 1:
                points = 0
            points -= max(5 - i, 1)

    return points


def up_to_one_change(my_string, other):
    counter = 0  # count differences
    for i, j in zip(my_string, other):
        if counter > 1:
            return False
        if i != j:
            counter += 1
    return True


def get_all_str(substring):  # Returns indexes from the Jason file of the relevant strings
    data = get_json()
    return [i for i in data if substring in perfect_str(data[i][0])]


def sub_str(sentence):
    set1 = set()
    for begin in range(len(sentence)):
        for end in range(begin, len(sentence)):
            set1.add(sentence[begin:end + 1])
    return list(set1)


def insert_into_trie(root, sentences_list):
    with open('data.json', 'r') as file:
        data_dict = json.load(file)
        current_dict = root
        for sub in sentences_list:
            counter = 0
            for letter in sub:
                counter += 1
                current_dict = current_dict.setdefault(letter, {})
                index_list = get_all_str(sub[:counter])
            for i in index_list:
                if '_end_' not in current_dict:
                    current_dict['_end_'] = []
                current_dict['_end_'].append({"index": i, "score": score(sub[:counter], data_dict[i][0])})
            current_dict['_end_'] = sorted(current_dict['_end_'], key=lambda k: k['score'])
            current_dict = root


def make_trie():
    data = get_json()
    root = dict()
    list_ = []
    for line in data:
        list_ += sub_str(data[line][0])
    insert_into_trie(root, list(set(list_)))
    return root


def offline():
    print("Loading the files and preparing the system....")
    write_to_json()
    return make_trie()
