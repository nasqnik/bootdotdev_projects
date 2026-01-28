def word_count(text):
    word_number = len(text.split())
    return word_number

def char_count(text):

    count = {}

    for ch in text.lower():
        if ch in count:
            count[ch] += 1
        else:
            count[ch] = 1
    return count

def sort_dictionary(dictionary):
    sorted_list = []

    for ch, count in dictionary.items():
        sorted_list.append({"char": ch, "num": count})
    sorted_list.sort(reverse=True, key=lambda item: item["num"])

    return sorted_list