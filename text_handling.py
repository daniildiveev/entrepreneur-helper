import numpy as np
import re
import pymorphy2
from tqdm import tqdm, trange
import nltk
nltk.download("punkt")
from nltk.tokenize import word_tokenize, wordpunct_tokenize

class TextPreprocessing:
    def __init__(self, corpus:list) -> None:
        self.corpus = corpus

    def remove_punctuation(self) -> list:
        for i in range(len(self.corpus)):
            self.corpus[i] = self.corpus[i].lower()
            self.corpus[i] = re.findall(r'\w+', self.corpus[i]) #regex for removing any punctuation
            self.corpus[i] = ' '.join(self.corpus[i])

        return self.corpus

    def preprocess_html(self, corpus:list) -> list:
        for i in range(len(corpus)):
            self.corpus[i] = str(self.corpus[i]).replace('[', '').replace(']', '')
            self.corpus[i] = re.sub(r"<.*?>", "", self.corpus[i])
            self.corpus[i] = re.sub(r"[a-zA-Z]", " ", self.corpus[i])
            self.corpus[i] = re.sub(r"[{}]|[()]", " ", self.corpus[i])
            self.corpus[i] = re.sub(r"\xa0|\n", " ", self.corpus[i])
            self.corpus[i] = re.sub(r"\s+", " ", self.corpus[i])

        return self.corpus

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
        self.corpus = self.punctuation()
        self.corpus = self.lemmatize()

        return self.corpus

    def extract_key_words(self):
        model = KeyBERT()
        keywords = []

        for i in range(len(self.corpus)):
            keywords.extend(model.extract_keywords(self.corpus[i]))

        return keywords


def find_most_relevant_part(query:str, 
                            text:str,
                            step:int, ) -> str:
    """
    Query: the pattern of words, we will be seeking for ITS most similar part
    Text: a big pile of words, hope to get something similar to query in it
    length: the length of
    """
    empty_token = '<ET>'
    stop_tokens = [empty_token] + list(',.!?')

    handler = TextPreprocessing([query])
    query = handler.remove_punctuation()[0]

    query_tokens = tuple(wordpunct_tokenize(query))
    text_tokens = word_tokenize(text)

    part_len = len(query_tokens)

    while len(text_tokens) % part_len != 0:
        text_tokens.extend([empty_token])

    max_sim_tokens = 0
    sim_tokens = 0
    best_part = ''

    for i in range(0, len(text_tokens) - step,):
        tokens = text_tokens[i:i+step]

        for token in tokens:
            if token in query_tokens and token not in stop_tokens:
                sim_tokens += 1

        if sim_tokens >= max_sim_tokens:
            max_sim_tokens = sim_tokens
            best_part = tokens

        sim_tokens = 0

    while empty_token in best_part:
        best_part.remove(empty_token)

    best_part = ' '.join(best_part)

    return best_part, max_sim_tokens