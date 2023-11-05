from flask import Flask
from flask import request,make_response

class Employee:
    def __init__(self,id,name,address):
        self.id=id
        self.name=name
        self.address=address
        
    def __str__(self):
        return str({
            "id":self.id,
            "name":self.name,
            "address":self.address
        })
        
company={
    1:Employee(1,"phani","Bangalore"),
    2:Employee(2,"aku","Hell"),
    3:Employee(3,"jack","Earth")
}
count=3
app=Flask(__name__)

@app.route("/api/addEmployee/",methods=["POST"])
def create_employee():
    global count
    employee=request.json
    count+=1
    company[count]=Employee(count,employee['name'],employee['address'])
    return str(company[count])

@app.route("/api/updateEmployee/<int:employee_no>",methods=["PUT"])
def update_employee(employee_no):
    employee=request.json
    company[employee_no].name=employee.get('name',company[employee_no].name)
    company[employee_no].address=employee.get('address',company[employee_no].address)
    return str(company[employee_no])

@app.route("/api/getEmployee/<int:employee_no>",methods=["GET"])
def get_employee(employee_no):
    return str(company[employee_no])

@app.route("/api/getEmployee/",methods=["GET"])
def get_company():
    all_records={}
    for employee_id,employee in company.items():
        all_records[employee_id]=employee.name
        
    return all_records


@app.route("/api/deleteEmployee/<int:employee_no>",methods=["DELETE"])
def delete_employee(employee_no):
    del company[employee_no]
    return make_response(""),200
