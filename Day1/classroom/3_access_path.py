from flask import Flask

app =Flask(__name__)

employees={
    1:"prashanth",
    2:"Phani",
    3:"shiva"    
}

@app.route("/<employee_name>",methods=["GET"])
def hello_employee(employee_name):
    return f"<p> hello {employee_name}"

@app.route("/<int:employee_id>",methods=["GET"])
def return_employee_name(employee_id):
    return f"<p>Hello, {employees.get(employee_id,'employee not found')}</p>"