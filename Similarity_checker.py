from difflib import SequenceMatcher
from res import *

def find_most_similar_list(input_string, lists):
    input_string = input_string.lower()
    max_ratio = 0.0
    most_similar_list = None

    for lst in lists:
        ratio = max(SequenceMatcher(None, input_string, word).ratio() for word in lst)
        if ratio > max_ratio:
            max_ratio = ratio
            most_similar_list = lst

    return most_similar_list


# Define the list of lists
all_lists =[greetings, greetings_franko]

# Example usage
input_string = 'hello'
most_similar_list = find_most_similar_list(input_string, all_lists)
if most_similar_list:
    print('The most similar list is:', most_similar_list)
else:
    print('No similar list found.')
