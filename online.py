from offline import get_json, perfect_str


def in_trie(trie, sentence):
    current_dict = trie
    flag = 0
    points = 0
    for i, letter in enumerate(sentence):
        if letter not in current_dict:
            if len(sentence) == 1:
                points -= 10
                return ["No matching sentence to complete"]
            flag += 1
        else:
            current_dict = current_dict[letter]
        if flag > 1:
            return ["No matching sentence to complete"]
    data = get_json()
    result = [data[j['index']] for j in current_dict['_end_']]
    return [i[0] + i[1] for i in result][:5]


def search(trie, string):
    string = perfect_str(string)
    result = in_trie(trie, string)
    return result


def print_adjustments(list_):
    for str in list_:
        print(str)


def online(trie):
    sentence = ''
    print("The system is ready.")
    while True:
        sentence += input(f"\nEnter something you want to search: {sentence}")
        if sentence[-1] == '#':
            sentence = ''
        else:
            print_adjustments(search(trie, sentence))
