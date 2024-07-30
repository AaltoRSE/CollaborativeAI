import nltk
from nltk.corpus import wordnet as wn

class NounNormalizer:
    def __init__(self):
        nltk.download('wordnet')
    
    def singularize_and_lowercase(self, word):
        singular_word = wn.morphy(word, wn.NOUN)
        if singular_word is None:
            singular_word = word
        return singular_word.lower()