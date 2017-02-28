# -*- coding: utf-8 -*-

from os import walk
from os.path import join
import numpy as np
from scipy import spatial
import json
import math
from collections import OrderedDict


class LanguageDetector(object):
    """ Language Detector detects the language of a given text. For this, it uses a 
    directory of samples language documets. The method process reads all the 
    documents in the directory and collects all the ngrams from 1 to ngram_max to 
    create avocabulary list (with associated frequencies) for each document, as well
    as a global vocabulary list for all documents. Then it builds a revers index
    with a vector of weights (calculated with tf-idf) that represents each file 
    in the hypespace where each dimension is an ngram. 

    The method detect_language receive a piece of text (query) and return a list of
    languages sorted decrementally by scores of similarity, i.e. the first entry
    of the vector is the most likely language according to the model. A text is
    treated in a similar fashion to the language documents; it is represented 
    as a vector of weights in the ngrams hyperspace.
    """


    def __init__(self, ngrams_max=3, data_dir="../data"):
        """ The constructs just creat some properties of the class, and 
        receive a couple of configuration parameters

        Args:
            ngrams_max (int): the ngrams that are going to be considered goes
                              from 1 to ngrams_max
            ngrams_dict (str): the directory that contains the documents of
                               languages to create the vector space
        """

        self.ngrams = {}
        self.ngrams_doc = {}
        self.idfs = {}
        self.weights = {}
        self.ngrams_max = ngrams_max
        self.data_dir = data_dir

    def process(self):
        """ It process the files in the directory by calculating frequencies 
        (of words in the vocabulary and individual documents), the reverse 
        indexes and the vector of weights that represent the documents in the
        hyperspace defined by the vocabulary
        """

        self.calculate_frequencies()
        self.calculate_inverse_document_frequency()
        self.calculate_weights()

    def add_ngram(self, ngram, ngrams_dict):
        """ Add an ngram to a dictionary, or increase its counter

        Args:
            ngram (str): the ngram to be added
            ngrams_dict (str): the dictionary that contains the ngrams

        """

        if ngram in ngrams_dict:
            ngrams_dict[ngram] += 1
        else:
            ngrams_dict[ngram] = 1

    def calculate_frequencies(self):
        """ Calculate the frequencies of the ngram of in each document and
        in the global vocabulary 
        """

        _, _, self.filenames = next(walk(self.data_dir), (None, None, []))

        for doc in self.filenames:
            with open(join(self.data_dir, doc), "r", encoding="utf-8") as text:
                self.ngrams_doc[doc] = {}

                ngram_buff = [""] * self.ngrams_max

                while True:
                    c = text.read(1).lower()

                    if not c:
                        break
                    if c == '\n' or c == ' ':
                        ngram_buff = [""] * self.ngrams_max
                        continue

                    # add all the ngrams of different sizes
                    for b in range(self.ngrams_max):

                        ngram_buff[b] = ngram_buff[b] + c

                        if len(ngram_buff[b]) > b+1:
                            ngram_buff[b] = ngram_buff[b][1:]

                        if len(ngram_buff[b]) == b+1:
                            if b+1 < 3:
                                self.add_ngram(ngram_buff[b], self.ngrams)
                                self.add_ngram(ngram_buff[b], self.ngrams_doc[doc])

                            #if there is at least 3 charactes in the ngram
                            else:
                                n_gram = ngram_buff[b][0] + '_' * (b-1) + ngram_buff[b][b]
                                self.add_ngram(n_gram, self.ngrams)
                                self.add_ngram(n_gram, self.ngrams_doc[doc])

    def calculate_inverse_document_frequency(self):
        """ Calculate the inverse document frequency using the presence
        of the ngram in the documents and the vocabulary
        """

        for (key, freq) in self.ngrams.items():
            self.idfs[key] = 0
            for doc in self.filenames:
                if key in self.ngrams_doc[doc]:
                    self.idfs[key] += 1
            self.idfs[key] = math.log(len(self.filenames)
                / float(self.idfs[key]))

    def calculate_weights(self):
        """ Calculate the weight vectors for all the documents using the the
        frequency of the ngram in the document and the inverse document 
        frequencies (idf)
        """

        for doc in self.filenames:
            self.weights[doc] = self.calculate_weight(self.ngrams_doc[doc])

    def calculate_weight(self, ngrams_dict):
        """ Calculte the weights of a document/text using the frequencies 
        of the ngrams (ngram_dict) and the inverse document frequencies (idk)

        Args:
            ngrams_dict (dict): the dictionary that contains the ngrams and
                                its frequencies

        Returns:
            the vector of weights

        """

        weights = np.zeros(len(self.idfs))
        ind = 0
        for (key, idf) in self.idfs.items():
            if key in ngrams_dict:
                weights[ind] = ngrams_dict[key] * idf
            else:
                weights[ind] = 0
            ind += 1

        return weights

    def detect_language(self, text):
        """ Compare the text with all the languages. First it calculates the
        frequencies of ngrams and the respective weight vector usind idk. Then
        compares this vector against all the languages weight vectors using
        cosine similarity.

        Args:
            text (str): to be compared

        Returns:
            a sorted array that contains all the comparisons in descendant 
            order, i.e. the most similar language first

        """


        ngrams_text = self.find_ngrams_text(text)
        weights_text = self.calculate_weight(ngrams_text)

        results = {}
        for doc in self.filenames:
            sim = 1 - spatial.distance.cosine(weights_text, self.weights[doc])
            results[doc] = sim
        return (sorted(results.items(), key=lambda x: x[1], reverse=True))


    def find_ngrams_text(self, text):
        """ Find all the ngrams of a given text. It iterates over all 
        characters and stores all found ngrams.

        Args:
            text (str): the text from which the ngrams will be extracted

        Returns:
            a dictionary with all the ngrams and its frequencies

        """

        ngrams_text = {}
        ngram_buffs = [""] * self.ngrams_max
        for c in text:
            for b in range(self.ngrams_max-1):
                ngram_buffs[b] = ngram_buffs[b] + c

                if len(ngram_buffs[b]) > b+1:
                    ngram_buffs[b] = ngram_buffs[b][1:]

                if len(ngram_buffs[b]) == b+1:
                    self.add_ngram(ngram_buffs[b], ngrams_text)

        return ngrams_text


