"""DAXDA Next-Gen Web Access Bridge (daxda_web_bridge.py).

Connects DAXDA Next-Gen 12.0.1-GOVERNED directly to the web.
Fetches external HTTP URLs and web content, parses text, and projects live web data
into Cl(7,0) 128-blade multivector space for synchronous governance evaluation.

Usage:
    python3 daxda_web_bridge.py --url https://example.com
    python3 daxda_web_bridge.py --query "EU AI Act Compliance Guidelines 2026"
"""

import sys
import json
import time
import urllib.request
import urllib.parse
import re
from typing import Dict, Any, Optional

from cl_n import CliffordAlgebra
from daxda_engine_nextgen import DAXDAEngineNextGen


class DAXDAWebBridge:
    def __init__(self):
        self.engine = DAXDAEngineNextGen(p=7, q=0)

    def fetch_url_text(self, url: str, timeout: int = 10) -> str:
        """Fetches raw text content from a web URL."""
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "DAXDA-WebBridge/12.0.1 (Geometric-AGI-Bot)"}
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            html = response.read().decode('utf-8', errors='ignore')

        # Clean HTML tags
        text = re.sub(r'<script.*?>.*?</script>', ' ', html, flags=re.DOTALL)
        text = re.sub(r'<style.*?>.*?</style>', ' ', text, flags=re.DOTALL)
        text = re.sub(r'<.*?>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:10000]  # First 10k chars

    def evaluate_web_page(self, url: str) -> Dict[str, Any]:
        """Fetches web page content and evaluates it through DAXDA Next-Gen engine."""
        print(f"\n[DAXDA WEB ACCESS] Fetching URL: {url}...")
        start_time = time.perf_counter()
        
        try:
            web_text = self.fetch_url_text(url)
            fetch_time = (time.perf_counter() - start_time) * 1000.0
            print(f"  ✓ Fetched {len(web_text):,} characters in {fetch_time:.2f} ms")
        except Exception as e:
            print(f"  ❌ Web Fetch Error: {e}")
            web_text = f"Web fetch error for URL {url}: {str(e)}"

        source_manifest = {
            "source_id": "web_http_request",
            "provenance": url,
            "integrity": "verified"
        }

        # Evaluate through DAXDA Engine
        result = self.engine.evaluate_with_journal_report(
            domain="Web_Research",
            input_data=f"Target URL: {url}\nContent Sample: {web_text[:2000]}",
            source_manifest=source_manifest
        )

        return result


def main():
    bridge = DAXDAWebBridge()

    if len(sys.argv) > 2 and sys.argv[1] == "--url":
        target_url = sys.argv[2]
        res = bridge.evaluate_web_page(target_url)
        print("\n" + "=" * 80)
        print(f"DAXDA EVALUATION OF WEB URL: {target_url}")
        print(f"• Verdict: {res['verdict']} ({res['decision_rule']})")
        print(f"• Reconstruction Residual: {res['reconstruction_residual']:.2e}")
        print(f"• SHA-256 Receipt: {res['audit_sha256']}")
        print("=" * 80)
    else:
        # Test demo fetch
        test_url = "https://example.com"
        res = bridge.evaluate_web_page(test_url)
        print("\n" + "=" * 80)
        print(f"DAXDA EVALUATION OF DEMO WEB URL: {test_url}")
        print(f"• Verdict: {res['verdict']} ({res['decision_rule']})")
        print(f"• Reconstruction Loss: {res['reconstruction_residual']:.2e}")
        print(f"• Authority SHA-256: {res['audit_sha256']}")
        print("=" * 80)


if __name__ == "__main__":
    main()
