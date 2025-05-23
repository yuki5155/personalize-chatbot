from app.infrastructure.persistence.database.connection import DynamoDBConnection
from app.infrastructure.models.chat_model import ChatModel, ChatMessage
from app.domain.enums import ChatMessageRole
from datetime import datetime
from typing import List
class ChatRepository:
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.dynamodb_connection = DynamoDBConnection(table_name)

    def create(self, chat_model: ChatModel):
        self.dynamodb_connection.create(chat_model.to_dict())

    def read(self, chat_model: ChatModel)->ChatModel:
        key = {'id': chat_model.id, 'createdAt': chat_model.createdAt}
        item = self.dynamodb_connection.read(key)
        if item is None:
            return None

        return ChatModel(
            id=item['id'],
            messages=[ChatMessage.from_json(message) for message in item['messages']],
            is_active=item['is_active'],
            title=item['title'],
            user_id=item['user_id'],
            createdAt=item['createdAt'],
            updatedAt=item['updatedAt']
        )
    
    def read_by_id(self, id: str)->ChatModel:
        # Query using only the partition key (id)
        items = self.dynamodb_connection.query(key_name='id', key_value=id)
        if not items or len(items) == 0:
            return None
        
        # Use the first matching item
        item = items[0]
        return ChatModel(
            id=item['id'],
            messages=[ChatMessage.from_json(message) for message in item['messages']],
            is_active=item['is_active'],
            title=item['title'],
            user_id=item['user_id'],
            createdAt=item['createdAt'],
            updatedAt=item['updatedAt']
        )

    def update(self, chat_model: ChatModel):
        key = {'id': chat_model.id, 'createdAt': chat_model.createdAt}
        # メッセージをJSON文字列のリストに変換
        messages_json = [message.to_json() for message in chat_model.messages]
        # Update the model's updatedAt before creating the update expression
        chat_model.updatedAt = datetime.now().isoformat()
        
        update_expression = "set messages = :m, user_id = :u"
        expression_attribute_values = {
            ':m': messages_json,
            ':u': chat_model.user_id
        }
        self.dynamodb_connection.update(key, update_expression, expression_attribute_values)

    def delete(self, chat_model: ChatModel):
        key = {'id': chat_model.id, 'createdAt': chat_model.createdAt}
        self.dynamodb_connection.delete(key)

    def list(self, user_id: str)->List[ChatModel]:
        items = self.dynamodb_connection.read_via_gsi('user_id-index', 'user_id', user_id)
        chat_models = []
        for item in items:
            chat_models.append(ChatModel(
                id=item['id'],
                messages=[ChatMessage.from_json(message) for message in item['messages']],
                user_id=item['user_id'],
                is_active=item['is_active'],
                title=item['title'],
                createdAt=item['createdAt'],
                updatedAt=item['updatedAt']
            ))
        return chat_models
    



if __name__ == "__main__":
    from app.infrastructure.models.chat_model import ChatMessage, ChatModel
    from app.domain.enums import ChatMessageRole
    
    chat_repository = ChatRepository("dev-chat-messages")
    chat_model = ChatModel(
        messages=[ChatMessage(message="Hello, how are you?", role=ChatMessageRole.USER)],
        user_id="test-user-123",
        title="Test Title",
        is_active=True
    )
    chat_repository.create(chat_model)
    # print(chat_repository.read(chat_model))
    chat_model.messages[0].message = "Hello, how are you?"
    chat_repository.update(chat_model)
    # print(chat_repository.read(chat_model))
    # print(chat_repository.list("test-user-123"))
    chat_repository.delete(chat_model)
    # print(chat_repository.read(chat_model))

    # session作成を想定してチャットを作成
    chat_model = ChatModel(
        user_id="test-user-123",
        title="Test Title"
    )
    
    from app.domain.threads_domain import ThreadDomain
    from app.domain.chat_messages_domain import ChatMessagesDomain, ChatMessageDomain
    
    # Create chat messages domain
    chat_messages = ChatMessagesDomain(
        messages=[]
    )
    
    # Create thread domain with required fields
    thread_domain = ThreadDomain(
        name="Test Thread",
        chat_messages=chat_messages,
        user_id="test-user-123",
        title="Test Title",
        is_active=True
    )

    print(thread_domain.to_repository())
    
    chat_repository.create(thread_domain.to_repository())
    
    # read
    chat_model = chat_repository.read_by_id(thread_domain.id)
    print(chat_model)

    # to domain
    chat_model_domain = chat_model.to_domain()
    print(chat_model_domain)

    # add message
    chat_model_domain.add_user_message("Hello, how are you?")
    print(chat_model_domain)
    
    # Save the updated model back to the repository
    updated_model = chat_model_domain.to_repository()
    chat_repository.update(updated_model)
    
    # Read it back to verify the changes
    updated_chat_model = chat_repository.read_by_id(thread_domain.id)
    print("Updated model from repository:")
    print(updated_chat_model)
    
    # Add an assistant message
    chat_model_domain.add_assistant_message("I'm doing well, thank you! How can I help you today?")
    updated_model = chat_model_domain.to_repository()
    chat_repository.update(updated_model)
    
    # Final read
    final_chat_model = chat_repository.read_by_id(thread_domain.id)
    print("Final model with assistant response:")
    print(final_chat_model.to_domain())



    
    