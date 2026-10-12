# FRICTION LOGS (+10% JUDGING BONUS)
## Amazon Developer Hackathon 2026: Concrete Friction Logs & Solutions

This document details explicit friction points encountered during development across **Alexa+ MCP**, **Fire TV / Vega OS**, **Ring API / Simulators**, **Bee Wearable AI**, and **AWS Bedrock**, with reproduction steps, severity, workarounds, and actionable suggestions for Amazon engineering teams.

---

### Friction Log #1: Alexa+ Streamable HTTP MCP Session Multiplexing & Reconnects
* **Target Technology:** Alexa+ Model Context Protocol (MCP) Server (Spec 2025-11-25)
* **Task Attempted:** Implementing long-lived Server-Sent Events (SSE) connections for ambient push notifications to Alexa+ with automatic reconnect handling.
* **Steps Taken:**
  1. Configured an SSE endpoint at `GET /sse`.
  2. Emitted the standard `endpoint` event containing `/mcp/message?session_id=<UUID>`.
  3. Attempted to send asynchronous notifications through the SSE stream after an initial `initialize` handshake.
* **Expected Behavior:** The client maintains a single streamable session and processes server-initiated tool events without renegotiating `initialize`.
* **Actual Behavior:** If network latency exceeds a standard heartbeat window, the client drops the stream and expects a brand-new session ID, causing loss of ongoing agent context.
* **Severity Rating:** **Medium (Severity 3)**
* **Workaround Used:** Built an in-memory `AlexaMCPSessionManager` in `alexa_mcp_server.py` with thread locking that caches session states and allows idempotent re-binding of existing session IDs upon reconnect.
* **Actionable Suggestion for Amazon Team:** Update the Alexa+ MCP client SDK to include a standardized `Last-Event-ID` reconnection header and implement automatic exponential backoff before session invalidation.

---

### Friction Log #2: Fire TV Web Engine 10-Foot Remote Focus Trapping on Modals
* **Target Technology:** Fire TV Web Engine / Vega OS Preview
* **Task Attempted:** Displaying a Picture-in-Picture (PIP) camera alert overlay over the running video view without losing remote D-Pad navigation focus.
* **Steps Taken:**
  1. Built a 10-foot TV UI with focusable cards using `tabindex="0"`.
  2. Dynamically rendered a `<div id="pip-modal">` alert when Ring triggered a doorbell press.
  3. Attempted to navigate the modal buttons using remote arrow keys.
* **Expected Behavior:** Remote arrow keys should navigate between the modal's "Dismiss" and "Unlock" buttons while trapping focus inside the modal.
* **Actual Behavior:** Focus leaked to background cards hidden behind the modal backdrop, causing accidental media control triggering.
* **Severity Rating:** **High (Severity 2)**
* **Workaround Used:** Implemented an explicit focus-trapping manager in `app.js` that disables background element tabindex while the modal is open and auto-focuses the primary action button.
* **Actionable Suggestion for Amazon Team:** Expose a native Fire OS Webview attribute (e.g. `tv-modal-trap="true"`) or provide an official Amazon 10-foot Navigation JavaScript library that automatically manages focus containment.

---

### Friction Log #3: Ring Webhook Local Simulation Sandbox
* **Target Technology:** Ring Developer APIs & Webhooks
* **Task Attempted:** Testing automated lock actuation upon doorbell dings in a local developer environment without requiring physical Ring hardware or public ngrok tunnels.
* **Steps Taken:**
  1. Explored available Ring developer documentation for local testing endpoints.
  2. Found that testing live event webhooks generally requires a registered cloud OAuth application and physical device credentials.
* **Expected Behavior:** A lightweight local CLI simulator or containerized mock server that generates synthetically valid Ring events on localhost.
* **Actual Behavior:** Developers must write custom mock event emitters from scratch to test event handling logic.
* **Severity Rating:** **Medium (Severity 3)**
* **Workaround Used:** Engineered a comprehensive `RingClient` simulator in `ring_integration/ring_client.py` that generates realistic event schemas (`ding`, `motion`, `lock_state_change`) with synthetic computer vision payloads.
* **Actionable Suggestion for Amazon Team:** Release an official `@amazon/ring-simulator` npm package / Python package that runs a local mock server emitting authentic Ring webhook payloads.

---

### Friction Log #4: Bee Wearable Ambient Audio Command Disambiguation
* **Target Technology:** Bee Wearable AI (CLI & Telemetry Stream)
* **Task Attempted:** Extracting smart-home commands from continuous stream-of-consciousness wearable voice memos.
* **Steps Taken:**
  1. Ingested audio transcripts recorded while user was moving around the house.
  2. Processed utterances like *"Remember to check front porch deliveries before leaving for the office"*.
* **Expected Behavior:** Built-in metadata tagging distinguishing ambient passive notes from actionable device intents.
* **Actual Behavior:** All transcriptions are received as raw unclassified text blobs, forcing the application to perform second-pass semantic intent extraction.
* **Severity Rating:** **Low (Severity 4)**
* **Workaround Used:** Added semantic keyword intent classification and biometric heart-rate thresholding in `bee_client.py` to classify urgency and map utterances to specific actuator intents.
* **Actionable Suggestion for Amazon Team:** Include an optional `intent_candidate` array in the Bee telemetry schema indicating whether the utterance was directed toward an assistant vs. a personal memo.

---

### Friction Log #5: AWS Bedrock SDK Offline / Local Sandbox Fallback
* **Target Technology:** AWS Bedrock Runtime (`boto3`)
* **Task Attempted:** Running automated unit tests on CI/CD and developer laptops without requiring active AWS account credentials or incurring API costs during test runs.
* **Steps Taken:**
  1. Ran `pytest tests/test_end_to_end.py`.
  2. Boto3 raised `NoCredentialsError` when `AWS_ACCESS_KEY_ID` was unset.
* **Expected Behavior:** Official SDK support for an offline sandbox or dry-run mock mode for testing client wrappers.
* **Actual Behavior:** Tests fail without explicit environment variables or manual mocking.
* **Severity Rating:** **Medium (Severity 3)**
* **Workaround Used:** Implemented an automatic credentials detector in `bedrock_agent.py` that seamlessly transitions to a verified local Strands SDK simulation if AWS credentials are not configured.
* **Actionable Suggestion for Amazon Team:** Provide an official `bedrock-mock` or `boto3-sandbox` fixture in AWS SDKs for developer testing and hackathon evaluations.
