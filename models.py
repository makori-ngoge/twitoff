from flask_sqlalchemy import SQLAlchemy

# creates our database
db = SQLAlchemy()

# Creates a 'user' table


class User(db.Model):
    # id column
    id = db.Column(db.BigInteger, primary_key=True)
    # username column
    username = db.Column(db.String(50), nullable=False)
    # keeps track of id for the latest tweet by the user
    newest_tweet_id = db.Column(db.BigInteger)

    def __repr__(self) -> str:
        return f'<User: {self.username}>'

# Create a 'tweet' table


class Tweet(db.Model):
    # id column
    id = db.Column(db.BigInteger, primary_key=True)
    # text column
    # Unicode allows for text, links, emojis etc
    text = db.Column(db.Unicode(300))

    # Create a relationsip between a tweet and a user
    user_id = db.Column(db.BigInteger, db.ForeignKey(
        'user.id'), nullable=False)

    # Finalizing the relationship making sure it goes both ways
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))
    # be able to include a word embedding on a tweet
    vect = db.Column(db.PickleType, nullable=False)

    def __repr__(self) -> str:
        return f'<User: {self.text}>'
