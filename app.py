from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
mongo = PyMongo(app, uri='mongodb://127.0.0.1:5000/mars_app')

@app.route('/')
def home():
    mars_data = mongo.db.mars_info.find_one()
    return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scrape():
    mars_data_scrape = scrape_mars.scraper()
    mongo.db.mars_info.update({}, mars_data_scrape, upsert=True)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)