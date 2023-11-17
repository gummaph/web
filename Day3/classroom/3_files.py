from flask import Flask, request, send_file
import os

app = Flask(__name__)


@app.route("/api/files/", methods=["POST"])
def file_upload():
    body = dict(request.form)
    # access text part of multi request
    file_name = body.get("name")
    file_id = body.get("file_id")

    file_path = os.getcwd() + "/storage/" + file_id

    # access file part of multi request

    file = request.files['file']

    overwrite = body.get("overwrite", False)

    if not overwrite and os.path.isfile(file_path):
        return str({"status": 400, "message": "File Already exists and cannot be overwritten"}), 400
    else:
        file.save(file_path)
        return "Success", 200


@app.route("/api/files/<file_id>", methods=["GET"])
def file_download(file_id):
    file_path = os.getcwd() + '/storage/' + file_id
    if not os.path.isfile(file_path):
        return str({404, "file not present"}), 404

    else:
        return send_file(file_path), 200


@app.route("/api/files/<file_id>", methods=["DELETE"])
def file_delete(file_id):
    file_path = os.getcwd() + '/storage/' + file_id
    if not os.path.isfile(file_path):
        return str({404, "file not present"}), 404

    else:
        os.remove(file_path)
        return "Success", 200
