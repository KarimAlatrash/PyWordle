import pandas as pd
import random
# TODO characterize subset, rank from word with most in common w rest of subset to least in common, take middle to
# create binary search

def characterize_guess (todays_word, guess_word):
    characterization = [0, 0, 0, 0, 0]
    # For each character in guess word, check if it is the same index or in the word at all
    for index, character in enumerate(guess_word):
        char_ind = todays_word.find(character)
        # Check if we have a correct character
        if char_ind == index:
            characterization[index] = 2
        # Check if the character exists in todays word
        elif char_ind != -1:
            characterization[index] = 1

    return characterization

# Current issue: reduced subset is pointer to possible_words, removing from reduced_subset increments index
# Conditions for inclusion in subet:
def reduce_words_set (characterization, guess_word, possible_words):
    length = len(possible_words)
    reduced_subset = []

    # Loop through every word in the subset
    for subset_word in possible_words:
        # Loop through each character in the guess word
        if guess_word == subset_word:
            continue
        reduced_subset.append(subset_word)
        for guess_index, guess_char in enumerate(guess_word):
            found_char_index = subset_word.find(guess_char)
            # Subset word should not contain any letters that were not found in todays word
            if characterization[guess_index] == 0 and found_char_index != -1:
                reduced_subset.remove(subset_word)
                break
            # Subset word should contain the same letters that were in the correct spot. The index should be the same
            if characterization[guess_index] == 2 and found_char_index != guess_index:
                reduced_subset.remove(subset_word)
                break
            # Subset word should contain the same letters that exist in the word but not at the same index.
            if characterization[guess_index] == 1 and (found_char_index == -1 or found_char_index == guess_index):
                reduced_subset.remove(subset_word)
                break



    return reduced_subset

guess_avg = 0
lost_count = 0
iterations = 1
for test in range(iterations):
    all_words = pd.read_csv('wordle/wordle_solns.csv', lineterminator='\n')

    todays_word ='nymph'# all_words['WORDS'][random.randrange(0, len(all_words)-1)]
    possible_words = list(all_words['WORDS'])
    guess_count = 0
    while len(possible_words) > 1:
        # Pick a random word
        if guess_count == 0:
            guess_word = "soare"
        else:
            guess_word = possible_words[random.randrange(0, len(possible_words)-1)]
        #Increment the guess
        guess_count += 1
        if guess_word != todays_word:
            # Update what we know about the guess word based on todays word
            characterization = characterize_guess (todays_word, guess_word)
            # Reduce the possible guess words
            possible_words = reduce_words_set(characterization, guess_word, possible_words)
        else:
            break

    guess_avg += guess_count
    if guess_count > 6:
        lost_count += 1
print("It took this many guesses:")
print(guess_avg/iterations)
print("Lost this percent of the time:")
print(lost_count*100/iterations)
