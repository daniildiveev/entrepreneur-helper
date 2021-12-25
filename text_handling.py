from keybert import KeyBERT
import numpy as np
import re
import pymorphy2
from tqdm import tqdm, trange

class TextPreprocessing:
    def __init__(self, corpus:list) -> None:
        self.corpus = corpus

    def punctuation(self) -> list:
        for i in trange(len(self.corpus), desc='Removing punctuation: '):
            self.corpus[i] = self.corpus[i].lower()
            words = re.findall(r'\w+', self.corpus[i]) #regex for removing any punctuation
            self.corpus[i] = ' '.join(words)

        return self.corpus

    def preprocess_html(self, corpus:list) -> list:
        for i in range(len(corpus)):
            self.corpus[i] = str(self.corpus[i]).replace('[', '').replace(']', '')
            self.corpus[i] = re.sub(r"<.*?>", "", self.corpus[i])
            self.corpus[i] = re.sub(r"[a-zA-Z]", " ", self.corpus[i])
            self.corpus[i] = re.sub(r"[{}]|[()]", " ", self.corpus[i])
            self.corpus[i] = re.sub(r"\xa0|\n", " ", self.corpus[i])
            self.corpus[i] = re.sub(r"\s+", " ", self.corpus[i])

    def lemmatize(self) -> list:
        morph = pymorphy2.MorphAnalyzer(lang='ru')

        for i in trange(len(self.corpus), desc='Lemmatizing: '):
            self.corpus[i] = self.corpus[i].split()

            for j in range(len(self.corpus[i])):
                self.corpus[i][j] = morph.parse(self.corpus[i][j])[0].normal_form 
                #retrieving normal form of word e.g cats -> cat etc. 
                
            self.corpus[i] = ' '.join(self.corpus[i])

        return self.corpus

    def full_preprocessing(self) -> list:
        self.punctuation()
        self.lemmatize()


def find_most_relevant_part(query:str, 
                            text:str, length:int, 
                            step:int, tokenizer) -> str:
    """
    Query: the pattern of words, we will be seeking for ITS most similar part
    Text: a big pile of words, hope to get something similar to query in it
    length: 
    """
    pass