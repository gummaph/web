from datetime import datetime, timedelta

import jwt

payload = {"sub": "Employee Token", "permission": ['emp.create', 'emp.list'], 'iss': "my Company",
           "exp": datetime.now() + timedelta(seconds=120)}
token = jwt.encode(payload, "signing_key")

print(token)

decode_payload = jwt.decode(token, "signing_key", algorithms=['HS256'])
print(decode_payload)
