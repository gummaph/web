import os
import uuid
from datetime import datetime, timedelta

from flask import Flask, request, send_file
import jwt

import exceptions
import authenticate
import decorators
import database

app = Flask(__name__)

signing_key = "secret"
payload = {
    "sub": "Employee Tokens",
    'iss': "my Company",
    "exp": datetime.now() + timedelta(seconds=600),
    "iat": datetime.now()
}


@app.route("/api/authenticate/", methods=['POST'])
def authorize():
    credentials = request.json

    if authenticate.is_valid_user(credentials):
        id = database.get_employee_id(credentials["name"])
        name = credentials["name"]
        permissions = database.get_employee_permissions(id)

        payload["id"] = id
        payload["name"] = name
        payload["permission"] = permissions

        token = jwt.encode(payload, signing_key)
        auth_token = {"token": token}
        return auth_token, 200
    else:
        err = exceptions.IncorrectPassword()
        return str(err), err.status


@app.route("/api/employee/", methods=['POST'])
@decorators.require_authentication
def create_employee():
    body = request.json
    id = database.get_available_id()
    database.employees_database[id] = [body['name'], body['address'], body['password'], True]
    return str({"id": id,
                "details": database.employees_database[id]}), 200


@app.route("/api/employee/<int:employee_id>", methods=['PUT'])
@decorators.require_authentication
def update_employee(employee_id):
    body = request.json
    try:
        employee = database.employees_database[employee_id]


    except KeyError as e:
        err = exceptions.InvalidData()
        return str(err), err.status

    employee[0] = body.get("name", employee[0])
    employee[1] = body.get("address", employee[1])
    employee[2] = body.get("password", employee[2])
    employee[3] = body.get("is_active", employee[3])

    return str({"id": employee_id,
                "details": database.employees_database[employee_id]}), 200


@app.route("/api/employee/<int:employee_id>", methods=['GET'])
@decorators.require_authentication
def get_employee(employee_id):
    try:
        database.employees_database[employee_id]

    except KeyError as e:
        err = exceptions.InvalidData()
        return str(err), err.status

    return str({"id": employee_id,
                "details": database.employees_database[employee_id]}), 200


@app.route("/api/employee/<int:employee_id>", methods=['DELETE'])
@decorators.require_authentication
def delete_employee(employee_id):
    try:
        employee = database.employees_database[employee_id]


    except KeyError as e:
        err = exceptions.InvalidData()
        return str(err), err.status

    employee[3] = False

    return str({"id": employee_id,
                "details": database.employees_database[employee_id]}), 200


@app.route("/api/files/", methods=["POST"])
def file_upload():
    # text portion
    form_data = dict(request.form)
    employee_name = form_data['name']
    overwrite = form_data.get('overwrite', False)

    # file portion
    file = request.files['profile_pic']
    file_name = file.filename
    file_id = str(uuid.uuid4())
    file_path = os.getcwd() + '/storage/' + file_id
    if not overwrite and os.path.isfile(file_path):
        return str({"file exists and cant be overwritten", 400}), 400
    else:
        file.save(file_path)
        pic_details = database.profile_pic_database[database.get_employee_id(employee_name)]
        if len(pic_details) == 0:
            pic_details.append(file_id)
            pic_details.append(file_name)
        else:
            pic_details[0] = file_id
            pic_details[1] = file_name
        print(database.profile_pic_database)
        return str({
            "message": "Success", "status": 200}), 200


@app.route("/api/files/<employee_name>", methods=['GET'])
def file_download(employee_name):
    employee_id = database.get_employee_id(employee_name)
    file_id = database.profile_pic_database[employee_id][0]
    file_path = os.getcwd() + "/storage/" + file_id
    if os.path.isfile(file_path):
        return send_file(file_path, download_name=database.profile_pic_database[employee_id][1]), 200
    else:
        return str({
            "message": "unable to retrieve file",
            "status": 404
        }), 404


@app.route("/api/files/<employee_name>", methods=['DELETE'])
def file_delete(employee_name):
    employee_id = database.get_employee_id(employee_name)
    if not employee_id:
        return str({
            "message": "employee not found",
            "status": 404
        }), 404
    try:

        file_id = database.profile_pic_database[employee_id][0]
    except IndexError as e:
        return str({
            "message": "file not found",
            "status": 404
        }), 404

    file_path = os.getcwd() + "/storage/" + file_id
    if os.path.isfile(file_path):
        os.remove(file_path)
        database.profile_pic_database[employee_id] = []
        return str({
            "message": "success",
            "status": 200
        }), 200
    else:
        return str({
            "message": "unable to retrieve file",
            "status": 404
        }), 404
