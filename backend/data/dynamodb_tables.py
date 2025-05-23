import os
from botocore.exceptions import ClientError
from data.dynamodb_connection import get_dynamodb_resource, get_dynamodb_client

def create_dynamodb_tables():
    """DynamoDBテーブルを作成する関数"""
    
    # DynamoDBリソースを取得
    dynamodb = get_dynamodb_resource()
    if not dynamodb:
        return
    
    # 環境に応じたテーブル名プレフィックス
    env = os.getenv('ENV', 'dev')
    
    # テーブル定義
    tables_config = [
        {
            'TableName': f"{env}-chat-messages",
            'KeySchema': [
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'createdAt',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            'AttributeDefinitions': [
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'createdAt',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'user_id',
                    'AttributeType': 'S'
                }
            ],
            'GlobalSecondaryIndexes': [
                {
                    'IndexName': 'user_id-index',
                    'KeySchema': [
                        {
                            'AttributeName': 'user_id',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'createdAt',
                            'KeyType': 'RANGE'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 5,
                        'WriteCapacityUnits': 5
                    }
                }
            ],
            'ProvisionedThroughput': {
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        }
    ]
    
    # テーブルを作成
    for table_config in tables_config:
        try:
            table = dynamodb.create_table(**table_config)
            print(f"テーブル '{table_config['TableName']}' を作成中...")
            table.wait_until_exists()
            print(f"テーブル '{table_config['TableName']}' が正常に作成されました。")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceInUseException':
                print(f"テーブル '{table_config['TableName']}' は既に存在します。")
            else:
                print(f"テーブル '{table_config['TableName']}' の作成中にエラーが発生しました: {e}")

def list_tables():
    """作成されたテーブルの一覧を表示"""
    client = get_dynamodb_client()
    if not client:
        return
    
    try:
        response = client.list_tables()
        print("作成されたテーブル:")
        for table_name in response['TableNames']:
            print(f"  - {table_name}")
    except ClientError as e:
        print(f"テーブル一覧の取得中にエラーが発生しました: {e}")

if __name__ == "__main__":
    create_dynamodb_tables()