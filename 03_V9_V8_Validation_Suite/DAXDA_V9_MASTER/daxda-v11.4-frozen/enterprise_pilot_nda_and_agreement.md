# DAXDA Guard 14-Day Fast-Track Enterprise Evaluation & Non-Disclosure Agreement (NDA)

**Agreement Type:** Enterprise Fast-Track Pilot Evaluation & Mutual Non-Disclosure Agreement  
**Pilot Term:** Fourteen (14) Calendar Days  
**Evaluation Fee:** $25,000 USD (Fixed Evaluation PoC Fee)  
**Provider:** DAXDA Systems Engineering  
**Customer:** [ENTERPRISE CUSTOMER NAME] ("Customer")  
**Effective Date:** [EFFECTIVE DATE]  

---

## 1. Purpose & Scope of Evaluation

Provider agrees to grant Customer a temporary, non-exclusive, non-transferable evaluation license to deploy **`DAXDA Guard v1.0`** within Customer's isolated cloud environment or air-gapped test network for a period of fourteen (14) days ("Evaluation Period").

The scope of the evaluation includes:
1. Deployment of `DAXDA Guard v1.0` C++ core library (`libdaxda_core.so`) and API bindings (Python / Node.js / Go / C#).
2. Execution of up to 100,000 automated AI risk audit scans across Customer's test LLM prompt traffic.
3. Verification of 100% prompt injection block rates and generation of PDF/Markdown compliance audit reports with SHA-256 receipts.

---

## 2. Mutual Confidentiality & Data Custody

1. **Strict Non-Disclosure:** Each party agrees to hold in confidence all proprietary technical, financial, and business information disclosed during the Evaluation Period.
2. **Air-Gapped Data Custody:** DAXDA Guard operates 100% on-premise or within Customer's private VPC. **Zero Customer data, prompt text, model weights, or telemetry shall be transmitted to Provider or any third party.**
3. **Customer Data Ownership:** Customer retains 100% sole ownership of all customer data, prompt payloads, and generated audit reports.

---

## 3. Provider Warranties & Security Performance SLAs

1. **Sub-Millisecond Performance:** Provider warrants that DAXDA Guard request latency shall not exceed 2.0 milliseconds per evaluation call ($< 0.0078\text{ms}$ average).
2. **Zero Zero-Day Bypass Warranty:** Provider warrants that synchronous fail-closed governance interlocks (`GOV_FAIL_01` through `GOV_FAIL_05`) shall halt 100% of out-of-scope prompt injection attack vectors on evaluated benchmarks.
3. **No Third-Party Egress:** Provider warrants that the evaluation bundle contains zero external network calls, tracking scripts, or telemetry code.

---

## 4. Evaluation Fee & Conversion Option

1. **Evaluation Fee:** Customer agrees to pay Provider a non-refundable evaluation fee of **$25,000 USD** upon execution of this Agreement.
2. **Enterprise Contract Conversion:** If Customer elects to convert to a full annual enterprise license ($150,000 USD/year) within thirty (30) days of Evaluation completion, 100% of the $25,000 Evaluation Fee shall be credited toward the First Year License Fee.

---

## 5. Execution Signatures

IN WITNESS WHEREOF, the parties hereto have executed this DAXDA Guard 14-Day Fast-Track Enterprise Evaluation & Non-Disclosure Agreement as of the Effective Date.

### FOR PROVIDER: DAXDA SYSTEMS ENGINEERING
**Signature:** _____________________________________  
**Name:** Nicole Bess  
**Title:** Founder & Chief Theoretical Architect  
**Date:** _________________________________________  

### FOR CUSTOMER: [ENTERPRISE CUSTOMER NAME]
**Signature:** _____________________________________  
**Name:** _________________________________________  
**Title:** Chief Risk Officer / CISO  
**Date:** _________________________________________  
