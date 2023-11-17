import jwt
import exceptions
import jwt_flask

def get_authorizations(token) ->[]:
    try:
        payload=jwt.decode(token,jwt_flask.signing_key,algorithms=["HS256"])
    except Exception as e:
        raise exceptions.InvalidToken()
    return payload.get("permission")