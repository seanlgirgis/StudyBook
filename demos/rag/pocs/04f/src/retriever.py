# src/retriever.py
import json
from pathlib import Path
from typing import List, Dict
import string
from difflib import SequenceMatcher

try:
    import Levenshtein  # pip install python-Levenshtein
except ImportError:  # pragma: no cover - runtime fallback
    Levenshtein = None
try:
    from nltk.stem import PorterStemmer
except ImportError:  # pragma: no cover - runtime fallback
    PorterStemmer = None

class SimpleRetriever:
    def __init__(self, knowledge_file: str, stopwords_file: str = None,
                 similarity_threshold: float = 0.75, match_fraction: float = 0.6):
        """
        knowledge_file: path to knowledge_base.json
        stopwords_file: optional path to JSON list of stopwords
        similarity_threshold: minimum ratio (0–1) for fuzzy token match
        match_fraction: minimum fraction of query tokens that must match
        """
        self.knowledge_file = Path(knowledge_file)
        if not self.knowledge_file.exists():
            raise FileNotFoundError(f"Knowledge base not found: {knowledge_file}")
        with self.knowledge_file.open("r", encoding="utf-8") as f:
            self.docs = json.load(f)

        # Load stopwords
        if stopwords_file:
            stopwords_path = Path(stopwords_file)
            if stopwords_path.exists():
                with stopwords_path.open("r", encoding="utf-8") as f:
                    self.stopwords = set(json.load(f))
            else:
                self.stopwords = set()
        else:
            self.stopwords = {"the", "a", "an", "service", "for", "of", "and", "on", "in", "with"}

        self.similarity_threshold = similarity_threshold
        self.match_fraction = match_fraction
        self.stemmer = PorterStemmer() if PorterStemmer is not None else None

    @staticmethod
    def _fallback_stem(token: str) -> str:
        for suffix in ("ing", "ed", "es", "s"):
            if token.endswith(suffix) and len(token) > len(suffix) + 2:
                return token[: -len(suffix)]
        return token

    @staticmethod
    def similarity_ratio(left: str, right: str) -> float:
        if Levenshtein is not None:
            return Levenshtein.ratio(left, right)
        return SequenceMatcher(None, left, right).ratio()

    def normalize_tokens(self, text: str) -> List[str]:
        """
        Split text into tokens, lowercase, strip punctuation, apply stemming
        """
        tokens = [t.lower().translate(str.maketrans('', '', string.punctuation))
                  for t in text.split() if t.strip(string.punctuation)]
        if self.stemmer is not None:
            return [self.stemmer.stem(t) for t in tokens]
        return [self._fallback_stem(t) for t in tokens]

    def retrieve(self, intent_text: str, top_k: int = 3) -> List[Dict]:
        """
        Retrieve documents matching intent_text using:
        - token normalization + stemming
        - stopwords removal
        - Levenshtein fuzzy matching
        - partial token fraction matching
        - both title and text checked
        """
        # Preprocess query tokens
        query_tokens = [t for t in self.normalize_tokens(intent_text) if t not in self.stopwords]
        if not query_tokens:
            return []

        results = []
        for doc in self.docs:
            # Normalize document tokens
            doc_tokens = self.normalize_tokens(doc.get("text", "") + " " + doc.get("title", ""))

            # Count how many query tokens match any doc token
            matched_tokens = 0
            for token in query_tokens:
                threshold = self.similarity_threshold
                if len(token) <= 6:
                    threshold = max(self.similarity_threshold - 0.1, 0.65)

                if any(self.similarity_ratio(token, doc_token) >= threshold for doc_token in doc_tokens):
                    matched_tokens += 1

            # Accept document if fraction of query tokens match
            if matched_tokens / len(query_tokens) >= self.match_fraction:
                results.append(doc)

            if len(results) >= top_k:
                break

        return results
