from transformers import pipeline
from sentence_transformers import SentenceTransformer
from config import QA_MODEL, SENTENCE_MODEL
from text_handling import TextPreprocessing
from scipy.spatial.distance import cosine
import numpy as np

def get_model_for_qa(model_name:str):
    return pipeline(task = 'question-answering',
              model=model_name,
              tokenizer=model_name)


def get_model_for_sentence_similarity(model_name:str):
    return SentenceTransformer(model_name)


def get_answer_from_text(qa_pipeline, q:str, context:str) -> str:
    prediction = qa_pipeline({
        "context" : context,
        "question" : q
    })

    return prediction['answer']


def get_most_similar_part(model, query:str, sentences:list) -> str:
    query_embed = model.encode([query])
    corpus_embed = model.encode(sentences)

    similarities = []

    for embedding in corpus_embed:
        similarities.append(1 - cosine(query_embed, embedding))

    similarities = np.array(similarities)

    best_index = np.argmax(similarities)
    best_part = sentences[best_index]
    
    return best_part
