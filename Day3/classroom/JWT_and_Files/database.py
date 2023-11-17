employees_database = {1: ["phani", "earth", "qwe123", True],
                      2: ["aku", "hell", "evil", False],
                      3: ["jack", "earth", "samurai", True]
                      }
permission_database = {1: ['create_employee', 'get_employee', 'update_employee', 'delete_employee'],
                       2: ['create_employee', 'get_employee'],
                       3: []
                       }
profile_pic_database={1:[],
             2:[],
             3:[]
}

def get_available_id():
    return len(employees_database) + 1


def get_employee_id(name):
    for employee_id, employee in employees_database.items():
        if name == employee[0]:
            return employee_id
    return None


def get_employee_permissions(id):
    return permission_database.get(id, [])
