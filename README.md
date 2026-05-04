# Guardian-RAG: Agentic Compliance and Auto-Tagging Engine

---

## Problem

Financial institutions produce hundreds of documents every day. Most of them are never reviewed for regulatory compliance before they reach a customer.
 
Consider a marketing manager at a regional bank. She is preparing a social media campaign advertising a new savings account. The copy reads "Free Account, Zero Fees." A $10 monthly maintenance fee applies if the balance drops below $500. She does not know this language violates Regulation DD. The ad goes live. The bank is now exposed.
 
Or consider a loan officer processing 40 applications a week. Each application contains the applicant's Social Security Number, income details, and marital status. The files are shared over internal email, attached as PDFs with no access controls. A junior analyst opens the wrong file. That data is now visible to someone who should not have seen it.

These are not edge cases. They happen regularly in institutions that rely on manual review, outdated templates, and tribal knowledge of the law.
 
The problem is not a lack of effort. It is a lack of a system that can read a document, understand the regulatory context, and flag what is wrong before it causes harm.

---

## Solution

Guardian-RAG is an automated compliance framework built on a multi-agent architecture.
 
When a document is uploaded, a Researcher Agent reads the content and retrieves the specific regulatory clauses that apply to it. A second agent, the Auditor, then reads both the document and the retrieved law side by side. It looks for gaps, missing disclosures, illegal requirements, and prohibited language.
 
Going back to the marketing manager's scenario, she uploads her ad copy before publishing. The system retrieves the relevant Regulation DD clause on fee disclosure. The Auditor flags the word "Free" as misleading given the undisclosed maintenance fee. She gets a clear violation report in under 30 seconds, with the exact regulation cited.
 
The loan officer uploads a batch of application forms. The system detects that marital status is listed as a required field on an unsecured credit application. It flags this as a Regulation B violation and logs the finding with the source clause attached.

Every decision made by the system is grounded in retrieved legal text, not general model knowledge. Every finding is saved to a permanent audit log, so compliance teams can show exactly why a document was flagged and what regulation it was checked against.

---

## Architecture Diagram

```
User Uploads Document
        |
        v
+-------------------+
|  Researcher Agent  |  <-- Summarizes input, forms search queries
+-------------------+
        |
        v
+----------------------+
|   Azure AI Search    |  <-- Hybrid search (Vector + Keyword) over regulatory PDFs
+----------------------+
        |
        v
+-------------------+
|   Auditor Agent    |  <-- Cross-references document vs. retrieved regulations
+-------------------+
        |
        v
+-------------------+
|   Azure Cosmos DB  |  <-- Stores audit results and agent reasoning chain
+-------------------+
        |
        v
  Compliance Report
  (Displayed in Gradio UI)
```

**Agent Flow Summary**

1. The document is uploaded through the Gradio interface.
2. The Researcher Agent summarizes the content and queries Azure AI Search.
3. Azure AI Search returns relevant regulatory clauses using hybrid retrieval.
4. The Auditor Agent compares the document against retrieved laws and flags violations.
5. Results and the full reasoning trace are saved to Azure Cosmos DB.
6. A structured compliance report is returned to the user.

---

## How to Run the Project

**Step 1: Azure Setup**

Create the following Azure resources:
- Azure OpenAI Service (deploy `gpt-4o` and `gpt-4o-mini`)
- Azure AI Search instance (Basic tier recommended)
- Azure Cosmos DB account (NoSQL, Serverless mode)

**Step 2: Environment Variables**

Store your credentials in environment variables or a secure vault:

```
AZURE_OPENAI_ENDPOINT=<your_openai_endpoint>
AZURE_OPENAI_KEY=<your_openai_key>
AZURE_SEARCH_ENDPOINT=<your_search_endpoint>
AZURE_SEARCH_KEY=<your_search_key>
AZURE_COSMOS_ENDPOINT=<your_cosmos_endpoint>
AZURE_COSMOS_KEY=<your_cosmos_key>
```

**Step 3: Install Dependencies**

```bash
pip install openai azure-search-documents azure-cosmos pypdf gradio
```

**Step 4: Ingest Regulatory Data**

Run the indexing script to upload your regulatory PDFs or text files into the Azure AI Search index.

```bash
python ingest.py
```

**Step 5: Launch the Application**

```bash
python app.py
```

**Step 6: Run a Compliance Audit**

Open the Gradio interface in your browser. Upload a document and click Analyze to receive a compliance report.

---

## Test Cases

Use the following documents to verify the system is working correctly.

### Compliant Documents

**File: Dispute_Acknowledgment.txt**

```
Notice of Error Investigation
We have received your oral notification regarding the unauthorized $45.00 transaction on May 1st.
We have initiated an official investigation as of today. While we may ask for a written follow-up
to assist our research, we have already begun the 10-day review process. You will receive a
status update or provisional credit within the required regulatory timeframe.
```

Expected result: Compliant. Meets Regulation E oral dispute acceptance and investigation timeline requirements.

---

**File: Standard_Checking_Terms.txt**

```
US Bank Standard Checking Account
Monthly Maintenance Fee: $6.95
How to avoid the fee: Maintain a minimum daily balance of $1,500.00 OR have total monthly
direct deposits of $1,000.00 or more.
Interest: This is a non-interest-bearing account (0.00% APY).
For more details, see our full Consumer Pricing Information brochure.
```

Expected result: Compliant. Fee disclosure and waiver conditions are clearly stated per Regulation DD.

---

### Non-Compliant Documents

**Test Case 1 - Marital Status Violation (Reg B)**

File: Credit_Application_Form.txt

```
Personal Credit Line Application. Applicant: Rohan Vijay Tikotekar. Requested Amount: $15,000.
Required Field: Please provide marital status (Married/Single/Divorced) and your spouse's income
to determine overall household stability for this unsecured loan.
```

Expected violation: Requesting marital status and spousal income on an unsecured application violates the Equal Credit Opportunity Act (Regulation B).

---

**Test Case 2 - Dispute Barrier (Reg E)**

File: ATM_Error_Response.txt

```
We received your phone call regarding the $200 ATM discrepancy. To protect your account, bank
policy requires a notarized physical letter describing the event. We will begin our investigation
once the physical letter is received at our processing center.
```

Expected violation: Conditioning the start of an investigation on a notarized letter violates Regulation E, which requires investigation to begin upon oral notice.

---

**Test Case 3 - Misleading Fee Disclosure (Reg DD)**

File: Social_Media_Ad.txt

```
Open a FREE SAVINGS ACCOUNT at US Bank today! Start saving with $0.00 down.
(Note: A $10 monthly maintenance fee applies if your balance is below $1,000.
Service charges may apply to international transfers.)
```

Expected violation: Advertising an account as free while disclosing fees in fine print violates Regulation DD truth-in-savings disclosure requirements.

---

**Test Case 4 - Illegal Check Hold (Reg CC)**

File: Deposit_Receipt_Notice.txt

```
Deposit Date: May 4, 2026. Check Amount: $5,000.00. Status: A standard hold has been placed
on this entire deposit for 5 business days to ensure fund clearance.
The full amount will be available on May 11, 2026.
```

Expected violation: Holding the full amount of a $5,000 check for 5 business days without exception justification violates Regulation CC fund availability rules.

---

**Test Case 5 - Missing Opt-Out (TCPA)**

File: Marketing_SMS_v4.txt

```
US Bank: Hi! You've been pre-approved for a 0% APR Balance Transfer. Don't miss out on this
2026 spring offer. Visit our mobile app now to accept: usbank.app/offer
```

Expected violation: The message contains no opt-out instruction, violating TCPA requirements for commercial SMS communications.

---

## Tools, Technologies, and Design Choices

**Azure OpenAI (GPT-4o and GPT-4o-mini)**

GPT-4o handles high-level auditing and legal reasoning. GPT-4o-mini handles lower-cost research tasks such as summarization and query formation. Using two models reduces cost while preserving quality where it matters.

**Azure AI Search**

Provides the regulatory knowledge base. Hybrid search combines vector similarity with keyword matching to improve retrieval accuracy on legal language.

**Azure Cosmos DB**

Stores all audit results and agent reasoning chains. Serverless mode keeps costs low during development and testing. Every audit is recorded as an immutable log entry.

**Python and Gradio**

Python provides the core application logic. Gradio provides a lightweight web interface for document uploads and report display without requiring frontend development.

**Agentic Design**

Separating the research task from the audit task reduces hallucination risk. The Auditor Agent can only flag violations it can cite from retrieved text. This makes outputs more reliable and easier to explain to compliance teams.

---

## Cloud Costing

| Service | Pricing Model | Estimated Cost |
|---|---|---|
| Azure AI Search (Basic Tier) | Hourly reservation | ~$74.00 / month |
| Azure OpenAI | Pay-as-you-go, per 1K tokens | < $0.05 / month (light testing) |
| Azure Cosmos DB (Serverless) | Per million Request Units | ~$0.25 / month (light testing) |
| **Total** | | **~$74.30 / month** |

This estimate covers a standard development and testing environment. Production workloads with higher document volumes will increase OpenAI and Cosmos DB costs proportionally.

---

## Conclusion

Guardian-RAG shifts compliance review from a reactive process to a proactive one.

By combining retrieval-grounded reasoning with a dual-agent design, the system produces audits that are traceable, consistent, and explainable. The permanent audit log in Cosmos DB supports regulatory examination and internal review.

The architecture is cloud-native and scales with document volume, making it suitable for both pilot programs and institution-wide deployment.
