from flask import jsonify, request, g, url_for, current_app
from .. import db
from ..models import Hit
from . import api
from ..responses import bad_request, success, not_found, conflict, system_error, forbidden
from ..exceptions import ValidationError, NotFoundError, WrongPasswordError, NotAllowedError
from sqlalchemy import exc
from flask_cors import cross_origin


@api.route('/hits/', methods=['POST'])
@cross_origin()
def create_hit():
    try:
        token = dict(request.headers).get('Authorization')
        if(token):
            token = token.split()[1]
            hit = Hit.create(token, request.json)
            print("hit", hit.to_json())
            db.session.add(hit)
            db.session.commit()
            return success(hit.to_json(), 201)
        else:
            return bad_request("A token is needed for authentication")
    except ValidationError as ve:
        return bad_request(str(ve))
    except exc.IntegrityError as ie:
        return conflict(str(ie))
    except NotAllowedError as ve:
        return forbidden("You do not have the needed permissions")
    except NotFoundError as nf:
        return not_found("No hitman exists with given hitman_uuid")
    except Exception as e:
        print(e)
        if("400" in str(e)):
            return bad_request("Invalid POST request. Please remember to include the body")
        return system_error(str(e))



@api.route('/hits/<hit_uuid>', methods=['PATCH'])
@cross_origin()
def patch_hit(hit_uuid):
    try:
        token = dict(request.headers).get('Authorization')
        if(token):
            token = token.split()[1]
            hit = Hit.patch_hit(token, hit_uuid, request.json)
            # db.session.add(hit)
            # db.session.commit()
            return success(hit.to_json(), 201)
        else:
            return bad_request("A token is needed for authentication")
    except ValidationError as ve:
        return bad_request(str(ve))
    except NotFoundError as nf:
        return not_found(str(nf))
    except Exception as e:
        print(e)
        if("400" in str(e)):
            return bad_request("Invalid PATCH request. Please remember to include the body")
        return system_error(str(e))


@api.route('/hits/')
@cross_origin()
def get_hits():
    try:
        token = dict(request.headers).get('Authorization')
        if(token):
            token = token.split()[1]
            hits = Hit.get_hits(token)
            return success(hits)

        else:
            return bad_request("A token is needed for authentication")
    except Exception as e:
        print(e)
        if("400" in str(e)):
            return bad_request("Invalid POST request. Please remember to include the body")
        return system_error(str(e))


@api.route('/hits/<hit_uuid>')
@cross_origin()
def get_hit(hit_uuid):
    try:
        token = dict(request.headers).get('Authorization')
        if(token):
            token = token.split()[1]
            hit = Hit.get_hit(token, hit_uuid)
            return success(hit.to_json())
        else:
            return bad_request("A token is needed for authentication")
    except NotFoundError as nf:
        return not_found("No hit exists or is assigned to the user with given hit_uuid")
    except Exception as e:
        print(e)
        if("400" in str(e)):
            return bad_request("Invalid POST request. Please remember to include the body")
        return system_error(str(e))