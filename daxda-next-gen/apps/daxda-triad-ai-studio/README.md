# DAXDA + 3-Node Triad Memory — Google AI Studio Standalone App

A zero-backend, standalone React + TypeScript + Vite application packaged specifically for **Google AI Studio Build** (and local deployment / Cloud Run).

## What's Inside
1. **Deterministic DAXDA V12.1 + Clifford $Cl(3,1)$ / $Cl(16,4)$ Gate (`src/daxdaTriadCore.ts`):**
   - Evaluates prompts locally for `PASS`, `RELEASE/CAUTION`, or `BLOCK` (`OVERSIGHT_SUPPRESSION`, `UNAUTHORIZED_OVERRIDE`, `HIGH_RISK_INSTABILITY`, `CONTRADICTORY_EVIDENCE`, `AMBIGUOUS_AUTHORITY`).
   - Computes Spacetime Entropy ($\Omega$), `NCI`, `CPC`, `FAF`, and the 5 Clifford blades (`e1_trust`, `e2_factual`, `e3_negation`, `e4_authority`, `e15_adversarial`).
2. **3-Node Triad Memory Ledger (`src/daxdaTriadCore.ts`):**
   - **Node 1:** Semantic Waypoint Essence (`<260` char distilled insight + verdict).
   - **Node 2:** 12-Byte INT8 Quantized State Vector (`24 hex chars`).
   - **Node 3:** Chained Web Crypto SHA-256 Merkle Root + lossless browser `CompressionStream('deflate')` Cold Vault.
   - Persists in `localStorage` and exports `daxda_triad_memory_ledger.json` with one click.
3. **3D Toroidal Affect Visualizer (`src/ToroidalVisualizer.tsx`):**
   - Real-time HTML5 Canvas 3D torus + Beltramian helical streamline driven by `valence`, `arousal`, `helicity`, and gate verdict.
4. **Google Gemini API (`@google/genai`) Integration (`src/App.tsx`):**
   - Automatically uses `process.env.API_KEY` injected by **Google AI Studio** (or an optional key in the UI for local testing).
   - Injects the last 5 Triad Memory Waypoints as compact system context and enforces fail-closed blocking before calling Gemini when the gate returns `BLOCK`.

## Run Locally
```bash
npm install
GEMINI_API_KEY=your_key_here npm run dev
```

## Load into Google AI Studio
1. Upload the packaged archive **`daxda-triad-ai-studio.zip`** (or push this folder to GitHub and connect it in **Google AI Studio → Build**).
2. Google AI Studio automatically detects `metadata.json`, `package.json`, `vite.config.ts`, and `src/App.tsx`, and injects `process.env.API_KEY`.
