import json
from src.common.utils import decode_jwt, http_response

def handler(event, context):

    try:
        auth_header = event.get('headers', {}).get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return http_response(401, {'message': 'Authorization header missing or malformed'})

        token = auth_header.split(' ')[1]

        try:
            decoded_payload = decode_jwt(token)
        except ValueError as e: 
            return http_response(401, {'message': f'Unauthorized: {e}'})
        
        user_id = decoded_payload.get('sub')
        tenant_id = decoded_payload.get('tenantId')
        roles = decoded_payload.get('roles', [])

        if not all([user_id, tenant_id]):
            return http_response(401, {'message': 'Invalid token payload (missing user/tenant info)'})

        return http_response(200, {
            'userId': user_id,
            'tenantId': tenant_id,
            'roles': roles,
            'message': 'Token is valid'
        })

    except Exception as e:
        print(f"Error validating token: {e}")
        return http_response(500, {'message': f'Internal server error: {e}'})