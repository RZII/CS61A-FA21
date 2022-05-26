"""Typing test implementation"""

from re import M
from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> choose(ps, s, 0)
    'hi'
    >>> choose(ps, s, 1)
    'fine'
    >>> choose(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    i = 0
    NL = [None] * 1000
    for l in paragraphs:
        if select (l):
            NL [i] = l
            i += 1
    if NL [k] == None:
        return ''
    else:
        return NL [k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def selection (paragraph):
        paragraph = remove_punctuation (paragraph)
        paragraph = lower (paragraph)
        L = split (paragraph)
        for word in L:
            for TW in topic:
                if word == TW:
                    return True
        return False
    return selection

    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    Arguments:
        typed: a string that may contain typos
        reference: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    if typed == "" and reference == "":
        return 100.0
    elif typed == "" or reference == "":
        return 0.0
    i = 0
    count = 0
    if len (typed_words) > len (reference_words):
        reference_words += [None] * (len (typed_words) - len (reference_words))

    while i < len (typed_words):
        if typed_words [i] == reference_words [i]:
            count += 1
        i += 1
    return count / len (typed_words) * 100
    
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    return len (typed) / 5 * 60 / elapsed
    # END PROBLEM 4


###########
# Phase 2 #
###########

def autocorrect(typed_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        valid_words: a list of strings representing valid words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    for l in valid_words:
        if typed_word == l:
            return typed_word

    lowest_dif = diff_function (typed_word, valid_words [0], limit)
    lowest_word = valid_words [0]

    for word in valid_words:
        if diff_function (typed_word, word, limit) < lowest_dif:
            lowest_dif = diff_function (typed_word, word, limit)
            lowest_word = word
    
    if lowest_dif <= limit:
        return lowest_word
    else:
        return typed_word

    
    # END PROBLEM 5

def FFH (start, goal, limit, i, count):
    if i == min (len (start), len (goal)):
        return count + abs (len (start) - len (goal))
    if count > limit:
        return count + 1
    if start [i] != goal [i]:
        count += 1
    return FFH (start, goal, limit, i + 1, count)


def feline_flips(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths and returns the result.

    Arguments:
        start: a starting word
        goal: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_flips("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_flips("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_flips("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_flips("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_flips("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    dif = FFH (start, goal, limit, 0, 0)
    return dif
    # END PROBLEM 6


def minimum_mewtations(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.
    This function takes in a string START, a string GOAL, and a number LIMIT.

    Arguments:
        start: a starting word
        goal: a goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> minimum_mewtations("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> minimum_mewtations("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> minimum_mewtations("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """

    if limit < 0:  # Fill in the condition
        # BEGIN
        return 0
        # END

    if start == "" and goal == "":  # Feel free to remove or add additional cases
        # BEGIN
        return 0
        # END

    elif start == '' or goal == '':
        return abs (len (start) - len (goal))

    elif start [0] == goal [0]:
        return minimum_mewtations (start [1:], goal [1:], limit)

    else:
        add = minimum_mewtations (start, goal [1:], limit - 1)  # Fill in these lines
        remove = minimum_mewtations (start [1:], goal, limit - 1)
        substitute = minimum_mewtations (start [1:], goal [1:], limit - 1)
        # BEGIN
        return min (add, remove, substitute) + 1
        # END


def final_diff(start, goal, limit):
    """A diff function that takes in a string START, a string GOAL, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function.'


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(sofar, prompt, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        sofar: a list of the words input so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> sofar = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(sofar, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    i = 0
    count = 0
    while i < len (sofar):
        if sofar [i] == prompt [i]:
            count += 1
        else:
            break
        i += 1
    d = {'id':user_id, 'progress':count / len (prompt)}
    upload(d)
    return count / len (prompt)
    # END PROBLEM 8


def time_per_word(words, times_per_player):
    """Given timing data, return a match data abstraction, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> get_words(match)
    ['collar', 'plush', 'blush', 'repute']
    >>> get_times(match)
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    times = [[x [i + 1] - x [i] for i in range (len(x) - 1)] for x in times_per_player]
    return match (words, times)
    # END PROBLEM 9


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match data abstraction as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    
    
    """player_indices = range(len(get_times(match)))  # contains an *index* for each player
    word_indices = range(len(get_words(match)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    final_output=[]
    for i in player_indices:
        final_output+=[[]]
    for word_index in word_indices:
        fastest_player_index=0
        for player_index in player_indices:
            if time(match,player_index,word_index)<time(match,fastest_player_index,word_index):
                fastest_player_index=player_index
        final_output[fastest_player_index]+=[word_at(match,word_index)]
    return final_output"""
    
    
    """The codes above: line 356 to line 368 is another solution (which is perhaps clearer and better) """
    """The codes below also works, but are somewhat ghastly written (bad style, bad logic, etc.)
       it was written when my brain wasn't working properly"""

    Fas = [None] * len (get_words (match)) #Fas = [None, None, None]
    i = 0
    number_of_players = len (get_times (match)) #number_of_players = 2
    while i < number_of_players:
        j = 0
        while j < len (get_words (match)):
            if Fas [j] == None:
                Fas [j] = i
            elif get_times (match) [i] [j] < get_times (match)[Fas [j]] [j]:
                Fas [j] = i
            j += 1          
        i += 1
    print ("Debug: Fas is", Fas)
    # By now, Fas should be [0, 0, 1]
    # NF = [0, 0] => NF = [2,1]
    # RL : [['have', 'fun'], ['Just']]
    NF = [0] * number_of_players
    k = 0
    while k < number_of_players:
        h = 0
        while h < len (Fas):
            if Fas [h] == k:
                NF [k] += 1
            h += 1
        k += 1
    print ("Debug: NF is", NF)
    a = 1
    RL = [[None] * NF [0] ]
    while a < len (NF):
        RL += [[None] * NF [a]]
        a += 1
    print ("Debug: RL is", RL)

    c0,c1,c2,c3,c4,c5 = 0,0,0,0,0,0
    II = 0
    for fastest_player_index in Fas:
        if fastest_player_index == 0:
            RL [fastest_player_index] [c0] = word_at (match, II)
            c0 += 1
        elif fastest_player_index == 1:
            RL [fastest_player_index] [c1] = word_at (match, II)
            c1 += 1
        elif fastest_player_index == 2:
            RL [fastest_player_index] [c2] = word_at (match, II)
            c2 += 1
        elif fastest_player_index == 3:
            RL [fastest_player_index] [c3] = word_at (match, II)
            c3 += 1
        elif fastest_player_index == 4:
            RL [fastest_player_index] [c4] = word_at (match, II)
            c4 += 1
        elif fastest_player_index == 5:
            RL [fastest_player_index] [c5] = word_at (match, II)
            c5 += 1
        II += 1
    return RL


    # END PROBLEM 10


def match(words, times):
    """A data abstraction containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(match, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(match[0]), "word_index out of range of words"
    return match[0][word_index]


def get_words(match):
    """A selector function for all the words in the match"""
    return match[0]


def get_times(match):
    """A selector function for all typing times for all players"""
    return match[1]


def time(match, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(match[0]), "word_index out of range of words"
    assert player_num < len(match[1]), "player_num out of range of players"
    return match[1][player_num][word_index]


def match_string(match):
    """A helper function that takes in a match object and returns a string representation of it"""
    return "match(%s, %s)" % (match[0], match[1])


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
