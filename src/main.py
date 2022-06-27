from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from configparser import ConfigParser
from scraper.emag_scraper import EmagScraper

ini_file = ConfigParser()
ini_file.read("config/pages.ini")
key = ini_file.get("pages", "key")

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = key
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    links = []
    if request.method == "POST":
        scraper = EmagScraper("https://www.emag.ro/search/", request.form["user-prompt"])
        results = scraper.get_results()
        for result in results:
            links.append(scraper.get_details(result))

    return render_template("index.html", links=links)


if __name__ == "__main__":
    app.run(port=80)
