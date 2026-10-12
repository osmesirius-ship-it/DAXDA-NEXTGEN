# DEMO VIDEO SCRIPT & TIMELINE (UNDER 3 MINUTES)
## Amazon Developer Hackathon 2026: DAXDA Sentry
**Target Duration:** 2 minutes, 45 seconds  
**Format:** Screen Recording + Voiceover + Webcam PIP  
**Platform:** YouTube (Public / Unlisted)  

---

### Timeline Breakdown

| Timestamp | Scene / Visual | Voiceover Audio (Spoken Word) |
| :--- | :--- | :--- |
| **0:00 – 0:25**<br>*(25 sec)* | **Title Slide & Architecture**<br>Display DAXDA Sentry logo, multi-device diagram showing Alexa+, Ring, Fire TV, Bee Wearable, and AWS Bedrock. | *"Welcome to DAXDA Sentry—the first project to unify Fire TV, Alexa+, Ring, and Bee Wearable AI into a single ambient intelligence mesh protected by mathematical fail-closed governance. Today, our smart home devices live in isolated silos: Ring detects visitors, but Fire TV plays loud movies; Bee records voice memos, but Alexa+ is unaware. DAXDA Sentry connects the front door, the living room, the wearable, and the cloud."* |
| **0:25 – 0:55**<br>*(30 sec)* | **Primary Track: Alexa+ Streamable MCP Server**<br>Show terminal running `alexa_mcp_server.py`. Switch to JSON-RPC inspector showing Spec 2025-11-25 SSE connection. | *"For our primary track, we built a self-hosted Streamable HTTP Model Context Protocol (MCP) server adhering strictly to the 2025-11-25 specification. Alexa+ dynamically discovers 5 specialized tools—querying Ring cameras, casting alerts to Fire TV, ingesting Bee wearable context, and running DAXDA's 16-layer policy verification."* |
| **0:55 – 1:30**<br>*(35 sec)* | **Ring & Fire TV Living Room Experience**<br>Show Fire TV 10-foot UI running on screen. Trigger a simulated Ring doorbell ding. An animated Picture-in-Picture camera alert pops up over the TV. | *"Watch what happens when Ring detects a delivery at the front porch. Alexa+ receives the event via MCP and automatically casts a live Picture-in-Picture overlay to our Fire TV living room app. Using standard Fire TV remote D-Pad controls, you can inspect the camera, check package detection status, and dismiss or unlock the door."* |
| **1:30 – 2:00**<br>*(30 sec)* | **Bee Wearable AI & AWS Bedrock**<br>Show Bee Wearable telemetry terminal. Show voice memo: 'Heading to office, check front door'. Show heart rate graph. Trigger AWS Bedrock synthesis. | *"Next, we connect Bee Wearable AI. As the user walks through the house, Bee streams voice memos and biometric heart rate telemetry. If Bee detects an elevated heart rate or a spoken note about an unfamiliar vehicle, AWS Bedrock instantly synthesizes the cross-device state using Claude 3.5 Sonnet, prioritizing camera alerts on Fire TV."* |
| **2:00 – 2:30**<br>*(30 sec)* | **DAXDA Fail-Closed Mathematical Governance**<br>Simulate an unauthorized smart lock override and an adversarial prompt injection in the web console. | *"Crucially, high-consequence physical actions—like unlocking doors—cannot rely on probabilistic AI prompts alone. In DAXDA Sentry, every actuator command must clear our 16-layer Nicole Protocol Policy Enforcement Point. When an adversarial prompt injection attacks the pipeline, the malicious energy is mapped to a Null-Vector Horizon ($v^2 = 0$) and dissipates safely with a tamper-evident SHA-256 audit receipt."* |
| **2:30 – 2:45**<br>*(15 sec)* | **Conclusion & GitHub Repo**<br>Show all 16 automated tests passing in terminal (100% green). Show GitHub repository with Apache 2.0 license. | *"DAXDA Sentry is 100% open source under the Apache 2.0 license, features 16 automated tests passing in under 0.1 seconds, and includes complete friction logs and product feedback for the Amazon teams. Thank you for building an open ecosystem for Fire TV, Alexa+, Ring, and Bee!"* |

---

### Production Recording Checklist

1. **Terminal 1:** Run `python3 mcp_server/alexa_mcp_server.py 8090`
2. **Terminal 2:** Run `python3 web_simulator/server.py 8080`
3. **Browser Tab 1:** Open `http://127.0.0.1:8080/` (Unified Simulator Console)
4. **Browser Tab 2:** Open `http://127.0.0.1:8080/firetv` (10-Foot Living Room TV UI)
5. **Terminal 3:** Run `./daxda-next-gen/.venv/bin/pytest tests/test_end_to_end.py -v` (Demonstrates 16/16 tests passing)
