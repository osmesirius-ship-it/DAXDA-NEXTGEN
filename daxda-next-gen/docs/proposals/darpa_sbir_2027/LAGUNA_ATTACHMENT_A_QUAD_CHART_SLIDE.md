# DARPA BTO LAGUNA (`DARPA-SN-27-15`) — ATTACHMENT A: EXECUTIVE QUAD-CHART SLIDE
## Future Program: Laguna (Biological Technologies Office — Dr. William Mounfield, `Laguna@darpa.mil`)
### Prime Federal Awardee: American Milestone Inc (SAM.gov UEI: `MXEFU6TQJUB9` | CAGE: `214X7` | Nicholas Hartman)
### Core Technology Partner & TA2 Modeling Lead: DAXDA AI, LLC (Ohio Small Business | PI: Nicole Bess | Architecture: Dexter)

---

### **SLIDE TITLE:**
**`LAGUNA-D2F`: Co-Product Functionalized Direct-to-Formulation TA2 Predictive Engine, TEA/LCA Optimizer & Zero-PFAS Sovereign Supply Assurance**

---

### **QUADRANT 1: DEFENSE PROBLEM & SOTA LIMITATIONS**
* **Foreign Specialty-Chemical Dependency:** Critical DoD coatings, structural adhesives, high-$T_g$ polymers, and fluoropolymer barriers depend heavily on foreign-sourced multi-step intermediates.
* **The Purification Cost & Yield Wall:** Conventional synthesis discards co-products across 5+ distillation/chromatography steps (~30–45% cumulative yield), driving purified cost to **`$21.65/kg` (`$30.14/kg` for PFAS barriers)** and **`12.98 kg CO2e/kg`**.
* **Why Naive One-Pot Fails:** Eliminating separation in unguided one-pot broths causes Carothers/Stockmayer reactor gelation, acid leachate, and spinodal phase crash (`0.42%` simulated physical pass rate).

---

### **QUADRANT 2: THE REVOLUTIONARY `LAGUNA-D2F` TA2 APPROACH**
* **Co-Product Functionalization (*"Every Byproduct Has a Structural Job"*):** Inverse-steers U.S. C5/C6 sugars (`$0.38/kg`), shale ethylene (`$0.62/kg`), and BTX (`$0.88/kg`) so reactor co-products serve directly as reactive diluent ($w_3$, zero VOC), toughener ($w_4$), and non-fluorinated surface bloom ($w_5$).
* **Physics-Coupled $Cl(16,4)$ TA2 Digital Twin:** Embeds HSP spinodal distance $R_a$, Stockmayer gel ratio $p_{\text{reactor}}/p_c$, Fox-DiMarzio $T_g$, WLF viscosity $\eta$, and TEA/LCA in one invariant solver with `OI-005` (`graded-rho`) PAT lot-drift correction.
* **4-Gate `AOG-1` Fail-Closed Firewall (`e_17..e_20`):** Cryptographically enforces Zero-PFAS ($N_{\text{C-F}}=0$), $\ge 95\%$ domestic feedstock mass, exotherm/gelation safety, and spinodal phase stability (SHA-256 HMAC passports).

---

### **QUADRANT 3: VERIFIED *IN SILICO* BENCHMARKS (`300,000` TRAJECTORIES ON DISK)**
*Benchmark Source:* [`laguna_d2f_100k_benchmark.json`](file:///Users/user/daxda%20next%20gen/DAXDA-NEXTGEN/daxda-next-gen/outputs/laguna_d2f_100k_benchmark.json) (*in silico* TA2 simulation; 5/5 unit tests passing; `420,995 sims/sec`).
* **3-Regime TEA/LCA Comparison (`100,000` trials/regime):**
  * **`DAXDA_LAGUNA_D2F`:** **`$3.52/kg`** (`83.72%` cost cut vs `$21.65/kg` import), **`3.23 kg CO2e/kg`** (`75.13%` $\text{CO}_2\text{e}$ cut vs `12.98`), **`96.12%`** pre-gate defense spec pass (**`100%`** PFAS-free & domestic post-`AOG-1`).
  * **`Unguided_Crude_OnePot`:** `0.41%` defense spec pass (`+95.70 pp` improvement via `LAGUNA-D2F`).
* **All 4 Official Laguna Target Classes Qualified (`25,000` trials/class, post-`AOG-1`):**
  * **`LAG-COAT-01` (Armor Coating):** `94.36%` auth pass | `$3.35/kg` | `518.5 cP` | $T_g=129.2^\circ\text{C}$ | `29.4 MPa`.
  * **`LAG-ADHV-02` (Struct. Adhesive):** `98.59%` auth pass | `$3.55/kg` | `1,845 cP` | $T_g=165.4^\circ\text{C}$ | `32.5 MPa`.
  * **`LAG-POLY-03` (High-$T_g$ Polymer):** `98.94%` auth pass | `$3.86/kg` | `2,521 cP` | $T_g=199.7^\circ\text{C}$ | `3.70 GPa`.
  * **`LAG-PFAS0-04` (PFAS-Free Barrier):** `98.40%` auth pass | `$3.34/kg` | **`120.7°` $\theta_W$** | **`17.97 mN/m`** (`0` C–F bonds).

---

### **QUADRANT 4: SCHEDULE, TEAMING & COST POSTURE (36 MONTHS)**
* **Period of Performance:** **36 Months** (Phase I: 18 Months | Phase II: 18 Months), aligned to DARPA BTO Laguna structure.
* **Funding Options:**
  * **Option A (Solo TA2 Predictive Modeling Lead — FFP/OTA):** **`$2,850,000 USD`** (Ph I: `$1.20M` | Ph II: `$1.65M`).
  * **Option B (Integrated TA1+TA2 Consortium Ceiling):** **`$8,500,000 USD`** (Ph I: `$3.60M` | Ph II: `$4.90M`).
* **Key Program Milestones:**
  * **M3:** Open TA2 API for HSP/Stockmayer/TEA/LCA inverse broth optimization across U.S. sugar/ethylene/BTX feeds.
  * **M6 / M12:** $<5\%$ viscosity & gel-time error on TA1 lab broths; $\gamma_{sv} \le 21\text{ mN/m}$ PFAS-free omniphobic validation across $\ge 3$ feedstock lots.
  * **M18 (Go/No-Go) & M24:** All 4 Laguna classes verified at kg-scale (`<$6/kg`, `>50%` LCA cut); autonomous PAT seasonal lot-shift adaptation.
  * **M36:** Delivery of 10 kg+ DoD evaluation coupons & certified TRL 5/6 `LAGUNA-D2F` pilot digital twin.
* **Teaming & Portal Readiness:** American Milestone Inc (`CAGE: 214X7` | `UEI: MXEFU6TQJUB9`) + DAXDA AI, LLC; open to TA2 pairing with FFRDCs, National Labs & TA1 synthesis performers upon formal BAA release.
