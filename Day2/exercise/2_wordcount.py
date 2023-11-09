import time

from flask import Flask
from flask import request
import time

app = Flask(__name__)


def setup_tracking(called):
    def f(*args, **kwargs):
        request.req_id = f"Req_{time.time() * 1000}"
        request.logger = app.logger
        return called(*args, **kwargs)

    f.__name__ = called.__name__
    return f


@app.route("/api/wordcount/", methods=["POST"])
@setup_tracking
def wordcount():
    log_message = {"tracking id": request.req_id, "operation": "word count", "status": "processing"}
    request.logger.info(str(log_message))

    body = request.json
    sentance = body['sentance']
    words = len(sentance.split())
    log_message["status"] = "done"
    request.logger.info(str(log_message))
    return str(words), 200
