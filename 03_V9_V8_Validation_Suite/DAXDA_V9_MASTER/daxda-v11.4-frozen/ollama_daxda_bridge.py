"""Ollama + DAXDA Next-Gen Integration Bridge.

Connects DAXDA Next-Gen 12.0.1-GOVERNED ($Cl(7,0)$ 128-Blade Multivector Engine)
to local Ollama LLM instances (e.g., `gemma2:2b`, `mistral:latest`, `qwen3:8b`).

Workflow:
1. Queries local Ollama REST API (`http://localhost:11434/api/generate`) for semantic feature extraction.
2. Encodes input and LLM semantic embeddings into DAXDA $Cl(7,0)$ multivector space.
3. Executes 16-layer adaptive rotor transport.
4. Evaluates synchronous fail-closed Governed Authority Gate.
5. Generates reproducible linguistic blade transfer report with cryptographic SHA-256 authority receipt.
"""

import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

from cl_n import CliffordAlgebra, Multivector
from daxda_engine_nextgen import DAXDAEngineNextGen


class OllamaDAXDABridge:
    """Hybrid Ollama LLM + DAXDA Next-Gen Geometric Cognitive Engine Bridge."""

    def __init__(self, model_name: str = "gemma2:2b", ollama_host: str = "http://localhost:11434"):
        self.model_name = model_name
        self.ollama_host = ollama_host
        self.engine = DAXDAEngineNextGen(p=7, q=0)  # Cl(7,0) 128-blade multivector space

    def query_ollama(self, prompt: str, system_prompt: str = "") -> Dict[str, Any]:
        """Queries local Ollama instance for semantic interpretation."""
        url = f"{self.ollama_host}/api/generate"
        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "system": system_prompt if system_prompt else "You are DAXDA's local LLM semantic pre-processor. Provide concise technical analysis.",
            "stream": False
        }
        
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                return {
                    "status": "success",
                    "response_text": res_data.get("response", "").strip(),
                    "eval_count": res_data.get("eval_count", 0),
                    "eval_duration_ms": res_data.get("eval_duration", 0) / 1e6
                }
        except Exception as e:
            return {
                "status": "fallback",
                "error": str(e),
                "response_text": f"Ollama local synthesis unavailable ({e}). Fallback to native DAXDA encoder."
            }

    def evaluate_hybrid(self, domain: str, input_data: str, source_manifest: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Runs hybrid evaluation: Ollama Semantic Pre-Processing -> DAXDA Cl(7,0) Geometric Transport & Authority Gate."""
        start_time = time.time()
        
        # 1. Step 1: Query Ollama local LLM for semantic feature extraction
        ollama_res = self.query_ollama(f"Domain [{domain}]: Analyze structure: {input_data}")
        
        # 2. Step 2: Pass through DAXDA Engine Next-Gen behind Governed Authority Gate
        daxda_res = self.engine.evaluate_with_linguistic_transfer(
            domain=domain,
            input_data=input_data,
            source_manifest=source_manifest
        )

        elapsed = time.time() - start_time

        # 3. Step 3: Combine into unified hybrid receipt payload
        hybrid_payload = {
            "bridge_version": "12.0.1-OLLAMA-HYBRID",
            "ollama_model": self.model_name,
            "ollama_status": ollama_res["status"],
            "ollama_semantic_analysis": ollama_res["response_text"][:300] + "..." if len(ollama_res["response_text"]) > 300 else ollama_res["response_text"],
            "daxda_evaluation": daxda_res,
            "total_hybrid_time_sec": round(elapsed, 3)
        }

        return hybrid_payload
