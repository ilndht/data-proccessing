"""
COMP20008 Elements of Data Processing
2022 Semester 1
Assignment 1

Solution to Task 6
"""

from utils import (
    read_articles,     # Returns a list of articles
)
import json
import os
from nltk.corpus import stopwords
import re
from collections import defaultdict, OrderedDict
stop_words = stopwords.words('english')


def preprocess(text):
    # Remove non-alphabetic and non-space characters
    pattern = r"[^a-zA-Z\s]"
    text = re.sub(pattern=pattern, string=text, repl=" ")

    # Replace all spaces into whitespace
    pattern = r"\s"
    text = re.sub(pattern=pattern, string=text, repl=" ")

    # Ensure only one whitespace between every two tokens
    text = " ".join(text.split())

    # Lowercase all characters
    text = text.lower()

    # Tokenise
    text = text.split()

    # Remove stopwords
    text = list(filter(lambda x: x not in stop_words, text))

    # Remove single-character tokens
    text = list(filter(lambda x: len(x) > 1, text))

    return text


def task6():
    articles = read_articles()
    token_to_articles = defaultdict(list)
    for article in articles:
        news_id = article["news_id"]
        text = article["text"]
        # Preprocess text
        tokens = preprocess(text)

        # Record article for each token
        for token in tokens:
            if news_id not in token_to_articles[token]:
                token_to_articles[token].append(news_id)

    # Sort the keys
    token_to_articles = OrderedDict(sorted(token_to_articles.items()))

    with open("task6.json", "w") as f:
        json.dump(token_to_articles, f)

