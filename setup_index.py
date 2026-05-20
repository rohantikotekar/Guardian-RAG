from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchFieldDataType, SearchableField, 
    SearchField, VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile
)
from src.config import search_index_client, search_client, index_name
from src.agents import get_embedding

def create_index_and_upload():
    print("Creating index schema...")
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchableField(name="category", type=SearchFieldDataType.String, filterable=True),
        SearchField(name="content_vector", type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
                    searchable=True, vector_search_dimensions=1536, vector_search_profile_name="myHnswProfile")
    ]

    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="myHnswAlg")],
        profiles=[VectorSearchProfile(name="myHnswProfile", algorithm_configuration_name="myHnswAlg")]
    )

    index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)
    search_index_client.create_or_update_index(index)
    print(f"Index '{index_name}' created successfully.")

    laws = [
    {
        "id": "type_carding_velocity",
        "category": "Carding Attack",
        "content": "Carding attacks involve a low-value micro-transaction (under $2.00) used as a test charge to verify card validity, rapidly followed by a high-value retail or electronics purchase (over $500) within a tight time window (under 10 minutes)."
    },
    {
        "id": "type_mule_layering",
        "category": "Money Laundering",
        "content": "Money mule behavior is characterized by rapid funds layering, where an account receives an unusually large inbound transfer (or multiple peer-to-peer transfers) and immediately distributes 90% or more of those funds to unverified external accounts or crypto wallets within 24 hours."
    },
    {
        "id": "type_synthetic_identity",
        "category": "Identity Fraud",
        "content": "Synthetic identity fraud involves credit applications using freshly issued SSNs or thin-file profiles that share high-risk velocity indicators, such as a phone number, email address, or physical address tied to previously blacklisted or charged-off accounts."
    },
    {
        "id": "type_ato_location",
        "category": "Account Takeover",
        "content": "Account Takeover (ATO) is flagged when a high-risk transaction originating from an IP address or geolocation exhibits an impossible travel distance (e.g., crossing continents) relative to the location of the customer's last cleared transaction within a 12-hour window."
    },
    {
        "id": "type_friendly_fraud",
        "category": "First Party Fraud",
        "content": "Friendly fraud or chargeback abuse patterns occur when a customer maintains a consistent digital fingerprint (matching IP, device ID, and historical shipping address) for a purchase, but subsequently files a dispute claiming the transaction was unauthorized."
    }
]
    
    print("Generating embeddings and uploading documents...")
    docs_to_upload = []
    for law in laws:
        law["content_vector"] = get_embedding(law["content"])
        docs_to_upload.append(law)

    search_client.upload_documents(documents=docs_to_upload)
    print("Regulatory laws uploaded to Azure AI Search.")

if __name__ == "__main__":
    create_index_and_upload()