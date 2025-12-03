from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
from collections import Counter
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm2

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/commits_data/")
def commits_data():
    url = "https://api.github.com/repos/zyxbya/5MCSI_Metriques/commits"

    response = urlopen(url)
    raw_content = response.read()
    json_content = json.loads(raw_content.decode("utf-8"))

    # On compte le nombre de commits par minute (0 à 59)
    minute_counter = Counter()

    for commit in json_content:
        date_str = commit.get("commit", {}).get("author", {}).get("date")
        if date_str:
            # Exemple de date : "2024-02-11T11:57:27Z"
            dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
            minute_counter[dt.minute] += 1

    # On renvoie un tableau de résultats pour toutes les minutes de 0 à 59
    results = []
    for minute in range(60):
        results.append({
            "minute": minute,
            "count": minute_counter.get(minute, 0)
        })

    return jsonify(results=results

@app.route("/commits/")
def commits():
    return render_template("commits.html")
  
if __name__ == "__main__":
  app.run(debug=True)
