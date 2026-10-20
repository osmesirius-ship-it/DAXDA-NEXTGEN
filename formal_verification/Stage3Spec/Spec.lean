/-
  DAXDA v14 — Stage 3 SPECIFICATION (NOT PROOF VERIFIED)
  =======================================================
  Oracle-complexity specification for the Baker–Gill–Solovay (1975) results.

  STATUS: every declaration in section SPEC_BRANCH_UNPROVED uses `sorry`.
  No declaration depending on `sorryAx` may be reported as verified.
  Declarations in section PROVED_FROM_SPEC are real proofs, but only
  conditional on the unproved SPEC_BRANCH lemmas (they will still show sorryAx).

  Inherited from Complexitylib (Apache-2.0, commit add0aca8):
    OracleTM, OracleCfg, OracleLocalTransition, BooleanOracle, Tape.oracleQuery,
    DTIME/NTIME/DSPACE/PSPACE, P, NP, FP, MapReducesPoly (≤ₚ), Language.
  NEW in this file: OracleNTM (+step/trace/acceptance), PRel, NPRel,
    Language.toOracle, unaryWitnessLang, and all theorem statements below.
-/
import Complexitylib.Stage3.Defs
import Complexitylib.Classes.NP.Reduction

open Complexity
open scoped Complexity

namespace Stage3Spec

/-! ## 3. SPEC_BRANCH_UNPROVED — statements only (`sorry`). NOT VERIFIED. -/

section SPEC_BRANCH_UNPROVED

/-- Model-compatibility (Q1): relativizing to the empty oracle recovers P. -/
theorem spec_PRel_empty : PRel ∅ = P := sorry

/-- Model-compatibility (Q1): relativizing to the empty oracle recovers NP. -/
theorem spec_NPRel_empty : NPRel ∅ = NP := sorry

/-- Deterministic oracle machines embed into nondeterministic ones. -/
theorem spec_PRel_subset_NPRel (A : Language) : PRel A ⊆ NPRel A := sorry

/-- Closure of `P^A` under polynomial-time many-one reductions to languages
decidable in `P^A` (needs query-then-answer composition). -/
theorem spec_PRel_closed_reduction (A L : Language) (h : L ≤ₚ A) : L ∈ PRel A := sorry

/-- Existence of a PSPACE-complete language under ≤ₚ. NOT available in
Complexitylib (only QBF syntax). Required new development. -/
theorem spec_exists_PSPACE_complete :
    ∃ A : Language, A ∈ PSPACE ∧ ∀ L ∈ PSPACE, L ≤ₚ A := sorry

/-- Key simulation: nondeterministic poly-time oracle machines with a PSPACE
oracle are simulable in deterministic polynomial space (space reuse across
queries and across the DFS over choice sequences). -/
theorem spec_NPRel_subset_PSPACE (A : Language) (hA : A ∈ PSPACE) :
    NPRel A ⊆ PSPACE := sorry

/-- Diagonalization (Baker–Gill–Solovay): some oracle B defeats every
polynomial-time deterministic oracle machine on `L_B`. -/
theorem spec_exists_oracle_not_in_PRel :
    ∃ B : Language, unaryWitnessLang B ∉ PRel B := sorry

/-- `L_B ∈ NP^B` for every B: guess `y` with `|y| = n`, one query. -/
theorem spec_unaryWitnessLang_mem_NPRel (B : Language) :
    unaryWitnessLang B ∈ NPRel B := sorry

end SPEC_BRANCH_UNPROVED

/-! ## 4. PROVED_FROM_SPEC — real proofs, conditional on section 3 -/

/-- BGS equality half. Assembly only; depends on the unproved lemmas above. -/
theorem bgs_equality : ∃ A : Language, PRel A = NPRel A := by
  obtain ⟨A, hAps, hAhard⟩ := spec_exists_PSPACE_complete
  refine ⟨A, Set.Subset.antisymm (spec_PRel_subset_NPRel A) ?_⟩
  intro L hL
  exact spec_PRel_closed_reduction A L (hAhard L (spec_NPRel_subset_PSPACE A hAps hL))

/-- BGS separation half. Assembly only; depends on the unproved lemmas above. -/
theorem bgs_separation : ∃ B : Language, PRel B ≠ NPRel B := by
  obtain ⟨B, hB⟩ := spec_exists_oracle_not_in_PRel
  refine ⟨B, fun h => hB ?_⟩
  rw [h]
  exact spec_unaryWitnessLang_mem_NPRel B

end Stage3Spec

open Stage3Spec in
#print axioms bgs_equality
open Stage3Spec in
#print axioms bgs_separation
