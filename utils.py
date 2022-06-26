"""
COMP20008 Elements of Data Processing
2022 Semester 1
Assignment 1

Utility functions
"""

import json
import os


def read_one_article(path):
    """
    Open a file for an article and return a dictionary for the article.
    """
    article_filename = os.path.split(path)[-1]

    with open(path, "r") as f:
        article = json.load(f)
        article["news_id"] = article_filename[:-5]

    return article


def read_articles():
    """
    Open the dataset/content/HealthStory folder, read all the json files and
    return a list of articles.
    """

    # Each article is a JSON file, so we iterate over all files in
    # the directory
    articles = []

    for article_filename in os.listdir(os.path.join("/", "course", "data", "a1", 
                                                    "content",
                                                    "HealthStory")):
        article_path = os.path.join("/", "course", "data", "a1",
                                    "content", "HealthStory", article_filename)
        article = read_one_article(article_path)
        articles.append(article)

    return articles


def read_reviews():
    """
    Open the data/reviews/HealthStory.json file, and return a list of reviews.
    """

    # All reviews are stored in the same JSON file
    reviews_path = os.path.join("/", "course", "data", "a1",
                                "reviews", "HealthStory.json")
    with open(reviews_path, "r") as f:
        reviews = json.load(f)

    # OPTIONAL: To shorten the criteria's descriptions, we map each one to a code.
    descr_to_code = {
        'Does the story compare the new approach with existing alternatives?': 'c1',
        'Does the story adequately explain/quantify the harms of the intervention?': 'c2',
        'Does the story seem to grasp the quality of the evidence? ': 'c3',
        'Does the story adequately quantify the benefits of the treatment/test/product/procedure?': 'c4',
        'Does the story establish the true novelty of the approach?': 'c5',
        'Does the story establish the availability of the treatment/test/product/procedure?': 'c6',
        'Does the story commit disease-mongering?': 'c7',
        'Does the story adequately discuss the costs of the intervention?': 'c8',
        'Does the story use independent sources and identify conflicts of interest?': 'c9',
        'Does the story appear to rely solely or largely on a news release?': 'c10'
    }

    for review in reviews:
        criteria = review["criteria"]

        # Format of criteria_abbr:
        # {"c1": "Satisfactory", "c2": "Not Satisfactory",...}
        criteria_abbr = dict()
        for criterion in criteria:
            criteron_abbr = descr_to_code[criterion["question"]]
            answer = criterion["answer"]
            criteria_abbr[criteron_abbr] = answer
        review["criteria"] = criteria_abbr

    return reviews


def read_tweets():
    """
    Open the data/engagements/HealthStory.json file, and return a dictionary of tweets.
    """

    tweets_path = os.path.join("/", "course", "data", "a1",
                               "engagements", "HealthStory.json")
    with open(tweets_path, "r") as f:
        tweets = json.load(f)

    return tweets

