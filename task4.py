"""
COMP20008 Elements of Data Processing
2022 Semester 1
Assignment 1

Solution to Task 4
"""


from matplotlib import pyplot as plt
import pandas as pd
from utils import (
    read_reviews,  # Returns a list of reviews
)


def task4():
    reviews = read_reviews()

    reviews_df = pd.DataFrame(columns=["news_source", "rating"])
    reviews_df.index.name = "news_id"
    for review in reviews:
        if review["news_source"] == "":
            continue
        reviews_df.loc[review["news_id"]] = [review["news_source"],
                                             review["rating"]]
    reviews_df["rating"] = reviews_df["rating"].astype(int)

    task4_df = reviews_df.groupby("news_source").count()
    task4_df.columns = ["num_articles"]
    task4_df["avg_rating"] = reviews_df.groupby("news_source").mean()

    # Sort by news_source
    task4_df = task4_df.sort_values("news_source")

    # Save data frame to CSV
    task4_df.to_csv("task4a.csv")

    # Plot the average rating of news sources with at least 5 articles
    task4_df_min5 = task4_df[task4_df.num_articles >= 5]
    task4_df_min5 = task4_df_min5.sort_values("avg_rating")
    task4_df_min5.plot.barh(y="avg_rating",
                            figsize=(5, 10),
                            legend=None)
    plt.yticks()
    plt.xlabel("Average rating", size=15)
    plt.ylabel("News source", size=15)
    plt.xticks(size=12)
    plt.yticks(size=12)
    plt.savefig("task4b.png", bbox_inches="tight")
    plt.close()

