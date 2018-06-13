# -*- coding: utf-8 -*-
"""
bigram_mmodel_ref.py: very simple implementation of a bigram model for
educational purposes

Copyright (C) 2018 Christina Bergmann (chbergma 'at' gmail.com)

Based on the original script by Maarten Versteegh

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# don't worry about this line
from __future__ import division

def read_corpus(filename):
    """ read corpus from '\n'-delimited text file
    returns a list of syllables """

    # initialize the return list as an empty list
    result = []

    # open the file for reading and loop over the lines
    for line in open(filename, 'r'):
        # get rid of end-of-line ('\n') symbols 
        syll = line.strip()
        # put syllable at end of list
        result.append(syll)

    # now that the result list is filled up, return it
    return result

# it makes sense to test each function, so let's do that now:
corpusfile = 'saffran_corpus.cor'
corpus = read_corpus(corpusfile)

def process_corpus(list_of_syllables):
    """ extract count of uni- & bigram occurrences from sequence
    of syllables in list_of_syllables """

    # dictionaries to hold the counts of the unigrams & bigrams
    unigram_dict = {}
    bigram_dict = {}

    # loop over the indices of list_of_syllables until the first to last element
    for syll_idx in range(len(list_of_syllables) - 1):
        # form unigram of syllables at index
        unigram = (list_of_syllables[syll_idx])

        # see if we have already seen this unigram
        if unigram in unigram_dict:
            # if so, up the count by 1
            unigram_dict[unigram] += 1
        else:
            # if not, set the count to 1
            unigram_dict[unigram] = 1

        # form bigram of subsequent syllables
        bigram = (list_of_syllables[syll_idx], list_of_syllables[syll_idx + 1])
        # see if we have already seen this bigram
        if bigram in bigram_dict:
            # if so, up the count by 1
            bigram_dict[bigram] += 1
        else:
            # if not, set the count to 1
            bigram_dict[bigram] = 1

    # correct for the off-by-1:
    unigram = list_of_syllables[-1]
    if unigram in unigram_dict:
        unigram_dict[unigram] += 1
    else:
        unigram_dict[unigram] = 1

    # return the dictionaries with the unigram and bigram counts
    return unigram_dict, bigram_dict

# again, we want to make sure the function does what we want it to:
unigram_dict, bigram_dict = process_corpus(corpus)

# if we get no error messages, we want to inspect the contents of the dictionaries
# the built-in print command shows the contents of variables on screen
# warning: do not do this for large data structures, there you want to inspect specific elements 

print(unigram_dict)
print(bigram_dict)


def estimated_bigram_probability(bigram, unigram_dict, bigram_dict):
    """ estimate the probability of bigram (= (syll_1,syll_2)) by:
    (count (syll_1,syll_2)) / (count syll_1)
    """

    # set the count to zero
    count = 0

    # check if bigram is actually in our dict
    if bigram in bigram_dict:
        # if so, set count to the value from bigram_dict
        count = bigram_dict[bigram]

    # divide the (bigram) count by the unigram count of the first syllable
    # to get the probability
    prob = count / unigram_dict[bigram[0]]

    # return the calculated probability
    return prob

def estimated_sequence_probability(list_of_syllables, unigram_dict, bigram_dict):
    """ estimate probability of sequence of syllables,
    represented as a list """
    
    # set probability to 1 initially
    p = 1.

    # loop over sequence indices
    for syll_idx in range(len(list_of_syllables) - 1):
        # form bigram from subsequent syllables
        bigram = (list_of_syllables[syll_idx], list_of_syllables[syll_idx + 1])
        
        # multiply previous probability with probability of this bigram
        p = p * estimated_bigram_probability(bigram, unigram_dict, bigram_dict)

    # return the estimated probability of the entire sequence
    return p

def test_model(unigram_dict, bigram_dict):
    """ test the model on saffran's words and non-words
    """
    
    # the words and non-words from the original study.
    words = [['tu','pi','ro'],
             ['go','la','bu'],
             ['bi','da','ku'],
             ['pa','do','ti']]
    non_words = [['da','pi','ku'],
                 ['ti','la','do']]

    # calculate the sum of the probabilities of the words
    sum_words = 0
    for word in words:
        sum_words += estimated_sequence_probability(word, unigram_dict, bigram_dict)

    # divide by the number of words to get the average
    average_word = sum_words / len(words)

    # idem for the non-words
    sum_non_words = 0
    for non_word in non_words:
        sum_non_words += estimated_sequence_probability(non_word, unigram_dict, bigram_dict)
    # divide by the number of words to get the average        
    average_non_word = sum_non_words / len(non_words)

    print('Average probability for words:', average_word)
    print('Average probability for non-words:', average_non_word)


# let's test this. we read in the corpus and built the dictionaries above.
# first, we told python the name of our corpus file (in the same directory)
# corpusfile = 'saffran_corpus.cor'
# next we built a corpus: corpus = read_corpus(corpusfile)
# then we called: unigram_dict, bigram_dict = process_corpus(corpus)
# now we can test the model

test_model(unigram_dict, bigram_dict)

# are the results what you expected?


#### Now let's use the same code we wrote for a different corpus! ###

# First we read in the new corpus, which comes from this paper:
# Pelucchi, B., Hay, J. F., & Saffran, J. R. (2009). Statistical learning in a natural language by 8‐month‐old infants. Child development, 80(3), 674-685.
# Specifically, we are using the stimuli from experiment 3.
# Note: If you open the file, you will see that it is preprocessed to look the same way as the other corpus file, with one syllable per line. This is crucial so we can reuse the scripts we wrote.

corpusfile_italian="Pelucci3B.cor"
corpus_italian = read_corpus(corpusfile_italian)

# Now, as before, we get unigrams and bigrams, use the print() command to inspect them.
unigram_dict_italian, bigram_dict_italian = process_corpus(corpus_italian)
print(unigram_dict_italian)
print(bigram_dict_italian)

# Now we just need to adapt the test_model routine. We change the name to not overwrite the previous function
def test_model_italian(unigram_dict, bigram_dict):
    """ test the model on saffran's words and non-words
    """
    
    # the words and non-words from Pelucci et al., experiment 3
    words = [['me', 'lo'],
             ['fu', 'ga']]
    non_words = [['bi', 'ci'],
                 ['ca', 'sa']]

    # calculate the sum of the probabilities of the words
    sum_words = 0
    for word in words:
        sum_words += estimated_sequence_probability(word, unigram_dict, bigram_dict)

    # divide by the number of words to get the average
    average_word = sum_words / len(words)

    # idem for the non-words
    sum_non_words = 0
    for non_word in non_words:
        sum_non_words += estimated_sequence_probability(non_word, unigram_dict, bigram_dict)
    # divide by the number of words to get the average        
    average_non_word = sum_non_words / len(non_words)

    print('Average probability for words:', average_word)
    print('Average probability for non-words:', average_non_word)


# Now test this:

test_model_italian(unigram_dict_italian, bigram_dict_italian)

# Note: If we know in advance that we want to process and test a lot of different corpora with different words and non_words, it would be more efficient to change the above test_model to take words and non_words as input. Try to implement it yourself!


    
