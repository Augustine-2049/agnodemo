from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

from agno.models.openai import OpenAILike
import os
GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
QWEN_API_KEY=os.getenv("QWEN_API_KEY")
 

qw_model = OpenAILike(
    id= 'qwen-turbo', # qwen-turbo / qwen3-235b-a22b / gemini-2.0-flash
    api_key=QWEN_API_KEY,
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1/',
)
gemini_model = OpenAILike(
    id='gemini-2.0-flash',
    api_key=GEMINI_API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)

agent_storage: str = "tmp/agents.db"

web_agent = Agent(
    name="Web Agent",
    model=gemini_model,
    tools=[
        # DuckDuckGoTools()
        ],
    instructions=["Always include sources"],
    # Store the agent sessions in a sqlite database
    storage=SqliteStorage(table_name="web_agent", db_file=agent_storage),
    # Adds the current date and time to the instructions
    add_datetime_to_instructions=True,
    # Adds the history of the conversation to the messages
    add_history_to_messages=True,
    # Number of history responses to add to the messages
    num_history_responses=5,
    # Adds markdown formatting to the messages
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    model=gemini_model, # OpenAIChat(id="gpt-4o"),
    tools=[
        # YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)
        ],
    instructions=["Always use tables to display data"],
    storage=SqliteStorage(table_name="finance_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

playground = Playground(agents=[web_agent, finance_agent])
app = playground.get_app()

if __name__ == "__main__":
    playground.serve("playground:app", reload=True)