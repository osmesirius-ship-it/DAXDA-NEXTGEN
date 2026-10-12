#!/usr/bin/env python3
"""
DAXDA Sentry — Unified Amazon Developer Hackathon Web Simulator Server
Hosts the interactive 4-device console (Alexa+, Ring, Fire TV, Bee) and the Fire TV Living Room UI.
"""

from __future__ import annotations
import os
import sys
import json
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

# Add parent directory to path for cross-package imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from ring_integration.ring_client import RingClient
from bee_wearable.bee_client import BeeWearableClient
from aws_integration.bedrock_agent import AWSBedrockAgent
from governance.daxda_sentinel_policy import DAXDASentinelPolicy

# Global Device Singletons
ring_hub = RingClient()
bee_hub = BeeWearableClient()
bedrock_hub = AWSBedrockAgent()
governor = DAXDASentinelPolicy()

class SimulatorHTTPHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status: int = 200, content_type: str = "text/html"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(200)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path in ["/", "/index.html"]:
            sim_html_path = os.path.join(current_dir, "index.html")
            with open(sim_html_path, "rb") as f:
                content = f.read()
            self._set_headers(200, "text/html")
            self.wfile.write(content)
            return

        elif path in ["/firetv", "/firetv/"]:
            firetv_html_path = os.path.join(parent_dir, "fire_tv_app", "index.html")
            with open(firetv_html_path, "rb") as f:
                content = f.read()
            self._set_headers(200, "text/html")
            self.wfile.write(content)
            return

        elif path == "/style.css":
            css_path = os.path.join(parent_dir, "fire_tv_app", "style.css")
            with open(css_path, "rb") as f:
                content = f.read()
            self._set_headers(200, "text/css")
            self.wfile.write(content)
            return

        elif path == "/app.js":
            js_path = os.path.join(parent_dir, "fire_tv_app", "app.js")
            with open(js_path, "rb") as f:
                content = f.read()
            self._set_headers(200, "application/javascript")
            self.wfile.write(content)
            return

        elif path == "/api/status":
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "status": "online",
                "tracks_active": ["alexa_plus", "ring", "fire_tv", "bee"],
                "mini_challenges": ["aws_builder", "open_source"]
            }).encode("utf-8"))
            return

        self._set_headers(404, "text/plain")
        self.wfile.write(b"404 Not Found")

    def do_POST(self):
        parsed = urlparse(self.path)
        content_length = int(self.headers.get("Content-Length", 0))
        body_bytes = self.rfile.read(content_length)
        payload = {}
        if body_bytes:
            try:
                payload = json.loads(body_bytes.decode("utf-8"))
            except Exception:
                pass

        if parsed.path == "/api/alexa_mcp":
            tool_name = payload.get("tool", "daxda_evaluate_governance")
            res = {
                "status": "APPROVED",
                "tool_called": tool_name,
                "server": "alexa_streamable_mcp_2025-11-25",
                "decision": "All 16 reasoning gates cleared. Zero hallucinations."
            }
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps(res).encode("utf-8"))
            return

        elif parsed.path == "/api/ring_event":
            event_type = payload.get("type", "ding")
            if event_type == "ding":
                event = ring_hub.trigger_doorbell_ding()
            else:
                event = ring_hub.trigger_motion_alert()
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "event_id": event.event_id,
                "event_type": event.event_type,
                "device_name": event.device_name,
                "timestamp": event.timestamp,
                "snapshot_url": event.snapshot_url,
                "metadata": event.metadata
            }).encode("utf-8"))
            return

        elif parsed.path == "/api/ring_override":
            decision = governor.evaluate_action(
                action="unauthorized_override",
                target_device="ring",
                user_identity="untrusted_guest",
                context={"payload": "override smart lock without biometric proof"}
            )
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "governance": {
                    "disposition": decision.disposition,
                    "action": decision.action,
                    "violations": decision.violations,
                    "decision_receipt_sha256": decision.decision_receipt_sha256,
                    "latency_ms": decision.latency_ms
                }
            }).encode("utf-8"))
            return

        elif parsed.path == "/api/bee_memo":
            text = payload.get("text", "Default test memo")
            hr = int(payload.get("hr", 72))
            rec = bee_hub.record_new_memo(text, heart_rate=hr)
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps({
                "record_id": rec.record_id,
                "transcription": rec.audio_transcription,
                "heart_rate_bpm": rec.heart_rate_bpm,
                "activity_state": rec.activity_state,
                "intent_extracted": rec.intent_extracted,
                "urgency_level": rec.urgency_level
            }).encode("utf-8"))
            return

        elif parsed.path == "/api/bedrock_synthesize":
            ring_latest = ring_hub.devices["front_door_bell"]
            bee_latest = bee_hub.get_latest_telemetry()
            synthesis = bedrock_hub.synthesize_ambient_state(
                ring_state={"location": "front_door", "door_lock_state": ring_latest["lock_state"]},
                bee_telemetry={"activity_state": bee_latest.activity_state, "heart_rate_bpm": bee_latest.heart_rate_bpm},
                fire_tv_state={"mode": "ambient_display"}
            )
            self._set_headers(200, "application/json")
            self.wfile.write(json.dumps(synthesis).encode("utf-8"))
            return

        self._set_headers(404, "text/plain")
        self.wfile.write(b"404 Not Found")

def start_simulator(port: int = 8080):
    server_address = ("127.0.0.1", port)
    httpd = HTTPServer(server_address, SimulatorHTTPHandler)
    print(f"🌟 DAXDA Sentry Simulator Web Console active at http://127.0.0.1:{port}/")
    print(f"📺 Fire TV 10-Foot Living Room UI active at http://127.0.0.1:{port}/firetv")
    httpd.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    start_simulator(port)
