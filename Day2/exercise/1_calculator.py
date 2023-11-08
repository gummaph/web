import time

from flask import Flask
from flask import request

app = Flask(__name__)


class BaseException(Exception):
    def __init__(self, status, message):
        super().__init__()
        self.status = status
        self.message = message

    def __str__(self):
        return str({
            "status": self.status,
            "message": self.message
        })


class InvalidData(BaseException):
    def __init__(self):
        super().__init__(400, "invalid data")


def time_request(called):
    def f(*args, **kwargs):
        req_start_time = time.time() * 1000
        res = called(*args, **kwargs)
        req_end_time = time.time() * 1000
        res_time = req_end_time - req_start_time
        app.logger.info(f"Response Time: {res_time}")
        return res

    f.__name__ = called.__name__
    return f


@app.route("/api/add/", methods=["POST"])
@time_request
def add():
    numbers = request.json
    try:
        result = float(numbers['x']) + float(numbers['y'])
    except Exception as e:
        err = InvalidData()
        return str(err), err.status
    return str(result), 200


@app.route("/api/sub/", methods=["POST"])
@time_request
def sub():
    numbers = request.json
    try:
        result = float(numbers['x']) - float(numbers['y'])
    except Exception as e:
        err = InvalidData()
        return str(err), err.status
    return str(result), 200


@app.route("/api/mul/", methods=["POST"])
@time_request
def mul():
    numbers = request.json
    try:
        result = float(numbers['x']) * float(numbers['y'])
    except Exception as e:
        err = InvalidData()
        return str(err), err.status
    return str(result), 200

@app.route("/api/div/", methods=["POST"])
@time_request
def div():
    numbers = request.json
    try:
        result = float(numbers['x']) / float(numbers['y'])
    except Exception as e:
        err = InvalidData()
        return str(err), err.status
    return str(result), 200
