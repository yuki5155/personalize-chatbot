import os
from data.dynamodb_connection import get_dynamodb_resource, get_dynamodb_client
from data.dynamodb_tables import create_dynamodb_tables, list_tables

# 後方互換性のためにエクスポート
if __name__ == "__main__":
    create_dynamodb_tables()
    list_tables()
