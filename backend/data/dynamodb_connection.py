import boto3
import os
from botocore.exceptions import ClientError

def get_dynamodb_resource():
    """DynamoDBリソースへの接続を取得する関数"""
    
    # 環境変数からDynamoDBの設定を取得
    is_local = os.getenv('IS_LOCAL', 'false').lower() == 'true'
    
    if is_local:
        # 接続エンドポイントの候補リスト
        endpoints = [
            os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:8000'),
            'http://dynamodb-local:8000',
            'http://host.docker.internal:8000',
            'http://localhost:8000'
        ]
        
        # 各エンドポイントを試す
        connected = False
        dynamodb = None
        for endpoint_url in endpoints:
            try:
                print(f"DynamoDB接続を試行中: {endpoint_url}")
                dynamodb = boto3.resource(
                    'dynamodb',
                    region_name=os.getenv('AWS_REGION', 'us-east-1'),
                    endpoint_url=endpoint_url,
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'dummy'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'dummy')
                )
                # 接続テスト
                client = dynamodb.meta.client
                client.list_tables()
                print(f"DynamoDB接続成功: {endpoint_url}")
                connected = True
                break
            except Exception as e:
                print(f"DynamoDB接続失敗 ({endpoint_url}): {e}")
        
        if not connected:
            print("すべてのエンドポイントへの接続に失敗しました。DynamoDB Localが起動していることを確認してください。")
            return None
    else:
        dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        # 接続テスト
        try:
            client = dynamodb.meta.client
            client.list_tables()
            print("DynamoDB接続成功")
        except Exception as e:
            print(f"DynamoDB接続エラー: {e}")
            return None
    
    return dynamodb

def get_dynamodb_client():
    """DynamoDBクライアントへの接続を取得する関数"""
    
    # 環境変数からDynamoDBの設定を取得
    is_local = os.getenv('IS_LOCAL', 'false').lower() == 'true'
    
    if is_local:
        # 接続エンドポイントの候補リスト
        endpoints = [
            os.getenv('DYNAMODB_ENDPOINT', 'http://localhost:8000'),
            'http://dynamodb-local:8000',
            'http://host.docker.internal:8000',
            'http://localhost:8000'
        ]
        
        # 各エンドポイントを試す
        connected = False
        client = None
        for endpoint_url in endpoints:
            try:
                print(f"DynamoDB接続を試行中: {endpoint_url}")
                client = boto3.client(
                    'dynamodb',
                    region_name=os.getenv('AWS_REGION', 'us-east-1'),
                    endpoint_url=endpoint_url,
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'dummy'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'dummy')
                )
                client.list_tables()
                print(f"DynamoDB接続成功: {endpoint_url}")
                connected = True
                break
            except Exception as e:
                print(f"DynamoDB接続失敗 ({endpoint_url}): {e}")
        
        if not connected:
            print("すべてのエンドポイントへの接続に失敗しました。DynamoDB Localが起動していることを確認してください。")
            return None
    else:
        client = boto3.client('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        # 接続テスト
        try:
            client.list_tables()
            print("DynamoDB接続成功")
        except Exception as e:
            print(f"DynamoDB接続エラー: {e}")
            return None
    
    return client 