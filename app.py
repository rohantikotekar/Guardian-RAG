import gradio as gr
from pypdf import PdfReader

# Import your tools from the 'src' architecture
from src.agents import researcher_agent, auditor_agent
from src.database import log_audit

# --- Helper to Extract Text from Files ---
def extract_text(file_obj, raw_text):
    # Priority 1: Use File if uploaded
    if file_obj is not None:
        if file_obj.name.endswith('.pdf'):
            reader = PdfReader(file_obj.name)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text, file_obj.name
        else:
            with open(file_obj.name, 'r', encoding='utf-8') as f:
                return f.read(), file_obj.name
    # Priority 2: Use Raw Text box
    return raw_text, "Manual_Entry.txt"

# --- Main Logic ---
def process_fraud_investigation(file_obj, raw_text):
    # Extract content and determine name
    content, doc_name = extract_text(file_obj, raw_text)

    if not content or content.strip() == "":
        return "Unknown", "N/A", "N/A", "Please upload a dossier file or paste transaction payload text."

    # 1. Research (Queries Azure AI Search for matching fraud typologies)
    evidence = researcher_agent(content)

    # 2. Audit / Forensic Evaluation
    audit_result = auditor_agent(content, evidence)

    # 3. Log to Cosmos DB
    log_audit(doc_name, content, evidence, audit_result)

    # --- Fixed UI Mapping Status Logic ---
    status_raw = audit_result.get('status', 'SUSPICIOUS').upper()
    
    if status_raw == "SAFE":
        status_text = "✅ SAFE"
    elif status_raw == "FRAUDULENT":
        status_text = "❌ FRAUDULENT"
    else:
        status_text = "⚠️ SUSPICIOUS (Review Required)"

    # Format risk indicators / violations
    violations_text = "\n".join([f"- {v}" for v in audit_result.get('violations', [])])
    if not violations_text:
        violations_text = "No risk anomalies flagged."

    return status_text, audit_result.get('reasoning', ''), violations_text, evidence

# --- Build the UI ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🛡️ Guardian-RAG: Credit Card Fraud Forensics Engine")

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 📥 Step 1: Provide Transaction Dossier")
            file_input = gr.File(label="Upload Dossier PDF or TXT", file_types=[".pdf", ".txt"])
            gr.Markdown("**OR**")
            text_input = gr.Textbox(label="Paste Raw Transaction / System Context Payload", lines=8, placeholder="Enter transaction log history here...")
            submit_btn = gr.Button("🚀 Run Forensic Intelligence Audit", variant="primary")

        with gr.Column():
            gr.Markdown("### ⚖️ Step 2: Investigation Results")
            status_out = gr.Textbox(label="Fraud Assessment Status")
            reason_out = gr.Textbox(label="Forensic Reasoning (Auto-Generated SAR Narrative)", lines=5)
            violation_out = gr.Textbox(label="Detected Risk Indicators / Anomalies", lines=3)

    with gr.Accordion("View Matched Reference Fraud Typologies", open=False):
        evidence_out = gr.Markdown()

    submit_btn.click(
        fn=process_fraud_investigation,
        inputs=[file_input, text_input],
        outputs=[status_out, reason_out, violation_out, evidence_out]
    )

if __name__ == "__main__":
    demo.launch(share=True, debug=True)