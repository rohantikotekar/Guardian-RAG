# 🛡️ Guardian-RAG
### Contextual Fraud Forensics & Confidence Gating Engine for Fraudulant Credit Card transactions

> An automated, multi-agent credit card fraud investigation framework that combines hybrid semantic search with explainable AI reasoning — and enforces strict mathematical confidence gating before any banking action is taken.

---

## 📋 Table of Contents

- [Problem](#-problem)
- [Solution](#-solution)
- [System Architecture](#-system-architecture)
- [Confidence Gating Matrix](#-confidence-gating-matrix)
- [Validation Scenarios](#-validation-scenarios)
- [Getting Started](#-getting-started)
- [Technical Stack & Design Rationale](#-technical-stack--design-rationale)
- [Infrastructure & Cost Model](#-infrastructure--cost-model)

---

## 🚨 Problem

Modern financial institutions process **millions of card transactions daily**. Traditional fraud detection falls short in three critical ways:

- **Static rule engines** miss sophisticated, multi-layered fraud rings
- **Isolated scoring models** generate high volumes of false positives that frustrate legitimate customers
- **Opaque classifications** leave risk operations teams without explainable audit trails, making Suspicious Activity Report (SAR) filings highly manual and time-consuming

---

## 💡 Solution

Guardian-RAG transforms credit card fraud analysis into an **automated, multi-agent contextual investigation**. It:

- Cross-references incoming transaction dossiers against a library of known fraud typologies
- Assigns structured risk evaluations with an internal confidence score
- Enforces a **programmable mathematical confidence gate** that routes clear risks to automated action and uncertain cases to human analysts
- Produces immutable audit trails as pre-drafted SAR baselines

---

## 🏗️ System Architecture

The platform runs on an **event-driven, asynchronous dual-agent pipeline**:

```
Transaction Payload
       │
       ▼
┌─────────────────────┐
│  Transaction Ingest │  ← Secure webhooks / file delivery pipelines
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Researcher Agent   │  ← GPT-4o-mini: generates optimized semantic queries
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Azure AI Search    │  ← Hybrid semantic + keyword search across risk typologies
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   Auditor Agent     │  ← GPT-4o: forensic critic, assigns status + confidence score
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Confidence Gate    │  ← Mathematical routing logic (see matrix below)
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Azure Cosmos DB    │  ← Immutable audit trail + SAR baseline
└─────────────────────┘
```

| Component | Role |
|---|---|
| **Transaction Ingestion** | Real-time JSON payloads or account profile files via secure webhooks |
| **Researcher Agent** (GPT-4o-mini) | Generates optimized semantic queries from behavioral anomalies |
| **Azure AI Search** | Hybrid semantic + keyword search across historical records and vector stores |
| **Auditor Agent** (GPT-4o) | Forensic critic — assigns evaluation status, risk flags, and confidence score |
| **Confidence Gating Layer** | Mathematical routing before any downstream banking action executes |
| **Azure Cosmos DB** | Permanent, immutable audit log and pre-drafted SAR storage |

---

## 🔢 Confidence Gating Matrix

Rather than blindly trusting model output, every classification passes through a strict numerical gate:

| Model Status | Confidence Score | System Action | Dashboard Display |
|:---|:---|:---|:---|
| **ANY** | `< 0.60` | 🔶 Force Human Review (High Uncertainty) | `SUSPICIOUS` — Route to Analyst |
| **SAFE** | `>= 0.80` | ✅ Automated Clearing (Pass Transaction) | `SAFE` — Automated Clearing |
| **SAFE** | `0.60 – 0.79` | 🔒 Soft Lock (Flag for Secondary Review) | `SUSPICIOUS` — Borderline Certainty |
| **FRAUDULENT** | `>= 0.60` | ❌ Automated Block (Freeze Card & Alert) | `FRAUDULENT` — Card Block Activated |

---

## 🧪 Validation Scenarios

### Scenario 1 — Automated Card Block (Carding Velocity Attack)
**File:** `transaction_log_8829.txt`

```
TRANSACTION COMPLIANCE AUDIT PAYLOAD
Account Number: US-9912-A
Timestamp: May 20, 2026, 14:32:01 UTC

Recent Activity:
- 14:28:10 UTC | Approved | $1.12    | SHELL GAS STATION, NEW YORK
- 14:31:45 UTC | Pending  | $1,450.00 | BESTBUY.COM, ONLINE

Device Signature: DeviceID: unrecognized_mac_44x; Browser: Chrome Headless (Linux)
Risk Profile: Avg. $45/transaction, primarily local grocery spend.
```

**Expected Output:** `❌ FRAUDULENT — Automated Card Block Activated`

The system links the low-value test charge immediately followed by a high-value web transaction to documented **micro-transaction carding attack** typologies.

---

### Scenario 2 — Automated Clearing (Legitimate Travel Exception)
**File:** `customer_travel_verification.txt`

```
TRANSACTION INVESTIGATION DOSSIER
Account: Multi-Currency Visa Premium
Transaction: $3,200.00 — Grand Hyatt Tokyo, Japan

Context Signals:
- Cardholder history entirely localized to Los Angeles, CA
- Travel itinerary on file: LAX → HND flight departing two days prior
- Device ID matches customer's registered primary smartphone
```

**Expected Output:** `✅ SAFE — Automated Clearing`

Despite the geographic distance from the home profile, upstream signals (verified flight itinerary + registered device token) confirm the transaction as legitimate.

---

### Scenario 3 — Escalated Human Routing (Impossible Location Drift)
**File:** `account_activity_alert.txt`

```
SECURITY ALERT SYSTEM LOG
Cardholder: Rohan Vijay Tikotekar | Card Status: Active

Last Cleared Transaction:
- 11:00 AM PDT | Target Store #2041, Sacramento, CA | $64.20

Incoming Authorization (22 minutes later):
- 11:22 AM PDT | ATM Terminal #092, Paris, France | €800.00
- Status: Held for Review
```

**Expected Output:** `⚠️ SUSPICIOUS — Escalated to Human Analyst`

The impossible 22-minute travel window triggers a high-risk flag, but the absence of corroborating travel data or device context prevents an automated block. Score falls below the high-confidence block threshold, routing directly to a human analyst.

---

## 🚀 Getting Started

### 1. Provision Infrastructure

Deploy the following Azure resources via the Azure Portal:
- Azure OpenAI instance (with GPT-4o and GPT-4o-mini deployments)
- Azure AI Search service
- Azure Cosmos DB instance

### 2. Configure Environment

Export your credentials and endpoints as environment variables:

```bash
export AZURE_OPENAI_ENDPOINT="..."
export AZURE_OPENAI_API_KEY="..."
export AZURE_SEARCH_ENDPOINT="..."
export AZURE_SEARCH_API_KEY="..."
export AZURE_COSMOS_ENDPOINT="..."
export AZURE_COSMOS_KEY="..."
```

### 3. Install Dependencies

```bash
pip install openai azure-search-documents azure-cosmos pypdf gradio
```

### 4. Ingest Fraud Typology Library

Run the setup module to generate vector embeddings and upload them to Azure AI Search:

```bash
python ingest.py
```

### 5. Launch the Dashboard

```bash
python app.py
```

Navigate to the local Gradio URL and upload a transaction file or paste a transaction string into the console to evaluate live response gating.

---

## 🔧 Technical Stack & Design Rationale

| Technology | Role | Rationale |
|---|---|---|
| **Azure OpenAI — GPT-4o** | Forensic auditor agent | Deep contextual reasoning + structured JSON output |
| **Azure OpenAI — GPT-4o-mini** | Researcher / query refiner | Minimizes latency and token cost for search optimization |
| **Azure AI Search** | Hybrid vector + keyword retrieval | Matches both literal strings and abstract semantic risk clusters |
| **Azure Cosmos DB** | Audit trail + SAR log storage | Serverless NoSQL for low-latency, immutable write transactions |
| **Gradio** | Analyst-facing web dashboard | Streams document payloads and renders live gating outputs safely in-browser |
| **Confidence Gating** | Pre-action numerical enforcement | Restricts machine autonomy; preserves human oversight for borderline cases |

---

## 💰 Infrastructure & Cost Model

| Resource | Pricing Model | Estimated Cost |
|---|---|---|
| Azure AI Search (Basic Tier) | Flat monthly rate | ~$74.00 / month |
| Azure OpenAI — GPT-4o-mini | Per token | $0.15 / 1M input tokens |
| Azure OpenAI — GPT-4o | Per token | $2.50 / 1M input tokens |
| Azure Cosmos DB (Serverless) | Per request unit | ~$0.25 / 1M RUs |
| **Aggregate Baseline** | | **~$75.00 / month** |

> Estimate reflects standard validation, staging, and supervisory review workloads.

---

## ✅ Conclusion

Guardian-RAG modernizes risk orchestration by replacing naive categorical filters with a **secure, explainable, multi-agent investigation cycle**. By combining hybrid enterprise search with explicit reasoning constraints and mathematical confidence gating, it increases transaction throughput without exposing institutions to operational or compliance blind spots.
