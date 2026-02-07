from __future__ import annotations

import os
import uuid
from dataclasses import dataclass
from typing import Dict, List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class MatchResult:
    category: str
    solution: str
    department: str
    location: str
    confidence: float


class HybridAIEngine:
    def __init__(self, data_file: str):
        if not os.path.exists(data_file):
            self.df = pd.DataFrame(
                [{"text": "water leakage", "category": "Water", "solution": "Raise BBMP water complaint", "department": "BWSSB", "location": "Bengaluru", "resolved_status": "yes"}]
            )
        else:
            self.df = pd.read_csv(data_file)
        required = {"text", "category", "solution", "department", "location", "resolved_status"}
        missing = required - set(self.df.columns)
        if missing:
            raise ValueError(f"Missing dataset columns: {missing}")
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
        self.text_vectors = self.vectorizer.fit_transform(self.df["text"].astype(str).tolist())

    def match(self, query: str) -> MatchResult:
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.text_vectors).flatten()
        idx = int(sims.argmax())
        row = self.df.iloc[idx]
        return MatchResult(
            category=str(row["category"]),
            solution=str(row["solution"]),
            department=str(row["department"]),
            location=str(row["location"]),
            confidence=float(sims[idx]),
        )

    def top_similar(self, query: str, k: int = 3) -> List[str]:
        qv = self.vectorizer.transform([query])
        sims = cosine_similarity(qv, self.text_vectors).flatten()
        top_idx = sims.argsort()[-k:][::-1]
        return [self.df.iloc[int(i)]["text"] for i in top_idx]

    def predict_severity(self, query: str) -> float:
        urgency_terms = ["urgent", "danger", "flood", "fire", "accident", "blocked", "no water"]
        text = query.lower()
        score = 0.2 + sum(0.12 for term in urgency_terms if term in text)
        return round(min(score, 1.0), 2)


def build_tracking_id() -> str:
    return f"CIV-{uuid.uuid4().hex[:10].upper()}"
