import sqlite3 as lite
from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

conn = lite.connect('flatmates_data.db')

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/about')
def about():
    return 'The about page'

@app.route('/projects/')
def projects():
    return 'The project page'


@app.route("/basic_top_suburb_view")
def basic_top_suburb_view():
    query = """ SELECT suburb, SUM(rooms_available),
            price/rooms_available as pr 
            FROM flatmates_rent_listings GROUP BY suburb ORDER BY pr DESC LIMIT 10;"""
    df = pd.read_sql_query(query,conn)

if __name__ == "__main__":
    app.run(debug=True)
