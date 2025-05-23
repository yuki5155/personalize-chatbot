import os
from data.dynamodb_connection import get_dynamodb_resource, get_dynamodb_client

def delete_dynamodb_table(table_name: str):
    dynamodb = get_dynamodb_resource()
    dynamodb.Table(table_name).delete()

if __name__ == "__main__":
    delete_dynamodb_table("dev-chat-messages")
