# dynamodbの接続

import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
import os

# CRUD操作

class DynamoDBConnection:
    def __init__(self, table_name: str, region_name: str = None):
        # 環境変数からDynamoDBの設定を取得
        is_local = os.getenv('IS_LOCAL', 'false').lower() == 'true'
        region = region_name or os.getenv('AWS_REGION', 'us-east-1')
        
        # Initialize the DynamoDB resource
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
            for endpoint_url in endpoints:
                try:
                    print(f"DynamoDB接続を試行中: {endpoint_url}")
                    dynamodb_resource = boto3.resource(
                        'dynamodb',
                        region_name=region,
                        endpoint_url=endpoint_url,
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'dummy'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'dummy')
                    )
                    # 接続テスト
                    dynamodb_resource.meta.client.list_tables()
                    print(f"DynamoDB接続成功: {endpoint_url}")
                    connected = True
                    break
                except Exception as e:
                    print(f"DynamoDB接続失敗 ({endpoint_url}): {e}")
            
            if not connected:
                raise ConnectionError("すべてのエンドポイントへの接続に失敗しました。DynamoDB Localが起動していることを確認してください。")
        else:
            dynamodb_resource = boto3.resource('dynamodb', region_name=region)
        
        self.table = dynamodb_resource.Table(table_name)

    def get_table(self):
        return self.table
    
    def create(self, item: dict):
        # itemにcreatedAtとupdatedAtがない場合は追加
        if 'createdAt' not in item:
            item['createdAt'] = datetime.now().isoformat()
        if 'updatedAt' not in item:
            item['updatedAt'] = datetime.now().isoformat()
        self.table.put_item(Item=item)

    def read(self, key: dict):
        response = self.table.get_item(Key=key)
        return response.get('Item')
    
    def read_via_gsi(self, gsi_name: str, key_name: str, key_value: str):
        response = self.table.query(
            IndexName=gsi_name,
            KeyConditionExpression=Key(key_name).eq(key_value)
        )
        return response.get('Items')
    
    def update(self, key: dict, update_expression: str, expression_attribute_values: dict, expression_attribute_names: dict = None):
        # 更新時にupdatedAtを自動的に設定
        if ':updatedAt' not in expression_attribute_values:
            if update_expression.startswith('set '):
                update_expression += ', updatedAt = :updatedAt'
            else:
                update_expression = 'set updatedAt = :updatedAt, ' + update_expression
            expression_attribute_values[':updatedAt'] = datetime.now().isoformat()
        
        update_params = {
            'Key': key,
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_attribute_values
        }
        
        if expression_attribute_names:
            update_params['ExpressionAttributeNames'] = expression_attribute_names
        
        self.table.update_item(**update_params)

    def delete(self, key: dict):
        self.table.delete_item(Key=key)
        
        
if __name__ == '__main__':
    # テーブルが既に作成されていることを確認してから実行
    # データモデルに合わせてキーを辞書形式で指定
    connection = DynamoDBConnection('dev-chat-messages')
    try:
        connection.create({'thread_id': '1', 'timestamp': datetime.now().isoformat(), 'message': 'Hello, world!', 'user_id': 'test-user'})
        print(connection.read({'thread_id': '1', 'timestamp': datetime.now().isoformat()}))
        
        # 更新の例
        connection.update(
            {'thread_id': '1', 'timestamp': datetime.now().isoformat()},
            'set message = :msg',
            {':msg': 'Hello, world! (updated)'}
        )
        
        # GSIを使った検索の例
        items = connection.read_via_gsi('user_id-index', 'user_id', 'test-user')
        print(f"Found {len(items)} items for user test-user")
        print(items)
    except Exception as e:
        print(f"Error: {e}")
        print("テーブルが存在しない場合は、docker-compose upでDynamoDB Localを起動し、")
        print("python data/dynamodbs.pyを実行してテーブルを作成してください。")