from openai import OpenAI
import os
 
GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
 
client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
 
response = client.chat.completions.create(
    model="gemini-2.0-flash",
    n=1,    # 返回一个候选回答
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Explain to me how AI works"
        }
    ]
)
 
print(response.choices[0].message)