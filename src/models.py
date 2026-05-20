from pydantic import BaseModel, Field
from typing import List, Optional

class TextAuditRequest(BaseModel):
    doc_name: str = Field(..., description="Name of the document being audited")
    content: str = Field(..., description="The raw text content to audit")

class AuditResponse(BaseModel):
    status: str
    violations: List[str]
    reasoning: str
    confidence_score: Optional[float] = None
    regulatory_evidence: str