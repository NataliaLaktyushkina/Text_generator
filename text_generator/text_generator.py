import random
from regex import match

from nltk.tokenize import WhitespaceTokenizer
from nltk import bigrams, trigrams
from collections import Counter

#import nltk
#nltk.download('punkt')

words = []
bgrms = []
trgrms = []
freq_dict = {}

def file_statistics():
    global words
    filename = input()

    with open(filename, 'r', encoding="utf-8") as corpus_file:
        text = corpus_file.read()
        tk = WhitespaceTokenizer()
        words = tk.tokenize(text)


def print_statistics():
    global  words

    unique_words = set(words)
    print(f'''Corpus statistics
All tokens: {len(words)}
Unique tokens: {len(unique_words)}''')


def print_tokens():
    global words

    while True:
        user_index = input()
        if user_index == 'exit':
            break
        try:
            token_index = int(user_index)
            print(words[token_index])
        except IndexError:
            print('Index Error. Please input an integer that is in the range of the corpus.')
        except TypeError:
            print('Type Error. Please input an integer.')
        except ValueError:
            print('Value Error (not Type Error)')


def transform_into_bigrams():
    global words, bgrms
    bgrms = list(bigrams(words))
#   print(f'Number of bigrams: {len(bgrms)}')


def transform_into_trigrams():
    global words, trgrms
    trgrms = list(trigrams(words))
#   print(f'Number of bigrams: {len(bgrms)}')

def print_bgrms():
    global bgrms

    while True:
        user_index = input()
        if user_index == 'exit':
            break
        try:
            bgrm_index = int(user_index)
            print(f'Head: {bgrms[bgrm_index][0]} Tail: {bgrms[bgrm_index][1]}')
        except IndexError:
            print('Index Error. Please input a value that is not greater than the number of all bigrams.')
        except TypeError:
            print('Type Error. Please input an integer.')
        except ValueError:
            print('Value Error (not Type Error)')


def Markov_chain_model():
    global bgrms, freq_dict
    # create empty dictionary
    freq_dict = {}

    # loop through text and count words
    for element in bgrms:
        head = element[0]
        tail = element[1]
        # set the default value to []
        freq_dict.setdefault(head, []).append(tail)

    for key, item in freq_dict.items():
        freq_counter = Counter(item)
        freq_dict[key] = dict(freq_counter.most_common())


def Markov_chain_model_trgrms():
    global trgrms, freq_dict
    # create empty dictionary
    freq_dict = {}

    # loop through text and count words
    for element in trgrms:
        head = ' '.join((element[0], element[1]))
        tail = element[2]
        # set the default value to []
        freq_dict.setdefault(head, []).append(tail)

    for key, item in freq_dict.items():
        freq_counter = Counter(item)
        freq_dict[key] = dict(freq_counter.most_common())


def test_model():
    global freq_dict
    while True:
        user_string = input()
        print(f'Head: {user_string}')
        if user_string == 'exit':
            break
        try:
            freq_dict_item = freq_dict[user_string]
            for key, item in freq_dict_item.items():
                print(f'Tail: {key}    Count: {item}')
        except KeyError:
            print('Key Error. The requested word is not in the model. Please input another word.')


def generate_sentence():
    heads = list(freq_dict.keys())
    for k in range(10):
        q = True
        sentence = []
        while q:
            head = random.choices(heads)[0]
            if  match(r'^[A-Z].*[^.?!]$', head):
                sentence.append(head)
                q = False
      #  n = random.randint(4, 9)
        n = 10
        i = 1
        while i in range(n):
            tails = list(freq_dict[head].keys())
            weights = list(freq_dict[head].values())
            w = True
            attempts = 0
            while w:
                if attempts > 10:
                    sentence.pop()
                    i -= 1
                next_word = random.choices(tails, weights)[0]
                head = next_word
                if i == n-1:
                    if match(r'.+[.?!]$', next_word):
                        sentence.append(next_word)
                        w = False
                        i += 1
                    else:
                        attempts += 1
                elif i >= 4 and match(r'.+[.?!]$', next_word):
                    sentence.append(next_word)
                    w = False
                    i = n
                else:
                    sentence.append(next_word)
                    w = False
                    i += 1

        print(' '.join(sentence))


def generate_sentence_trgrms():
    heads = list(freq_dict.keys())

  #  for k in range(10):
    k = 0
    while k < 10:
        q = True
        sentence = []
        while q:
            head = random.choices(heads)[0]
            if  match(r'^[A-Z].*[^.?!]$', head.split()[0]) and not match(r'.+[.?!]$', head.split()[1]) and len(head.split()) > 1:
                sentence.append(head.split()[0])
                sentence.append(head.split()[1])
                q = False

        n = 9
        i = 1
        while i in range(n):
            tails = list(freq_dict[head].keys())
            weights = list(freq_dict[head].values())
            w = True
    #        attempts = 0
            while w:
   #             if attempts > 10:
    #                sentence.pop()
     #               i -= 1
                next_word = random.choices(tails, weights)[0]

                if i == n-1:
                    if match(r'.+[.?!]$', next_word):
                        sentence.append(next_word)
                        head = ' '.join((head.split()[-1], next_word))
                        w = False
                        i += 1
                    else:
      #                  attempts += 1
                        w = False
                        i = n
                        k -= 1
                        sentence = []
                elif i >= 4 and match(r'.+[.?!]$', next_word):
                    sentence.append(next_word)
                    head = ' '.join((head.split()[-1], next_word))
                    w = False
                    i = n
                elif i < 4 and match(r'.+[.?!]$', next_word):
                    w = False
                    i = n
                    k -= 1
                    sentence = []
                elif match(r'.+[.?!]$', next_word):
                    sentence = []
                    k -= 1
                    i = n
                else:
                    sentence.append(next_word)
                    head = ' '.join((head.split()[-1], next_word))
                    w = False
                    i += 1

        if sentence != []:
            print(' '.join(sentence))
        k += 1


file_statistics()

# print_statistics(words)
# print_tokens(words)

#transform_into_bigrams()
transform_into_trigrams()
# print_bgrms()

#arkov_chain_model()
Markov_chain_model_trgrms()
#test_model()

#generate_sentence()
generate_sentence_trgrms()
