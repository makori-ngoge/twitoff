from models import User
from twitter import vectorize_tweet
from sklearn.linear_model import LogisticRegression
import numpy as np


def predict_user(username0, username1, hypo_tweet_text):

    # Query our two users
    user0 = User.query.filter(User.username == username0).one()
    user1 = User.query.filter(User.username == username1).one()

    # Get the tweet vectorizations
    uservects0 = np.array
    uservects1 = np.array

    # Combine the vectors into an X matrix
    X = np.vstack([uservects0, uservects1])

    # Generate labels and 0s and 1s for a y vector
    y = np.concatenate(np.zeros(len(user0.tweets)), np.ones(len(user1.tweets)))

    # fit our Logistic regression model
    log_reg = LogisticRegression().fit(X, y)

    # vectorize our hypothetical tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    # return the predicted label: (0 or 1)
    return log_reg.predict(hypo_tweet_vect.reshape(1, -1))
