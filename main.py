from flask import Flask, request, render_template_string
from meteo import getWeather

app = Flask(__name__)

# HTML-Template für die Eingabeseite
form_template = """
<!doctype html>
<html>
    <head>
        <title>Addition</title>
    </head>
    <body>
        <h1>Geben Sie die Koordinaten für den Wetterbericht ein:</h1>
        <form action="/result" method="post">
            <label for="num1">Latitude:</label>
            <input type="number" id="num1" name="num1" step="0.01" required>
            <br><br>
            <label for="num2">Longitude:</label>
            <input type="number" id="num2" name="num2" step="0.01" required>
            <br><br>
            <button type="submit">Wetterbericht</button>
        </form>
    </body>
</html>
"""

# HTML-Template für die Ergebnisseite
result_template = """
<!doctype html>
<html>
    <head>
        <title>Ergebnis</title>
    </head>
    <body>
        Die Höhe beträgt {{ elevation }} m<br>
        Die Temperatur beträgt: {{ temperature }}<br>
        <a href="/">Zurück</a>
    </body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(form_template)

@app.route("/result", methods=["POST"])
def result():
    try:
        latitude = float(request.form["num1"])
        longitude = float(request.form["num2"])
        response = getWeather(latitude, longitude)
        current = response.Current()
        elevation = response.Elevation()
        result = current.Variables(0).Value()
    except ValueError:
        result = "Ungültige Eingabe!"
    return render_template_string(result_template, temperature=result, elevation=elevation)

if __name__ == "__main__":
    app.run(debug=True)
