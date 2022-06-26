"""
COMP20008 Elements of Data Processing
2022 Semester 1
Assignment 1

Solution to Task 3
"""

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from utils import (
    read_articles,  # Returns a list of articles
)


def task3():

    articles = read_articles()
    publish_dates = [[article["news_id"], article["publish_date"]]
                     for article in articles
                     if article["publish_date"] is not None]
    for row in publish_dates:
        date = datetime.fromtimestamp(row[1])
        row[1:] = [date.year, date.month, date.day]
    publish_dates = pd.DataFrame(publish_dates, columns=[
                                 "news_id", "year", "month", "day"])
    publish_dates.set_index("news_id", inplace=True)

    # Save data frame to CSV
    publish_dates.sort_index().to_csv("task3a.csv")

    # Plot the number of articles published each year, and save to PNG
    publish_dates.groupby("year").count().month.plot.bar()
    plt.xlabel("Year", size=15)
    plt.ylabel("Number of articles", size=15)
    plt.xticks(rotation=0)
    plt.xticks(size=12)
    plt.yticks(size=12)
    plt.savefig("task3b.png", bbox_inches="tight")
    plt.close()

