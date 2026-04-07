from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.sample_data import ensure_corpus


TOPIC_QUERIES = {
    "course_objectives": "What are the main learning goals and outcomes of the course?",
    "weekly_plan": "How is the course structured over the weeks and modules?",
    "deliverables": "What do students need to submit and how should the work be structured?",
    "study_strategy": "How should students prepare, review, and manage study time?",
    "evaluation_focus": "What should students know about evaluation metrics and rubric expectations?",
}


def retrieve_for_topic(base_dir: str | Path, topic_query: str, top_k: int = 2) -> list[dict]:
    dataset = ensure_corpus(base_dir)
    corpus = pd.read_csv(dataset["corpus_path"])
    search_text = corpus["title"].fillna("") + " " + corpus["section_title"].fillna("") + " " + corpus["content"].fillna("")

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    matrix = vectorizer.fit_transform(search_text)
    query_vector = vectorizer.transform([topic_query])
    similarities = cosine_similarity(query_vector, matrix).ravel()

    corpus = corpus.copy()
    corpus["similarity"] = similarities
    ranked = corpus.sort_values("similarity", ascending=False).head(top_k)

    return [
        {
            "doc_id": row.doc_id,
            "module": row.module,
            "title": row.title,
            "section_title": row.section_title,
            "content": row.content,
            "similarity": round(float(row.similarity), 4),
        }
        for row in ranked.itertuples(index=False)
    ]
