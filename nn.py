from transformers import pipeline
from sentence_transformers import SentenceTransformer
from config import QA_MODEL, SENTENCE_MODEL
from text_handling import TextPreprocessing
from scipy.spatial.distance import cosine
import numpy as np

def get_model_for_qa(model_name:str):
    return pipeline(task = 'question-answering',
              model=model_name,
              tokenizer=model_name
              )

def get_model_for_sentence_similarity(model_name:str):
    return SentenceTransformer(model_name)

def get_answer_from_text(qa_pipeline, q:str, context:str) -> str:
    prediction = qa_pipeline({
        "context" : context,
        "question" : q
    })

    return prediction['answer']

def embed_similatiry(query:str, embeddings:list):
    cosine_similarities = []

    for i in range(len(embeddings)):
        cosine_similarities.append(1 - cosine(query, embeddings[i]))

    return cosine_similarities

def get_most_similar_part(model, query:str, sentences:list) -> str:
    preprocessing = TextPreprocessing([query] + sentences)
    preprocessing.full_preprocessing()

    
    query = preprocessing.corpus[0]
    corpus = preprocessing.corpus [1:]

    query_embed = model.encode([query])
    corpus_embed = model.encode(corpus)

    similarities = np.array(embed_similatiry(query, corpus_embed))

    best_index = np.argmax(similarities)
    max_similarity = similarities[best_index]
    best_part = sentences[best_index]

    return best_part, max_similarity
