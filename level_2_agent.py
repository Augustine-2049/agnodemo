from agno.agent import Agent
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge.url import UrlKnowledge
from agno.models.anthropic import Claude
from agno.storage.sqlite import SqliteStorage
from agno.vectordb.lancedb import LanceDb, SearchType


from agno.models.openai import OpenAILike
from agno.models.google import Gemini
from agno.embedder.google import GeminiEmbedder
from agno.agent import AgentKnowledge
from agno.vectordb.pgvector import PgVector
import os

GOOGLE_API_KEY= os.getenv("GOOGLE_API_KEY")
print(GOOGLE_API_KEY)


# Embed sentence in database
embeddings = GeminiEmbedder().get_embedding("The quick brown fox jumps over the lazy dog.")

# Print the embeddings and their dimensions
print(f"Embeddings: {embeddings[:5]}")
print(f"Dimensions: {len(embeddings)}")
# Use an embedder in a knowledge base
# knowledge_base = AgentKnowledge(
#     vector_db=PgVector(
#         db_url="postgresql+psycopg://ai:ai@localhost:5532/ai",
#         table_name="gemini_embeddings",
#         embedder=GeminiEmbedder(),
#     ),
#     num_documents=2,
# )

# Load Agno documentation in a knowledge base
# You can also use `https://docs.agno.com/llms-full.txt` for the full documentation
knowledge = UrlKnowledge(
	# 需要嵌入的知识信息url
    urls=["https://docs.agno.com/introduction.md"],
    # 数据库信息
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="agno_docs",
        search_type=SearchType.hybrid,
        embedder=GeminiEmbedder(),
    ),
)


# Store agent sessions in a SQLite database
storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")

GEMINI_API_KEY= os.getenv("GEMINI_API_KEY")
 
gemini_model = OpenAILike(
    id='gemini-2.0-flash',
    api_key=GEMINI_API_KEY,
    base_url='https://generativelanguage.googleapis.com/v1beta/openai/'
)
agent = Agent(
    name="Agno Assist",
    model=Gemini(id="gemini-2.0-flash"),
    instructions=[
        "Search your knowledge before answering the question.",
        "Only include the output in your response. No other text.",
    ],
    knowledge=knowledge,
    storage=storage,
    add_datetime_to_instructions=True,
    # Add the chat history to the messages
    add_history_to_messages=True,
    # Number of history runs
    num_history_runs=3,
    markdown=True,
    debug_mode=True,
    monitoring=True,
)
if __name__ == "__main__":
    # Load the knowledge base, comment out after first run
    # Set recreate to True to recreate the knowledge base if needed
    agent.knowledge.load(recreate=False)
    agent.print_response("What is Agno?", stream=True)