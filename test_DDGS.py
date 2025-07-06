from duckduckgo_search import DDGS
import time


# proxies = {
#     "http": "http://your-proxy-ip:port",
#     "https": "http://your-proxy-ip:port",
# }

# with DDGS(proxies=proxies) as ddgs:
#     results = ddgs.text("python programming", max_results=5)
#     time.sleep(2)  # 每次请求后等待 2 秒
#     print(results)


target_results = DDGS().text(
    keywords="python programming", 
    region="cn-zh",
    max_results=5
)
print(target_results)

