import os
import json
import jwt
import datetime
import bcrypt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'cloudcomputing20251')

def generate_hashed_password(password):

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_jwt(user_id, tenant_id, roles, expires_in_seconds=3600):

    payload = {
        'sub': user_id,
        'tenantId': tenant_id,
        'roles': roles,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in_seconds),
        'iat': datetime.datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def decode_jwt(token):

    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

def http_response(status_code, body):

    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*', 
            'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'
        },
        'body': json.dumps(body)
    }