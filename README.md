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

# Testing
An alternatively and seemingly quicker way to index the dictionaries and
reduce dimensionalities is provided by 

    python3 nongram.py 3

Here, the characters inside the ngrams are ignored

# Data set of documents
The documents are the translation of the Human Rights Declaration taken from 
here: http://www.ohchr.org/EN/UDHR/Pages/SearchByLang.aspx
