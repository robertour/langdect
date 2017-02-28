# langdect
A language detector

# Brief Explanation
This code uses an adaptation of the vector space model to ngrams in text
documents in order to detect languages.

The code is still experimental and just a proof of concept.

# Requirements

Python 3.5.2 (older versions haven't been tested but it is likely that it 
will work)
numpy
scipy

# Usage
Just run the code inside the langdect folder with the max number of ngrams 
desired as a parameter. Depending on this paramenter it might take a few 
seconds to load

    python3 ngram.py 3

Then introduce the text for which you want to detect the language. Usually
it gives good results for a paragraph of text

# Testing (Idea)
An alternatively and seemingly quicker way to index the dictionaries and
reduce dimensionalities is provided by 

    python3 nongram.py 3

Here, the characters inside the ngrams are ignored

# Implementation details where improvements are possible/required

1. there is no control of stop words
2. the only characters controlled are '\n' and ' '
3. the indexes are generated each time the code is run (so it can be slow to 
start if you put many characters); the indexes should be save and loaded from
files
4. there is no way to control the minimum amount of ngrams
5. you can include more languages by copying and pasting more translations of
the Human Rights Declaration 

# Data set of documents
The documents are the translation of the Human Rights Declaration taken from 
here: http://www.ohchr.org/EN/UDHR/Pages/SearchByLang.aspx
