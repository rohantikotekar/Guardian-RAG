import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.cosmos import CosmosClient

# Load environment variables from your .env file
load_dotenv()

# --- Azure OpenAI ---
# Used for the Researcher and Auditor agents, and generating embeddings
openai_client = AzureOpenAI(
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
    api_key=os.getenv('AZURE_OPENAI_KEY'),
    api_version="2024-02-15-preview" 
)
MODEL_NAME = os.getenv('OPENAI_MODEL_NAME', 'guardian-auditor')
EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL', 'guardian-embedder')

# --- Azure AI Search ---
# Used for vector search and retrieving regulatory laws
search_credential = AzureKeyCredential(os.getenv('AZURE_SEARCH_KEY'))
search_endpoint = os.getenv('AZURE_SEARCH_ENDPOINT')
index_name = os.getenv('SEARCH_INDEX_NAME', 'guardian-regulatory-index')

search_index_client = SearchIndexClient(endpoint=search_endpoint, credential=search_credential)
search_client = SearchClient(endpoint=search_endpoint, index_name=index_name, credential=search_credential)

# --- Azure Cosmos DB ---
# Used for logging the full audit trails
cosmos_client = CosmosClient(
    url=os.getenv('COSMOS_ENDPOINT'), 
    credential=os.getenv('COSMOS_KEY')
)