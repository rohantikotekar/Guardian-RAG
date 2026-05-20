from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pypdf import PdfReader
from src.models import TextAuditRequest, AuditResponse
from src.agents import researcher_agent, auditor_agent
from src.database import log_audit

router = APIRouter()

@router.post("/audit/text", response_model=AuditResponse)
def audit_raw_text(request: TextAuditRequest):
    """Audits raw text submitted via JSON payload."""
    try:
        # 1. Research Phase
        evidence = researcher_agent(request.content)
        
        # 2. Audit Phase
        audit_result = auditor_agent(request.content, evidence)
        
        # 3. Log to Database
        log_audit(request.doc_name, request.content, evidence, audit_result)
        
        # 4. Construct Response
        return AuditResponse(
            status=audit_result.get("status", "UNKNOWN"),
            violations=audit_result.get("violations", []),
            reasoning=audit_result.get("reasoning", "No reasoning provided."),
            confidence_score=audit_result.get("confidence_score"),
            regulatory_evidence=evidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audit/file", response_model=AuditResponse)
async def audit_file(file: UploadFile = File(...), doc_name: str = Form(...)):
    """Audits an uploaded PDF or TXT file."""
    if not file.filename.endswith(('.pdf', '.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are supported.")
        
    try:
        content = ""
        contents = await file.read()
        
        if file.filename.endswith('.pdf'):
            # Save temporarily to read with pypdf
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                temp_pdf.write(contents)
                temp_pdf_path = temp_pdf.name
                
            reader = PdfReader(temp_pdf_path)
            content = "".join([page.extract_text() + "\n" for page in reader.pages])
        else:
            content = contents.decode('utf-8')
            
        # Run identical pipeline
        evidence = researcher_agent(content)
        audit_result = auditor_agent(content, evidence)
        log_audit(doc_name, content, evidence, audit_result)
        
        return AuditResponse(
            status=audit_result.get("status", "UNKNOWN"),
            violations=audit_result.get("violations", []),
            reasoning=audit_result.get("reasoning", "No reasoning provided."),
            confidence_score=audit_result.get("confidence_score"),
            regulatory_evidence=evidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))