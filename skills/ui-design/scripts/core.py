#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BM25 search engine for UI design tokens, guidelines, blueprints, and reference data."""

import argparse
import csv
import json
import re
from collections import defaultdict
from math import log
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DEFAULT_MAX_RESULTS = 3

CSV_CONFIG = {
    "style": {
        "file": "styles.csv",
        "search_cols": ["Style Category", "Type", "Keywords", "Best For"],
        "output_cols": [
            "Style Category",
            "Type",
            "Keywords",
            "Primary Colors",
            "Effects & Animation",
            "Best For",
            "Performance",
            "Accessibility",
            "AI Prompt Keywords",
            "CSS/Technical Keywords",
        ],
    },
    "color": {
        "file": "colors.csv",
        "search_cols": ["Product Type", "Keywords", "Notes"],
        "output_cols": [
            "Product Type",
            "Primary (Hex)",
            "Secondary (Hex)",
            "CTA (Hex)",
            "Background (Hex)",
            "Text (Hex)",
            "Border (Hex)",
            "Notes",
        ],
    },
    "blueprint": {
        "file": "blueprints.csv",
        "search_cols": ["Product Type", "Keywords", "Primary Style Recommendation", "Key Considerations"],
        "output_cols": [
            "Product Type",
            "Primary Style Recommendation",
            "Secondary Styles",
            "Landing Page Pattern",
            "Dashboard Style",
            "Color Palette Focus",
            "Key Considerations",
        ],
    },
    "pattern": {
        "file": "patterns.csv",
        "search_cols": ["Pattern Name", "Keywords", "Conversion Optimization"],
        "output_cols": [
            "Pattern Name",
            "Section Order",
            "Primary CTA Placement",
            "Color Strategy",
            "Recommended Effects",
            "Conversion Optimization",
        ],
    },
    "chart": {
        "file": "charts.csv",
        "search_cols": ["Data Type", "Keywords", "Best Chart Type"],
        "output_cols": [
            "Data Type",
            "Best Chart Type",
            "Secondary Options",
            "Color Guidance",
            "Performance Impact",
            "Accessibility Notes",
            "Library Recommendation",
        ],
    },
    "icon": {
        "file": "icons.csv",
        "search_cols": ["Category", "Icon Name", "Keywords", "Usage", "Best For"],
        "output_cols": [
            "Category",
            "Icon Name",
            "Library",
            "Import Code",
            "Usage",
            "Best For",
        ],
    },
    "ux": {
        "file": "ux-guidelines.csv",
        "search_cols": ["Category", "Issue", "Description", "Do", "Don't"],
        "output_cols": [
            "Category",
            "Issue",
            "Platform",
            "Description",
            "Do",
            "Don't",
            "Code Example Good",
            "Severity",
        ],
    },
    "web": {
        "file": "web-standards.csv",
        "search_cols": ["Category", "Issue", "Keywords", "Description", "Do", "Don't"],
        "output_cols": [
            "Category",
            "Issue",
            "Platform",
            "Description",
            "Do",
            "Don't",
            "Code Example Good",
            "Severity",
        ],
    },
}


class BM25:
    """Okapi BM25 ranking algorithm."""

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus: list[list[str]] = []
        self.doc_lengths: list[int] = []
        self.avgdl: float = 0.0
        self.idf: dict[str, float] = {}
        self.doc_freqs: dict[str, int] = defaultdict(int)
        self.n_docs: int = 0

    def tokenize(self, text: str) -> list[str]:
        """Tokenize text into lowercase words, preserving 2+ character terms (e.g. ui, ux, 3d, ai)."""
        text = re.sub(r"[^\w\s]", " ", str(text).lower())
        return [w for w in text.split() if len(w) >= 2]

    def fit(self, documents: list[str]) -> None:
        """Fit BM25 parameters over a list of document strings."""
        self.corpus = [self.tokenize(doc) for doc in documents]
        self.n_docs = len(self.corpus)
        if self.n_docs == 0:
            return
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avgdl = sum(self.doc_lengths) / self.n_docs
        for doc in self.corpus:
            seen = set()
            for word in doc:
                if word not in seen:
                    self.doc_freqs[word] += 1
                    seen.add(word)
        for word, freq in self.doc_freqs.items():
            self.idf[word] = log((self.n_docs - freq + 0.5) / (freq + 0.5) + 1.0)

    def score(self, query: str) -> list[tuple[int, float]]:
        """Score all documents against query string."""
        query_tokens = self.tokenize(query)
        scores = []
        for idx, doc in enumerate(self.corpus):
            score = 0.0
            doc_len = self.doc_lengths[idx]
            term_freqs: dict[str, int] = defaultdict(int)
            for word in doc:
                term_freqs[word] += 1
            for token in query_tokens:
                if token in self.idf:
                    tf = term_freqs[token]
                    idf = self.idf[token]
                    num = tf * (self.k1 + 1.0)
                    den = tf + self.k1 * (1.0 - self.b + self.b * doc_len / (self.avgdl or 1.0))
                    score += idf * num / den
            scores.append((idx, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)


def search(query: str, domain: str = "style", max_results: int = DEFAULT_MAX_RESULTS) -> dict:
    """Search reference dataset by domain using BM25 retrieval."""
    if domain not in CSV_CONFIG:
        return {
            "error": f"Invalid domain: '{domain}'. Available domains: {list(CSV_CONFIG.keys())}",
            "domain": domain,
        }

    config = CSV_CONFIG[domain]
    filepath = DATA_DIR / config["file"]
    if not filepath.exists():
        return {"error": f"Dataset file not found: {filepath}", "domain": domain}

    with open(filepath, mode="r", encoding="utf-8") as f:
        data = list(csv.DictReader(f))

    if not data:
        return {"domain": domain, "query": query, "count": 0, "results": []}

    documents = [
        " ".join(str(row.get(col, "")) for col in config["search_cols"])
        for row in data
    ]

    engine = BM25()
    engine.fit(documents)
    ranked = engine.score(query)

    output_cols = config.get("output_cols")
    results = []
    for idx, score in ranked:
        if score <= 0:
            continue
        row = data[idx]
        if output_cols:
            filtered_row = {col: row.get(col, "") for col in output_cols if col in row}
            filtered_row["_score"] = round(score, 3)
            results.append(filtered_row)
        else:
            row_copy = dict(row)
            row_copy["_score"] = round(score, 3)
            results.append(row_copy)
        if len(results) >= max_results:
            break

    return {
        "domain": domain,
        "query": query,
        "count": len(results),
        "results": results,
    }


def main():
    import sys
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="CLI BM25 search engine for UI design tokens, styles, palettes, blueprints, and guidelines."
    )
    parser.add_argument("query", help="Search query string (e.g., 'minimalist landing', 'coffee shop', 'saas')")
    parser.add_argument(
        "--domain",
        default="style",
        choices=list(CSV_CONFIG.keys()),
        help=f"Dataset domain to query. Choices: {', '.join(CSV_CONFIG.keys())} (default: style)",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=DEFAULT_MAX_RESULTS,
        help=f"Maximum number of results to return (default: {DEFAULT_MAX_RESULTS})",
    )
    args = parser.parse_args()

    results = search(args.query, domain=args.domain, max_results=args.max)
    print(json.dumps(results, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
