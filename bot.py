import os
import requests
import random

from flask import Flask, request


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "RA Bot is running :)"


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


def chicken_tenders(food):
    if "Chicken Tenders" in food:
        return True
    return False


def read(msg):
    text = msg.split(" ")

    if msg == "/menu":
        send(
            """RA BOT MENU: \n
             Type in a command! \n
             Pick a num between 1-10: /pick \n
             Flip a coin: /flip \n
             Phone Numbers: /numbers \n"""
        )
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
    data = {
        "bot_id": os.getenv("BOT_ID"),
        "text": msg,
    }
    r = requests.post("https://api.groupme.com/v3/bots/post", json=data)
