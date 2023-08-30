import os
import requests
import time
import random
import datetime

from datetime import datetime
from threading import Timer
from bs4 import BeautifulSoup
from flask import Flask, request


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Where my bot for Montgomery Hall lives :) - Jason, implementing SSL soon"


# print() are in the log file
@app.route("/", methods=["POST"])
def receive():
    print("Incoming message:")
    data = request.get_json()
    print(data)

    # prevent self-reply
    if data["sender_type"] != "RA BOT":
        read(data["text"].lower())

        if data["text"].startswith("/ping"):
            send(data["name"] + " pinged me!")

    return "ok", 200


def goodMorning():
    send("Good Morning Montgomery Hall")


def showMenu():
    return """RA BOT MENU: \n
             Type in a command! \n
             Pick a num between 1-10: /pick \n
             Flip a coin: /flip \n
             Phone Numbers: /numbers \n"""


# scrapes data from umd dining menu
def getFood():
    page = requests.get("http://nutrition.umd.edu/")  # not secured smh
    soup = BeautifulSoup(page.content, "html.parser")
    elements = soup.find_all("a")
    food = set()

    for i in range(12, len(elements)):
        item = str(elements[i])
        item = item[item.find(">") + 1 :].replace(
            "</a>", ""
        )  # locate food, and remove tags

        # don't add the leftover tags
        if not (
            item.startswith(" <span") or item.startswith("(") or item.startswith("http")
        ):
            food.add(item)

    f = open("food.txt", "w")
    for item in food:
        f.write(item + "\n")

    return food


def chicken_tenders(food):
    if "Chicken Tenders" in food:
        return True
    return False


def read(msg):
    text = msg.split(" ")

    if msg == "/menu":
        send(showMenu())
    elif msg == "/pick":
        send(str(random.randint(1, 10)))
    elif msg == "/flip":
        toss = random.randint(1, 2)
        if toss == 1:
            send("tails")
        else:
            send("heads")
    elif msg == "/numbers":
        send(
            """Jason: 240-340-3777\n
                UMPD: 301-405-3555\n
                4-Work: 301-314-9675"""
        )


def send(msg):
    url = "https://api.groupme.com/v3/bots/post"

    data = {
        "bot_id": os.getenv("BOT_ID"),
        "text": msg,
    }
    r = requests.post(url, json=data)
