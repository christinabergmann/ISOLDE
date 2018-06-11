# -*- coding: utf-8 -*-
"""
vocab_model_ref.py: A very simple model to predict vocabulary acquisition

@author:  Christina Bergmann (chbergma 'at' gmail.com)

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

# import useful functions from the pandas library for dealing with tables
import pandas as pd

# now some mathy functions
import numpy as np

# to learn more about pandas, you can for example go to this site: http://pandas.pydata.org/pandas-docs/stable/10min.html

# for visualization, we will use these libraries
import matplotlib.pyplot as plt
import seaborn as sns



def read_in_files(filename_wordbank, filename_corpus):
    """read a vocabulary file downloaded from http://wordbank.stanford.edu/
    the file contains a table with single words and the percentage of children who know the word at different ages
    returns a pandas dataframe"""
    
    # we make use of a special function in pandas which processes tables correctly for our purposes
    vocabulary =  pd.read_csv(filename_wordbank)
    
    # we want to clean the words up a bit, because some words contain specifications, 
    # like "chicken (animal)" which we cannot distinguish in the input data
    
    vocabulary["definition"] = vocabulary.definition.str.split("(").str[0].str.strip("(")
    # we now have 12 duplicate items
    
    raw_input_corpus = pd.read_csv(filename_corpus, usecols = ['mw_stem'])
    # the corpus file is quite large, so we only read in one column which contains all info we need for now
    # 'mw_stem' (multiword stem) contains the utterances in citation form
    
    # there is a lot of noise, so we first remove all rows for which we do not have data
    # to do so, we ask that all elements are not empty
    raw_input_corpus = raw_input_corpus[raw_input_corpus.mw_stem.notnull()]
    
    return vocabulary, raw_input_corpus

def explore_vocabulary(vocabulary, age = 20):
    """ examine the contents of the vocabulary file. 
    Age is set by default to 20 months
    you can also paste this code into the notebook, here it is a function for convenience"""
    
    # check that age falls into the possible range of 16 to 30
    if int(age) in range(16 , 31, 1):
        # First let's look at the distribution over age, this is easier if we sort the data first
        vocabulary_sorted = vocabulary.sort_values(by = str(age)).reset_index(drop=True)
    
        # now we make the actual plot of the vocabulary profile
        plt.plot(vocabulary_sorted.index, vocabulary_sorted[[str(age)]])
        plt.xlabel("Index sorted by percent")
        plt.ylabel("Percent of children of " + str(age) + " months old know this word")
        plt.show()
        
        # if you want to see what happens over ages, you can add a for-loop here and add multiple lines.
        
        # We might want to know the distribution of the percentage of children knowing words per category
        sns.violinplot(x = str(age), y = 'category', data = vocabulary, palette = "Set2")
        plt.ylabel("Percent of children of " + str(age) + " months old know this word")
        
        # you can also experiment with different plot types, for example a stripplot
        # the code is very similar:
        # sns.stripplot(x = str(age), y = 'category', data = vocabulary, palette = "Set2")
        

        # we can also have the script return some descriptives
        overall_vocabulary = vocabulary[[str(age)]].describe()
        category_vocabulary = vocabulary[['category', str(age)]].groupby(by = 'category').describe()
    else:
        # this is a very simple way of catching errors, which helps others use your scripts
        print("Age argument wrong")
    
    # let's return our descriptives
    return overall_vocabulary, category_vocabulary
        

def extract_word_frequency(raw_input_corpus): 
    """ process a raw corpus data frame and extract word frequencies
    the corpus has a lot of additional info, and words are embedded in utterances 
    we want a different sort of file structure where we note the frequency for each word"""
    
    # what we do here is a concatenation of commands that are applied in sequence, you can also go through them line by line
    # first we take the column of the input corpus which contains the stems of all words
    # then we split the string (it automatically uses blank spaces, but you can also define when to split the string)
    # next we spread out the words so that we end up with a longer list where each word is in a separate line
    # finally we remove information how the stem was uttered
    utterances = raw_input_corpus.mw_stem.str.split().apply(pd.Series).stack().reset_index(drop=True).str.split(";").str[0]
    # fun fact: this is called "data wrangling" and a big part of the job when you analyze complex data
    # usually, googling the problem helps a lot!
    # because we have so many utternaces (almost 300,000!!) this might take some time!
    
    # we come back to dictionaries and can apply what we did yesterday, counting words should be easy!
    frequency_dict = {}
    
    # this time we only look at single words, so we don't need to look at the index and directly iterate over the words
    for word in utterances:
        # we check whether we already saw this word
        if word in frequency_dict:
            # note that we saw it once more
            frequency_dict[word] += 1
        else:
            # note that we saw this word for the first time
            frequency_dict[word] = 1
            
    # as a last step, we should create a data frame, this makes it possible to order elements
    # we ask python to make a list of all dictionary entries, let pandas turn this into two columns, and name those word and frequency 
    frequency =  pd.DataFrame(list(frequency_dict.items()), columns = ["definition", "frequency"])
    # we have over 5000 words
        
    return frequency


def explore_frequency(frequency):
    """ examine the contents of the frequency data we extracted from the corpus. 
    you can also paste this code into the notebook, here it is a function for convenience"""
    
    # First let's look at the distribution, this is easier if we sort the data first
    frequency_sorted = frequency.sort_values(by = 'frequency').reset_index(drop=True)

    # now we make the actual plot of the input frequency profile
    plt.plot(frequency_sorted.index, frequency_sorted.frequency)
    plt.xlabel("Index sorted by frequency")
    plt.ylabel("Number of times this word appears in the corpus")
    plt.show()
    
    # we can also have the script return some descriptives
    overall_frequency = frequency.frequency.describe()

    
    # let's return our descriptives
    return overall_frequency

def compare_frequency_acquisition(frequency, vocabulary, age = 20):
    """take the vocabulary information and input frequency and information how well they correlate.
    needs an age between 16 and 30 months, this is pre-set to 20 months"""
    
       
    # first we create a new data structure that is matched on the words
    joint_data = frequency.merge(vocabulary, on = 'definition', how = 'inner')
    # we have 398 datapoints we can work with, not too bad.
    
    # let's first visualize the dataset and compute a simple correlation
    
    sns.jointplot(x = 'frequency', y = str(age), data = joint_data)
    # oh no, that looks like a floor effect! 
    # maybe we should remove words that occur less than 10 times
    
    joint_data_filtered = joint_data[joint_data['frequency']> 9]
    # wow, that removed over 200 data points. We saw that when inspecting the data earlier though
    
    
    sns.jointplot(x = 'frequency', y = str(age), data = joint_data_filtered)

    # but let's think back to the distribution we looked at before, it was skewed!
    # maybe it makes sense to look at the log distribution 
    # first we create a log frequency column
    joint_data['log_frequency'] = np.log(joint_data.frequency)
    
    # now let's take a look again
    sns.jointplot(x = 'log_frequency', y = str(age), data = joint_data)
    # now we got a correlation, how exciting!
    # and note we didn't use the sorted dataset...
    
    
   
def extract_first_word_frequency(raw_input_corpus): 
    """ process a raw corpus data frame and extract word frequencies 
    for the first word in an utterance
    """
    
    # interestingly enough, we can reuse some code from earlier, 
    # but since we are not splitting up utterances, we can just always look 
    # at the first word and remove inflection 
    first_words = raw_input_corpus.mw_stem.str.split().str[0]

    # we come back to dictionaries and can apply what we did yesterday, counting words should be easy!
    first_word_dict = {}
    
    # this time we only look at single words, so we don't need to look at the index and directly iterate over the words
    for word in first_words:
        # we check whether we already saw this word
        if word in first_word_dict:
            # note that we saw it once more
            first_word_dict[word] += 1
        else:
            # note that we saw this word for the first time
            first_word_dict[word] = 1
            
    # as a last step, we should create a data frame, this makes it possible to order elements
    # we ask python to make a list of all dictionary entries, let pandas turn this into two columns, and name those word and frequency 
    first_word_frequency =  pd.DataFrame(list(first_word_dict.items()), columns = ["definition", "frequency"])
    # we have over 5000 words
        
    return first_word_frequency

    

    
# now we can test those routines
# the example files we worked with are now specified
# (make sure they are in the same directory if you use a notebook or in the working directory if you wor with python):
filename_wordbank = 'wordbank_data.csv'
filename_corpus = 'Eng-NA_Brent_Utterance.csv'

vocabulary, raw_input_corpus = read_in_files(filename_wordbank, filename_corpus)

overall_vocabulary, category_vocabulary = explore_vocabulary(vocabulary)

frequency = extract_word_frequency(raw_input_corpus)