import json
from src.common.utils import check_password, generate_jwt, http_response
from src.common.db_operations import get_user_by_username_or_email

def handler(event, context):

    try:
        body = json.loads(event.get('body', '{}'))
        tenant_id = body.get('tenantId')
        username_or_email = body.get('username') 
        password = body.get('password')

        if not all([tenant_id, username_or_email, password]):
            return http_response(400, {'message': 'Missing required fields (tenantId, username/email, password)'})

        user = get_user_by_username_or_email(tenant_id, username_or_email, is_email='@' in username_or_email)
        
        if not user:
            return http_response(401, {'message': 'Invalid credentials'})

        if not check_password(password, user['passwordHash']):
            return http_response(401, {'message': 'Invalid credentials'})

        token = generate_jwt(user['userId'], user['tenantId'], user.get('roles', ['customer']))

        return http_response(200, {
            'token': token,
            'message': 'Login successful'
        })

    except json.JSONDecodeError:
        return http_response(400, {'message': 'Invalid JSON body'})
    except Exception as e:
        print(f"Error logging in user: {e}")
        return http_response(500, {'message': f'Internal server error: {e}'})