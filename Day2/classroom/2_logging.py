from flask import Flask
from flask import request, make_response


class Employee:
    def __init__(self, id, name, address):
        self.id = id
        self.name = name
        self.address = address

    def __str__(self):
        return str({
            "id": self.id,
            "name": self.name,
            "address": self.address
        })

    def validate(self):
        validate_name = len(self.name) > 0 and len(self.name) < 256
        validate_address = len(self.address) > 0 and len(self.address) < 1024
        return validate_name and validate_address


# Exception handling classes
class BaseException(Exception):
    def __init__(self, status, message):
        super().__init__()
        self.status = status
        self.message = message

    def __str__(self):
        return str({"status": self.status,
                    "message": self.message})


class ValidationError(BaseException):
    def __init__(self):
        super().__init__(400, "invalid inputs")


class EmployeeNotPresent(BaseException):
    def __init__(self):
        super().__init__(404, "employee not found")


# logging setup

def setup_logger(called):
    def f(*args, **kwargs):
        request.logger = app.logger
        return called(*args, **kwargs)

    f.__name__ = called.__name__
    return f


company = {
    1: Employee(1, "phani", "Bangalore"),
    2: Employee(2, "aku", "Hell"),
    3: Employee(3, "jack", "Earth")
}
count = 3
app = Flask(__name__)


@app.route("/api/addEmployee/", methods=["POST"])
@setup_logger
def create_employee():
    log_message = {'operation': 'create employee', 'status': 'processing'}
    request.logger.info(str(log_message))
    global count
    employee = request.json
    count += 1
    emp_obj = Employee(count, employee['name'], employee['address'])
    if not emp_obj.validate():
        log_message['status'] = "unsuccessful"
        request.logger.error(str(log_message))
        error = ValidationError()
        return str(error), error.status
    company[count] = emp_obj
    log_message['status'] = "successful"
    request.logger.info(str(log_message))
    return str(company[count])


@app.route("/api/updateEmployee/<int:employee_no>", methods=["PUT"])
@setup_logger
def update_employee(employee_no):
    log_message = {'operation': 'update employee', 'status': 'processing'}
    request.logger.info(str(log_message))
    employee = request.json
    try:
        company[employee_no].name = employee.get('name', company[employee_no].name)
        company[employee_no].address = employee.get('address', company[employee_no].address)
    except KeyError as e:
        log_message['status'] = "unsuccessful"
        request.logger.error(str(log_message))
        err = EmployeeNotPresent()
        return str(err), err.status

    log_message['status'] = "successful"
    request.logger.info(str(log_message))

    return str(company[employee_no])


@app.route("/api/getEmployee/<int:employee_no>", methods=["GET"])
@setup_logger
def get_employee(employee_no):
    log_message = {'operation': 'update employee', 'status': 'processing'}
    request.logger.info(str(log_message))
    try:
        company[employee_no]
    except KeyError as e:
        log_message['status'] = "unsuccessful"
        request.logger.error(str(log_message))

        err = EmployeeNotPresent()
        return str(err), err.status

    log_message['status'] = "successful"
    request.logger.info(str(log_message))
    return str(company[employee_no])


@app.route("/api/getEmployee/", methods=["GET"])
@setup_logger
def get_company():
    log_message = {'operation': 'update employee', 'status': 'processing'}
    request.logger.info(str(log_message))
    all_records = {}
    for employee_id, employee in company.items():
        all_records[employee_id] = employee.name

    log_message['status'] = "successful"
    request.logger.info(str(log_message))
    return all_records


@app.route("/api/deleteEmployee/<int:employee_no>", methods=["DELETE"])
@setup_logger
def delete_employee(employee_no):
    log_message = {'operation': 'update employee', 'status': 'processing'}
    request.logger.info(str(log_message))
    try:
        company[employee_no]
    except KeyError as e:
        log_message['status'] = "unsuccessful"
        request.logger.error(str(log_message))
        err = EmployeeNotPresent()
        return str(err), err.status

    del company[employee_no]
    log_message['status'] = "successful"
    request.logger.info(str(log_message))
    return make_response(""), 200
