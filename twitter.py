'''Handles connection to Twitter API using Tweepy'''

from os import getenv
import tweepy
import spacy
from models import db, Tweet, User

from dotenv import load_dotenv

load_dotenv()

# Get API keys from .env
KEY = getenv('TWITTER_API_KEY')
SECRET = getenv('TWITTER_API_KEY_SECRET')

# Connect to the Twitter API
TWITTER_AUTH = tweepy.OAuthHandler(KEY, SECRET)
TWITER = tweepy.API(TWITTER_AUTH)

# Load our pretrained SpaCy Word Embeddings model
nlp = spacy.load('my_model/')

# Turn tweet text into word embeddings


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector

# function to query the API for a user and add the user to the db


def add_or_update_user(username):
    try:
        # get a twitter user from the API
        twitter_user = TWITER.get_user(screen_name=username)

        # Check to see if that user already exists in our db
        # If the user is already in the database, grab the user
        # If not, make a new user in the db
        db_user = (User.query.get(twitter_user.id)) or User(
            id=twitter_user.id, username=username)

        # add the user to the db if they don't already exist
        db.session.add(db_user)

        # Grab the recent tweets of our twitter_user
        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False,
                                       tweet_mode="extended", since_id=db_user.newest_tweet_id)

        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # add this individual tweets to the db session
        for tweet in tweets:
            tweet_vector = vectorize_tweet(tweet.text)
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text,
                             user_id=db_user.id, vect=tweet_vector)
            # make sure the tweet is connected to our user
            db_user.tweets.append(db_tweet)
            db.session.add(db_tweet)
    except Exception as e:
        print('Error processing {}: {}'.format(username, e))
        raise e

    else:
        # Commit a new save to the db
        db.session.commit()


def get_all_usernames():
    usernames = []
    Users = User.query.all()
    for user in Users:
        usernames.append(user.username)
    return usernames
