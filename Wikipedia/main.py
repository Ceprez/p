import requests
from bs4 import BeautifulSoup
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///countries.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = 'supersecretkey'

db = SQLAlchemy(app)


class CountryPopulation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100))
    population = db.Column(db.String(100))


@app.route('/')
def home():
    return "Flask App"


def populate_database():
    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find('table', {'class': 'wikitable sortable'})

    if table:
        rows = table.find_all('tr')
        with app.app_context():
            for row in rows:
                name = row.find('a')
                populations = row.find_all('td')
                pop = []
                if name:
                    name = name.text.strip()
                    if name != 'Country' and name != '[3]':
                        print(name)
                        for population in populations:
                            pop.append(population.text.strip())
                            if len(pop) != 6:
                                continue
                            elif pop[1] == 'World':
                                continue
                            print(pop[1])
                            country_population = CountryPopulation(country=name, population=pop[1])
                            db.session.add(country_population)
                            db.session.commit()


@app.route('/<country>')
def get_population_by_country(country):
    population_data = CountryPopulation.query.filter_by(country=country).first()
    if population_data:
        return population_data.population
    else:
        return "Country not found in the database"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        get_population_by_country('China')
    app.run()
