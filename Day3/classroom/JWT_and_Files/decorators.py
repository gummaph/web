from flask import make_response, request

import authorization
import exceptions


def require_authentication(called):
    def f(*args, **kwargs):
        headers = request.headers

        try:
            token = headers.get("token")
            user_authorization = authorization.get_authorizations(token)
            print(user_authorization)
        except KeyError as e:
            err = exceptions.InvalidData()
            return str(err), err.status
        except exceptions.InvalidToken as e:
            return str(e), e.status

        if called.__name__ not in user_authorization:
            err = exceptions.InsufficientPrivilage()
            return str(err), err.status

        res, status = called(*args, **kwargs)
        send_response = make_response(res)
        return send_response,200
    f.__name__=called.__name__
    return f
