"""
COMP20008 Elements of Data Processing
2022 Semester 1
Assignment 1

Solution to Task 5
"""

from matplotlib import pyplot as plt
import pandas as pd
import os
from utils import (
    read_tweets,  # Returns a dictionary of tweets
    read_reviews  # Returns a list of reviews
)


"""
COMP20008 Elements of Data Processing
2022 Semester 1
Assignment 1

Solution to Task 5
"""

from matplotlib import pyplot as plt
import pandas as pd
import os
from utils import (
    read_tweets,  # Returns a dictionary of tweets
    read_reviews
)


def task5():
    # The the tweets and reviews
    tweets = read_tweets()
    reviews = read_reviews()

    # [[news_id1, rating1, num_tweets1],...]
    rating_tweets_df = []

    for review in reviews:

        if "news_id" not in review or not review["news_id"]:
            continue

        if "rating" not in review:
            continue
        
        news_id, rating = review["news_id"], review["rating"]

        if news_id not in tweets:
            continue
        
        tweets_about_article = tweets[news_id]

        total_tweets = set()

        # These are tweets that contain the article's URL
        original_tweets = tweets_about_article["tweets"]
        total_tweets.update(original_tweets)

        # These are retweets about the article
        retweets = tweets_about_article["retweets"]
        total_tweets.update(retweets)

        # These are replies to tweets about the article
        replies = tweets_about_article["replies"]
        total_tweets.update(replies)

        rating_tweets_df.append([news_id, rating, len(total_tweets)])

    rating_tweets_df = pd.DataFrame(rating_tweets_df,
                                    columns=["news_id", "rating", "num_tweets"])

    tweet_means = rating_tweets_df.groupby("rating")["num_tweets"].mean()
    tweet_means.sort_index(inplace=True)

    # Plot article rating against avg number of tweets, and save to PNG
    plt.bar(tweet_means.index, tweet_means)
    plt.xlabel("Article rating", size=15)
    plt.ylabel("Average number of tweets", size=15)
    plt.savefig("task5.png", bbox_inches="tight")
    plt.close()
