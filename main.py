from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from configparser import ConfigParser

ini_file = ConfigParser()
ini_file.read("config/pages.ini")
key = ini_file.get("pages", "key")

app = Flask(__name__)
app.secret_key = key
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def index():
    URL = "https://www.emag.ro/search/ariel?ref=trending"
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    out = soup.find_all(class_="card-v2-info")
    links: list[dict[str, str]] = []
    limit = 5
    for item in out:
        if (limit := limit - 1) == 0:
            break
        current = BeautifulSoup(bytes(str(item), "utf-8"), "html.parser")
        link = current.find(class_="card-v2-thumb")
        if not isinstance(link, Tag):
            continue
        link = link["href"]

        title = requests.get(str(link))
        title_name = BeautifulSoup(title.content, "html.parser")
        title_text = title_name.find(class_="page-title")
        if title_text is not None:
            links.append({title_text.text.strip(): str(link)})

    return render_template("index.html", links=links)


if __name__ == "__main__":
    app.run(port=80)
