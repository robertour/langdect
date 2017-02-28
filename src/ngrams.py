# -*- coding: utf-8 -*-

import sys
from language_detector import LanguageDetector

ld = LanguageDetector(ngrams_max=int(sys.argv[1]), data_dir="../data")
ld.process()

while True:
    var = input("\nPlease enter the text: ")
    results = ld.detect_language(var)
    for r in range(5):
        print(r+1, results[r][0], results[r][1])

