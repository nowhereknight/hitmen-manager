from sqlalchemy.dialects.postgresql import UUID
import os
import uuid
import bcrypt 
import jwt
from flask import current_app, request, url_for
from . import db
from .validators import validate_post_hitman, validate_login, validate_create_hit, validate_patch_hit_by_manager, validate_patch_hit_by_hitman, validate_patch_hitman
from .exceptions import ValidationError, NotFoundError, WrongPasswordError, NotAllowedError, ForbiddenError, InvalidChangeError
from .utils import password_check


SECRET_KEY = os.getenv('SECRET_KEY') or '12QwAsZx'


class Company(db.Model):
    __tablename__ = 'companies'
    company_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_name = db.Column(db.Text)
    description = db.Column(db.Text)
    symbol = db.Column(db.Text)
    market_values = db.Column(db.ARRAY(db.Integer))
    is_active = db.Column(db.Boolean, default=True)


    def __init__(self, data):
        self.company_name=data['name']
        self.description=data['description']
        self.symbol=data['symbol']
    
    @staticmethod
    def create_from_json(body):
        if body is None or body in [ "", {}]:
            raise ValidationError('Request does not have a body')
        validation = validate_post_company(body)
        if(validation["error"]):
            raise ValidationError(validation["error"])
        elif(not is_symbol_available(body["symbol"].split(":")[1])):
            raise ValidationError("Symbol is not available for use")
        else:
            return Company(body)
    

    def update_from_json(self, body):
        if body is None or body in [ "", {}]:
            raise ValidationError('Request does not have a body')
        validation = validate_put_company(body)
        if(validation["error"]):
            raise ValidationError(validation["error"])
        elif(body.get('symbol') and not is_symbol_available(body["symbol"].split(":")[1])):
            raise ValidationError("Symbol is not available for use")
        else:
            self.company_name = body.get('name') if body.get('name') else self.company_name
            self.description = body.get('description') if body.get('description') else self.description
            self.symbol = body.get('symbol') if body.get('symbol') else self.symbol


    def soft_delete(self):
        self.is_active = False


    def to_json(self):
        json_company = {
            'company_uuid': self.company_uuid,
            'company_name': self.company_name,
            'description': self.description,
            'symbol': self.symbol,
            'is_active': self.is_active,
        }
        return json_company

            
class Hitman(db.Model):
    __tablename__ = 'hitmen'
    hitman_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.Text, nullable=False)
    lastname_1 = db.Column(db.Text, nullable=False)
    lastname_2 = db.Column(db.Text)
    email = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text)
    rank = db.Column(db.Text)
    manager_uuid = db.Column(UUID(as_uuid=True),db.ForeignKey('hitmen.hitman_uuid'))


    def __init__(self, data):
        self.name=data.get('name')
        self.lastname_1=data.get('lastname_1')
        self.lastname_2=data.get('lastname_2')
        self.email=data.get('email')
        password = data["password"].encode('utf-8')
        hashedPassword = bcrypt.hashpw(password, bcrypt.gensalt(10))
        hashedPassword = hashedPassword.decode('UTF-8')
        print('hashedPassword', hashedPassword)
        self.password=hashedPassword
        self.status="active"
        self.rank="hitman"


    @staticmethod
    def create_from_json(body):
        print(body, type(body))
        if body is None or body in [ "", {}]:
            raise ValidationError('Request does not have a body')
        validation = validate_post_hitman(body)
        if(validation["error"]):
            raise ValidationError(validation["error"])
        password_errors = password_check(body["password"])
        if password_errors:
            raise ValidationError(",".join(password_errors))
        else:
            return Hitman(body)

    
    @staticmethod
    def login(body):
        if body is None or body in [ "", {}]:
            raise ValidationError('Request does not have a body')
        validation = validate_login(body)
        if(validation["error"]):
            raise ValidationError(validation["error"])
        else:
            hitman = Hitman.query.filter_by(email=body["email"]).first()
            if(hitman):
                check = body["password"]
                check = check.encode('utf-8')
                hashed = hitman.to_json().get("password").encode('utf-8')
                print(check, hashed) 
                if bcrypt.checkpw(check, hashed):
                    print("Yei")
                    token = jwt.encode(
                        payload=hitman.to_json(),
                        key=SECRET_KEY,
                        algorithm="HS256"
                    )
                    try:
                        token = token.decode()
                    except (UnicodeDecodeError, AttributeError):
                        pass
                    return {"token":token, "hitman":hitman.to_json()}
                else:
                    raise WrongPasswordError()
            raise NotFoundError()


    @staticmethod
    def get_hitmen(token):
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if(decoded.get('rank') == 'hitman'):
            raise ForbiddenError()
        elif(decoded.get('rank') == 'manager'):
            hitmen = Hitman.query.filter_by(manager_uuid=decoded.get('hitman_uuid')).all()
            response = {
                "asignees": [hitman.to_json().get('hitman_uuid') for hitman in hitmen]
            }
            return response
        elif(decoded.get('rank') == 'god'):
            hitmen = Hitman.query.all()
            response = {
                "all_hitmen": [ 
                    { 
                        'hitman_uuid' : hitman.to_json().get('hitman_uuid'),
                        'name' : hitman.to_json().get('name'),
                        'lastname_1' : hitman.to_json().get('lastname_1'),
                        'status' : hitman.to_json().get('status'),
                        'rank' : hitman.to_json().get('rank'),

                    } for hitman in hitmen
                ]
            }
            return response


    @staticmethod
    def get_hitman(token, hitman_uuid):
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if(decoded.get('rank') == 'hitman'):
            raise ForbiddenError()    
        elif(decoded.get('rank') == 'manager'):
            hitman = Hitman.query.filter_by(hitman_uuid=hitman_uuid, manager_uuid=decoded.get('hitman_uuid')).first()
            if(not hitman):
                raise NotFoundError("No hitman with given hitman_uuid and/or assigned to the manager found")
            return hitman.to_json()
        elif(decoded.get('rank') == 'god'):
            hitman = Hitman.query.filter_by(hitman_uuid=hitman_uuid).first()
            if(not hitman):
                raise NotFoundError("No hitman with given hitman_uuid found")
            return hitman.to_json()


    @staticmethod
    def patch_hitman(token, hitman_uuid, body):
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if(decoded.get('rank') != "god"):
            raise ForbiddenError()
        if body is None or body in [ "", {}]:
            raise ValidationError('Request does not have a body')
        validation = validate_patch_hitman(body)
        if(validation["error"]):
            raise ValidationError(validation["error"])
        else:
            print("So far so good")
            hitman = Hitman.query.get(hitman_uuid)
            if(not hitman):
                raise NotFoundError("No hitman exists with given hitman_uuid")
            hitman.update_from_json(body)
            return hitman


    def update_from_json(self, body):
        if(body.get('status') == "active" and self.status == "inactive"):
            raise InvalidChangeError("Cannot turn from inactive to active")

        if(body.get('rank') == "hitman" and self.rank == "manager"):
            raise InvalidChangeError("Cannot turn from manager to hitman (for now)")
        
        if(body.get('manager_uuid')):
            print(body.get('manager_uuid'), str(self.hitman_uuid), body.get('manager_uuid') == str(self.hitman_uuid))
            manager = Hitman.query.get(body.get('manager_uuid'))
            if(not manager):
                raise NotFoundError("No hitman found with given manager_uuid")
            elif(manager.to_json().get('rank')=='hitman'):
                raise InvalidChangeError("Hitman with manager_uuid found but doesn't have the rank needed to be manager")
            elif(body.get('manager_uuid') == str(self.hitman_uuid)):
                raise InvalidChangeError("One cannot be one's own manager")


        
        self.status = body.get('status') or self.status
        self.rank = body.get('rank') or self.rank
        self.manager_uuid = body.get('manager_uuid') or self.manager_uuid


    def to_json(self):
        json_hitman = {
            'name': self.name,
            'lastname_1': self.lastname_1,
            'lastname_2': self.lastname_2,
            'password': str(self.password),
            'email': self.email,
            'status': self.status,
            'rank': self.rank,
            'manager_uuid': str(self.manager_uuid),
        }
        if(self.hitman_uuid):
            json_hitman['hitman_uuid'] = str(self.hitman_uuid)

        return json_hitman


class Hit(db.Model):
    __tablename__ = 'hits'
    hit_uuid = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    identifier = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_name = db.Column(db.Text, nullable=False)
    target_lastname_1 = db.Column(db.Text, nullable=False)
    target_lastname_2 = db.Column(db.Text)
    status = db.Column(db.Text)
    hitman_uuid = db.Column(UUID(as_uuid=True),db.ForeignKey('hitmen.hitman_uuid'))
    creator_uuid = db.Column(UUID(as_uuid=True),db.ForeignKey('hitmen.hitman_uuid'))


    def __init__(self, data):
        self.identifier=data.get('identifier')
        self.description=data.get('description')
        self.target_name=data.get('target_name')
        self.target_lastname_1=data.get('target_lastname_1')
        self.target_lastname_2=data.get('target_lastname_2')
        self.status="assigned"
        self.creator_uuid=data.get('creator_uuid')
        self.hitman_uuid=data.get('hitman_uuid')
    

    @staticmethod
    def get_hits(token):    
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if(decoded.get('rank') == 'hitman'):
            hits = Hit.query.filter_by(hitman_uuid=decoded.get('hitman_uuid'))
            print(hits)
            return {
                "hits":[hit.to_json().get('hit_uuid') for hit in hits]
            }
        elif(decoded.get('rank') == 'manager'):
            hits_hitmen = db.session.query(Hit, Hitman).filter(Hit.hitman_uuid == Hitman.hitman_uuid).filter(Hitman.manager_uuid == decoded.get('hitman_uuid')).all()
            print(hits_hitmen)
            asignees = {}
            for hit_hitman in hits_hitmen:
                hit = hit_hitman[0]
                hitman_uuid = str(hit_hitman[1].to_json().get('hitman_uuid'))
                if asignees.get(hitman_uuid):
                    asignees[hitman_uuid].append(hit.to_json())
                else:
                    asignees[hitman_uuid] = [ hit.to_json()]
            return {"asignees":asignees}
        elif(decoded.get('rank') == 'god'):
            results = {}
            hitmen = Hitman.query.all()
            for hitman in hitmen:
                hitman_uuid = hitman.to_json().get('hitman_uuid')
                hits = Hit.query.filter_by(hitman_uuid=hitman_uuid)
                results[hitman_uuid] = {
                    "hits":[ hit.to_json().get('hit_uuid') for hit in hits]
                }
                for key, value in hitman.to_json().items():
                    results[hitman_uuid][key] = value
            return results


    @staticmethod
    def get_hit(token, hit_uuid):    
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print("decoded", decoded)
        if(decoded.get('rank') == 'hitman'):
            hit = Hit.query.filter_by(hit_uuid=hit_uuid,hitman_uuid=decoded.get('hitman_uuid')).first()
            if(not hit):
                raise NotFoundError()
            return hit
        elif(decoded.get('rank') == 'manager'):
            hit_hitman = db.session.query(Hit, Hitman).filter(Hit.hitman_uuid == Hitman.hitman_uuid).filter(Hitman.manager_uuid == decoded.get('hitman_uuid')).filter(Hit.hit_uuid == hit_uuid).first()
            if(not hit_hitman):
                raise NotFoundError()
            return hit_hitman[0]
        elif(decoded.get('rank') == 'god'):
            hit = Hit.query.filter_by(hit_uuid=hit_uuid).first()
            if(not hit):
                raise NotFoundError()
            return hit


    @staticmethod
    def create(token, body):
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        print(decoded)
        ### TO DO: Validar que los managers solo le puedan crear a sus lacallos
        if(decoded.get('rank') in ['manager', 'god']):
            if body is None or body in [ "", {}]:
                raise ValidationError('Request does not have a body')
            validation = validate_create_hit(body)
            if(validation["error"]):
                raise ValidationError(validation["error"])
            else:
                body['creator_uuid'] = decoded.get('hitman_uuid')
                asignee_uuid = body.get('hitman_uuid')
                hitman = Hitman.query.get(asignee_uuid)
                if(not hitman):
                    raise NotFoundError()
                return Hit(body)
        else:
            raise NotAllowedError()
 

    @staticmethod
    def patch_hit(token, hit_uuid, body):
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        if body is None or body in [ "", {}]:
            raise ValidationError('Request does not have a body')
        
        if(decoded.get('rank') == "hitman"):
            hit = Hit.query.filter_by(hit_uuid=hit_uuid, hitman_uuid=decoded.get('hitman_uuid')).first()
            if(not hit):
                raise NotFoundError("No hit found with given hit_uuid or associated to your user")
            validation = validate_patch_hit_by_hitman(body)
            if(validation["error"]):
                raise ValidationError(validation["error"])
            else:
                hit.status = body.get('status') or hit.status
                return hit
        elif(decoded.get('rank') == "manager"):
            hit_hitman = db.session.query(Hit, Hitman).filter(Hit.hitman_uuid == Hitman.hitman_uuid).filter(Hitman.manager_uuid == decoded.get('hitman_uuid')).filter(Hit.hit_uuid == hit_uuid).first()
            if(not hit_hitman):
                raise NotFoundError("No hit found with given hit_uuid or to any of your asignees")
            hit = hit_hitman[0]
            print("hit",hit.to_json())
            validation = validate_patch_hit_by_manager(body)
            if(validation["error"]):
                raise ValidationError(validation["error"])
            else:
                if(body.get('hitman_uuid')):
                    hitman = Hitman.query.get(body.get('hitman_uuid'))
                    if(not hitman):
                        raise NotFoundError("No hitman was found with given hitman_uuid")
                    hit.hitman_uuid = body.get('hitman_uuid') or hit.hitman_uuid
                hit.status = body.get('status') or hit.status
                return hit
        elif(decoded.get('rank') == "god"):
            #hit_hitman = db.session.query(Hit, Hitman).filter(Hit.hitman_uuid == Hitman.hitman_uuid).filter(Hit.hit_uuid == hit_uuid).first()
            hit = Hit.query.get(hit_uuid)
            if(not hit):
                raise NotFoundError("No hit found with given hit_uuid")
            print(hit.to_json())
            validation = validate_patch_hit_by_manager(body)
            if(validation["error"]):
                raise ValidationError(validation["error"])
            else:
                if(body.get('hitman_uuid')):
                    hitman = Hitman.query.get(body.get('hitman_uuid'))
                    if(not hitman):
                        raise NotFoundError("No hitman was found with given hitman_uuid")
                    hit.hitman_uuid = body.get('hitman_uuid') or hit.hitman_uuid
                hit.status = body.get('status') or hit.status
                return hit



    def to_json(self):
        json_hitman = {
            'identifier': self.identifier,
            'description': self.description,
            'target_name': self.target_name,
            'target_lastname_1': self.target_lastname_1,
            'target_lastname_2': self.target_lastname_2,
            'status': self.status,
            'hitman_uuid': self.hitman_uuid,
            'creator_uuid': self.creator_uuid,
        }
        if(self.hit_uuid):
            json_hitman['hit_uuid'] = str(self.hit_uuid)

        return json_hitman

