import json
import jsonschema
from jsonschema import validate
from .exceptions import ValidationError


COMPANY_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 2, "maxLength": 50},
        "description": {"type": "string",  "minLength": 2, "maxLength": 100},
        "symbol": {
            "type": "string",  "minLength": 2,  "maxLength": 10,    
            "pattern": "(NYSE|AMEX|NASDAQ):([A-Z]{1,4})"
        },
    },
    "required":[
        "name",
        "description",
        "symbol",
    ],
    "additionalProperties": False
}


COMPANY_PUT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 2, "maxLength": 50},
        "description": {"type": "string",  "minLength": 2, "maxLength": 100},
        "symbol": {
            "type": "string",  "minLength": 2,  "maxLength": 10,    
            "pattern": "(NYSE|AMEX|NASDAQ):([A-Z]{1,4})"
        },
    },
    "additionalProperties": False
}


HITMAN_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 2, "maxLength": 100},
        "lastname_1": {"type": "string", "minLength": 2, "maxLength": 100},
        "lastname_2": {"type": "string", "minLength": 2, "maxLength": 100},
        "email": {"type": "string", "minLength": 2, "maxLength": 50,"format": "email","pattern": "^\\S+@\\S+\\.\\S+$",
},
        "password": {"type": "string",  "minLength": 6, "maxLength": 20},
        "rank": {"type": "string",  "minLength": 2, "maxLength": 20},

    },
    "required":[
        "name",
        "lastname_1",
        "email",
        "password",
    ],
    "additionalProperties": False
}


HITMAN_PATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "minLength": 2, "maxLength": 20,
            "enum": [
                "active",
                "inactive"
            ]},
        "rank": {"type": "string", "minLength": 2, "maxLength": 20,
            "enum": [
                    "hitman",
                    "manager",
            ]},
        "manager_uuid": {"type": "string", "minLength": 36,"maxLength": 36,"format": "uuid", "pattern": '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'},
    },
    "additionalProperties": False
}


HITMAN_LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "minLength": 2, "maxLength": 50,"format": "email","pattern": "^\\S+@\\S+\\.\\S+$",
},
        "password": {"type": "string",  "minLength": 6, "maxLength": 20},
    },
    "required":[
        "email",
        "password",
    ],
    "additionalProperties": False
}


HIT_POST_SCHEMA = {
    "type": "object",
    "properties": {
        "identifier": {"type": "string", "minLength": 2, "maxLength": 20},
        "description": {"type": "string", "minLength": 2, "maxLength": 100},
        "target_name": {"type": "string", "minLength": 2, "maxLength": 100},
        "target_lastname_1": {"type": "string", "minLength": 2, "maxLength": 100},
        "target_lastname_2": {"type": "string", "minLength": 2, "maxLength": 100},
        "hitman_uuid": {"type": "string", "minLength": 36,"maxLength": 36,"format": "uuid", "pattern": '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'},
    },
    "required":[
        "identifier",
        "description",
        "target_name",
        "target_lastname_1",
        "hitman_uuid"
    ],
    "additionalProperties": False
}

HIT_PATCH_BY_HITMAN_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "minLength": 2, "maxLength": 20,
            "enum": [
                "assigned",
                "completed",
                "failed"
            ]},
    },
    "additionalProperties": False
}


HIT_PATCH_BY_MANAGER_SCHEMA = {
    "type": "object",
    "properties": {
        "hitman_uuid": {"type": "string", "minLength": 36,"maxLength": 36,"format": "uuid", "pattern": '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'},
        "status": {"type": "string", "minLength": 2, "maxLength": 20,
            "enum": [
                "assigned",
                "completed",
                "failed"
            ]},
    },
    "additionalProperties": False
}


def validate_json(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
        return {"error":None}
    except jsonschema.exceptions.ValidationError as err:
        return {"error":err.message}


def validate_post_company(json_data):
    return validate_json(json_data, COMPANY_POST_SCHEMA)


def validate_put_company(json_data):
    return validate_json(json_data, COMPANY_PUT_SCHEMA)


def validate_post_hitman(json_data):
    return validate_json(json_data, HITMAN_POST_SCHEMA)


def validate_login(json_data):
    return validate_json(json_data, HITMAN_LOGIN_SCHEMA)

def validate_create_hit(json_data):
    return validate_json(json_data, HIT_POST_SCHEMA)


def validate_patch_hitman(json_data):
    return validate_json(json_data, HITMAN_PATCH_SCHEMA)


def validate_patch_hit_by_hitman(json_data):
    return validate_json(json_data, HIT_PATCH_BY_HITMAN_SCHEMA)


def validate_patch_hit_by_manager(json_data):
    return validate_json(json_data, HIT_PATCH_BY_MANAGER_SCHEMA)


