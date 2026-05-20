import json
from src.config import openai_client, search_client, MODEL_NAME, EMBEDDING_MODEL

def get_embedding(text: str) -> list[float]:
    """Generates vector embeddings using Azure OpenAI."""
    text = text.replace("\n", " ")
    return openai_client.embeddings.create(input=[text], model=EMBEDDING_MODEL).data[0].embedding

def researcher_agent(dossier_text: str) -> str:
    """Agent A: Finds matching reference fraud typologies based on the transaction data."""
    
    # 1. Generate search query focused on transactional anomalies
    query_response = openai_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system", 
                "content": "You are a Cyber Forensics Intelligence Researcher. Summarize the main transactional or behavioral anomaly of this dossier into a 5-word search query to retrieve matching fraud typologies."
            },
            {"role": "user", "content": dossier_text}
        ]
    )
    search_query = query_response.choices[0].message.content

    # 2. Query Azure AI Search with a hybrid approach (Vector + Text)
    vector_query = get_embedding(search_query)
    results = search_client.search(
        search_text=search_query,
        vector_queries=[{"vector": vector_query, "fields": "content_vector", "kind": "vector"}],
        top=2
    )

    # 3. Consolidate forensic evidence
    evidence = ""
    for res in results:
        evidence += f"- {res['content']}\n"

    return evidence if evidence else "No matching reference fraud typologies found in database."

def auditor_agent(dossier_text: str, evidence: str) -> dict:
    """Agent B: The Forensic Analyst evaluating the payload against intelligence trends."""
    
    system_prompt = """
    You are a Senior Financial Fraud Investigator at a Bank.
    Your goal is to identify unauthorized activity or coordinated attack patterns by evaluating a 'Transaction Dossier' against retrieved 'Fraud Typologies'.

    CRITICAL INSTRUCTION:
    - If the dossier indicates confirmed fraudulent patterns or compromised credentials, flag it as 'FRAUDULENT'.
    - If the activity aligns with verified legitimate customer behavior or pre-authenticated context, flag it as 'SAFE'.
    - If the transaction exhibits high-risk indicators but requires immediate human review (e.g., suspected account takeover), flag it as 'SUSPICIOUS'.

    Output ONLY a valid JSON object:
    {
        "status": "SAFE" | "FRAUDULENT" | "SUSPICIOUS",
        "violations": ["list of specific risk indicators or anomalies detected"],
        "reasoning": "Brief forensic explanation of the transaction behavior",
        "confidence_score": 0.0-1.0
    }
    """

    user_content = f"RETRIEVED FRAUD TYPOLOGIES:\n{evidence}\n\nTRANSACTION DOSSIER TO EVALUATE:\n{dossier_text}"

    response = openai_client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ],
        response_format={ "type": "json_object" }
    )

    return json.loads(response.choices[0].message.content)