from langchain_anthropic import ChatAnthropic
import os
from langgraph.prebuilt import create_react_agent
import asyncio
from langchain_core.messages import HumanMessage
from app.infrastructure.repositories.chat_repository import ChatRepository

model = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    anthropic_api_key=os.environ["ANTHROPIC_API_KEY"],
)

tools = []

agent_executor = create_react_agent(
   model, tools
)

async def chat_message_service(message: str):
    async for step, metadata in agent_executor.astream(
        {"messages": [HumanMessage(content=message)]},
        stream_mode="messages",
    ):
        if metadata["langgraph_node"] == "agent" and (text := step.text()):
            yield text

class ChatMessageService:
    def __init__(self, chat_repository: ChatRepository = ChatRepository(f"{os.environ['ENV']}-chat-messages")):
        self.chat_repository = chat_repository

    async def get_threads_by_user_id(self, user_id: str):
        threads = self.chat_repository.list(user_id)
        return threads



# Run the async function
if __name__ == "__main__":
    async def main():
        chat_message_service = ChatMessageService()
        threads = await chat_message_service.get_threads_by_user_id("test-user-123")
        print(threads)

    asyncio.run(main())
    