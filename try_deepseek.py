# Please install OpenAI SDK first: `pip3 install openai`
 
from openai import OpenAI
import os

DEEPSEEK_API_KEY= os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
 
response = client.chat.completions.create(
    # model="deepseek-chat",
    model='deepseek-reasoner',
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False
)
 
print(response.choices[0].message.content)