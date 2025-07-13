import os
import boto3
from botocore.exceptions import ClientError

USERS_TABLE_NAME = os.environ.get('USERS_TABLE_NAME')
dynamodb = boto3.resource('dynamodb')
users_table = dynamodb.Table(USERS_TABLE_NAME)

def get_user_by_username_or_email(tenant_id, identifier, is_email=False):

    try:
        if is_email:
            
            response = users_table.query(
                IndexName='EmailIndex',
                KeyConditionExpression='tenantId = :tid AND email = :id',
                ExpressionAttributeValues={
                    ':tid': tenant_id,
                    ':id': identifier
                }
            )
        else:
            response = users_table.query(
                IndexName='UsernameIndex',
                KeyConditionExpression='tenantId = :tid AND username = :id',
                ExpressionAttributeValues={
                    ':tid': tenant_id,
                    ':id': identifier
                }
            )
        return response['Items'][0] if response['Items'] else None
    except ClientError as e:
        print(f"Error querying user by identifier: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def put_user_item(user_data):

    try:
        users_table.put_item(Item=user_data)
        return True
    except ClientError as e:
        print(f"Error putting user item: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False