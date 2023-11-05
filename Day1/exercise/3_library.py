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


library = {
    1: Book("Animal Farm", "Orwell"),
    2: Book("1987", "Orwell"),
    3: Book("Moby Dick", "H. Melville")
}
count = 3

app = Flask(__name__)


@app.route("/api/addbook/", methods=["POST"])
def add_book():
    global count
    book = request.json
    count += 1
    library[count] = Book(book["Book Name"], book["Author"])
    return str({count: str(library[count])})


@app.route("/api/updatebook/<int:book_id>", methods=["PUT"])
def edit_book(book_id):
    book = request.json
    library[book_id].book_name = book.get(
        "Book Name", library[count].book_name)
    library[book_id].author = book.get("Author", library[count].author)
    return str({book_id: str(library[book_id])})


@app.route("/api/getbook/<int:book_id>", methods=["GET"])
def get_book(book_id):
    return str({book_id: str(library[book_id])})


@app.route("/api/getbooks/", methods=["GET"])
def get_books():
    all_books = {}
    for book_id, book in library.items():
        all_books[book_id] = book.book_name
    return str(all_books)


@app.route("/api/deletebook/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    del library[book_id]
    return make_response("Deleted"), 200
