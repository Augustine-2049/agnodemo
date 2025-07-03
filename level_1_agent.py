from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.openai import OpenAILike
from agno.tools.yfinance import YFinanceTools


from agno.models.google import Gemini
agent = Agent(
    model=Gemini(id="gemini-2.0-flash"),
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