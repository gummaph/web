from flask import Flask
from flask import request

app=Flask(__name__)

@app.route("/api/add/",methods=["POST"])
def add():
    numbers=request.json
    result = numbers['x']+numbers['y']
    return str(result)



@app.route("/api/sub/",methods=["POST"])
def sub():
    numbers=request.json
    result = numbers['x']-numbers['y']
    return str(result)



@app.route("/api/mul/",methods=["POST"])
def mul():
    numbers=request.json
    result = numbers['x']*numbers['y']
    return str(result)



@app.route("/api/div/",methods=["POST"])
def div():
    numbers=request.json
    result = numbers['x']/numbers['y']
    return str(result)


