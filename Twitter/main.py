from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twitter.db'
db = SQLAlchemy(app)

class Tweet(db.Model):
    __tablename__ = 'sports'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    description = db.Column(db.String(250))
    author = db.Column(db.String(30))
    upload_date = db.Column(db.String(15))
    edit_date = db.Column(db.String(15))
    likes = db.Column(db.Integer)

# curl -X GET -H "Content-Type: application/json" http://127.0.0.1:5000/api
@app.route("/api", methods=['GET'])
def get_tweets():
    tweets = Tweet.query.all()
    tweet_list = []
    for tweet in tweets:
        tweet_list.append({'id': tweet.id, 'title': tweet.title, 'description': tweet.description, 'author': tweet.author, 'upload_date': tweet.upload_date, 'edit_date': tweet.edit_date, 'likes': tweet.likes})
    return jsonify(tweet_list)

# curl -X POST -H "Content-Type: application/json" -d '{"title": "Trump Dead", "description": "Oh no He Dead", "author": "Maisa", "upload_date": "23/03/2021", "edit_date": "20/05/2022", "likes": 202}' http://127.0.0.1:5000/api
@app.route("/api", methods=['POST'])
def create_tweet():
    data = request.get_json()
    title = data["title"]
    description = data["description"]
    author = data["author"]
    upload_date = data["upload_date"]
    edit_date = data["edit_date"]
    likes = data["likes"]
    tweet = Tweet(title=title, description=description, author=author, upload_date=upload_date, edit_date=edit_date, likes=likes)
    db.session.add(tweet)
    db.session.commit()
    return "Created tweet"

# curl -X PUT -H "Content-Type: application/json" -d '{"title": "Trump Dead", "description": "Oh no He Dead but like dead daeadaew addadwadjnkdcs", "author": "Revaz Cicqishvili", "upload_date": "23/03/2021", "edit_date": "20/05/2022", "likes": 69}' http://127.0.0.1:5000/api/1
@app.route("/api/<int:id>", methods=['PUT'])
def edit_tweet(id):
    data = request.get_json()
    title = data["title"]
    description = data["description"]
    author = data["author"]
    upload_date = data["upload_date"]
    edit_date = data["edit_date"]
    likes = data["likes"]
    tweet = Tweet.query.get(id)
    if tweet is not None:
        tweet.title = title
        tweet.description = description
        tweet.author = author
        tweet.upload_date = upload_date
        tweet.edit_date = edit_date
        tweet.likes = likes
        db.session.commit()
        return "Edited", 200

# curl -X DELETE http://127.0.0.1:5000/api/1
@app.route("/api/<int:id>", methods=['Delete'])
def delete_tweet(id):
    tweet = Tweet.query.get(id)
    db.session.delete(tweet)
    db.session.commit()
    return "deleted", 200


with app.app_context():
    db.create_all()
    app.run()