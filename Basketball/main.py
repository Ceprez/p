import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nba.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'supersecretkey'

db = SQLAlchemy(app)


class Nba(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.String(5), unique=True)
    points = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "team": self.team,
            "points": self.points
        }


def add_nba():
    url = "https://www.basketball-reference.com/playoffs/NBA_2023.html"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {'id': 'totals-team'}).tbody
    rows = table.find_all('tr')
    for row in rows:
        name = row.find("td", {"data-stat": "team"}).text.strip()
        points = row.find("td", {"data-stat": "pts"}).text.strip()
        if len(points) == 0:
            points = 0
        add_team = Nba(team=name, points=int(points))
        db.session.add(add_team)
        db.session.commit()


@app.route('/')
def index():
    try:
        add_nba()
        return "successfully added"
    except:
        return "not added"


@app.route('/<team>')
def get_points_by_club(team):
    club_data = Nba.query.filter_by(team=team).first()
    if club_data:
        return f"{club_data.id} id of {club_data.team} has {club_data.points} points"
    else:
        return f"{team} not found in the database"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()