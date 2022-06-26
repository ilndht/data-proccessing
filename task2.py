"""
COMP20008 Elements of Data Processing
2022 Semester 1
Assignment 1

Solution to Task 2
"""

import pandas as pd
from utils import (
    read_articles,  # Returns a list of articles
    read_reviews,   # Returns a list of reviews
)


def extract_review_info(review):
    num_satisfactory = 0
    for criterion, answer in review["criteria"].items():
        num_satisfactory += answer.lower() == "satisfactory"
    return {
        "review_title": review["title"],
        "rating": review["rating"],
        "num_satisfactory": num_satisfactory
    }


def task2():
    articles = read_articles()
    reviews = read_reviews()

    merged_df = pd.DataFrame(columns=["news_id", "news_title", "review_title",
                                      "rating", "num_satisfactory"])
    merged_df.set_index("news_id", inplace=True)

    for article in articles:
        article_id = article["news_id"]

        # Find the review matching this article ID
        review = next(filter(lambda x: x["news_id"] == article_id,
                             reviews))
        row = [article["title"]]
        review_info = extract_review_info(review)
        row.extend([review_info["review_title"],
                    review_info["rating"],
                    review_info["num_satisfactory"],])
        merged_df.loc[article_id] = row
    
    # Save output to CSV
    merged_df.index.name = "news_id"
    merged_df.sort_index().to_csv("task2.csv")
    
