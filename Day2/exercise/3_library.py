import time

from flask import Flask
from flask import request, make_response


class Book:

    def __init__(self, book_name, author):
        self.book_name = book_name
        self.author = author

    def __str__(self):
        return str({
            "Book Name": self.book_name,
            "Author": self.author
        })

    def validate(self):
        book_name_check = len(self.book_name) in range(1, 256 + 1)
        author_check = len(self.author) in range(1, 256 + 1)

        return book_name_check and author_check


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
        super().__init__(400, "invalid Data")


class BookNotFound(BaseException):
    def __init__(self):
        super().__init__(404, "Book not found")


# add logging and tracking
def setup_logging(called):
    def f(*args, **kwargs):
        req_id = f"Req_{time.time() * 1000}"
        request.logger = app.logger
        request.req_id = req_id
        resp, status = called(*args, **kwargs)
        resp_send = make_response(resp)
        resp_send.headers['x-Request_id'] = req_id
        return resp_send, status

    f.__name__ = called.__name__
    return f


library = {
    1: Book("Animal Farm", "Orwell"),
    2: Book("1987", "Orwell"),
    3: Book("Moby Dick", "H. Melville")
}
count = 3

app = Flask(__name__)


@app.route("/api/addbook/", methods=["POST"])
@setup_logging
def add_book():
    log_message = {"Tracking ID": request.req_id, "Operation": "add book", "status": "processing"}
    request.logger.info(log_message)
    global count
    book = request.json
    # validations
    new_book = Book(book["Book Name"], book["Author"])
    if not new_book.validate():
        err = InvalidData()
        log_message["status"] = "failed"
        request.logger.error(log_message)
        return str(err), err.status

    count += 1
    library[count] = new_book
    log_message["status"] = "success"
    request.logger.info(log_message)
    return str({count: str(library[count])}), 200


@app.route("/api/updatebook/<int:book_id>", methods=["PUT"])
def edit_book(book_id):
    log_message = {"Tracking ID": request.req_id, "Operation": "update book", "status": "processing"}
    request.logger.info(log_message)
    book = request.json
    new_book = Book(book["Book Name"], book["Author"])
    if not new_book.validate():
        err = InvalidData()
        log_message["status"] = "failed"
        request.logger.error(log_message)
        return str(err), err.status

    try:
        library[book_id].book_name = book.get(
            "Book Name", library[count].book_name)
        library[book_id].author = book.get("Author", library[count].author)
    except KeyError as e:
        err = BookNotFound()
        log_message["status"] = "failed"
        request.logger.error(log_message)
        return str(err), err.status

    log_message["status"] = "success"
    request.logger.info(log_message)
    return str({book_id: str(library[book_id])}), 200


@app.route("/api/getbook/<int:book_id>", methods=["GET"])
def get_book(book_id):
    log_message = {"Tracking ID": request.req_id, "Operation": "get book", "status": "processing"}
    request.logger.info(log_message)
    try:
        library[book_id]
    except KeyError as e:
        err = BookNotFound()
        log_message["status"] = "failed"
        request.logger.error(log_message)
        return str(err), err.status

    log_message["status"] = "success"
    request.logger.info(log_message)
    return str({book_id: str(library[book_id])}), 200


@app.route("/api/getbooks/", methods=["GET"])
def get_books():
    log_message = {"Tracking ID": request.req_id, "Operation": "get library", "status": "processing"}
    request.logger.info(log_message)
    all_books = {}
    for book_id, book in library.items():
        all_books[book_id] = book.book_name

    log_message["status"] = "success"
    request.logger.info(log_message)
    return str(all_books), 200


@app.route("/api/deletebook/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    log_message = {"Tracking ID": request.req_id, "Operation": "delete book", "status": "processing"}
    request.logger.info(log_message)
    try:
        del library[book_id]
    except KeyError as e:
        err = BookNotFound()
        log_message["status"] = "failed"
        request.logger.error(log_message)
        return str(err), err.status

    log_message["status"] = "success"
    request.logger.info(log_message)
    return make_response("Deleted"), 200
