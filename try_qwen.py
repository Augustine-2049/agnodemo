from agno.agent import Agent
from agno.models.openai import OpenAILike
import os
from agno.playground import Playground
from agno.tools import tool

qw_model = OpenAILike(
    id= 'qwen-turbo', # qwen-turbo / qwen3-235b-a22b
    api_key='sk-295ced4ab5a042d3949d48232553c078',
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1/',
    
    # extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    # parameters={"enable_thinking": False},  # 添加这行关键参数
    # enable_thinking=False,
)

@tool()
def add_tools(x: int, y: int) -> str:
    """计算两个数之和"""
    return x + y

agent = Agent(
    model=qw_model,
    tools=[add_tools],
    instructions="请你使用中文回答问题",
    markdown=True,
    debug_mode=True,
    # extra_body={"chat_template_kwargs": {"enable_thinking": False}},
)

playground = Playground(agents=[agent])
app = playground.get_app()

# agent.run("请计算1 + 2 /no_think") 跑起来自身可能就是server
if __name__ == "__main__":
    playground.serve("main:app", reload=True)



