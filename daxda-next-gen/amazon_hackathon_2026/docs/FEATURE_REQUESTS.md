# FEATURE REQUESTS REPORT
## Amazon Developer Ecosystem: Prioritized Feature Requests

This document outlines prioritized feature requests for the Amazon Developer teams building **Fire TV**, **Alexa+**, **Ring**, **Bee**, and **AWS Bedrock**.

---

### 1. Critical (Urgent / High-Impact Blockers)

1. **Native Streamable HTTP MCP Client Inside Alexa+ Core**
   * **Why it matters:** Currently, many developers simulate or wrap MCP inside standard Lambda skills. Having Alexa+ natively maintain persistent Streamable HTTP (SSE) connections directly to developer-hosted MCP servers over mutual TLS would eliminate latency bottlenecks and allow instant local smart home execution.
   * **Target Team:** Alexa+ Developer Team.
2. **Unified Cross-Device Event Bus (The "Ambient Event Mesh")**
   * **Why it matters:** Right now, bridging an event from Ring (e.g. motion) to Fire TV (video PIP) and Bee (haptic cue) requires custom backend glue code. An Amazon-managed ambient event bus where developers can subscribe to cross-device events with zero boilerplate would unleash a wave of multi-device applications.
   * **Target Team:** Amazon Ambient Computing / Device OS.

---

### 2. Important (Developer Ergonomics & Ecosystem Growth)

1. **Official Fire TV / Vega OS Web App Starter Kit & D-Pad Polyfill**
   * **Why it matters:** Web technologies are the fastest way to build for Fire TV, but new developers frequently struggle with D-Pad keycode differences, focus management, and overscan margins. A lightweight, official npm package (`@amazon/firetv-web-nav`) would cut onboarding time in half.
   * **Target Team:** Fire TV / Vega OS Team.
2. **Ring Local Area Network (LAN) WebSocket / WebRTC Streaming**
   * **Why it matters:** Streaming live video from Ring to Fire TV or local dashboards currently routes through cloud servers. A local peer-to-peer RTSP/WebRTC stream option for verified home devices would reduce camera pop-up latency from ~3 seconds to under 300ms.
   * **Target Team:** Ring Engineering.
3. **Bee Wearable Biometric Streaming via MCP Resource Subscription**
   * **Why it matters:** Exposing Bee's real-time heart rate and activity states as an MCP Resource (`mcp://bee/telemetry/stream`) that Alexa+ can continuously monitor would allow adaptive audio responses (e.g. speaking softer or lowering music volume when user is in high-stress focus).
   * **Target Team:** Bee Wearable AI Team.

---

### 3. Nice-to-Have (Polish & Quality-of-Life)

1. **Bedrock Strands SDK Zero-Config Local Test Server**
   * **Why it matters:** A local CLI command (`aws bedrock test-server`) that returns synthetic responses for standard model IDs without requiring IAM setup would make hackathon judging and offline development much easier.
   * **Target Team:** AWS Bedrock / AI Developer Tools.
2. **Fire TV Vega OS Simulator for macOS Apple Silicon**
   * **Why it matters:** Native ARM64 macOS simulator binaries for Vega OS would provide lightning-fast developer feedback loops without physical Fire TV stick hardware.
   * **Target Team:** Amazon Device Developer Relations.
