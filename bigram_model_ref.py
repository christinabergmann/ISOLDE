"""
bigram_model_ref.py: very simple implementation of a bigram model for
educational purposes

@author: Maarten Versteegh (m.versteegh 'at' let.ru.nl)
Modifications: Christina Bergmann (chbergma 'at' gmail.com)

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
    
    # the words and non-words from saffran
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

if __name__ == '__main__':
    corpus = read_corpus(corfile)
    unigram_dict, bigram_dict = process_corpus(corpus)
    test_model(unigram_dict, bigram_dict)
    
