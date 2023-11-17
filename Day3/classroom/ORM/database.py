from models import Employee, session




def get_id(name):
    employee_id = session.query(Employee.id).filter_by(name=name).one_or_none()
    return employee_id


def save_employee(name, address, password, pic_id="default_pic"):
    employee = Employee(name=name, address=address, password=password, pic_id=pic_id)
    session.add(employee)
    session.commit()

def Update_employee(id,name,address,password):
    employee=session.query(Employee).filter_by(id=id).one_or_none()

    employee.name=name if name else employee.name
    employee.address=address if address else employee.address
    employee.password=password if password else employee.password
    session.commit()
    return employee

def get_employee(id):
    employee = session.query(Employee).filter_by(id=id).one_or_none()

    return employee

def delete_employee(id):
    employee = session.query(Employee).filter_by(id=id).one_or_none()
    if employee:
        session.delete(employee)
        session.commit()
        return "success"
    else:
        return None


