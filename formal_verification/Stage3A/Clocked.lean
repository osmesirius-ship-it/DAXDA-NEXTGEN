/-
  Stage 3: Clocked Oracle Turing Machines and Enumeration Completeness
  =====================================================================
  Formalization of Orders 1–4 from the BGS Separation Architecture:
  1. `polyClock C d n := C * (n + 1)^d + C`
  2. `polyClock_dominates`: Every asymptotic polynomial bound f =O (· ^ d)
     is dominated everywhere by `polyClock C d` for some C ≥ 1.
  3. `ClockedOracleTM`: Normalized oracle TMs paired with clocks.
  4. `PRel_iff_exists_clocked` & `PRel_represented`: Completeness of ClockedOracleTM for PRel.
  5. `oracleQuerySet`: Query extraction from the actual execution trace.
  6. `oracleQuerySet_card_le`: Query set cardinality bounded by runtime.
  7. `exists_unqueried_string`: Combinatorial pigeonhole producing unqueried strings.
-/
import Complexitylib.Stage3.Defs
import Complexitylib.Stage3.Normalize
import Complexitylib.Stage3.Probes
import Complexitylib.Asymptotics
import Complexitylib.Models.TuringMachine.UTM.HierarchySupport
import Mathlib.Analysis.SpecificLimits.Normed

open Complexity
open scoped Complexity
open Stage3Spec

namespace Stage3Separation

/-! ## 1. Polynomial clock definition and domination -/

/-- Explicit polynomial clock bounding runtime everywhere: `C * (n + 1)^d + C`. -/
def polyClock (C d n : ℕ) : ℕ :=
  C * (n + 1) ^ d + C

theorem polyClock_pos (C d n : ℕ) (hC : 1 ≤ C) :
    1 ≤ polyClock C d n := by
  dsimp [polyClock]
  omega

theorem polyClock_monotone (C d : ℕ) :
    Monotone (polyClock C d) := by
  intro a b hab
  dsimp [polyClock]
  have hpow : (a + 1) ^ d ≤ (b + 1) ^ d :=
    Nat.pow_le_pow_left (by omega) d
  have hmul : C * (a + 1) ^ d ≤ C * (b + 1) ^ d :=
    Nat.mul_le_mul_left C hpow
  omega

theorem polyClock_bigO (C d : ℕ) :
    (fun n => polyClock C d n) =O ((· ^ d) : ℕ → ℕ) := by
  change (fun n => C * (n + 1) ^ d + C) =O ((· ^ d) : ℕ → ℕ)
  have h1 : (fun n => C * (n + 1) ^ d) =O ((· ^ d) : ℕ → ℕ) := by
    have hbase : (fun n => n + 1) =O (id : ℕ → ℕ) := by
      apply Asymptotics.IsBigO.of_bound 2
      filter_upwards [Filter.eventually_ge_atTop 1] with n hn
      simp only [Real.norm_natCast, id_eq]
      exact_mod_cast (by omega : n + 1 ≤ 2 * n)
    have hpow : (fun n => (n + 1) ^ d) =O ((· ^ d) : ℕ → ℕ) := by
      have := BigO.pow hbase d
      exact this
    exact BigO.const_mul_left C hpow
  have h2 : (fun _ : ℕ => C) =O ((· ^ d) : ℕ → ℕ) :=
    BigO.const_le_pow C d
  exact BigO.add h1 h2

/-- Dominance: Any function `f =O (· ^ d)` is dominated everywhere by
    `polyClock C d` for some `C ≥ 1`. Handles both the asymptotic regime
    and finite initial exceptional inputs. -/
theorem polyClock_dominates {f : ℕ → ℕ} {d : ℕ} (hf : f =O ((· ^ d) : ℕ → ℕ)) :
    ∃ C ≥ 1, ∀ n, f n ≤ polyClock C d n := by
  rw [BigO, Asymptotics.isBigO_iff] at hf
  obtain ⟨C_real, hC⟩ := hf
  rw [Filter.eventually_atTop] at hC
  obtain ⟨N, hN⟩ := hC
  set M : ℕ := (Finset.range N).sup f with hM_def
  set C_nat : ℕ := ⌈C_real⌉₊ with hC_nat_def
  set C : ℕ := max 1 (max C_nat M) with hC_def
  have hC_ge_1 : 1 ≤ C := le_max_left 1 _
  have hC_ge_Cnat : C_nat ≤ C := le_trans (le_max_left C_nat M) (le_max_right 1 _)
  have hC_ge_M : M ≤ C := le_trans (le_max_right C_nat M) (le_max_right 1 _)
  refine ⟨C, hC_ge_1, fun n => ?_⟩
  dsimp [polyClock]
  by_cases hn : n < N
  · have hf_le_M : f n ≤ M := Finset.le_sup (f := f) (Finset.mem_range.mpr hn)
    have : f n ≤ C := le_trans hf_le_M hC_ge_M
    omega
  · push Not at hn
    have hb := hN n hn
    simp only [Real.norm_natCast] at hb
    have hC_le : C_real ≤ (C_nat : ℝ) := Nat.le_ceil C_real
    have h_nd_nonneg : (0 : ℝ) ≤ ((n ^ d : ℕ) : ℝ) := by positivity
    have h_real : (f n : ℝ) ≤ (C_nat : ℝ) * ((n ^ d : ℕ) : ℝ) :=
      le_trans hb (mul_le_mul_of_nonneg_right hC_le h_nd_nonneg)
    have h_nat : f n ≤ C_nat * n ^ d := by exact_mod_cast h_real
    have h_nd_le : n ^ d ≤ (n + 1) ^ d := Nat.pow_le_pow_left (by omega) d
    have h_mul_le : C_nat * n ^ d ≤ C * (n + 1) ^ d :=
      Nat.mul_le_mul hC_ge_Cnat h_nd_le
    omega

/-- **Order 5: Growth Property.**
    The polynomial clock `polyClock C d n` is eventually strictly dominated
    by the exponential function `2^n`. For every lower bound `lower`, there exists
    `n > lower` such that `polyClock C d n < 2^n`. -/
theorem polyClock_lt_pow_exists (C d lower : ℕ) :
    ∃ n, lower < n ∧ polyClock C d n < 2 ^ n := by
  by_cases hC0 : C = 0
  · subst hC0
    refine ⟨lower + 1, by omega, ?_⟩
    dsimp [polyClock]
    have : 0 < 2 ^ (lower + 1) := Nat.two_pow_pos _
    omega
  · have hC_pos : 1 ≤ C := Nat.one_le_iff_ne_zero.mpr hC0
    have hshift : (fun n => n + 1) =O (id : ℕ → ℕ) := by
      apply Asymptotics.IsBigO.of_bound 2
      filter_upwards [Filter.eventually_ge_atTop 1] with n hn
      simp only [Real.norm_natCast, id_eq]
      exact_mod_cast (by omega : n + 1 ≤ 2 * n)
    have hpow : (fun n => (n + 1) ^ d) =O ((· ^ d) : ℕ → ℕ) := BigO.pow hshift d
    have h2_cast : (fun n => ((n ^ d : ℕ) : ℝ)) =o[Filter.atTop] (fun n => ((2 ^ n : ℕ) : ℝ)) := by
      have key := isLittleO_pow_const_const_pow_of_one_lt (R := ℝ) d (by norm_num : (1 : ℝ) < 2)
      simp only [Nat.cast_pow]
      exact key
    have hlo : LittleO (fun n => (n + 1) ^ d) (fun n => 2 ^ n) :=
      hpow.trans_isLittleO h2_cast
    obtain ⟨N, hN⟩ := LittleO.nat_mul_le hlo (2 * C + 1)
    set n := max (lower + 1) (max 1 N) with hn_def
    have hlower_lt_n : lower < n := by
      have : lower + 1 ≤ n := le_max_left _ _
      omega
    have hn_ge_1 : 1 ≤ n := le_trans (le_max_left 1 N) (le_max_right (lower + 1) _)
    have hn_ge_N : N ≤ n := le_trans (le_max_right 1 N) (le_max_right (lower + 1) _)
    have hbound := hN n hn_ge_N
    have hpow_ge_1 : 1 ≤ (n + 1) ^ d := by
      have : 1 ≤ n + 1 := by omega
      have : 1 ^ d ≤ (n + 1) ^ d := Nat.pow_le_pow_left this d
      simpa using this
    have hC_le : C ≤ C * (n + 1) ^ d := by
      have := Nat.mul_le_mul_left C hpow_ge_1
      simpa using this
    have hpoly_le : polyClock C d n ≤ 2 * C * (n + 1) ^ d := by
      dsimp [polyClock]
      linarith
    have hstrict : 2 * C * (n + 1) ^ d < (2 * C + 1) * (n + 1) ^ d := by
      have : 0 < (n + 1) ^ d := by omega
      nlinarith
    refine ⟨n, hlower_lt_n, ?_⟩
    exact lt_of_le_of_lt hpoly_le (lt_of_lt_of_le hstrict hbound)

/-! ## 2. Clocked Oracle Turing Machines and Completeness (R1) -/

theorem OracleTM.DecidesInTime.mono {k : ℕ} (m : OracleTM k) (oracle : BooleanOracle)
    (L : Language) {T₁ T₂ : ℕ → ℕ} (hdec : m.DecidesInTime oracle L T₁)
    (hle : ∀ n, T₁ n ≤ T₂ n) :
    m.DecidesInTime oracle L T₂ := by
  intro input
  obtain ⟨cfg, time, htime, hreach, hhalt, hyes, hno⟩ := hdec input
  refine ⟨cfg, time, le_trans htime (hle input.length), hreach, hhalt, hyes, hno⟩

/-- A clocked oracle Turing machine: a machine `m` with `k` work tapes,
    paired with a positive clock multiplier `C ≥ 1` and degree `d`. -/
structure ClockedOracleTM where
  /-- Number of ordinary work tapes. -/
  k : ℕ
  /-- The underlying deterministic oracle TM. -/
  m : OracleTM k
  /-- Clock multiplier `C ≥ 1`. -/
  C : ℕ
  /-- Polynomial degree `d`. -/
  d : ℕ
  /-- Positivity of the clock multiplier. -/
  hC : 1 ≤ C

namespace ClockedOracleTM

/-- The clock of a `ClockedOracleTM`: `polyClock C d`. -/
def clock (M : ClockedOracleTM) : ℕ → ℕ :=
  polyClock M.C M.d

/-- A `ClockedOracleTM` decides `L` relative to `oracle` within its explicit clock. -/
def Decides (M : ClockedOracleTM) (oracle : BooleanOracle) (L : Language) : Prop :=
  M.m.DecidesInTime oracle L M.clock

/-- Normalize a `ClockedOracleTM` to have canonical state space `Fin (Fintype.card M.m.Q)`. -/
noncomputable def normalize (M : ClockedOracleTM) : ClockedOracleTM where
  k := M.k
  m := M.m.normalize
  C := M.C
  d := M.d
  hC := M.hC

theorem normalize_clock (M : ClockedOracleTM) :
    M.normalize.clock = M.clock := rfl

/-- Normalizing a clocked oracle machine preserves its decision behavior under any oracle. -/
theorem normalize_decides (M : ClockedOracleTM) (oracle : BooleanOracle)
    (L : Language) (h : M.Decides oracle L) :
    M.normalize.Decides oracle L := by
  dsimp [Decides, normalize, clock]
  exact M.m.normalize_decidesInTime oracle h

end ClockedOracleTM

/-- **R1: Enumeration Completeness Theorem.**
    A language `L` belongs to `PRel A` if and only if it is decided by some
    `ClockedOracleTM` within its explicit everywhere-dominating polynomial clock.
    This replaces non-effective asymptotic existential quantifiers (`f =O (· ^ d)`)
    with an everywhere-valid clock `C * (n + 1)^d + C`. -/
theorem PRel_iff_exists_clocked (A : Language) (L : Language) :
    L ∈ PRel A ↔ ∃ M : ClockedOracleTM, M.Decides (oracleOf A) L := by
  constructor
  · rintro ⟨k, d, m, f, hdec, hbigO⟩
    obtain ⟨C, hC, hdom⟩ := polyClock_dominates hbigO
    have hdec_clock : m.DecidesInTime (oracleOf A) L (polyClock C d) :=
      OracleTM.DecidesInTime.mono m (oracleOf A) L hdec hdom
    refine ⟨⟨k, m, C, d, hC⟩, hdec_clock⟩
  · rintro ⟨M, hdec⟩
    refine ⟨M.k, M.d, M.m, M.clock, hdec, polyClock_bigO M.C M.d⟩

/-- Direct forward direction of completeness: every polynomial-time oracle decider
    is represented by a clocked oracle machine. -/
theorem PRel_represented (A : Language) {L : Language} (hL : L ∈ PRel A) :
    ∃ M : ClockedOracleTM, M.Decides (oracleOf A) L :=
  (PRel_iff_exists_clocked A L).mp hL

/-- Every polynomial-time oracle decider can be represented by a clocked oracle machine
    whose state space is canonical: `Fin q` for some `q : ℕ`. -/
theorem PRel_exists_normalized (A : Language) {L : Language} (hL : L ∈ PRel A) :
    ∃ M : ClockedOracleTM, (∃ q : ℕ, M.m.Q = Fin q) ∧ M.Decides (oracleOf A) L := by
  obtain ⟨M, hM⟩ := PRel_represented A hL
  refine ⟨M.normalize, ⟨Fintype.card M.m.Q, rfl⟩, M.normalize_decides (oracleOf A) L hM⟩

/-! ## 3. Query Extraction and Query Set Cardinality (Orders 2 & 3) -/

/-- Collect the finite set of strings queried during `T` transitions of `m`
    from configuration `cfg` under oracle `oracle`. Matches the exact step semantics:
    query transitions inspect `cfg.query.oracleQuery`, while local transitions and
    halted states issue no queries. -/
def querySetFrom {k : ℕ} (m : OracleTM k) (oracle : BooleanOracle) :
    ℕ → OracleCfg k m.Q → Finset (List Bool)
  | 0, _ => ∅
  | T + 1, cfg =>
      match m.step oracle cfg with
      | none => ∅
      | some next =>
          let thisQuery : Finset (List Bool) :=
            match m.queryTransition cfg.state with
            | some _ => {cfg.query.oracleQuery}
            | none => ∅
          thisQuery ∪ querySetFrom m oracle T next

/-- The finite set of strings queried by `m` on input `x` within `T` steps under `oracle`. -/
def oracleQuerySet {k : ℕ} (m : OracleTM k) (oracle : BooleanOracle)
    (x : List Bool) (T : ℕ) : Finset (List Bool) :=
  querySetFrom m oracle T (m.initCfg x)

/-- The query set of a `ClockedOracleTM` on input `x` within `T` steps. -/
def ClockedOracleTM.querySet (M : ClockedOracleTM) (oracle : BooleanOracle)
    (x : List Bool) (T : ℕ) : Finset (List Bool) :=
  oracleQuerySet M.m oracle x T

/-- **Order 3: Query Set Cardinality Bound.**
    Every step issues at most one query; `T` transitions produce at most `T` distinct queries. -/
theorem querySetFrom_card_le {k : ℕ} (m : OracleTM k) (oracle : BooleanOracle) :
    ∀ (T : ℕ) (cfg : OracleCfg k m.Q),
      (querySetFrom m oracle T cfg).card ≤ T
  | 0, _ => by
      dsimp [querySetFrom]
      omega
  | T + 1, cfg => by
      dsimp [querySetFrom]
      cases hstep : m.step oracle cfg with
      | none =>
          simp
      | some next =>
          simp only
          have ih := querySetFrom_card_le m oracle T next
          have hcard_union := Finset.card_union_le
            (match m.queryTransition cfg.state with | some _ => {cfg.query.oracleQuery} | none => ∅)
            (querySetFrom m oracle T next)
          cases hq : m.queryTransition cfg.state with
          | some states =>
              simp only [hq] at hcard_union ⊢
              have : ({cfg.query.oracleQuery} : Finset (List Bool)).card = 1 :=
                Finset.card_singleton _
              omega
          | none =>
              simp only [hq, Finset.empty_union] at hcard_union ⊢
              omega

theorem oracleQuerySet_card_le {k : ℕ} (m : OracleTM k) (oracle : BooleanOracle)
    (x : List Bool) (T : ℕ) :
    (oracleQuerySet m oracle x T).card ≤ T :=
  querySetFrom_card_le m oracle T (m.initCfg x)

theorem ClockedOracleTM.querySet_card_le (M : ClockedOracleTM)
    (oracle : BooleanOracle) (x : List Bool) (T : ℕ) :
    (M.querySet oracle x T).card ≤ T :=
  oracleQuerySet_card_le M.m oracle x T

/-- Exact name matching Order 3 acceptance specification: query count bounded by time. -/
theorem querySet_card_le_time (M : ClockedOracleTM)
    (oracle : BooleanOracle) (x : List Bool) (T : ℕ) :
    (M.querySet oracle x T).card ≤ T :=
  M.querySet_card_le oracle x T

/-! ## 4. Combinatorial Pigeonhole: Unqueried Strings of Length n (Order 4) -/

/-- The finite set of all binary strings of length `n`. -/
def binaryStrings (n : ℕ) : Finset (List Bool) :=
  (Finset.univ : Finset (Fin n → Bool)).image List.ofFn

theorem length_of_mem_binaryStrings {n : ℕ} {w : List Bool}
    (hw : w ∈ binaryStrings n) : w.length = n := by
  dsimp [binaryStrings] at hw
  rw [Finset.mem_image] at hw
  obtain ⟨f, _, rfl⟩ := hw
  exact List.length_ofFn

theorem card_binaryStrings (n : ℕ) : (binaryStrings n).card = 2 ^ n := by
  dsimp [binaryStrings]
  rw [Finset.card_image_of_injective _ List.ofFn_injective]
  rw [Finset.card_univ, Fintype.card_fun, Fintype.card_bool, Fintype.card_fin]

/-- **Order 4: Unqueried String Lemma.**
    Since there are `2^n` binary strings of length `n` and at most `T` strings queried,
    any condition `T < 2^n` guarantees the existence of a length-`n` binary string
    that was never queried. -/
theorem exists_unqueried_string (Q : Finset (List Bool)) {n T : ℕ}
    (hQ : Q.card ≤ T) (hgap : T < 2 ^ n) :
    ∃ y : List Bool, y.length = n ∧ y ∉ Q := by
  have hcard_S : (binaryStrings n).card = 2 ^ n := card_binaryStrings n
  have hnot_sub : ¬ (binaryStrings n ⊆ Q) := by
    intro hsub
    have hle := Finset.card_le_card hsub
    omega
  have hne : (binaryStrings n \ Q).Nonempty := by
    rw [Finset.nonempty_iff_ne_empty]
    intro heq
    rw [Finset.sdiff_eq_empty_iff_subset] at heq
    exact hnot_sub heq
  obtain ⟨y, hy⟩ := hne
  rw [Finset.mem_sdiff] at hy
  exact ⟨y, length_of_mem_binaryStrings hy.1, hy.2⟩

/-- Specialized to a `ClockedOracleTM`: If `M.clock |x| < 2^n`, there is an unqueried
    witness string of length `n`. -/
theorem ClockedOracleTM.exists_unqueried_witness (M : ClockedOracleTM)
    (oracle : BooleanOracle) (x : List Bool) {n : ℕ}
    (hgap : M.clock x.length < 2 ^ n) :
    ∃ y : List Bool, y.length = n ∧ y ∉ M.querySet oracle x (M.clock x.length) :=
  exists_unqueried_string (M.querySet oracle x (M.clock x.length))
    (M.querySet_card_le oracle x (M.clock x.length)) hgap

/-! ## 5. Execution Trace and Query Preservation under Oracle Agreement (R2) -/

/-- Exact `T`-step deterministic trace of an `OracleTM`. -/
def trace {k : ℕ} (m : OracleTM k) (oracle : BooleanOracle) :
    ℕ → OracleCfg k m.Q → OracleCfg k m.Q
  | 0, cfg => cfg
  | T + 1, cfg =>
      match m.step oracle cfg with
      | none => cfg
      | some next => trace m oracle T next

/-- One-step preservation: If two oracles agree on the query issued at `cfg`
    (if any), then `m.step` produces the exact same next configuration. -/
theorem step_congr_of_query_agree {k : ℕ} (m : OracleTM k) (O₁ O₂ : BooleanOracle)
    (cfg : OracleCfg k m.Q)
    (hagree : match m.queryTransition cfg.state with
      | some _ => O₁ cfg.query.oracleQuery = O₂ cfg.query.oracleQuery
      | none => True) :
    m.step O₁ cfg = m.step O₂ cfg := by
  dsimp only [OracleTM.step]
  by_cases hhalt : cfg.state = m.qhalt
  · simp only [hhalt, ↓reduceIte]
  · simp only [hhalt, ↓reduceIte]
    cases hq : m.queryTransition cfg.state with
    | some states =>
        obtain ⟨yesState, noState⟩ := states
        simp only [hq] at hagree
        rw [hagree]
    | none =>
        rfl

/-- **R2: Multi-Step Trace and Query Preservation Theorem.**
    If two oracles agree on every query in the query set of a `T`-step run,
    then the execution traces and query sets under both oracles are identical. -/
theorem trace_congr_of_querySet_agree {k : ℕ} (m : OracleTM k) (O₁ O₂ : BooleanOracle) :
    ∀ (T : ℕ) (cfg : OracleCfg k m.Q),
      (∀ q ∈ querySetFrom m O₁ T cfg, O₁ q = O₂ q) →
      trace m O₁ T cfg = trace m O₂ T cfg ∧
      querySetFrom m O₁ T cfg = querySetFrom m O₂ T cfg
  | 0, _, _ => ⟨rfl, rfl⟩
  | T + 1, cfg, hagree => by
      dsimp only [trace, querySetFrom]
      cases hstep₁ : m.step O₁ cfg with
      | none =>
          have hhalt : cfg.state = m.qhalt := by
            by_contra hne
            have hsome : (m.step O₁ cfg).isSome := by
              dsimp only [OracleTM.step]
              simp only [hne, ↓reduceIte]
              cases m.queryTransition cfg.state <;> rfl
            simp [hstep₁] at hsome
          have hstep₂ : m.step O₂ cfg = none := by
            dsimp only [OracleTM.step]
            simp only [hhalt, ↓reduceIte]
          simp only [hstep₂, and_self]
      | some next =>
          have hstep_eq : querySetFrom m O₁ (T + 1) cfg =
              (match m.queryTransition cfg.state with
              | some _ => {cfg.query.oracleQuery}
              | none => ∅) ∪ querySetFrom m O₁ T next := by
            dsimp only [querySetFrom]
            rw [hstep₁]
          have hthisQuery_agree : match m.queryTransition cfg.state with
              | some _ => O₁ cfg.query.oracleQuery = O₂ cfg.query.oracleQuery
              | none => True := by
            cases hq : m.queryTransition cfg.state with
            | some states =>
                dsimp only
                apply hagree
                rw [hstep_eq, hq]
                exact Finset.mem_union_left _ (Finset.mem_singleton_self _)
            | none =>
                trivial
          have hstep₂ : m.step O₂ cfg = some next := by
            rw [← step_congr_of_query_agree m O₁ O₂ cfg hthisQuery_agree, hstep₁]
          have hrest_agree : ∀ q ∈ querySetFrom m O₁ T next, O₁ q = O₂ q := by
            intro q hq
            apply hagree
            rw [hstep_eq]
            exact Finset.mem_union_right _ hq
          obtain ⟨htrace_rest, hquery_rest⟩ :=
            trace_congr_of_querySet_agree m O₁ O₂ T next hrest_agree
          refine ⟨by simp only [hstep₂, htrace_rest], ?_⟩
          dsimp only
          rw [hquery_rest, hstep₂]

/-- Preservation under extending an oracle by an unqueried string `w*`:
    adding `w*` does not change any query answer in `querySetFrom`, so the trace
    is completely identical. -/
theorem trace_invariant_of_unqueried {k : ℕ} (m : OracleTM k) (A : Language)
    (T : ℕ) (cfg : OracleCfg k m.Q) (w : List Bool)
    (hw : w ∉ querySetFrom m (oracleOf A) T cfg) :
    trace m (oracleOf (A ∪ {w})) T cfg = trace m (oracleOf A) T cfg := by
  have hagree : ∀ q ∈ querySetFrom m (oracleOf A) T cfg,
      oracleOf A q = oracleOf (A ∪ {w}) q := by
    intro q hq
    dsimp [oracleOf]
    have hne : q ≠ w := by
      rintro rfl
      exact hw hq
    have hiff : q ∈ A ∪ {w} ↔ q ∈ A := by
      simp only [Set.mem_union, Set.mem_singleton_iff, or_iff_left hne]
    rw [hiff]
  exact (trace_congr_of_querySet_agree m (oracleOf A) (oracleOf (A ∪ {w})) T cfg hagree).1.symm

/-- **Protected query agreement lemma (Order 6 interface):**
    If two language oracles agree on membership for all queries in a finite set `Q`,
    then their boolean indicator functions `oracleOf` agree on all queries in `Q`. -/
theorem protected_query_agreement
    (A B : Language)
    (Q : Finset (List Bool))
    (hagree : ∀ q, q ∈ Q → (q ∈ A ↔ q ∈ B)) :
    ∀ q ∈ Q, oracleOf A q = oracleOf B q := by
  intro q hq
  dsimp [oracleOf]
  rw [decide_eq_decide]
  exact hagree q hq

/-- Single-query indicator agreement lemma. -/
theorem oracleOf_congr {A B : Language} {q : List Bool} (h : q ∈ A ↔ q ∈ B) :
    oracleOf A q = oracleOf B q := by
  dsimp [oracleOf]
  rw [decide_eq_decide]
  exact h

/-! ## 6. Stage Recurrence, Query Horizon, and Diagonalization Record (Orders 5 & 6) -/

/-- Maximum length among queries in a finite set, with default 0 if empty.
    Matches `R_i = max({|q| : q ∈ Q_i} ∪ {0})`. -/
def queryHorizon (Q : Finset (List Bool)) : ℕ :=
  Q.sup List.length

theorem length_le_queryHorizon {q : List Bool} {Q : Finset (List Bool)} (hq : q ∈ Q) :
    q.length ≤ queryHorizon Q :=
  Finset.le_sup hq

/-- **Order 5: Stage Length Selection Theorem.**
    For any machine `M`, prior stage length `n_prev`, and prior query horizon `R_prev`,
    there exists a stage length `n` satisfying:
    1. Freshness: `n_prev < n`
    2. Query Protection Horizon: `R_prev < n`
    3. Exponential Gap: `M.clock n < 2^n`. -/
theorem stageLength_exists (n_prev R_prev : ℕ) (M : ClockedOracleTM) :
    ∃ n : ℕ, n_prev < n ∧ R_prev < n ∧ M.clock n < 2 ^ n := by
  obtain ⟨n, hlower, hgap⟩ := polyClock_lt_pow_exists M.C M.d (max n_prev R_prev)
  have hn_prev : n_prev < n := lt_of_le_of_lt (le_max_left n_prev R_prev) hlower
  have hR_prev : R_prev < n := lt_of_le_of_lt (le_max_right n_prev R_prev) hlower
  exact ⟨n, hn_prev, hR_prev, hgap⟩

/-- Standalone stage execution record packaging all stage parameters, execution artifacts,
    and the branch-consistent oracle extension with explicit equation fields. -/
structure StageRecord (M : ClockedOracleTM) (B_prev : Language) (n_prev R_prev : ℕ) where
  /-- The chosen fresh stage length. -/
  n : ℕ
  /-- Freshness: strictly greater than all previous stage lengths. -/
  hn_fresh : n_prev < n
  /-- Query horizon: strictly greater than all previous query lengths. -/
  hn_horizon : R_prev < n
  /-- Exponential gap: enough unqueried strings exist. -/
  hgap : M.clock n < 2 ^ n
  /-- The canonical input string 1^n. -/
  input : List Bool := List.replicate n true
  /-- Queries issued during the execution on 1^n under B_prev. -/
  queries : Finset (List Bool) :=
    M.querySet (oracleOf B_prev) (List.replicate n true) (M.clock n)
  /-- Query horizon for this run. -/
  horizon : ℕ := queryHorizon queries
  /-- Final configuration after M.clock n steps. -/
  finalCfg : OracleCfg M.k M.m.Q :=
    trace M.m (oracleOf B_prev) (M.clock n) (M.m.initCfg (List.replicate n true))
  /-- Boolean decision: does M accept 1^n within M.clock n steps? -/
  accepts : Bool :=
    decide (M.m.halted finalCfg ∧ finalCfg.output.cells 1 = Γ.one)
  /-- The optional inserted string. -/
  newString : Option (List Bool)
  /-- Branch correctness: string inserted iff machine rejects. -/
  h_branch_none : newString = none ↔ accepts = true
  h_branch_some : (∃ w, newString = some w) ↔ accepts = false
  /-- If inserted, witness length matches stage length n. -/
  h_new_length : ∀ w, newString = some w → w.length = n
  /-- If inserted, witness was never queried. -/
  h_new_unqueried : ∀ w, newString = some w → w ∉ queries
  /-- The updated oracle language. -/
  B_next : Language := match newString with
    | none => B_prev
    | some w => B_prev ∪ {w}
  /-- Equation: input definition. -/
  h_input : input = List.replicate n true := by rfl
  /-- Equation: query set definition. -/
  h_queries : queries = M.querySet (oracleOf B_prev) input (M.clock n) := by rfl
  /-- Equation: horizon definition. -/
  h_horizon : horizon = queryHorizon queries := by rfl
  /-- Equation: final configuration definition. -/
  h_finalCfg : finalCfg = trace M.m (oracleOf B_prev) (M.clock n) (M.m.initCfg input) := by rfl
  /-- Equation: accepts decision definition. -/
  h_accepts : accepts = decide (M.m.halted finalCfg ∧ finalCfg.output.cells 1 = Γ.one) := by rfl
  /-- Equation: branch-consistent B_next definition. -/
  h_B_next : B_next = match newString with
    | none => B_prev
    | some w => B_prev ∪ {w} := by rfl

/-- Constructive existence of a valid `StageRecord` for any stage. -/
noncomputable def makeStageRecord (M : ClockedOracleTM) (B_prev : Language)
    (n_prev R_prev : ℕ) : StageRecord M B_prev n_prev R_prev := by
  have hex := stageLength_exists n_prev R_prev M
  set n := Classical.choose hex with hn_def
  have hn_fresh := (Classical.choose_spec hex).1
  have hn_horizon := (Classical.choose_spec hex).2.1
  have hgap := (Classical.choose_spec hex).2.2
  set input := List.replicate n true with hinput_def
  set queries := M.querySet (oracleOf B_prev) input (M.clock n) with hqueries_def
  set finalCfg := trace M.m (oracleOf B_prev) (M.clock n) (M.m.initCfg input) with hfinal_def
  set accepts := decide (M.m.halted finalCfg ∧ finalCfg.output.cells 1 = Γ.one) with hacc_def
  by_cases hacc : accepts = true
  · exact {
      n := n
      hn_fresh := hn_fresh
      hn_horizon := hn_horizon
      hgap := hgap
      input := input
      queries := queries
      horizon := queryHorizon queries
      finalCfg := finalCfg
      accepts := accepts
      newString := none
      h_branch_none := by simp [hacc]
      h_branch_some := by simp [hacc]
      h_new_length := by intro w hw; cases hw
      h_new_unqueried := by intro w hw; cases hw
      B_next := B_prev
    }
  · have hacc_false : accepts = false := Bool.eq_false_of_not_eq_true hacc
    have hlen : input.length = n := by simp [input]
    have hgap' : M.clock input.length < 2 ^ n := by rw [hlen]; exact hgap
    have hw_exists := M.exists_unqueried_witness (oracleOf B_prev) input (n := n) hgap'
    set w := Classical.choose hw_exists with hw_def
    have hw_spec := Classical.choose_spec hw_exists
    have hw_queries : w ∉ queries := by
      have : queries = M.querySet (oracleOf B_prev) input (M.clock n) := rfl
      rw [this, ← hlen]
      exact hw_spec.2
    exact {
      n := n
      hn_fresh := hn_fresh
      hn_horizon := hn_horizon
      hgap := hgap
      input := input
      queries := queries
      horizon := queryHorizon queries
      finalCfg := finalCfg
      accepts := accepts
      newString := some w
      h_branch_none := by simp [hacc_false]
      h_branch_some := by simp [hacc_false]
      h_new_length := by
        intro w' hw'
        injection hw' with heq
        subst heq
        exact hw_spec.1
      h_new_unqueried := by
        intro w' hw'
        injection hw' with heq
        subst heq
        exact hw_queries
      B_next := B_prev ∪ {w}
    }

/-- Helper lemma for Option cases without dependent generalization. -/
theorem option_cases {α : Type _} (o : Option α) : o = none ∨ ∃ a, o = some a := by
  cases o with
  | none => left; rfl
  | some a => right; exact ⟨a, rfl⟩

/-! ## 7. Stage Recurrence and Trace Preservation (Orders 5 & 6) -/

/-- Package containing previous stage context and the verified `StageRecord`. -/
structure StagePack (M : ClockedOracleTM) where
  B_prev : Language
  n_prev : ℕ
  R_prev : ℕ
  record : StageRecord M B_prev n_prev R_prev

/-- The stage sequence defined by primitive recursion over an enumeration of clocked machines. -/
noncomputable def stageSeq (machines : ℕ → ClockedOracleTM) : (i : ℕ) → StagePack (machines i) :=
  Nat.rec
    { B_prev := ∅
      n_prev := 0
      R_prev := 0
      record := makeStageRecord (machines 0) ∅ 0 0 }
    (fun i prev =>
      { B_prev := prev.record.B_next
        n_prev := prev.record.n
        R_prev := prev.record.horizon
        record := makeStageRecord (machines i.succ) prev.record.B_next prev.record.n prev.record.horizon })

/-- Oracle language at the end of stage `i`. -/
noncomputable def stageOracle (machines : ℕ → ClockedOracleTM) (i : ℕ) : Language :=
  (stageSeq machines i).record.B_next

/-- Stage length chosen at stage `i`. -/
noncomputable def stageN (machines : ℕ → ClockedOracleTM) (i : ℕ) : ℕ :=
  (stageSeq machines i).record.n

/-- Query set generated by machine `i` at stage `i`. -/
noncomputable def stageQueries (machines : ℕ → ClockedOracleTM) (i : ℕ) : Finset (List Bool) :=
  (stageSeq machines i).record.queries

/-- Query horizon at stage `i`. -/
noncomputable def stageHorizon (machines : ℕ → ClockedOracleTM) (i : ℕ) : ℕ :=
  (stageSeq machines i).record.horizon

theorem stageSeq_zero_B_prev (machines : ℕ → ClockedOracleTM) :
    (stageSeq machines 0).B_prev = ∅ := rfl

theorem stageSeq_succ_B_prev (machines : ℕ → ClockedOracleTM) (i : ℕ) :
    (stageSeq machines i.succ).B_prev = stageOracle machines i := rfl

theorem stageSeq_succ_n_prev (machines : ℕ → ClockedOracleTM) (i : ℕ) :
    (stageSeq machines i.succ).n_prev = stageN machines i := rfl

theorem stageSeq_succ_R_prev (machines : ℕ → ClockedOracleTM) (i : ℕ) :
    (stageSeq machines i.succ).R_prev = stageHorizon machines i := rfl

theorem stageHorizon_eq_queryHorizon (machines : ℕ → ClockedOracleTM) (j : ℕ) :
    stageHorizon machines j = queryHorizon (stageQueries machines j) :=
  (stageSeq machines j).record.h_horizon

theorem stageQueries_eq (machines : ℕ → ClockedOracleTM) (j : ℕ) :
    stageQueries machines j =
    querySetFrom (machines j).m (oracleOf (stageSeq machines j).B_prev)
      ((machines j).clock (stageN machines j))
      ((machines j).m.initCfg (List.replicate (stageN machines j) true)) := by
  have hq := (stageSeq machines j).record.h_queries
  have hi := (stageSeq machines j).record.h_input
  have hqueries : stageQueries machines j = (stageSeq machines j).record.queries := rfl
  have hn : stageN machines j = (stageSeq machines j).record.n := rfl
  rw [hqueries, hn, hq, hi]
  rfl

theorem stageFinalCfg_eq (machines : ℕ → ClockedOracleTM) (j : ℕ) :
    (stageSeq machines j).record.finalCfg =
    trace (machines j).m (oracleOf (stageSeq machines j).B_prev)
      ((machines j).clock (stageN machines j))
      ((machines j).m.initCfg (List.replicate (stageN machines j) true)) := by
  have hf := (stageSeq machines j).record.h_finalCfg
  have hi := (stageSeq machines j).record.h_input
  have hn : stageN machines j = (stageSeq machines j).record.n := rfl
  rw [hn, hf, hi]

theorem stageRecord_B_prev_subset (M : ClockedOracleTM) (B_prev : Language)
    (n_prev R_prev : ℕ) (rec : StageRecord M B_prev n_prev R_prev) :
    B_prev ⊆ rec.B_next := by
  rcases rec with ⟨n, hn_fresh, hn_horizon, hgap, input, queries, horizon,
    finalCfg, accepts, newString, h_branch_none, h_branch_some,
    h_new_length, h_new_unqueried, B_next,
    h_input, h_queries, h_horizon, h_finalCfg, h_accepts, h_B_next⟩
  dsimp only at h_B_next ⊢
  rw [h_B_next]
  intro x hx
  cases newString with
  | none => exact hx
  | some w => exact Set.mem_union_left _ hx

theorem stageRecord_queries_mem_iff (M : ClockedOracleTM) (B_prev : Language)
    (n_prev R_prev : ℕ) (rec : StageRecord M B_prev n_prev R_prev)
    {q : List Bool} (hq : q ∈ rec.queries) :
    q ∈ rec.B_next ↔ q ∈ B_prev := by
  rcases rec with ⟨n, hn_fresh, hn_horizon, hgap, input, queries, horizon,
    finalCfg, accepts, newString, h_branch_none, h_branch_some,
    h_new_length, h_new_unqueried, B_next,
    h_input, h_queries, h_horizon, h_finalCfg, h_accepts, h_B_next⟩
  dsimp only at h_B_next hq ⊢
  rw [h_B_next]
  cases newString with
  | none => rfl
  | some w =>
      dsimp only
      constructor
      · intro hmem
        rcases hmem with h1 | h2
        · exact h1
        · have hnot := h_new_unqueried w rfl
          have heq : q = w := h2
          subst heq
          exact False.elim (hnot hq)
      · intro hmem
        exact Set.mem_union_left _ hmem

theorem stageOracle_step_subset (machines : ℕ → ClockedOracleTM) (i : ℕ) :
    stageOracle machines i ⊆ stageOracle machines i.succ :=
  stageRecord_B_prev_subset _ _ _ _ (stageSeq machines i.succ).record

theorem stageOracle_mono (machines : ℕ → ClockedOracleTM) {j i : ℕ} (hji : j ≤ i) :
    stageOracle machines j ⊆ stageOracle machines i := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hji
  clear hji
  induction d with
  | zero => exact Set.Subset.rfl
  | succ d ih =>
      have heq : j + (d + 1) = (j + d).succ := by omega
      rw [heq]
      exact Set.Subset.trans ih (stageOracle_step_subset machines (j + d))

theorem stageN_lt_succ (machines : ℕ → ClockedOracleTM) (i : ℕ) :
    stageN machines i < stageN machines i.succ :=
  (stageSeq machines i.succ).record.hn_fresh

theorem stageN_strictMono (machines : ℕ → ClockedOracleTM) :
    StrictMono (stageN machines) :=
  strictMono_nat_of_lt_succ (stageN_lt_succ machines)

theorem stageN_lt_of_lt (machines : ℕ → ClockedOracleTM) {j i : ℕ} (h : j < i) :
    stageN machines j < stageN machines i :=
  stageN_strictMono machines h

theorem stageN_le_of_le (machines : ℕ → ClockedOracleTM) {j i : ℕ} (h : j ≤ i) :
    stageN machines j ≤ stageN machines i :=
  (stageN_strictMono machines).monotone h

theorem stageHorizon_lt_stageN_succ (machines : ℕ → ClockedOracleTM) (j : ℕ) :
    stageHorizon machines j < stageN machines j.succ :=
  (stageSeq machines j.succ).record.hn_horizon

theorem query_length_le_stageHorizon (machines : ℕ → ClockedOracleTM) (j : ℕ)
    {q : List Bool} (hq : q ∈ stageQueries machines j) :
    q.length ≤ stageHorizon machines j := by
  rw [stageHorizon_eq_queryHorizon]
  exact length_le_queryHorizon hq

theorem query_length_lt_stageN_succ (machines : ℕ → ClockedOracleTM) (j : ℕ)
    {q : List Bool} (hq : q ∈ stageQueries machines j) :
    q.length < stageN machines j.succ :=
  lt_of_le_of_lt (query_length_le_stageHorizon machines j hq)
    (stageHorizon_lt_stageN_succ machines j)

theorem query_length_lt_stageN_of_gt (machines : ℕ → ClockedOracleTM) {j k : ℕ}
    (hjk : j < k) {q : List Bool} (hq : q ∈ stageQueries machines j) :
    q.length < stageN machines k := by
  have hsucc : j.succ ≤ k := Nat.succ_le_of_lt hjk
  exact lt_of_lt_of_le (query_length_lt_stageN_succ machines j hq)
    (stageN_le_of_le machines hsucc)

theorem stageRecord_diff_length (M : ClockedOracleTM) (B_prev : Language)
    (n_prev R_prev : ℕ) (rec : StageRecord M B_prev n_prev R_prev) {x : List Bool}
    (hx : x ∈ rec.B_next) (hnot : x ∉ B_prev) :
    x.length = rec.n := by
  rcases rec with ⟨n, hn_fresh, hn_horizon, hgap, input, queries, horizon,
    finalCfg, accepts, newString, h_branch_none, h_branch_some,
    h_new_length, h_new_unqueried, B_next,
    h_input, h_queries, h_horizon, h_finalCfg, h_accepts, h_B_next⟩
  dsimp only at h_B_next hx ⊢
  rw [h_B_next] at hx
  cases newString with
  | none =>
      dsimp only at hx
      exact False.elim (hnot hx)
  | some w =>
      dsimp only at hx
      rcases hx with h1 | h2
      · exact False.elim (hnot h1)
      · have hlen := h_new_length w rfl
        have heq : x = w := h2
        subst heq
        exact hlen

theorem mem_stageOracle_succ_diff (machines : ℕ → ClockedOracleTM) (i : ℕ) {x : List Bool}
    (hx : x ∈ stageOracle machines i.succ) (hnot : x ∉ stageOracle machines i) :
    x.length = stageN machines i.succ :=
  stageRecord_diff_length _ _ _ _ (stageSeq machines i.succ).record hx hnot

theorem query_not_mem_diff_succ (machines : ℕ → ClockedOracleTM) {j i : ℕ}
    (hji : j ≤ i) {q : List Bool} (hq : q ∈ stageQueries machines j) :
    q ∉ stageOracle machines i.succ \ stageOracle machines i := by
  rintro ⟨hsucc, hnot⟩
  have hlen : q.length = stageN machines i.succ :=
    mem_stageOracle_succ_diff machines i hsucc hnot
  have hlt : q.length < stageN machines i.succ :=
    query_length_lt_stageN_of_gt machines (Nat.lt_succ_of_le hji) hq
  exact (ne_of_lt hlt) hlen

theorem query_mem_succ_iff (machines : ℕ → ClockedOracleTM) {j i : ℕ}
    (hji : j ≤ i) {q : List Bool} (hq : q ∈ stageQueries machines j) :
    q ∈ stageOracle machines i.succ ↔ q ∈ stageOracle machines i := by
  constructor
  · intro hq_succ
    by_contra hnot
    exact query_not_mem_diff_succ machines hji hq ⟨hq_succ, hnot⟩
  · intro hqi
    exact stageOracle_step_subset machines i hqi

/-- **Order 6, Layer A (Query agreement across finite stages):**
    For any `j ≤ i`, the stage-`j` query set has identical membership answers
    under `stageOracle machines j` and `stageOracle machines i`. -/
theorem stageQueries_mem_iff_of_le (machines : ℕ → ClockedOracleTM) {j i : ℕ}
    (hji : j ≤ i) {q : List Bool} (hq : q ∈ stageQueries machines j) :
    q ∈ stageOracle machines i ↔ q ∈ stageOracle machines j := by
  obtain ⟨d, rfl⟩ := Nat.exists_eq_add_of_le hji
  clear hji
  induction d with
  | zero => rfl
  | succ d ih =>
      have hstep := query_mem_succ_iff machines (Nat.le_add_right j d) hq
      have heq : j + (d + 1) = (j + d).succ := by omega
      rw [heq, hstep]
      exact ih

theorem stageQueries_mem_prev_iff_of_le (machines : ℕ → ClockedOracleTM) {j i : ℕ}
    (hji : j ≤ i) {q : List Bool} (hq : q ∈ stageQueries machines j) :
    q ∈ stageOracle machines i ↔ q ∈ (stageSeq machines j).B_prev := by
  rw [stageQueries_mem_iff_of_le machines hji hq]
  exact stageRecord_queries_mem_iff (machines j) _ _ _ (stageSeq machines j).record hq

/-- **Order 6, Layer A: Finite-stage trace preservation theorem.**
    For any `j ≤ i`, machine `j`'s execution on `1^{n_j}` under oracle `B_i`
    is identical to its canonical stage-`j` execution record. -/
theorem stage_preserves_previous_runs (machines : ℕ → ClockedOracleTM) {j i : ℕ}
    (hji : j ≤ i) :
    trace (machines j).m (oracleOf (stageOracle machines i))
      ((machines j).clock (stageN machines j))
      ((machines j).m.initCfg (List.replicate (stageN machines j) true)) =
    (stageSeq machines j).record.finalCfg := by
  have hagree : ∀ q ∈ querySetFrom (machines j).m
      (oracleOf (stageSeq machines j).B_prev)
      ((machines j).clock (stageN machines j))
      ((machines j).m.initCfg (List.replicate (stageN machines j) true)),
      oracleOf ((stageSeq machines j).B_prev) q =
      oracleOf (stageOracle machines i) q := by
    intro q hq
    have hq' : q ∈ stageQueries machines j := by
      rw [stageQueries_eq]
      exact hq
    exact (oracleOf_congr (stageQueries_mem_prev_iff_of_le machines hji hq')).symm
  have htrace := (trace_congr_of_querySet_agree (machines j).m
    (oracleOf (stageSeq machines j).B_prev)
    (oracleOf (stageOracle machines i))
    ((machines j).clock (stageN machines j))
    ((machines j).m.initCfg (List.replicate (stageN machines j) true))
    hagree).1
  rw [stageFinalCfg_eq]
  exact htrace.symm

/-- **The Baker-Gill-Solovay Diagonal Oracle.**
    Defined as the countable union of all finite stage oracles: `B = ⋃_i B_i`. -/
def bgsOracle (machines : ℕ → ClockedOracleTM) : Language :=
  { x | ∃ i, x ∈ stageOracle machines i }

theorem mem_bgsOracle_iff (machines : ℕ → ClockedOracleTM) (x : List Bool) :
    x ∈ bgsOracle machines ↔ ∃ i, x ∈ stageOracle machines i := Iff.rfl

theorem stageOracle_subset_bgsOracle (machines : ℕ → ClockedOracleTM) (i : ℕ) :
    stageOracle machines i ⊆ bgsOracle machines := by
  intro x hx
  exact ⟨i, hx⟩

/-- **Order 6, Layer B (Query agreement between infinite union and stage j):**
    For every query `q ∈ Q_j`, `q ∈ B ↔ q ∈ B_j`. -/
theorem query_mem_bgsOracle_iff (machines : ℕ → ClockedOracleTM) (j : ℕ)
    {q : List Bool} (hq : q ∈ stageQueries machines j) :
    q ∈ bgsOracle machines ↔ q ∈ stageOracle machines j := by
  constructor
  · rintro ⟨k, hqk⟩
    rcases le_total k j with hkj | hjk
    · exact stageOracle_mono machines hkj hqk
    · exact (stageQueries_mem_iff_of_le machines hjk hq).mp hqk
  · intro hqj
    exact stageOracle_subset_bgsOracle machines j hqj

theorem query_mem_bgsOracle_iff_prev (machines : ℕ → ClockedOracleTM) (j : ℕ)
    {q : List Bool} (hq : q ∈ stageQueries machines j) :
    q ∈ bgsOracle machines ↔ q ∈ (stageSeq machines j).B_prev := by
  rw [query_mem_bgsOracle_iff machines j hq]
  exact stageRecord_queries_mem_iff (machines j) _ _ _ (stageSeq machines j).record hq

/-- **Order 6, Layer B: Infinite-union trace preservation theorem.**
    The execution trace of machine `j` on `1^{n_j}` under the infinite-union
    oracle `bgsOracle` is completely identical to its canonical stage-`j` execution. -/
theorem finalOracle_trace_preserved (machines : ℕ → ClockedOracleTM) (j : ℕ) :
    trace (machines j).m (oracleOf (bgsOracle machines))
      ((machines j).clock (stageN machines j))
      ((machines j).m.initCfg (List.replicate (stageN machines j) true)) =
    (stageSeq machines j).record.finalCfg := by
  have hagree : ∀ q ∈ querySetFrom (machines j).m
      (oracleOf (stageSeq machines j).B_prev)
      ((machines j).clock (stageN machines j))
      ((machines j).m.initCfg (List.replicate (stageN machines j) true)),
      oracleOf ((stageSeq machines j).B_prev) q =
      oracleOf (bgsOracle machines) q := by
    intro q hq
    have hq' : q ∈ stageQueries machines j := by
      rw [stageQueries_eq]
      exact hq
    exact (oracleOf_congr (query_mem_bgsOracle_iff_prev machines j hq')).symm
  have htrace := (trace_congr_of_querySet_agree (machines j).m
    (oracleOf (stageSeq machines j).B_prev)
    (oracleOf (bgsOracle machines))
    ((machines j).clock (stageN machines j))
    ((machines j).m.initCfg (List.replicate (stageN machines j) true))
    hagree).1
  rw [stageFinalCfg_eq]
  exact htrace.symm

/-- Corollary: Machine `j`'s acceptance decision under `bgsOracle` matches `accepts`. -/
theorem finalOracle_accepts_eq (machines : ℕ → ClockedOracleTM) (j : ℕ) :
    let finalCfg := trace (machines j).m (oracleOf (bgsOracle machines))
      ((machines j).clock (stageN machines j))
      ((machines j).m.initCfg (List.replicate (stageN machines j) true))
    decide ((machines j).m.halted finalCfg ∧ finalCfg.output.cells 1 = Γ.one) =
    (stageSeq machines j).record.accepts := by
  intro finalCfg
  have htrace : finalCfg = (stageSeq machines j).record.finalCfg :=
    finalOracle_trace_preserved machines j
  have hcongr := congrArg (fun (cfg : OracleCfg (machines j).k (machines j).m.Q) =>
    decide ((machines j).m.halted cfg ∧ cfg.output.cells 1 = Γ.one)) htrace
  rw [hcongr]
  exact (stageSeq machines j).record.h_accepts.symm

/-- Input 1^n belongs to unaryWitnessLang B iff some witness of length n exists in B. -/
theorem mem_unaryWitnessLang_replicate_iff (B : Language) (n : ℕ) :
    List.replicate n true ∈ unaryWitnessLang B ↔ ∃ y ∈ B, y.length = n := by
  dsimp [unaryWitnessLang]
  have hall : ∀ b ∈ List.replicate n true, b = true := by
    intro b hb
    have := List.mem_replicate.mp hb
    exact this.2
  have hlen : (List.replicate n true).length = n := List.length_replicate
  constructor
  · rintro ⟨-, y, hy, hyl⟩
    rw [hlen] at hyl
    exact ⟨y, hy, hyl⟩
  · rintro ⟨y, hy, hyl⟩
    refine ⟨hall, y, hy, ?_⟩
    rw [hlen, hyl]

theorem stageRecord_mem_next_iff (M : ClockedOracleTM) (B_prev : Language)
    (n_prev R_prev : ℕ) (rec : StageRecord M B_prev n_prev R_prev) (x : List Bool) :
    x ∈ rec.B_next ↔ x ∈ B_prev ∨ rec.newString = some x := by
  rcases rec with ⟨n, hn_fresh, hn_horizon, hgap, input, queries, horizon,
    finalCfg, accepts, newString, h_branch_none, h_branch_some,
    h_new_length, h_new_unqueried, B_next,
    h_input, h_queries, h_horizon, h_finalCfg, h_accepts, h_B_next⟩
  dsimp only at h_B_next ⊢
  rw [h_B_next]
  cases newString with
  | none =>
      dsimp only
      simp
  | some w =>
      dsimp only
      simp only [Set.mem_union, Set.mem_singleton_iff, Option.some.injEq]
      tauto

theorem mem_stageOracle_succ_iff (machines : ℕ → ClockedOracleTM) (i : ℕ) (x : List Bool) :
    x ∈ stageOracle machines i.succ ↔
      x ∈ stageOracle machines i ∨ (stageSeq machines i.succ).record.newString = some x :=
  stageRecord_mem_next_iff _ _ _ _ (stageSeq machines i.succ).record x

theorem mem_stageOracle_zero_iff (machines : ℕ → ClockedOracleTM) (x : List Bool) :
    x ∈ stageOracle machines 0 ↔ (stageSeq machines 0).record.newString = some x := by
  have h := stageRecord_mem_next_iff (machines 0) _ _ _ (stageSeq machines 0).record x
  dsimp only [stageOracle]
  rw [h]
  have hprev : (stageSeq machines 0).B_prev = ∅ := rfl
  have : (x ∈ (stageSeq machines 0).B_prev) ↔ False := by
    rw [hprev]; simp
  rw [this]
  simp

theorem mem_stageOracle_iff_exists_newString (machines : ℕ → ClockedOracleTM) (i : ℕ) (x : List Bool) :
    x ∈ stageOracle machines i ↔ ∃ k ≤ i, (stageSeq machines k).record.newString = some x := by
  induction i with
  | zero =>
      rw [mem_stageOracle_zero_iff]
      constructor
      · intro h; exact ⟨0, Nat.le_refl 0, h⟩
      · rintro ⟨k, hk, h⟩
        have : k = 0 := by omega
        subst this
        exact h
  | succ i ih =>
      rw [mem_stageOracle_succ_iff, ih]
      constructor
      · rintro (⟨k, hki, hk_eq⟩ | hsucc)
        · exact ⟨k, le_trans hki (Nat.le_succ i), hk_eq⟩
        · exact ⟨i.succ, Nat.le_refl _, hsucc⟩
      · rintro ⟨k, hki, hk_eq⟩
        rcases Nat.lt_or_eq_of_le hki with hlt | heq
        · left
          exact ⟨k, Nat.le_of_lt_succ hlt, hk_eq⟩
        · right
          subst heq
          exact hk_eq

theorem mem_bgsOracle_iff_exists_newString (machines : ℕ → ClockedOracleTM) (x : List Bool) :
    x ∈ bgsOracle machines ↔ ∃ k, (stageSeq machines k).record.newString = some x := by
  rw [mem_bgsOracle_iff]
  constructor
  · rintro ⟨i, hi⟩
    rw [mem_stageOracle_iff_exists_newString] at hi
    obtain ⟨k, _, hk⟩ := hi
    exact ⟨k, hk⟩
  · rintro ⟨k, hk⟩
    refine ⟨k, ?_⟩
    rw [mem_stageOracle_iff_exists_newString]
    exact ⟨k, Nat.le_refl k, hk⟩

theorem bgsOracle_witness_iff (machines : ℕ → ClockedOracleTM) (j : ℕ) :
    (∃ y ∈ bgsOracle machines, y.length = stageN machines j) ↔
    (stageSeq machines j).record.accepts = false := by
  constructor
  · rintro ⟨y, hy, hlen⟩
    rw [mem_bgsOracle_iff_exists_newString] at hy
    obtain ⟨k, hk⟩ := hy
    have hlen_k := (stageSeq machines k).record.h_new_length y hk
    have heq_len : stageN machines k = stageN machines j := by
      have hn : stageN machines k = (stageSeq machines k).record.n := rfl
      rw [hn, ← hlen_k, hlen]
    have hkj : k = j := (stageN_strictMono machines).injective heq_len
    have hk' : (stageSeq machines j).record.newString = some y := hkj ▸ hk
    exact (stageSeq machines j).record.h_branch_some.mp ⟨y, hk'⟩
  · intro hacc_false
    obtain ⟨w, hw⟩ := (stageSeq machines j).record.h_branch_some.mpr hacc_false
    have hlen_w := (stageSeq machines j).record.h_new_length w hw
    have hw_mem : w ∈ bgsOracle machines := by
      rw [mem_bgsOracle_iff_exists_newString]
      exact ⟨j, hw⟩
    refine ⟨w, hw_mem, ?_⟩
    have hn : stageN machines j = (stageSeq machines j).record.n := rfl
    rw [hn, hlen_w]

/-- **The Diagonalization Flip (Order 8):**
    Input `1^{n_j}` belongs to `unaryWitnessLang (bgsOracle machines)` if and only if
    machine `j`'s canonical stage simulation rejected it (`accepts = false`). -/
theorem bgsOracle_unaryWitnessLang_replicate_iff (machines : ℕ → ClockedOracleTM) (j : ℕ) :
    List.replicate (stageN machines j) true ∈ unaryWitnessLang (bgsOracle machines) ↔
    (stageSeq machines j).record.accepts = false := by
  rw [mem_unaryWitnessLang_replicate_iff]
  exact bgsOracle_witness_iff machines j

theorem trace_of_reachesIn_halted {k : ℕ} (m : OracleTM k) (oracle : BooleanOracle) :
    ∀ (time : ℕ) (start cfg : OracleCfg k m.Q),
      m.reachesIn oracle time start cfg → m.halted cfg →
      ∀ T, time ≤ T → trace m oracle T start = cfg := by
  intro time
  induction time with
  | zero =>
      intro start cfg hreach hhalt T hT
      cases hreach
      induction T with
      | zero => rfl
      | succ T ih =>
          dsimp [trace]
          have hstep : m.step oracle start = none := by
            dsimp [OracleTM.step]
            simp [hhalt]
          rw [hstep]
  | succ time ih =>
      intro start cfg hreach hhalt T hT
      cases hreach with
      | step hstep hrest =>
          cases T with
          | zero => omega
          | succ T =>
              have hle : time ≤ T := Nat.le_of_succ_le_succ hT
              dsimp [trace]
              rw [hstep]
              exact ih _ _ hrest hhalt T hle

/-- **Order 8 Disagreement Theorem:**
    Machine `j` in the sequence cannot decide `unaryWitnessLang (bgsOracle machines)`.
    Its decision on input `1^{n_j}` is inverted by the diagonalization flip. -/
theorem not_decides_stage (machines : ℕ → ClockedOracleTM) (j : ℕ) :
    ¬ (machines j).Decides (oracleOf (bgsOracle machines)) (unaryWitnessLang (bgsOracle machines)) := by
  intro hdec
  dsimp [ClockedOracleTM.Decides, OracleTM.DecidesInTime] at hdec
  set input := List.replicate (stageN machines j) true
  obtain ⟨cfg, time, htime, hreach, hhalt, hyes, hno⟩ := hdec input
  have hlen : input.length = stageN machines j := List.length_replicate
  rw [hlen] at htime
  have htrace_eq := trace_of_reachesIn_halted (machines j).m (oracleOf (bgsOracle machines))
    time ((machines j).m.initCfg input) cfg hreach hhalt
    ((machines j).clock (stageN machines j)) htime
  have hfinal_eq : (stageSeq machines j).record.finalCfg = cfg := by
    rw [← (finalOracle_trace_preserved machines j), htrace_eq]
  have hacc_eq : (stageSeq machines j).record.accepts =
      decide ((machines j).m.halted cfg ∧ cfg.output.cells 1 = Γ.one) := by
    have h := (stageSeq machines j).record.h_accepts
    rw [hfinal_eq] at h
    exact h
  by_cases hacc : (stageSeq machines j).record.accepts = true
  · have hdec_true : decide ((machines j).m.halted cfg ∧ cfg.output.cells 1 = Γ.one) = true := by
      rw [← hacc_eq, hacc]
    rw [decide_eq_true_iff] at hdec_true
    have hcell_one : cfg.output.cells 1 = Γ.one := hdec_true.2
    have hcell_ne_zero : cfg.output.cells 1 ≠ Γ.zero := by
      rw [hcell_one]
      intro h_eq
      cases h_eq
    have hin : input ∈ unaryWitnessLang (bgsOracle machines) := by
      by_contra hnot
      have := hno hnot
      exact hcell_ne_zero this
    have hflip := (bgsOracle_unaryWitnessLang_replicate_iff machines j).mp hin
    rw [hacc] at hflip
    revert hflip
    decide
  · have hacc_false : (stageSeq machines j).record.accepts = false := by
      revert hacc
      cases (stageSeq machines j).record.accepts <;> decide
    have hin : input ∈ unaryWitnessLang (bgsOracle machines) :=
      (bgsOracle_unaryWitnessLang_replicate_iff machines j).mpr hacc_false
    have hcell_one : cfg.output.cells 1 = Γ.one := hyes hin
    have hdec_true : decide ((machines j).m.halted cfg ∧ cfg.output.cells 1 = Γ.one) = true := by
      rw [decide_eq_true_iff]
      exact ⟨hhalt, hcell_one⟩
    have hcontra : (stageSeq machines j).record.accepts = true := by
      rw [hacc_eq, hdec_true]
    rw [hacc_false] at hcontra
    revert hcontra
    decide

/-- Given a complete surjective enumeration of clocked oracle TMs,
    the Baker-Gill-Solovay diagonal oracle `B = bgsOracle enum` satisfies
    `unaryWitnessLang B ∉ PRel B`. -/
theorem bgs_diagonal_not_in_PRel (enum : ℕ → ClockedOracleTM)
    (hsurj : Function.Surjective enum) :
    unaryWitnessLang (bgsOracle enum) ∉ PRel (bgsOracle enum) := by
  intro hP
  rw [PRel_iff_exists_clocked] at hP
  obtain ⟨M, hM⟩ := hP
  obtain ⟨j, rfl⟩ := hsurj M
  exact not_decides_stage enum j hM

/-- **Baker-Gill-Solovay Relativized Separation Theorem (Conditional on Complete Enumeration):**
    For any complete surjective enumeration of clocked oracle TMs,
    `PRel (bgsOracle enum) ≠ NPRel (bgsOracle enum)`. -/
theorem bgs_separation_of_enumeration (enum : ℕ → ClockedOracleTM)
    (hsurj : Function.Surjective enum) :
    PRel (bgsOracle enum) ≠ NPRel (bgsOracle enum) := by
  intro heq
  have hnot := bgs_diagonal_not_in_PRel enum hsurj
  have hin : unaryWitnessLang (bgsOracle enum) ∈ NPRel (bgsOracle enum) :=
    Stage3A.unaryWitnessLang_mem_NPRel (bgsOracle enum)
  rw [← heq] at hin
  exact hnot hin

end Stage3Separation

#check LittleO.nat_mul_le

open Stage3Separation in
#print axioms polyClock_dominates
open Stage3Separation in
#print axioms polyClock_lt_pow_exists
open Stage3Separation in
#print axioms polyClock_bigO
open Stage3Separation in
#print axioms PRel_iff_exists_clocked
open Stage3Separation in
#print axioms PRel_represented
open Stage3Separation in
#print axioms oracleQuerySet_card_le
open Stage3Separation in
#print axioms querySet_card_le_time
open Stage3Separation in
#print axioms exists_unqueried_string
open Stage3Separation in
#print axioms step_congr_of_query_agree
open Stage3Separation in
#print axioms trace_congr_of_querySet_agree
open Stage3Separation in
#print axioms trace_invariant_of_unqueried
open Stage3Separation in
#print axioms protected_query_agreement
open Stage3Separation in
#print axioms stageLength_exists
open Stage3Separation in
#print axioms makeStageRecord
open Stage3Separation in
#print axioms stage_preserves_previous_runs
open Stage3Separation in
#print axioms finalOracle_trace_preserved
open Stage3Separation in
#print axioms finalOracle_accepts_eq
open Stage3Separation in
#print axioms bgsOracle_unaryWitnessLang_replicate_iff
open Stage3Separation in
#print axioms not_decides_stage
open Stage3Separation in
#print axioms bgs_diagonal_not_in_PRel
open Stage3Separation in
#print axioms bgs_separation_of_enumeration

open Stage3Separation in
#print axioms ClockedOracleTM.normalize_decides

open Stage3Separation in
#print axioms PRel_exists_normalized

#print Stage3Separation.polyClock_lt_pow_exists

