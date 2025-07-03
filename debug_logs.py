from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.google import Gemini
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

agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),# gemini_model,
    tools=[YFinanceTools(stock_price=True)],
    instructions="Use tables to display data. Don't include any other text.",
    markdown=True,
    # debug_mode=True,
    monitoring=True,
)

agent.print_response("What is the stock price of Apple??", stream=True)