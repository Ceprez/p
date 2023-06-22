import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clubs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'supersecretkey'

db = SQLAlchemy(app)


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(5))
    club = db.Column(db.String(100), unique=True)
    points = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "group": self.group,
            "club": self.club,
            "points": self.points
        }


def add_clubs():
    url = "https://www.skysports.com/champions-league-table"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tables = soup.find_all("table", class_="standing-table__table")

    for table in tables:
        group = table.find('caption', {'class': 'standing-table__caption'}).text.strip()[30]
        rows = table.find_all("tr")
        print(group + '\n')
        for row in rows:
            cells = row.find_all("td")
            infos = []
            for cell in cells:
                info = cell.text.strip()
                if info != '':
                    infos.append(info)
            if len(infos) > 0:
                add_club = Club(club=infos[1], points=int(infos[-1]), group=group)
                db.session.add(add_club)
                db.session.commit()


@app.route('/')
def home():
    return "Flask App"


@app.route('/club/<club>')
def get_points_by_club(club):
    club_data = Club.query.filter_by(club=club).first()
    if club_data:
        return club_data.points
    else:
        return "Club not found in the database"


@app.route('/outsider/<group>')
def get_outsider(group):
    group_dominator = Club.query.filter_by(group=group).order_by(Club.points.desc()).first()
    group_outsider = Club.query.filter_by(group=group).order_by(Club.points).first()
    return f"Outsider is {group_outsider.club} with {group_outsider.points} points <br>" \
           f"Dominator is {group_dominator.club} with {group_dominator.points} points"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
