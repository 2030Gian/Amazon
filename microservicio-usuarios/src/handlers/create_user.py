import json
import uuid
import time
from src.common.utils import generate_hashed_password, http_response
from src.common.db_operations import get_user_by_username_or_email, put_user_item

def handler(event, context):

    try:
        body = json.loads(event.get('body', '{}'))
        tenant_id = body.get('tenantId')
        username = body.get('username')
        email = body.get('email')
        password = body.get('password')

        if not all([tenant_id, username, email, password]):
            return http_response(400, {'message': 'Missing required fields (tenantId, username, email, password)'})
        
        if len(password) < 8:
            return http_response(400, {'message': 'Password must be at least 8 characters long'})

        if get_user_by_username_or_email(tenant_id, username, is_email=False):
            return http_response(400, {'message': f'Username "{username}" already exists for tenant "{tenant_id}"'})
        
        if get_user_by_username_or_email(tenant_id, email, is_email=True):
            return http_response(400, {'message': f'Email "{email}" already exists for tenant "{tenant_id}"'})

        hashed_password = generate_hashed_password(password)

        user_id = str(uuid.uuid4())
        current_time = int(time.time())

        user_data = {
            'tenantId': tenant_id,
            'userId': user_id,
            'username': username,
            'email': email,
            'passwordHash': hashed_password,
            'createdAt': current_time,
            'updatedAt': current_time,
            'roles': ['customer'] 
        }

        if not put_user_item(user_data):
            return http_response(500, {'message': 'Could not create user due to a database error'})

        return http_response(200, {
            'userId': user_id,
            'message': 'User created successfully'
        })

    except json.JSONDecodeError:
        return http_response(400, {'message': 'Invalid JSON body'})
    except Exception as e:
        print(f"Error creating user: {e}")
        return http_response(500, {'message': f'Internal server error: {e}'})