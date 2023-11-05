from flask import Flask
from flask import request

app=Flask(__name__)


@app.route("/wordcount",methods=["POST"])
def wordcount():
    sentance=request.json
    no_of_words=len(sentance["data"].split())
    return str(no_of_words)