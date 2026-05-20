import uuid
from datetime import datetime
from src.config import cosmos_client

DATABASE_NAME = 'GuardianAuditDB'
CONTAINER_NAME = 'AuditLogs'

def get_audit_container():
    """Ensures database and container exist, returns the container client."""
    db = cosmos_client.create_database_if_not_exists(id=DATABASE_NAME)
    container = db.create_container_if_not_exists(
        id=CONTAINER_NAME,
        partition_key="/doc_name",
        offer_throughput=400
    )
    return container

def log_audit(doc_name: str, content: str, evidence: str, audit_result: dict):
    """Saves the full context of an audit to Cosmos DB."""
    container = get_audit_container()
    
    audit_entry = {
        "id": str(uuid.uuid4()),
        "doc_name": doc_name,
        "timestamp": datetime.utcnow().isoformat(),
        "input_content": content[:1000],  # Store snippet for preview
        "retrieved_evidence": evidence,
        "final_decision": audit_result,
        "framework_version": "FS-AI RMF 2026"
    }
    
    container.upsert_item(audit_entry)