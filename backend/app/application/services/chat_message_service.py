from langchain_anthropic import ChatAnthropic
import os
from langgraph.prebuilt import create_react_agent
import asyncio
from langchain_core.messages import HumanMessage

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

async def main():
    async for text in chat_message_service("would you generate a poem about a cat"):
        print(text)


# Run the async function
if __name__ == "__main__":
    asyncio.run(main())
    