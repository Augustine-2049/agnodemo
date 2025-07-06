# 金融研报自动生成系统
这首先是一个基于 https://docs.agno.com/ 的学习文档，由于CloseAI的API要钱，所以我使用Gemini重写运行。
- 目前部分代码仍未跑通，比如YFinance请求过快
- 需要详细了解memory、reasoning、knowledge等模块以优化返回信息。

后续或许会是基于 agno 工作流引擎的智能金融研报生成系统，支持企业分析、行业分析、宏观经济分析。

技术栈：agno\MCP\agent\prompt


# 环境配置
```bash
uv init  # 如果有pyproject.toml则不需要这一行
uv add agno openai 
uv add fastapi uvicorn yfinance  # level_1_agent
uv add sqlalchemy lancedb tantivy  # level_2/3
uv add duckduckgo-search  # level_4 一种web搜索引擎
uv add pgvector psycopg pylance # level_2(gemini)

uv add anthropic  # 如果使用claude模型
uv run .\main.py  # 注意使用千问模型，则需要提前配置API_KEY
```

全局变量设置
- `win + R` -> input `sysdm.cpl` -> `高级` -> `环境变量` -> `系统变量`，根据需要添加以下变量名:
  - `OPENAI_API_KEY`
  - `GOOGLE_API_KEY`, `GEMINI_API_KEY`
  - ...

不同模型配置方法
- https://blog.csdn.net/2401_83010216/article/details/148111686
- https://blog.csdn.net/kkkkkkkkkasey/article/details/147295684
- [x] qwen + gemini
- [ ] deepseek + gpt(money) + claude(close register)


# agno 常用库
```py
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.openai import OpenAILike

from agno.utils.log import logger
from agno.utils.pprint import pprint_run_response
from agno.team.team import Team
from agno.workflow import Workflow

from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.url import UrlKnowledge
from agno.storage.sqlite import SqliteStorage
from agno.vectordb.lancedb import LanceDb, SearchType

from agno.tools.yfinance import YFinanceTools
```

# 数据收集层
## 财务报告

## 公告
- [x] 上交所
- [x] 深交所
- [ ] 港交所


## 舆情
- [x] 东方财富网
- [ ] 雪球
- [ ] 同花顺
- [ ] 新浪财经
- [ ] 腾讯财经
- [ ] 网易财经
- [ ] 金融界

## 新闻
- [ ] 新浪财经
- [ ] 腾讯财经
- [ ] 网易财经
- [ ] 金融界



## 政策
- [ ] 证券时报网
- [ ] 中国证券网


# UI
- ui界面默认起在了 http://localhost:3000
- Uvicorn running on http://localhost:7777
```bash
cd ..
npx create-agent-ui@latest
cd agent-ui && npm run dev
```


# 备注
1. 使用千问模型qwen-turbo，注意最新的千问模型需要传enable_thinking，还不知咋搞。


