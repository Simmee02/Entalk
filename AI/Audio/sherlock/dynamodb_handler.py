import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def get_dynamodb_client():
    aws_access_key_id = os.getenv('aws_access_key_id')
    aws_secret_access_key = os.getenv('aws_secret_access_key')
    region_name = os.getenv('region_name')

    dynamodb = boto3.client('dynamodb',
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            region_name=region_name)
    return dynamodb

def get_text_from_dynamodb(dynamodb, table_name):
    try:
        response = dynamodb.scan(TableName=table_name)
        items = response['Items']

        max_project = max(items, key=lambda x: int(x['entalkproject']['N']))
        filtered_items = [item for item in items if item['entalkproject']['N'] == max_project['entalkproject']['N'] and item['id']['S'] == '2']

        if filtered_items:
            return filtered_items[0]['text']['S']
        else:
            return "조건에 맞는 항목이 없습니다."
    except Exception as e:
        return "데이터 가져오기 오류: " + str(e)
