# employees={1:["phani","earth","qwe123"],
#            2:["aku","hell","evil"],
#            3:["jack","earth","samurai"]
# }
from database import employees_database


def is_valid_user(credentials):
    emp_name = credentials['name']
    password = credentials['password']

    for id, employee in employees_database.items():
        if emp_name== employee[0] and password == employee[2] and employee[3]:
            return True
    return False
