"""
COMP20008 Elements of Data Processing
2022 Semester 1
Assignment 1

Solution to Task 7
"""
import json
import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from utils import (
    read_articles,  # Returns a list of articles
)


def task7():

    # Read the articles
    articles = read_articles()

    # Read the tokenised articles
    assert os.path.isfile("task6.json"), "Task 6's JSON output not found."
    with open("task6.json", "r") as f:
        token_to_articles = json.load(f)

    # Read the merged data frame for articles and reviews
    assert os.path.isfile("task2.csv"), "Task 2's CSV output not found."
    merged_df = pd.read_csv("task2.csv", index_col="news_id")

    num_real = merged_df[merged_df.rating >= 3].shape[0]
    num_fake = merged_df[merged_df.rating < 3].shape[0]
    num_articles = merged_df.shape[0]
    assert num_real + num_fake == num_articles

    def count_real_fake(news_ids):
        """
        Take a list of news IDs and return the count of
        real and fake articles
        """
        sub_df = merged_df.loc[news_ids]
        num_real = sub_df[sub_df.rating >= 3].shape[0]
        num_fake = sub_df[sub_df.rating < 3].shape[0]
        assert num_real + num_fake == len(news_ids)
        return num_real, num_fake

    # Count the number of real and fake articles containing each word
    real_fake_tally = pd.DataFrame(columns=["real", "fake"], index=[],
                                   dtype=np.float32)
    for token, news_ids in token_to_articles.items():

        # Remove word that appear in fewer than 10 articles and those that
        # appear in all articles
        if len(news_ids) < 10 or len(news_ids) >= num_articles:
            continue

        real, fake = count_real_fake(news_ids)

        # Remove words that are exclusive to real or fake articles
        if real <= 0 or fake <= 0:
            continue

        real_fake_tally.loc[token, "real"] = real
        real_fake_tally.loc[token, "fake"] = fake

    # Log odds ratio
    p_f = real_fake_tally["fake"] / num_fake
    o_f = p_f / (1 - p_f)
    p_r = real_fake_tally["real"] / num_real
    o_r = p_r / (1 - p_r)
    log_odds_ratios = pd.Series(data=np.log10(o_f / o_r),
                                index=real_fake_tally.index,
                                name="log_odds_ratio")
    log_odds_ratios.index.name = "word"
    log_odds_ratios = log_odds_ratios.sort_values()

    # Save to csv
    log_odds_ratios.sort_index().round(5).to_csv("task7a.csv")

    plt.figure(figsize=(5, 5))
    plt.axvline(x=log_odds_ratios.mean(), c="red", alpha=0.8)
    plt.hist(log_odds_ratios, bins=50, alpha=0.6,
             weights=np.ones_like(log_odds_ratios) / len(log_odds_ratios))
    plt.xlabel("$log_{10}$ odds ratio (fake / real)", size=20)
    plt.xticks(size=10)
    plt.ylabel("Probability", size=20)
    plt.yticks(size=10)
    plt.annotate(xy=(0, 0.1),
                 text=f"$\mu = {log_odds_ratios.mean() : .2f}$\n"
                 f"$\sigma = {log_odds_ratios.std() : .2f}$",
                 size=15, va="center", ha="left")
    plt.savefig("task7b.png", bbox_inches="tight")
    plt.close()

    num_words = 15
    df = log_odds_ratios[:num_words]
    df = pd.concat([df, log_odds_ratios[-num_words:]])

    ax = df.plot.barh(y="or", figsize=(6, 8),
                      color=(df > 0).map({True: 'r', False: 'b'}),
                      legend=None)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.xlabel("$log_{10}$ odds ratio (fake vs. real news)", size=15)
    plt.ylabel("")
    plt.xticks(size=12)
    plt.yticks(size=12)
    plt.grid("y", alpha=0.3)
    colors = {"Fake news": "r", "Real news": "b"}
    handles = [plt.Rectangle((0, 0), 1, 1, color=colors[label])
               for label in colors]
    plt.legend(handles, colors.keys(), prop={'size': 13},
               bbox_to_anchor=(0.4, 0.5))

    labels = ax.get_yticklabels()
    for label in labels:
        text = label.get_text()
        _, y = label.get_position()
        alignment = "right" if df[text] > 0 else "left"
        hspace = 0.02 * (1 if alignment == "left" else -1)
        ax.text(x=0 + hspace, y=y, s=text, ha=alignment, va="center", size=12)

    ax.set_yticks([])

    plt.savefig("task7c.png", bbox_inches="tight")
    plt.close()

