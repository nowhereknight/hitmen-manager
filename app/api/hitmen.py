from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Hitman
from . import api
from ..responses import bad_request, success, not_found, conflict, system_error, forbidden
from ..exceptions import ValidationError, NotFoundError, WrongPasswordError, ForbiddenError, InvalidChangeError
from sqlalchemy import exc
from flask_cors import cross_origin


@api.route('/register/', methods=['POST'])
@cross_origin()
def register():
    try:
        print("Hitman to insert", request.get_json())
        hitman = Hitman.create_from_json(request.json)
        print("hitman",hitman.to_json())
        db.session.add(hitman)
        db.session.commit()
        return success(hitman.to_json(), 201)
    except ValidationError as ve:
        return bad_request(str(ve))
    except exc.IntegrityError as ie:
        return conflict(str(ie))
    except Exception as e:
        if("400" in str(e)):
            return bad_request("Invalid POST request. Please remember to include the body")
        return system_error(str(e))


@api.route('/login/', methods=['POST'])
@cross_origin()
def login():
    try:
        print("Login info", request.get_json())
        response = Hitman.login(request.json)
        print("response", response)
        return success(response, 200)
    except ValidationError as ve:
        return bad_request(str(ve))
    except exc.IntegrityError as ie:
        return conflict(str(ie))
    except NotFoundError as nf:
        return not_found()
    except WrongPasswordError as wp:
        return bad_request("Wrong password")
    except Exception as e:
        print(e)
        if("400" in str(e)):
            return bad_request("Invalid POST request. Please remember to include the body")
        return system_error(str(e))


@api.route('/hitmen/<hitman_uuid>', methods=['PATCH'])
@cross_origin()
def patch_hitman(hitman_uuid):
    try:
        token = dict(request.headers).get('Authorization')
        if(token):
            token = token.split()[1]
            print("Data to update", request.get_json())
            hitman = Hitman.patch_hitman(token,hitman_uuid,request.json)
            db.session.add(hitman)
            db.session.commit()
            return success(hitman.to_json(), 200)
        else:
            return bad_request("A token is needed for authentication")
    except InvalidChangeError as ic:
        return bad_request(str(ic))
    except NotFoundError as nf:
        return not_found(str(nf))
    except ForbiddenError as wp:
        return forbidden("You do not have the needed permissions")
    except Exception as e:
        if("400" in str(e)):
            return bad_request("Invalid PATCH request. Please remember to include the body")
        return system_error(str(e))


@api.route('/hitmen')
@cross_origin()
def get_hitmen():
    try:
        token = dict(request.headers).get('Authorization')
        if(token):
            token = token.split()[1]
            hitmen = Hitman.get_hitmen(token)
            return success(hitmen, 200)
        else:
            return bad_request("A token is needed for authentication")
    except ForbiddenError as wp:
        return forbidden("You do not have the needed permissions")
    except Exception as e:
        if("400" in str(e)):
            return bad_request("Invalid PATCH request. Please remember to include the body")
        return system_error(str(e))


@api.route('/hitmen/<hitman_uuid>')
@cross_origin()
def get_hitman(hitman_uuid):
    try:
        token = dict(request.headers).get('Authorization')
        if(token):
            token = token.split()[1]
            hitman = Hitman.get_hitman(token, hitman_uuid)
            return success(hitman, 200)
        else:
            return bad_request("A token is needed for authentication")
    except NotFoundError as nf:
        return not_found(str(nf))
    except ForbiddenError as wp:
        return forbidden("You do not have the needed permissions")
    except Exception as e:
        if("400" in str(e)):
            return bad_request("Invalid PATCH request. Please remember to include the body")
        return system_error(str(e))