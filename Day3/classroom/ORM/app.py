import sqlite3

import sqlalchemy
from flask import Flask, request
import database
import exceptions

app = Flask(__name__)


@app.route("/api/employee/", methods=["POST"])
def create_employee():
    # get data from request body
    data = request.json
    try:
        name = data["name"]
        address = data["address"]
        password = data["password"]
        pic_id = data.get("pic_id", "default_pic")
    except KeyError as e:
        err = exceptions.InvalidData()
        return err.message, err.status

    try:
        database.save_employee(name, address, password, pic_id)
    except sqlalchemy.exc.IntegrityError as e:
        return "Name already exists", 400
    employee_id = database.get_id(name)
    return str({
        "id": employee_id
    }), 200


@app.route("/api/employee/<int:employee_id>", methods=["PUT"])
def update_employee(employee_id):
    data = request.json
    name = data.get("name", None)
    address = data.get("address", None)
    password = data.get("password", None)

    try:
        employee = database.Update_employee(employee_id, name, address, password)
    except sqlalchemy.exc.IntegrityError as e:
        return str({"status": 500,
                    "message": "internal database error"}), 500

    return str(employee), 200

@app.route("/api/employee/<int:employee_id>",methods=["GET"])
def get_employee(employee_id):
    employee=database.get_employee(employee_id)
    if employee:
        return str(employee),200
    else:
        return str({"status":404,
                    "message":"employee not found"
                    })

@app.route("/api/employee/<int:employee_id>",methods=["DELETE"])
def delete_employee(employee_id):
    try:
        result=database.delete_employee(employee_id)
    except sqlalchemy.exc.IntegrityError as e:
        return str({"status": 500,
                    "message": "internal database error"}), 500
    if result:
        return str({
            "status":200,
            "message":"deleted"
        }), 200
    else:
        return str({
            "status":404,
            "message":"employee not found"
        }),404

