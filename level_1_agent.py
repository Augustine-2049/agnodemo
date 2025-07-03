from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.openai import OpenAILike
from agno.tools.yfinance import YFinanceTools

qw_model = OpenAILike(
    id= 'qwen-turbo', # qwen-turbo / qwen3-235b-a22b
    api_key='sk-295ced4ab5a042d3949d48232553c078',
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1/',
)
agent = Agent(
    model=qw_model,
    tools=[YFinanceTools(stock_price=True)],
    instructions="Use tables to display data. Don't include any other text.",
    markdown=True,
    debug_mode=True,
)
# agent = Agent(
#     model=Claude(id="claude-sonnet-4-20250514"),
#     tools=[YFinanceTools(stock_price=True)],
#     instructions="Use tables to display data. Don't include any other text.",
#     markdown=True,
# )
agent.print_response("What is the stock price of Apple?", stream=True)