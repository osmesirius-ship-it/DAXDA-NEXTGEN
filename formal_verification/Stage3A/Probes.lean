/-
  Stage 3A — Model Probes
  =======================
  Verified proofs for the Baker–Gill–Solovay relativization infrastructure.
  Axiom audit policy: depends strictly on standard Lean foundation axioms
  [propext, Classical.choice, Quot.sound]. ZERO sorry dependencies.
-/
import Complexitylib.Stage3.Defs
import Complexitylib.Models.TuringMachine.Combinators

open Complexity
open scoped Complexity
open Stage3Spec
open Classical

namespace OracleTM

variable {n : ℕ}

theorem reachesIn_zero_iff (machine : OracleTM n) (oracle : BooleanOracle)
    {c c' : OracleCfg n machine.Q} :
    machine.reachesIn oracle 0 c c' ↔ c = c' :=
  ⟨fun h => by cases h; rfl, fun h => h ▸ OracleTM.reachesIn.zero⟩

theorem reachesIn_succ_iff (machine : OracleTM n) (oracle : BooleanOracle)
    {t : ℕ} {c c' : OracleCfg n machine.Q} :
    machine.reachesIn oracle (t + 1) c c' ↔
      ∃ c'', machine.step oracle c = some c'' ∧ machine.reachesIn oracle t c'' c' :=
  ⟨fun h => by cases h with | step hstep hrest => exact ⟨_, hstep, hrest⟩,
   fun ⟨_, hstep, hrest⟩ => OracleTM.reachesIn.step hstep hrest⟩

end OracleTM

namespace Stage3A

variable {n : ℕ} (m : OracleTM n) (oracle : BooleanOracle) (b : Bool) (cfg : OracleCfg n m.Q)

/-- Zero-overhead embedding from deterministic to nondeterministic oracle TM.
The choice bit is ignored in local transitions; query states are choice-independent. -/
def toNTM : OracleNTM n where
  Q := m.Q
  qstart := m.qstart
  qhalt := m.qhalt
  queryTransition := m.queryTransition
  localTransition := fun _ => m.localTransition
  localTransition_right_of_start :=
    fun _ q i qh w o => m.localTransition_right_of_start q i qh w o

theorem toNTM_step (cfg : OracleCfg n m.Q) : (toNTM m).step oracle b cfg = m.step oracle cfg := by
  dsimp [OracleNTM.step, OracleTM.step, toNTM]
  by_cases hhalt : cfg.state = m.qhalt
  · simp [hhalt]
  · simp [hhalt]
    cases hq : m.queryTransition cfg.state <;> rfl

theorem toNTM_trace_of_halted (c : OracleCfg n m.Q) (hh : m.halted c) :
    ∀ (T : ℕ) (choices : Fin T → Bool), (toNTM m).trace oracle T choices c = c := by
  intro T
  induction T with
  | zero => intro _; rfl
  | succ T ih =>
      intro choices
      have hs : (toNTM m).step oracle (choices ⟨0, Nat.zero_lt_succ T⟩) c = none := by
        rw [toNTM_step]
        exact OracleTM.step_eq_none_iff_halted.2 hh
      simp only [OracleNTM.trace, hs]
      rfl

theorem toNTM_trace_of_reachesIn (time : ℕ) :
    ∀ {cfg res : OracleCfg n m.Q},
    m.reachesIn oracle time cfg res → m.halted res →
    ∀ (T : ℕ), time ≤ T → ∀ choices : Fin T → Bool,
      (toNTM m).trace oracle T choices cfg = res := by
  induction time with
  | zero =>
      intro cfg res hr hh T hT choices
      have heq : cfg = res := (OracleTM.reachesIn_zero_iff m oracle).1 hr
      rw [heq]
      exact toNTM_trace_of_halted m oracle res hh T choices
  | succ t ih =>
      intro cfg res hr hh T hT choices
      obtain ⟨middle, hstep, hreach⟩ := (OracleTM.reachesIn_succ_iff m oracle).1 hr
      cases T with
      | zero => omega
      | succ T =>
          have hstepNTM : (toNTM m).step oracle (choices ⟨0, Nat.zero_lt_succ T⟩) cfg = some middle := by
            rw [toNTM_step, hstep]
          simp only [OracleNTM.trace, hstepNTM]
          exact ih hreach hh T (by omega) _

theorem toNTM_initCfg (x : List Bool) : (toNTM m).initCfg x = m.initCfg x := rfl

/-- Probe 3: `P^A ⊆ NP^A` for every oracle A. -/
theorem PRel_subset_NPRel (A : Language) : PRel A ⊆ NPRel A := by
  rintro L ⟨k, d, m, f, hdec, hO⟩
  refine ⟨k, d, toNTM m, f, ⟨?_, ?_⟩, hO⟩
  · intro x choices
    obtain ⟨cfg, t, ht, hr, hh, -, -⟩ := hdec x
    have htrace := toNTM_trace_of_reachesIn m (oracleOf A) t hr hh (f x.length) ht choices
    rw [toNTM_initCfg]
    exact htrace.symm ▸ hh
  · intro x
    obtain ⟨cfg, t, ht, hr, hh, hin, hout⟩ := hdec x
    constructor
    · intro hx
      refine ⟨fun _ => false, ?_⟩
      have htrace := toNTM_trace_of_reachesIn m (oracleOf A) t hr hh (f x.length) ht (fun _ => false)
      rw [toNTM_initCfg]
      exact htrace.symm ▸ ⟨hh, hin hx⟩
    · rintro ⟨choices, hh', hacc⟩
      by_contra hx
      have htrace := toNTM_trace_of_reachesIn m (oracleOf A) t hr hh (f x.length) ht choices
      have := hout hx
      rw [toNTM_initCfg] at hacc
      rw [htrace] at hacc
      rw [this] at hacc
      exact absurd hacc (by decide)

/-- Probe 1a: `P ⊆ P^A` for every oracle A (generalizes P ⊆ P^∅). -/
theorem P_subset_PRel (A : Language) : P ⊆ PRel A := by
  intro L hL
  simp only [P, Set.mem_iUnion] at hL
  obtain ⟨d, k, tm, f, hdec, hO⟩ := hL
  exact ⟨k, d, tm.toOracleTM, f,
    (TM.toOracleTM_decidesInTime_iff tm (oracleOf A) L f).2 hdec, hO⟩

/-! ## Stage 02 — Probe 2a: Embedding ordinary NTM into oracle model (`NP ⊆ NP^A`) -/

/-- Embedding from ordinary NTM to OracleNTM with an inert query tape. -/
@[reducible] def toOracleNTM (machine : NTM n) : OracleNTM n where
  Q := machine.Q
  qstart := machine.qstart
  qhalt := machine.qhalt
  queryTransition := fun _ => none
  localTransition := fun b q inputHead queryHead workHeads outputHead =>
    let (nextState, workWrites, outputWrite, inputDir, workDirs, outputDir) :=
      machine.δ b q inputHead workHeads outputHead
    { nextState
      queryWrite := Γw.blank
      workWrites
      outputWrite
      inputDir
      queryDir := if queryHead = Γ.start then Dir3.right else Dir3.stay
      workDirs
      outputDir }
  localTransition_right_of_start := by
    intro b q inputHead queryHead workHeads outputHead
    have hmachine := machine.δ_right_of_start b q inputHead workHeads outputHead
    dsimp only
    generalize htransition : machine.δ b q inputHead workHeads outputHead = transition at hmachine
    obtain ⟨nextState, workWrites, outputWrite, inputDir, workDirs, outputDir⟩ := transition
    simp only [htransition] at hmachine ⊢
    refine ⟨hmachine.1, ?_, hmachine.2.1, hmachine.2.2⟩
    intro hquery
    simp [hquery]

theorem erase_initCfg (machine : NTM n) (x : List Bool) :
    ((toOracleNTM machine).initCfg x).erase = machine.initCfg x := rfl

theorem erase_step (machine : NTM n) (oracle : BooleanOracle) (b : Bool)
    (c : OracleCfg n machine.Q) :
    ((toOracleNTM machine).step oracle b c).map OracleCfg.erase =
      if c.state = machine.qhalt then none
      else
        let (q', workWrites, outWrite, inDir, workDirs, outDir) :=
          machine.δ b c.state c.input.read (fun i => (c.work i).read) c.output.read
        some { state := q'
               input := c.input.move inDir
               work := fun i => (c.work i).writeAndMove (workWrites i) (workDirs i)
               output := c.output.writeAndMove outWrite outDir } := by
  dsimp [OracleNTM.step, toOracleNTM]
  by_cases hhalt : c.state = machine.qhalt
  · simp [hhalt]
  · simp [hhalt]
    rfl

theorem erase_trace (machine : NTM n) (oracle : BooleanOracle) (T : ℕ) :
    ∀ (choices : Fin T → Bool) (c : OracleCfg n machine.Q),
      ((toOracleNTM machine).trace oracle T choices c).erase =
        machine.trace T choices c.erase := by
  induction T with
  | zero => intro _ _; rfl
  | succ T ih =>
      intro choices c
      dsimp only [OracleNTM.trace, NTM.trace]
      by_cases hhalt : c.state = machine.qhalt
      · have hs : (toOracleNTM machine).step oracle (choices ⟨0, Nat.zero_lt_succ T⟩) c = none := by
          dsimp [OracleNTM.step, toOracleNTM]
          simp only [hhalt, ↓reduceIte]
        rw [hs]
        have hhalt' : c.erase.state = machine.qhalt := hhalt
        simp only [hhalt', ↓reduceIte]
      · have hs : ∃ c', (toOracleNTM machine).step oracle (choices ⟨0, Nat.zero_lt_succ T⟩) c = some c' := by
          dsimp [OracleNTM.step, toOracleNTM]
          simp only [hhalt, ↓reduceIte]
          exact ⟨_, rfl⟩
        obtain ⟨c', hc'⟩ := hs
        rw [hc']
        have hhalt' : ¬ c.erase.state = machine.qhalt := hhalt
        simp only [hhalt', ↓reduceIte]
        rw [ih]
        have herase := erase_step machine oracle (choices ⟨0, Nat.zero_lt_succ T⟩) c
        rw [hc'] at herase
        simp only [Option.map_some] at herase
        simp only [hhalt, ↓reduceIte] at herase
        injection herase with herase'
        rw [herase']
        dsimp [OracleCfg.erase]

theorem trace_erase_initCfg (machine : NTM n) (oracle : BooleanOracle) (T : ℕ)
    (choices : Fin T → Bool) (x : List Bool) :
    ((toOracleNTM machine).trace oracle T choices ((toOracleNTM machine).initCfg x)).erase =
      machine.trace T choices (machine.initCfg x) := by
  have h := erase_trace machine oracle T choices ((toOracleNTM machine).initCfg x)
  rwa [erase_initCfg] at h

theorem trace_state_eq_init (machine : NTM n) (oracle : BooleanOracle) (T : ℕ)
    (choices : Fin T → Bool) (x : List Bool) :
    ((toOracleNTM machine).trace oracle T choices ((toOracleNTM machine).initCfg x)).state =
      (machine.trace T choices (machine.initCfg x)).state :=
  congr_arg Cfg.state (trace_erase_initCfg machine oracle T choices x)

theorem trace_output_eq_init (machine : NTM n) (oracle : BooleanOracle) (T : ℕ)
    (choices : Fin T → Bool) (x : List Bool) :
    ((toOracleNTM machine).trace oracle T choices ((toOracleNTM machine).initCfg x)).output =
      (machine.trace T choices (machine.initCfg x)).output :=
  congr_arg Cfg.output (trace_erase_initCfg machine oracle T choices x)

theorem toOracleNTM_allPathsHaltIn_iff (machine : NTM n) (oracle : BooleanOracle) (T : ℕ → ℕ) :
    (toOracleNTM machine).AllPathsHaltIn oracle T ↔ machine.AllPathsHaltIn T := by
  constructor
  · intro h x choices
    have hx := h x choices
    dsimp [OracleNTM.halted] at hx
    dsimp [NTM.halted, Cfg.isHalted]
    rw [← trace_state_eq_init]
    exact hx
  · intro h x choices
    have hx := h x choices
    dsimp [NTM.halted, Cfg.isHalted] at hx
    dsimp [OracleNTM.halted]
    rw [trace_state_eq_init]
    exact hx

theorem toOracleNTM_acceptsInTime_iff (machine : NTM n) (oracle : BooleanOracle)
    (x : List Bool) (T : ℕ) :
    (toOracleNTM machine).AcceptsInTime oracle x T ↔ machine.AcceptsInTime x T := by
  dsimp [OracleNTM.AcceptsInTime, NTM.AcceptsInTime]
  constructor
  · rintro ⟨choices, hhalt, hout⟩
    refine ⟨choices, ?_, ?_⟩
    · dsimp [NTM.halted, Cfg.isHalted]
      rw [← trace_state_eq_init]
      exact hhalt
    · rw [← trace_output_eq_init]
      exact hout
  · rintro ⟨choices, hhalt, hout⟩
    refine ⟨choices, ?_, ?_⟩
    · dsimp [OracleNTM.halted]
      rw [trace_state_eq_init]
      exact hhalt
    · rw [trace_output_eq_init]
      exact hout

theorem toOracleNTM_decidesInTime_iff (machine : NTM n) (oracle : BooleanOracle)
    (L : Language) (T : ℕ → ℕ) :
    (toOracleNTM machine).DecidesInTime oracle L T ↔ machine.DecidesInTime L T := by
  dsimp [OracleNTM.DecidesInTime, NTM.DecidesInTime]
  rw [toOracleNTM_allPathsHaltIn_iff]
  refine and_congr_right (fun _ => forall_congr' (fun x => ?_))
  rw [toOracleNTM_acceptsInTime_iff]

/-- Probe 2a: `NP ⊆ NP^A` for every oracle A (generalizes `NP ⊆ NP^∅`). -/
theorem NP_subset_NPRel (A : Language) : NP ⊆ NPRel A := by
  intro L hL
  simp only [NP, Set.mem_iUnion] at hL
  obtain ⟨d, k, ntm, f, hdec, hO⟩ := hL
  exact ⟨k, d, toOracleNTM ntm, f,
    (toOracleNTM_decidesInTime_iff ntm (oracleOf A) L f).2 hdec, hO⟩

/-! ## Simulator Infrastructure — Query Tape Preservation (Prerequisite Correction) -/

/-- Pack an OracleCfg into an ordinary Cfg with (n + 1) work tapes.
    Work tape 0 is the dedicated query tape; work tapes 1..n are original work tapes. -/
def packCfg {Q : Type} (c : OracleCfg n Q) : Cfg (n + 1) Q where
  state := c.state
  input := c.input
  work := Fin.cons c.query c.work
  output := c.output

/-- Unpack an ordinary Cfg with (n + 1) work tapes into an OracleCfg. -/
def unpackCfg {Q : Type} (c : Cfg (n + 1) Q) : OracleCfg n Q where
  state := c.state
  input := c.input
  query := c.work 0
  work := fun i => c.work i.succ
  output := c.output

@[simp] theorem unpack_pack {Q : Type} (c : OracleCfg n Q) : unpackCfg (packCfg c) = c := by
  cases c; rfl

@[ext] theorem OracleCfg_ext {n : ℕ} {Q : Type} (c1 c2 : OracleCfg n Q)
    (hs : c1.state = c2.state)
    (hinp : c1.input = c2.input)
    (hq : c1.query = c2.query)
    (hw : c1.work = c2.work)
    (hout : c1.output = c2.output) : c1 = c2 := by
  cases c1; cases c2; cases hs; cases hinp; cases hq; cases hw; cases hout; rfl

/-- Ordinary deterministic simulator with (n + 1) work tapes for OracleTM n.
    Work tape 0 preserves the query tape. Oracle queries route deterministically to noState. -/
@[reducible] def oracleTMToTM (m : OracleTM n) : TM (n + 1) where
  Q := m.Q
  qstart := m.qstart
  qhalt := m.qhalt
  δ := fun q iHead wHeads oHead =>
    match m.queryTransition q with
    | some (_, noState) =>
        (noState,
         fun i => TM.readBackWrite (wHeads i),
         TM.readBackWrite oHead,
         TM.idleDir iHead,
         fun i => TM.idleDir (wHeads i),
         TM.idleDir oHead)
    | none =>
        let t := m.localTransition q iHead (wHeads 0) (fun i => wHeads i.succ) oHead
        (t.nextState,
         Fin.cons t.queryWrite t.workWrites,
         t.outputWrite,
         t.inputDir,
         Fin.cons t.queryDir t.workDirs,
         t.outputDir)
  δ_right_of_start := by
    intro q iHead wHeads oHead
    dsimp only
    cases hq : m.queryTransition q with
    | some states =>
        obtain ⟨yesState, noState⟩ := states
        dsimp only
        exact TM.rightOfStart_allReadBack iHead wHeads oHead
    | none =>
        dsimp only
        have htm := m.localTransition_right_of_start q iHead (wHeads 0) (fun i => wHeads i.succ) oHead
        dsimp only at htm
        generalize ht : m.localTransition q iHead (wHeads 0) (fun i => wHeads i.succ) oHead = t at htm
        obtain ⟨nextState, qWrite, wWrites, oWrite, inDir, qDir, wDirs, oDir⟩ := t
        refine ⟨htm.1, ?_, htm.2.2.2⟩
        intro i hi
        cases i using Fin.cases with
        | zero =>
            simp only [Fin.cons_zero] at hi ⊢
            exact htm.2.1 hi
        | succ j =>
            simp only [Fin.cons_succ] at hi ⊢
            exact htm.2.2.1 j hi

theorem oracleTMToTM_step_local (c : OracleCfg n m.Q)
    (hhalt : c.state ≠ m.qhalt) (hq : m.queryTransition c.state = none) :
    (oracleTMToTM m).step (packCfg c) = (m.step (oracleOf ∅) c).map packCfg := by
  have hq0 : ((Fin.cons c.query c.work : Fin (n + 1) → Tape) 0).read = c.query.read := rfl
  have hqs : (fun i => ((Fin.cons c.query c.work : Fin (n + 1) → Tape) i.succ).read) = fun i => (c.work i).read := rfl
  dsimp [oracleTMToTM, packCfg, TM.step, OracleTM.step]
  simp only [hhalt, ↓reduceIte]
  rw [hq]
  dsimp [packCfg]
  rw [hq0, hqs]
  congr 1
  refine Cfg.ext rfl rfl ?_ rfl
  funext i
  cases i using Fin.cases with
  | zero => rfl
  | succ j => rfl

theorem oracleTMToTM_step_query (c : OracleCfg n m.Q)
    (hhalt : c.state ≠ m.qhalt) (yesState noState : m.Q)
    (hq : m.queryTransition c.state = some (yesState, noState))
    (hinp : c.input.read ≠ Γ.start)
    (hquery : c.query.read ≠ Γ.start)
    (hwork : ∀ i, (c.work i).read ≠ Γ.start)
    (hout : c.output.read ≠ Γ.start) :
    (oracleTMToTM m).step (packCfg c) = (m.step (oracleOf ∅) c).map packCfg := by
  have hw0 : ((Fin.cons c.query c.work : Fin (n + 1) → Tape) 0).read ≠ Γ.start := hquery
  have hws : ∀ i : Fin n, ((Fin.cons c.query c.work : Fin (n + 1) → Tape) (Fin.succ i)).read ≠ Γ.start := hwork
  have hwall : ∀ i : Fin (n + 1), ((Fin.cons c.query c.work : Fin (n + 1) → Tape) i).read ≠ Γ.start := by
    intro i
    cases i using Fin.cases with
    | zero => exact hw0
    | succ j => exact hws j
  dsimp [oracleTMToTM, packCfg, TM.step, OracleTM.step]
  simp only [hhalt, ↓reduceIte]
  rw [hq]
  dsimp
  have horacle : oracleOf ∅ c.query.oracleQuery = false := by
    dsimp [oracleOf]
    rw [decide_eq_false_iff_not]
    intro h
    cases h
  rw [horacle]
  simp only [Bool.false_eq_true, ↓reduceIte]
  dsimp [packCfg]
  congr 1
  refine Cfg.ext rfl ?_ ?_ ?_
  · exact TM.transitionInput_eq_self hinp
  · funext i
    exact TM.transitionTape_eq_self (hwall i)
  · exact TM.transitionTape_eq_self hout

theorem oracleTMToTM_step_halt (c : OracleCfg n m.Q) (hhalt : c.state = m.qhalt) :
    (oracleTMToTM m).step (packCfg c) = (m.step (oracleOf ∅) c).map packCfg := by
  dsimp [oracleTMToTM, packCfg, TM.step, OracleTM.step]
  simp [hhalt]

theorem oracleTMToTM_step (c : OracleCfg n m.Q)
    (hinp : c.input.read ≠ Γ.start)
    (hquery : c.query.read ≠ Γ.start)
    (hwork : ∀ i, (c.work i).read ≠ Γ.start)
    (hout : c.output.read ≠ Γ.start) :
    (oracleTMToTM m).step (packCfg c) = (m.step (oracleOf ∅) c).map packCfg := by
  by_cases hhalt : c.state = m.qhalt
  · exact oracleTMToTM_step_halt m c hhalt
  · cases hq : m.queryTransition c.state with
    | none => exact oracleTMToTM_step_local m c hhalt hq
    | some states =>
        obtain ⟨yesState, noState⟩ := states
        exact oracleTMToTM_step_query m c hhalt yesState noState hq hinp hquery hwork hout

theorem pack_initCfg (x : List Bool) :
    packCfg (m.initCfg x) = (oracleTMToTM m).initCfg x := by
  refine Cfg.ext rfl rfl ?_ rfl
  funext i
  cases i using Fin.cases with
  | zero => rfl
  | succ j => rfl

/-- Ordinary nondeterministic simulator with (n + 1) work tapes for OracleNTM n.
    Preserves choice branches `b` and maps query tape to work tape 0. -/
@[reducible] def oracleNTMToNTM (m : OracleNTM n) : NTM (n + 1) where
  Q := m.Q
  qstart := m.qstart
  qhalt := m.qhalt
  δ := fun b q iHead wHeads oHead =>
    match m.queryTransition q with
    | some (_, noState) =>
        (noState,
         fun i => TM.readBackWrite (wHeads i),
         TM.readBackWrite oHead,
         TM.idleDir iHead,
         fun i => TM.idleDir (wHeads i),
         TM.idleDir oHead)
    | none =>
        let t := m.localTransition b q iHead (wHeads 0) (fun i => wHeads i.succ) oHead
        (t.nextState,
         Fin.cons t.queryWrite t.workWrites,
         t.outputWrite,
         t.inputDir,
         Fin.cons t.queryDir t.workDirs,
         t.outputDir)
  δ_right_of_start := by
    intro b q iHead wHeads oHead
    dsimp only
    cases hq : m.queryTransition q with
    | some states =>
        obtain ⟨yesState, noState⟩ := states
        dsimp only
        exact TM.rightOfStart_allReadBack iHead wHeads oHead
    | none =>
        dsimp only
        have htm := m.localTransition_right_of_start b q iHead (wHeads 0) (fun i => wHeads i.succ) oHead
        dsimp only at htm
        generalize ht : m.localTransition b q iHead (wHeads 0) (fun i => wHeads i.succ) oHead = t at htm
        obtain ⟨nextState, qWrite, wWrites, oWrite, inDir, qDir, wDirs, oDir⟩ := t
        refine ⟨htm.1, ?_, htm.2.2.2⟩
        intro i hi
        cases i using Fin.cases with
        | zero =>
            simp only [Fin.cons_zero] at hi ⊢
            exact htm.2.1 hi
        | succ j =>
            simp only [Fin.cons_succ] at hi ⊢
            exact htm.2.2.1 j hi

theorem pack_initCfg_ntm (m : OracleNTM n) (x : List Bool) :
    packCfg (m.initCfg x) = (oracleNTMToNTM m).initCfg x := by
  refine Cfg.ext rfl rfl ?_ rfl
  funext i
  cases i using Fin.cases with
  | zero => rfl
  | succ j => rfl

theorem unpack_initCfg_ntm (m : OracleNTM n) (x : List Bool) :
    unpackCfg ((oracleNTMToNTM m).initCfg x) = m.initCfg x := by
  cases x; rfl; rfl

theorem unpack_step_local (m : OracleNTM n) (b : Bool) (c : Cfg (n + 1) m.Q)
    (hhalt : c.state ≠ m.qhalt) (hq : m.queryTransition c.state = none) :
    let (q', workWrites, outWrite, inDir, workDirs, outDir) :=
      (oracleNTMToNTM m).δ b c.state c.input.read (fun i => (c.work i).read) c.output.read
    let c' : Cfg (n + 1) m.Q :=
      { state := q'
        input := c.input.move inDir
        work := fun i => (c.work i).writeAndMove (workWrites i) (workDirs i)
        output := c.output.writeAndMove outWrite outDir }
    some (unpackCfg c') = m.step (oracleOf ∅) b (unpackCfg c) := by
  dsimp [oracleNTMToNTM, unpackCfg, OracleNTM.step]
  simp only [hhalt, ↓reduceIte]
  rw [hq]
  dsimp [unpackCfg]
  congr 1

theorem unpack_step_query (m : OracleNTM n) (b : Bool) (c : Cfg (n + 1) m.Q)
    (hhalt : c.state ≠ m.qhalt) (yesState noState : m.Q)
    (hq : m.queryTransition c.state = some (yesState, noState))
    (hinp : c.input.read ≠ Γ.start)
    (hquery : (c.work 0).read ≠ Γ.start)
    (hwork : ∀ i : Fin n, (c.work i.succ).read ≠ Γ.start)
    (hout : c.output.read ≠ Γ.start) :
    let (q', workWrites, outWrite, inDir, workDirs, outDir) :=
      (oracleNTMToNTM m).δ b c.state c.input.read (fun i => (c.work i).read) c.output.read
    let c' : Cfg (n + 1) m.Q :=
      { state := q'
        input := c.input.move inDir
        work := fun i => (c.work i).writeAndMove (workWrites i) (workDirs i)
        output := c.output.writeAndMove outWrite outDir }
    some (unpackCfg c') = m.step (oracleOf ∅) b (unpackCfg c) := by
  have hwall : ∀ i : Fin (n + 1), (c.work i).read ≠ Γ.start := by
    intro i
    cases i using Fin.cases with
    | zero => exact hquery
    | succ j => exact hwork j
  dsimp [oracleNTMToNTM, unpackCfg, OracleNTM.step]
  simp only [hhalt, ↓reduceIte]
  rw [hq]
  have horacle : oracleOf ∅ (c.work 0).oracleQuery = false := by
    dsimp [oracleOf]
    rw [decide_eq_false_iff_not]
    intro h
    cases h
  rw [horacle]
  dsimp [unpackCfg]
  apply congr_arg some
  apply OracleCfg_ext
  · rfl
  · exact TM.transitionInput_eq_self hinp
  · exact TM.transitionTape_eq_self hquery
  · funext i
    exact TM.transitionTape_eq_self (hwork i)
  · exact TM.transitionTape_eq_self hout

/-- Trace / configuration correspondence for single execution steps under the empty oracle. -/
theorem unpack_step (m : OracleNTM n) (b : Bool) (c : Cfg (n + 1) m.Q)
    (hhalt : c.state ≠ m.qhalt)
    (hinp : c.input.read ≠ Γ.start)
    (hquery : (c.work 0).read ≠ Γ.start)
    (hwork : ∀ i : Fin n, (c.work i.succ).read ≠ Γ.start)
    (hout : c.output.read ≠ Γ.start) :
    let (q', workWrites, outWrite, inDir, workDirs, outDir) :=
      (oracleNTMToNTM m).δ b c.state c.input.read (fun i => (c.work i).read) c.output.read
    let c' : Cfg (n + 1) m.Q :=
      { state := q'
        input := c.input.move inDir
        work := fun i => (c.work i).writeAndMove (workWrites i) (workDirs i)
        output := c.output.writeAndMove outWrite outDir }
    some (unpackCfg c') = m.step (oracleOf ∅) b (unpackCfg c) := by
  cases hq : m.queryTransition c.state with
  | none => exact unpack_step_local m b c hhalt hq
  | some states =>
      obtain ⟨yesState, noState⟩ := states
      exact unpack_step_query m b c hhalt yesState noState hq hinp hquery hwork hout

/-- Trace correspondence for deterministic oracle TM under empty oracle. -/
theorem oracleTMToTM_reachesIn (m : OracleTM n) (t : ℕ)
    (hstep : ∀ {c next : OracleCfg n m.Q}, m.step (oracleOf ∅) c = some next →
      (oracleTMToTM m).step (packCfg c) = some (packCfg next))
    {c c' : OracleCfg n m.Q}
    (hreach : m.reachesIn (oracleOf ∅) t c c') :
    (oracleTMToTM m).reachesIn t (packCfg c) (packCfg c') := by
  exact @OracleTM.reachesIn_map n m (oracleOf ∅) (n + 1) (oracleTMToTM m) packCfg
    (fun {cfg next} h => hstep h) t c c' hreach

/-- Deterministic simulation theorem: when single-step transitions match on reachable
    configurations, the deterministic simulator decides the same language in polynomial time. -/
theorem PRel_empty_subset_P_of_step_sim
    (hstep_sim : ∀ (k : ℕ) (m : OracleTM k) {c next : OracleCfg k m.Q},
      m.step (oracleOf ∅) c = some next → (oracleTMToTM m).step (packCfg c) = some (packCfg next)) :
    PRel ∅ ⊆ P := by
  rintro L ⟨k, d, m, f, hdec, hO⟩
  apply Set.mem_iUnion.mpr
  refine ⟨d, k + 1, oracleTMToTM m, f, ?_, hO⟩
  intro x
  obtain ⟨cfg, t, ht, hreach, hhalt, hyes, hno⟩ := hdec x
  refine ⟨packCfg cfg, t, ht, ?_, hhalt, hyes, hno⟩
  rw [← pack_initCfg]
  exact oracleTMToTM_reachesIn m t (hstep_sim k m) hreach

/-- Nondeterministic trace correspondence: inductive simulation across all choice branches. -/
@[simp] theorem unpack_state {Q : Type} (c : Cfg (n + 1) Q) :
    (unpackCfg c).state = c.state := rfl

@[simp] theorem unpack_output {Q : Type} (c : Cfg (n + 1) Q) :
    (unpackCfg c).output = c.output := rfl

/-- Nondeterministic trace correspondence: inductive simulation across all choice branches. -/
theorem unpack_trace_of_step_sim (m : OracleNTM n) (T : ℕ)
    (hstep_sim : ∀ (b : Bool) (c : Cfg (n + 1) m.Q),
      c.state ≠ m.qhalt →
      let (q', workWrites, outWrite, inDir, workDirs, outDir) :=
        (oracleNTMToNTM m).δ b c.state c.input.read (fun i => (c.work i).read) c.output.read
      let c' : Cfg (n + 1) m.Q :=
        { state := q'
          input := c.input.move inDir
          work := fun i => (c.work i).writeAndMove (workWrites i) (workDirs i)
          output := c.output.writeAndMove outWrite outDir }
      some (unpackCfg c') = m.step (oracleOf ∅) b (unpackCfg c)) :
    ∀ (choices : Fin T → Bool) (c : Cfg (n + 1) m.Q),
      unpackCfg ((oracleNTMToNTM m).trace T choices c) =
        m.trace (oracleOf ∅) T choices (unpackCfg c) := by
  induction T with
  | zero => intro _ _; rfl
  | succ T ih =>
      intro choices c
      dsimp only [NTM.trace, OracleNTM.trace]
      by_cases hhalt : c.state = (oracleNTMToNTM m).qhalt
      · simp only [hhalt, ↓reduceIte]
        have horacle_halt : (unpackCfg c).state = m.qhalt := hhalt
        have horacle_none : m.step (oracleOf ∅) (choices ⟨0, Nat.zero_lt_succ T⟩) (unpackCfg c) = none := by
          unfold OracleNTM.step
          split
          · rfl
          · next hne => exact False.elim (hne horacle_halt)
        rw [horacle_none]
      · simp only [hhalt, ↓reduceIte]
        have hstep_eq := hstep_sim (choices ⟨0, Nat.zero_lt_succ T⟩) c hhalt
        dsimp only at hstep_eq
        rw [← hstep_eq]
        dsimp only
        exact ih (fun i => choices ⟨i.val + 1, by omega⟩) _

/-- Nondeterministic simulation theorem: when step equivalence holds along execution,
    every language decidable in `NP^∅` is decidable in ordinary `NP`. -/
theorem NPRel_empty_subset_NP_of_step_sim
    (hstep_sim : ∀ (k : ℕ) (m : OracleNTM k) (b : Bool) (c : Cfg (k + 1) m.Q),
      c.state ≠ m.qhalt →
      let (q', workWrites, outWrite, inDir, workDirs, outDir) :=
        (oracleNTMToNTM m).δ b c.state c.input.read (fun i => (c.work i).read) c.output.read
      let c' : Cfg (k + 1) m.Q :=
        { state := q'
          input := c.input.move inDir
          work := fun i => (c.work i).writeAndMove (workWrites i) (workDirs i)
          output := c.output.writeAndMove outWrite outDir }
      some (unpackCfg c') = m.step (oracleOf ∅) b (unpackCfg c)) :
    NPRel ∅ ⊆ NP := by
  rintro L ⟨k, d, m, f, ⟨hhalts, hacc⟩, hO⟩
  apply Set.mem_iUnion.mpr
  refine ⟨d, k + 1, oracleNTMToNTM m, f, ⟨?_, ?_⟩, hO⟩
  · intro x choices
    have htrace := unpack_trace_of_step_sim m (f x.length) (hstep_sim k m) choices ((oracleNTMToNTM m).initCfg x)
    rw [unpack_initCfg_ntm] at htrace
    have hpath := hhalts x choices
    dsimp [OracleNTM.halted] at hpath
    dsimp [NTM.halted, Cfg.isHalted]
    have hstate : ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x)).state =
      (m.trace (oracleOf ∅) (f x.length) choices (m.initCfg x)).state := by
      calc ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x)).state
        _ = (unpackCfg ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x))).state := rfl
        _ = (m.trace (oracleOf ∅) (f x.length) choices (m.initCfg x)).state := by rw [htrace]
    rw [hstate]
    exact hpath
  · intro x
    constructor
    · intro hx
      obtain ⟨choices, hh, hout⟩ := (hacc x).1 hx
      refine ⟨choices, ?_, ?_⟩
      · have htrace := unpack_trace_of_step_sim m (f x.length) (hstep_sim k m) choices ((oracleNTMToNTM m).initCfg x)
        rw [unpack_initCfg_ntm] at htrace
        dsimp [NTM.halted, Cfg.isHalted]
        have hstate : ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x)).state =
          (m.trace (oracleOf ∅) (f x.length) choices (m.initCfg x)).state := by
          calc ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x)).state
            _ = (unpackCfg ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x))).state := rfl
            _ = (m.trace (oracleOf ∅) (f x.length) choices (m.initCfg x)).state := by rw [htrace]
        rw [hstate]
        exact hh
      · have htrace := unpack_trace_of_step_sim m (f x.length) (hstep_sim k m) choices ((oracleNTMToNTM m).initCfg x)
        rw [unpack_initCfg_ntm] at htrace
        have houtput : ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x)).output =
          (m.trace (oracleOf ∅) (f x.length) choices (m.initCfg x)).output := by
          calc ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x)).output
            _ = (unpackCfg ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x))).output := rfl
            _ = (m.trace (oracleOf ∅) (f x.length) choices (m.initCfg x)).output := by rw [htrace]
        rw [houtput]
        exact hout
    · rintro ⟨choices, hh, hout⟩
      apply (hacc x).2
      refine ⟨choices, ?_, ?_⟩
      · have htrace := unpack_trace_of_step_sim m (f x.length) (hstep_sim k m) choices ((oracleNTMToNTM m).initCfg x)
        rw [unpack_initCfg_ntm] at htrace
        dsimp [OracleNTM.halted]
        have hstate : ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x)).state =
          (m.trace (oracleOf ∅) (f x.length) choices (m.initCfg x)).state := by
          calc ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x)).state
            _ = (unpackCfg ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x))).state := rfl
            _ = (m.trace (oracleOf ∅) (f x.length) choices (m.initCfg x)).state := by rw [htrace]
        rw [← hstate]
        exact hh
      · have htrace := unpack_trace_of_step_sim m (f x.length) (hstep_sim k m) choices ((oracleNTMToNTM m).initCfg x)
        rw [unpack_initCfg_ntm] at htrace
        have houtput : ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x)).output =
          (m.trace (oracleOf ∅) (f x.length) choices (m.initCfg x)).output := by
          calc ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x)).output
            _ = (unpackCfg ((oracleNTMToNTM m).trace (f x.length) choices ((oracleNTMToNTM m).initCfg x))).output := rfl
            _ = (m.trace (oracleOf ∅) (f x.length) choices (m.initCfg x)).output := by rw [htrace]
        rw [← houtput]
        exact hout

/-- Assembly: `NP^∅ = NP` derived from verified inclusions `NP ⊆ NP^∅` and `NP^∅ ⊆ NP`. -/
theorem NPRel_empty_eq_NP_of_step_sim
    (hstep_sim : ∀ (k : ℕ) (m : OracleNTM k) (b : Bool) (c : Cfg (k + 1) m.Q),
      c.state ≠ m.qhalt →
      let (q', workWrites, outWrite, inDir, workDirs, outDir) :=
        (oracleNTMToNTM m).δ b c.state c.input.read (fun i => (c.work i).read) c.output.read
      let c' : Cfg (k + 1) m.Q :=
        { state := q'
          input := c.input.move inDir
          work := fun i => (c.work i).writeAndMove (workWrites i) (workDirs i)
          output := c.output.writeAndMove outWrite outDir }
      some (unpackCfg c') = m.step (oracleOf ∅) b (unpackCfg c)) :
    NPRel ∅ = NP :=
  Set.Subset.antisymm (NPRel_empty_subset_NP_of_step_sim hstep_sim) (NP_subset_NPRel ∅)


/-! ## 5. Probe 4: Relativized NP Witness Language (unaryWitnessLang B ∈ NPRel B) -/

abbrev QW := Fin 6
def qw_start : QW := 0
def qw_scan : QW := 1
def qw_query : QW := 2
def qw_accept : QW := 3
def qw_reject : QW := 4
def qw_halt : QW := 5

def witnessNTM : OracleNTM 0 where
  Q := QW
  qstart := qw_start
  qhalt := qw_halt
  queryTransition := fun q =>
    if q = qw_query then some (qw_accept, qw_reject)
    else none
  localTransition := fun b q iHead qHead wHeads oHead =>
    let (nextState, qWrite, oWrite, rawInDir, rawQDir, rawOutDir) :=
      if q = qw_start then
        (qw_scan, Γw.blank, Γw.blank, Dir3.right, Dir3.right, Dir3.right)
      else if q = qw_scan then
        match iHead with
        | Γ.one =>
            (qw_scan, if b then Γw.one else Γw.zero, Γw.blank, Dir3.right, Dir3.right, Dir3.stay)
        | Γ.blank =>
            (qw_query, Γw.blank, Γw.blank, Dir3.stay, Dir3.stay, Dir3.stay)
        | _ =>
            (qw_reject, Γw.blank, Γw.blank, Dir3.stay, Dir3.stay, Dir3.stay)
      else if q = qw_accept then
        (qw_halt, Γw.blank, Γw.one, Dir3.stay, Dir3.stay, Dir3.stay)
      else if q = qw_reject then
        (qw_halt, Γw.blank, Γw.zero, Dir3.stay, Dir3.stay, Dir3.stay)
      else
        (qw_halt, Γw.blank, Γw.blank, Dir3.stay, Dir3.stay, Dir3.stay)
    { nextState
      queryWrite := qWrite
      workWrites := fun i => Fin.elim0 i
      outputWrite := oWrite
      inputDir := if iHead = Γ.start then Dir3.right else rawInDir
      queryDir := if qHead = Γ.start then Dir3.right else rawQDir
      workDirs := fun i => Fin.elim0 i
      outputDir := if oHead = Γ.start then Dir3.right else rawOutDir }
  localTransition_right_of_start := by
    intro b q iHead qHead wHeads oHead
    dsimp only
    refine ⟨?_, ?_, fun i => Fin.elim0 i, ?_⟩
    · intro hi; simp [hi]
    · intro hq; simp [hq]
    · intro ho; simp [ho]

theorem witnessNTM_time_bigO : (fun n => n + 4) =O (· ^ 1) := by
  have hn : (fun n : ℕ => n) =O (· ^ 1) := by
    simpa [pow_one] using BigO.refl (fun n : ℕ => n)
  exact BigO.add hn (BigO.const_le_pow 4 1)

theorem first_false_or_all_ones (x : List Bool) :
    (∀ b ∈ x, b = true) ∨
    (∃ (k : ℕ) (hk : k < x.length), (∀ (j : ℕ) (hj : j < k), x[j] = true) ∧ x[k] = false) := by
  induction x with
  | nil =>
    left
    intro b hb
    cases hb
  | cons a xs ih =>
    cases ha : a with
    | false =>
      right
      refine ⟨0, by simp, fun j hj => by omega, by simp [ha]⟩
    | true =>
      cases ih with
      | inl h_all =>
        left
        intro b hb
        simp only [List.mem_cons] at hb
        rcases hb with rfl | hb'
        · rfl
        · exact h_all b hb'
      | inr h_ex =>
        right
        obtain ⟨k, hk, hprev, hfalse⟩ := h_ex
        refine ⟨k + 1, by simp [hk], ?_, ?_⟩
        · intro j hj
          cases j with
          | zero => rfl
          | succ j' =>
            have hj' : j' < k := by omega
            exact hprev j' hj'
        · exact hfalse

@[simp] theorem trace_of_halted {n : ℕ} (m : OracleNTM n) (oracle : BooleanOracle) :
    ∀ (T : ℕ) (choices : Fin T → Bool) (c : OracleCfg n m.Q),
      m.halted c → m.trace oracle T choices c = c
  | 0, _, c, _ => rfl
  | T + 1, choices, c, h => by
    have hstep : m.step oracle (choices ⟨0, Nat.zero_lt_succ T⟩) c = none := by
      simp [OracleNTM.step, h]
    unfold OracleNTM.trace
    cases hmatch : m.step oracle (choices ⟨0, Nat.zero_lt_succ T⟩) c with
    | none => rfl
    | some c' => rw [hstep] at hmatch; contradiction

theorem trace_succ_of_step {n : ℕ} (m : OracleNTM n) (oracle : BooleanOracle)
    (T : ℕ) (choices : Fin (T + 1) → Bool) (c c' : OracleCfg n m.Q)
    (hstep : m.step oracle (choices ⟨0, Nat.zero_lt_succ T⟩) c = some c') :
    m.trace oracle (T + 1) choices c =
      m.trace oracle T (fun i => choices ⟨i.val + 1, by omega⟩) c' := by
  conv_lhs => unfold OracleNTM.trace
  rw [hstep]

def c1 (x : List Bool) : OracleCfg 0 QW where
  state := qw_scan
  input := (Tape.init (x.map Γ.ofBool)).move Dir3.right
  query := (Tape.init []).move Dir3.right
  work := fun _ => Tape.init []
  output := (Tape.init []).move Dir3.right

def queryTapeScan (k : ℕ) (c : Fin k → Bool) : Tape where
  head := k + 1
  cells := fun i =>
    if i = 0 then Γ.start
    else if h : i - 1 < k then Γ.ofBool (c ⟨i - 1, h⟩)
    else Γ.blank

def scanCfg (x : List Bool) (k : ℕ) (c : Fin k → Bool) : OracleCfg 0 QW where
  state := qw_scan
  input := { head := k + 1, cells := (Tape.init (x.map Γ.ofBool)).cells }
  query := queryTapeScan k c
  work := fun _ => Tape.init []
  output := (Tape.init []).move Dir3.right

theorem c1_eq_scanCfg_zero (x : List Bool) :
    c1 x = scanCfg x 0 (fun i => Fin.elim0 i) := by
  ext <;> rfl

theorem step_init (B : Language) (x : List Bool) (b : Bool) :
    witnessNTM.step (oracleOf B) b (witnessNTM.initCfg x) = some (c1 x) := by
  dsimp [OracleNTM.step, witnessNTM, OracleNTM.initCfg, OracleCfg.init, Tape.read, qw_start, qw_scan, qw_halt, qw_query]
  dsimp [Tape.write, Tape.move, Tape.init, c1]
  congr 1
  ext
  · rfl
  · rfl
  · rfl
  · rfl
  · rfl
  · exact Fin.elim0 ‹Fin 0›
  · exact Fin.elim0 ‹Fin 0›
  · rfl
  · rfl

theorem write_cells_of_ne_zero {t : Tape} {s : Γ} (h : t.head ≠ 0) :
    (t.write s).cells = Function.update t.cells t.head s := by
  simp [Tape.write, h]

def snoc (k : ℕ) (c : Fin k → Bool) (b : Bool) : Fin (k + 1) → Bool :=
  fun ⟨i, _hi⟩ =>
    if h : i < k then c ⟨i, h⟩
    else b

theorem snoc_eq_of_prefix {y : List Bool} (k : ℕ) (hk : k < y.length) :
    snoc k (fun ⟨i, _hi⟩ => y[i]'(by omega)) (y[k]'hk) =
      (fun ⟨i, _hi⟩ => y[i]'(by omega)) := by
  ext ⟨i, hi⟩
  dsimp [snoc]
  split_ifs with h
  · rfl
  · have : i = k := by omega
    subst this
    rfl

theorem queryTapeScan_step (k : ℕ) (c : Fin k → Bool) (b : Bool) :
    (queryTapeScan k c).writeAndMove (if b then Γw.one else Γw.zero).toΓ Dir3.right =
      queryTapeScan (k + 1) (snoc k c b) := by
  have hhead : (queryTapeScan k c).head = k + 1 := rfl
  have hne : (queryTapeScan k c).head ≠ 0 := by rw [hhead]; omega
  ext
  · simp only [Tape.writeAndMove, Tape.move, Tape.write_head, hhead]
    rfl
  · next i =>
    simp only [Tape.writeAndMove, Tape.move_cells, write_cells_of_ne_zero hne, hhead, Function.update]
    dsimp only [queryTapeScan, snoc, Γw.toΓ]
    by_cases h0 : i = 0
    · subst h0; simp
    · by_cases hk : i = k + 1
      · subst hk
        simp only [if_neg h0, if_pos rfl]
        have hlt : k + 1 - 1 < k + 1 := by omega
        simp only [dif_pos hlt]
        have hnot : ¬ (k + 1 - 1 < k) := by omega
        simp only [dif_neg hnot]
        cases b <;> rfl
      · by_cases hlt : i - 1 < k
        · have hlt' : i - 1 < k + 1 := by omega
          simp only [dif_pos hlt, dif_pos hlt']
          rw [dif_neg hk]
        · have hnot : ¬ (i - 1 < k + 1) := by omega
          simp only [dif_neg hlt, dif_neg hnot]
          rw [dif_neg hk]

theorem oracleQuery_queryTapeScan (k : ℕ) (c : Fin k → Bool) :
    (queryTapeScan k c).oracleQuery = List.ofFn c := by
  dsimp only [Tape.oracleQuery, queryTapeScan]
  apply List.ext_getElem
  · simp
  · intro i h1 h2
    simp only [List.getElem_ofFn]
    have hi0 : i + 1 ≠ 0 := by omega
    have hlt : i < k := by
      have : i < (List.ofFn c).length := h2
      simpa using this
    have hlt' : i + 1 - 1 < k := by omega
    simp only [hi0, ite_false]
    rw [dif_pos hlt']
    cases hc : c ⟨i, hlt⟩
    · simp [Γ.ofBool, hc]
    · simp [Γ.ofBool, hc]

theorem output_tape_blank_step :
    (((Tape.init ([] : List Γ)).move Dir3.right).writeAndMove Γ.blank Dir3.stay).cells =
      ((Tape.init ([] : List Γ)).move Dir3.right).cells := by
  ext i
  simp only [Tape.writeAndMove, Tape.move, Tape.write, Tape.init]
  have hne : 0 + 1 ≠ 0 := by omega
  simp only [hne, ite_false, Function.update]
  by_cases hi : i = 0 + 1
  · subst hi
    simp
  · simp [hi]

theorem step_scan_one (B : Language) (x : List Bool) (k : ℕ) (c : Fin k → Bool) (b : Bool)
    (hk : (Tape.init (x.map Γ.ofBool)).cells (k + 1) = Γ.one) :
    witnessNTM.step (oracleOf B) b (scanCfg x k c) = some (scanCfg x (k + 1) (snoc k c b)) := by
  have hq_head : (queryTapeScan k c).head = k + 1 := rfl
  have ho_head : ((Tape.init ([] : List Γ)).move Dir3.right).head = 1 := rfl
  have hq_read : (queryTapeScan k c).cells (queryTapeScan k c).head = Γ.blank := by
    rw [hq_head]
    dsimp [queryTapeScan]
    have hnot0 : k + 1 ≠ 0 := by omega
    have hnotlt : ¬ (k + 1 - 1 < k) := by omega
    simp [hnot0, hnotlt]
  have ho_read : ((Tape.init ([] : List Γ)).move Dir3.right).cells
      ((Tape.init ([] : List Γ)).move Dir3.right).head = Γ.blank := by
    rw [ho_head]
    dsimp [Tape.move, Tape.init]
  have hq_step : (queryTapeScan k c).writeAndMove
      (match if b = true then Γw.one else Γw.zero with
      | Γw.zero => Γ.zero | Γw.one => Γ.one | Γw.blank => Γ.blank) Dir3.right =
      queryTapeScan (k + 1) (snoc k c b) := by
    cases b
    · exact queryTapeScan_step k c false
    · exact queryTapeScan_step k c true
  dsimp [OracleNTM.step, witnessNTM, scanCfg, Tape.read, qw_scan, qw_halt, qw_query, qw_start, qw_accept, qw_reject]
  rw [hk, hq_read, ho_read]
  dsimp
  congr 1
  ext
  · rfl
  · rfl
  · rfl
  · exact congr_arg Tape.head hq_step
  · exact congr_fun (congr_arg Tape.cells hq_step) _
  · exact Fin.elim0 ‹Fin 0›
  · exact Fin.elim0 ‹Fin 0›
  · rfl
  · exact congr_fun output_tape_blank_step _

theorem init_cells_length_add_one (contents : List Γ) :
    (Tape.init contents).cells (contents.length + 1) = Γ.blank := by
  dsimp [Tape.init]
  have hne : contents.length + 1 ≠ 0 := by omega
  have hget : contents[contents.length]? = none := List.getElem?_eq_none (by omega)
  simp [hne, hget]

theorem unary_init_cell (x : List Bool) (k : ℕ) (hk : k < x.length) (hx : x[k] = true) :
    (Tape.init (x.map Γ.ofBool)).cells (k + 1) = Γ.one := by
  dsimp [Tape.init]
  have hk_map : k < (x.map Γ.ofBool).length := by simpa using hk
  have hmap : (x.map Γ.ofBool)[k]'hk_map = Γ.one := by
    simp [hx, Γ.ofBool]
  have hget : (x.map Γ.ofBool)[k]? = some Γ.one := by
    rw [List.getElem?_eq_getElem hk_map, hmap]
  rw [hget]
  rfl

theorem zero_init_cell (x : List Bool) (k : ℕ) (hk : k < x.length) (hx : x[k] = false) :
    (Tape.init (x.map Γ.ofBool)).cells (k + 1) = Γ.zero := by
  dsimp [Tape.init]
  have hk_map : k < (x.map Γ.ofBool).length := by simpa using hk
  have hmap : (x.map Γ.ofBool)[k]'hk_map = Γ.zero := by
    simp [hx, Γ.ofBool]
  have hget : (x.map Γ.ofBool)[k]? = some Γ.zero := by
    rw [List.getElem?_eq_getElem hk_map, hmap]
  rw [hget]
  rfl

theorem trace_succ_add_one {n : ℕ} (m : OracleNTM n) (oracle : BooleanOracle)
    (T_rem m_step : ℕ) (choices : Fin (T_rem + (m_step + 1)) → Bool) (c c' : OracleCfg n m.Q)
    (hstep : m.step oracle (choices ⟨0, Nat.zero_lt_succ (T_rem + m_step)⟩) c = some c') :
    m.trace oracle (T_rem + (m_step + 1)) choices c =
      m.trace oracle (T_rem + m_step) (fun i => choices ⟨i.val + 1, by omega⟩) c' :=
  trace_succ_of_step m oracle (T_rem + m_step) choices c c' hstep

theorem scanCfg_congr {x y : List Bool} {a b : ℕ} (ha : a ≤ y.length) (h : a = b) :
    (scanCfg x a fun ⟨i, _hi⟩ => y[i]'(by omega)) =
    (scanCfg x b fun ⟨i, _hi⟩ => y[i]'(by omega)) := by
  subst h
  rfl

theorem trace_scan_steps_prefix (B : Language) (x : List Bool)
    (y : List Bool) (hylen : y.length = x.length) :
    ∀ (m : ℕ) (k : ℕ) (hkm : k + m ≤ x.length)
      (hx : ∀ (j : ℕ) (hj : j < k + m), x[j] = true) (T_rem : ℕ)
      (choices : Fin (T_rem + m) → Bool)
      (hch : ∀ (i : ℕ) (hi : i < m), choices ⟨i, by omega⟩ = y[k + i]'(by omega)),
      witnessNTM.trace (oracleOf B) (T_rem + m) choices
        (scanCfg x k (fun ⟨i, _hi⟩ => y[i]'(by omega))) =
      witnessNTM.trace (oracleOf B) T_rem (fun i => choices ⟨i.val + m, by omega⟩)
        (scanCfg x (k + m) (fun ⟨i, _hi⟩ => y[i]'(by omega)))
  | 0, k, _hkm, _hx, T_rem, choices, _hch => by
    have hchoices : (fun i : Fin T_rem => choices ⟨i.val + 0, by omega⟩) = choices := by
      ext ⟨i, hi⟩
      rfl
    exact congr_arg (fun ch => witnessNTM.trace (oracleOf B) T_rem ch (scanCfg x k (fun ⟨i, _hi⟩ => y[i]'(by omega)))) hchoices.symm
  | m + 1, k, hkm, hx, T_rem, choices, hch => by
    have hk_lt : k < x.length := by omega
    have hxk : x[k] = true := hx k (by omega)
    have hcell : (Tape.init (x.map Γ.ofBool)).cells (k + 1) = Γ.one :=
      unary_init_cell x k hk_lt hxk
    have hch0 : choices ⟨0, Nat.zero_lt_succ (T_rem + m)⟩ = y[k]'(by omega) := by
      have h := hch 0 (Nat.zero_lt_succ m)
      simpa using h
    have hstep0 : witnessNTM.step (oracleOf B) (choices ⟨0, Nat.zero_lt_succ (T_rem + m)⟩)
        (scanCfg x k (fun ⟨i, _hi⟩ => y[i]'(by omega))) =
        some (scanCfg x (k + 1) (fun ⟨i, _hi⟩ => y[i]'(by omega))) := by
      rw [hch0]
      have hs := step_scan_one B x k (fun ⟨i, _hi⟩ => y[i]'(by omega)) (y[k]'(by omega)) hcell
      have hsnoc : snoc k (fun ⟨i, _hi⟩ => y[i]'(by omega)) (y[k]'(by omega)) =
          (fun ⟨i, _hi⟩ => y[i]'(by omega)) :=
        snoc_eq_of_prefix k (by omega)
      rw [hsnoc] at hs
      exact hs
    have htrace1 := trace_succ_add_one witnessNTM (oracleOf B) T_rem m choices
      (scanCfg x k (fun ⟨i, _hi⟩ => y[i]'(by omega)))
      (scanCfg x (k + 1) (fun ⟨i, _hi⟩ => y[i]'(by omega))) hstep0
    rw [htrace1]
    have hih := trace_scan_steps_prefix B x y hylen m (k + 1) (by omega)
      (fun j hj => hx j (by omega)) T_rem
      (fun i => choices ⟨i.val + 1, by omega⟩)
      (fun i hi => by
        have h := hch (i + 1) (by omega)
        have h_get : y[k + 1 + i]'(by omega) = y[k + (i + 1)]'(by omega) :=
          congr_arg (y.get) (Fin.ext (by dsimp; omega))
        rw [h_get]
        exact h)
    rw [hih]
    have h_ch : (fun i : Fin T_rem => choices ⟨(i.val + m) + 1, by omega⟩) =
        (fun i => choices ⟨i.val + (m + 1), by omega⟩) := by
      ext ⟨i, hi⟩
      exact congr_arg choices (Fin.ext (by dsimp; omega))
    rw [h_ch]
    have h_cfg := scanCfg_congr (x := x) (y := y) (by omega) (by omega : k + 1 + m = k + (m + 1))
    rw [h_cfg]

theorem trace_scan_steps (B : Language) (x : List Bool) (hx : ∀ b ∈ x, b = true)
    (y : List Bool) (hylen : y.length = x.length)
    (m : ℕ) (k : ℕ) (hkm : k + m ≤ x.length) (T_rem : ℕ)
    (choices : Fin (T_rem + m) → Bool)
    (hch : ∀ (i : ℕ) (hi : i < m), choices ⟨i, by omega⟩ = y[k + i]'(by omega)) :
    witnessNTM.trace (oracleOf B) (T_rem + m) choices
      (scanCfg x k (fun ⟨i, _hi⟩ => y[i]'(by omega))) =
    witnessNTM.trace (oracleOf B) T_rem (fun i => choices ⟨i.val + m, by omega⟩)
      (scanCfg x (k + m) (fun ⟨i, _hi⟩ => y[i]'(by omega))) :=
  trace_scan_steps_prefix B x y hylen m k hkm (fun j hj => hx x[j] (List.getElem_mem (by omega))) T_rem choices hch

def queryCfg (x : List Bool) (c : Fin x.length → Bool) : OracleCfg 0 QW where
  state := qw_query
  input := { head := x.length + 1, cells := (Tape.init (x.map Γ.ofBool)).cells }
  query := queryTapeScan x.length c
  work := fun _ => Tape.init []
  output := (Tape.init []).move Dir3.right

def acceptCfg (x : List Bool) (c : Fin x.length → Bool) : OracleCfg 0 QW where
  state := qw_accept
  input := { head := x.length + 1, cells := (Tape.init (x.map Γ.ofBool)).cells }
  query := queryTapeScan x.length c
  work := fun _ => Tape.init []
  output := (Tape.init []).move Dir3.right

def rejectCfg (x : List Bool) (c : Fin x.length → Bool) : OracleCfg 0 QW where
  state := qw_reject
  input := { head := x.length + 1, cells := (Tape.init (x.map Γ.ofBool)).cells }
  query := queryTapeScan x.length c
  work := fun _ => Tape.init []
  output := (Tape.init []).move Dir3.right

def haltAcceptCfg (x : List Bool) (c : Fin x.length → Bool) : OracleCfg 0 QW where
  state := qw_halt
  input := { head := x.length + 1, cells := (Tape.init (x.map Γ.ofBool)).cells }
  query := queryTapeScan x.length c
  work := fun _ => Tape.init []
  output := { head := 1, cells := fun i => if i = 0 then Γ.start else if i = 1 then Γ.one else Γ.blank }

theorem query_tape_blank_stay (k : ℕ) (c : Fin k → Bool) :
    (queryTapeScan k c).writeAndMove Γ.blank Dir3.stay = queryTapeScan k c := by
  ext
  · rfl
  · next i =>
    simp only [Tape.writeAndMove, Tape.move, Tape.write, queryTapeScan]
    have hne : k + 1 ≠ 0 := by omega
    simp only [hne, ite_false, Function.update]
    by_cases hi : i = k + 1
    · subst hi
      have hnotlt : ¬ (k + 1 - 1 < k) := by omega
      simp [hnotlt]
    · simp [hi]

theorem step_scan_blank (B : Language) (x : List Bool) (c : Fin x.length → Bool) (b : Bool) :
    witnessNTM.step (oracleOf B) b (scanCfg x x.length c) = some (queryCfg x c) := by
  have hk : (Tape.init (x.map Γ.ofBool)).cells (x.length + 1) = Γ.blank := by
    have h := init_cells_length_add_one (x.map Γ.ofBool)
    simpa using h
  have hq_head : (queryTapeScan x.length c).head = x.length + 1 := rfl
  have ho_head : ((Tape.init ([] : List Γ)).move Dir3.right).head = 1 := rfl
  have hq_read : (queryTapeScan x.length c).cells (queryTapeScan x.length c).head = Γ.blank := by
    rw [hq_head]
    dsimp [queryTapeScan]
    have hnot0 : x.length + 1 ≠ 0 := by omega
    have hnotlt : ¬ (x.length + 1 - 1 < x.length) := by omega
    simp [hnot0, hnotlt]
  have ho_read : ((Tape.init ([] : List Γ)).move Dir3.right).cells
      ((Tape.init ([] : List Γ)).move Dir3.right).head = Γ.blank := by
    rw [ho_head]
    dsimp [Tape.move, Tape.init]
  have hq_stay : (queryTapeScan x.length c).writeAndMove Γ.blank Dir3.stay = queryTapeScan x.length c :=
    query_tape_blank_stay x.length c
  dsimp [OracleNTM.step, witnessNTM, scanCfg, queryCfg, Tape.read, qw_scan, qw_halt, qw_query, qw_start, qw_accept, qw_reject]
  rw [hk, hq_read, ho_read]
  dsimp
  congr 1
  ext
  · rfl
  · rfl
  · rfl
  · exact congr_arg Tape.head hq_stay
  · exact congr_fun (congr_arg Tape.cells hq_stay) _
  · exact Fin.elim0 ‹Fin 0›
  · exact Fin.elim0 ‹Fin 0›
  · rfl
  · exact congr_fun output_tape_blank_step _

theorem step_query_accept (B : Language) (x : List Bool) (c : Fin x.length → Bool) (b : Bool)
    (hB : List.ofFn c ∈ B) :
    witnessNTM.step (oracleOf B) b (queryCfg x c) = some (acceptCfg x c) := by
  dsimp [OracleNTM.step, witnessNTM, queryCfg, acceptCfg, qw_query, qw_halt, qw_accept, qw_reject]
  have hoq : (queryTapeScan x.length c).oracleQuery = List.ofFn c :=
    oracleQuery_queryTapeScan x.length c
  dsimp [oracleOf]
  rw [hoq]
  simp [hB]

theorem output_tape_one_step :
    (((Tape.init ([] : List Γ)).move Dir3.right).writeAndMove Γ.one Dir3.stay).cells =
      (fun i => if i = 0 then Γ.start else if i = 1 then Γ.one else Γ.blank) := by
  ext i
  simp only [Tape.writeAndMove, Tape.move, Tape.write, Tape.init]
  have hne : 0 + 1 ≠ 0 := by omega
  simp only [hne, ite_false, Function.update]
  by_cases hi : i = 0 + 1
  · subst hi
    simp
  · by_cases h0 : i = 0
    · subst h0; simp
    · simp [hi, h0]

theorem step_accept (B : Language) (x : List Bool) (c : Fin x.length → Bool) (b : Bool) :
    witnessNTM.step (oracleOf B) b (acceptCfg x c) = some (haltAcceptCfg x c) := by
  have hk : (Tape.init (x.map Γ.ofBool)).cells (x.length + 1) = Γ.blank := by
    have h := init_cells_length_add_one (x.map Γ.ofBool)
    simpa using h
  have hq_head : (queryTapeScan x.length c).head = x.length + 1 := rfl
  have hq_read : (queryTapeScan x.length c).cells (queryTapeScan x.length c).head = Γ.blank := by
    rw [hq_head]
    dsimp [queryTapeScan]
    have hnot0 : x.length + 1 ≠ 0 := by omega
    have hnotlt : ¬ (x.length + 1 - 1 < x.length) := by omega
    simp [hnot0, hnotlt]
  have ho_head : ((Tape.init ([] : List Γ)).move Dir3.right).head = 1 := rfl
  have ho_read : ((Tape.init ([] : List Γ)).move Dir3.right).cells
      ((Tape.init ([] : List Γ)).move Dir3.right).head = Γ.blank := by
    rw [ho_head]
    dsimp [Tape.move, Tape.init]
  have hq_stay : (queryTapeScan x.length c).writeAndMove Γ.blank Dir3.stay = queryTapeScan x.length c :=
    query_tape_blank_stay x.length c
  dsimp [OracleNTM.step, witnessNTM, acceptCfg, haltAcceptCfg, Tape.read, qw_accept, qw_halt, qw_query, qw_start, qw_reject, qw_scan]
  rw [hk, hq_read, ho_read]
  dsimp
  congr 1
  ext
  · rfl
  · rfl
  · rfl
  · exact congr_arg Tape.head hq_stay
  · exact congr_fun (congr_arg Tape.cells hq_stay) _
  · exact Fin.elim0 ‹Fin 0›
  · exact Fin.elim0 ‹Fin 0›
  · rfl
  · exact congr_fun output_tape_one_step _

def haltRejectCfg (x : List Bool) (c : Fin x.length → Bool) : OracleCfg 0 QW where
  state := qw_halt
  input := { head := x.length + 1, cells := (Tape.init (x.map Γ.ofBool)).cells }
  query := queryTapeScan x.length c
  work := fun _ => Tape.init []
  output := { head := 1, cells := fun i => if i = 0 then Γ.start else if i = 1 then Γ.zero else Γ.blank }

theorem output_tape_zero_step :
    (((Tape.init ([] : List Γ)).move Dir3.right).writeAndMove Γ.zero Dir3.stay).cells =
      (fun i => if i = 0 then Γ.start else if i = 1 then Γ.zero else Γ.blank) := by
  ext i
  simp only [Tape.writeAndMove, Tape.move, Tape.write, Tape.init]
  have hne : 0 + 1 ≠ 0 := by omega
  simp only [hne, ite_false, Function.update]
  by_cases hi : i = 0 + 1
  · subst hi
    simp
  · by_cases h0 : i = 0
    · subst h0; simp
    · simp [hi, h0]

theorem step_query_reject (B : Language) (x : List Bool) (c : Fin x.length → Bool) (b : Bool)
    (hB : List.ofFn c ∉ B) :
    witnessNTM.step (oracleOf B) b (queryCfg x c) = some (rejectCfg x c) := by
  dsimp [OracleNTM.step, witnessNTM, queryCfg, rejectCfg, qw_query, qw_halt, qw_accept, qw_reject]
  have hoq : (queryTapeScan x.length c).oracleQuery = List.ofFn c :=
    oracleQuery_queryTapeScan x.length c
  dsimp [oracleOf]
  rw [hoq]
  simp [hB]

theorem step_reject (B : Language) (x : List Bool) (c : Fin x.length → Bool) (b : Bool) :
    witnessNTM.step (oracleOf B) b (rejectCfg x c) = some (haltRejectCfg x c) := by
  have hk : (Tape.init (x.map Γ.ofBool)).cells (x.length + 1) = Γ.blank := by
    have h := init_cells_length_add_one (x.map Γ.ofBool)
    simpa using h
  have hq_head : (queryTapeScan x.length c).head = x.length + 1 := rfl
  have hq_read : (queryTapeScan x.length c).cells (queryTapeScan x.length c).head = Γ.blank := by
    rw [hq_head]
    dsimp [queryTapeScan]
    have hnot0 : x.length + 1 ≠ 0 := by omega
    have hnotlt : ¬ (x.length + 1 - 1 < x.length) := by omega
    simp [hnot0, hnotlt]
  have ho_head : ((Tape.init ([] : List Γ)).move Dir3.right).head = 1 := rfl
  have ho_read : ((Tape.init ([] : List Γ)).move Dir3.right).cells
      ((Tape.init ([] : List Γ)).move Dir3.right).head = Γ.blank := by
    rw [ho_head]
    dsimp [Tape.move, Tape.init]
  have hq_stay : (queryTapeScan x.length c).writeAndMove Γ.blank Dir3.stay = queryTapeScan x.length c :=
    query_tape_blank_stay x.length c
  dsimp [OracleNTM.step, witnessNTM, rejectCfg, haltRejectCfg, Tape.read, qw_reject, qw_halt, qw_query, qw_start, qw_accept, qw_scan]
  rw [hk, hq_read, ho_read]
  dsimp
  congr 1
  ext
  · rfl
  · rfl
  · rfl
  · exact congr_arg Tape.head hq_stay
  · exact congr_fun (congr_arg Tape.cells hq_stay) _
  · exact Fin.elim0 ‹Fin 0›
  · exact Fin.elim0 ‹Fin 0›
  · rfl
  · exact congr_fun output_tape_zero_step _

def scanRejectCfg (x : List Bool) (k : ℕ) (c : Fin k → Bool) : OracleCfg 0 QW where
  state := qw_reject
  input := { head := k + 1, cells := (Tape.init (x.map Γ.ofBool)).cells }
  query := queryTapeScan k c
  work := fun _ => Tape.init []
  output := (Tape.init []).move Dir3.right

def haltScanRejectCfg (x : List Bool) (k : ℕ) (c : Fin k → Bool) : OracleCfg 0 QW where
  state := qw_halt
  input := { head := k + 1, cells := (Tape.init (x.map Γ.ofBool)).cells }
  query := queryTapeScan k c
  work := fun _ => Tape.init []
  output := { head := 1, cells := fun i => if i = 0 then Γ.start else if i = 1 then Γ.zero else Γ.blank }

theorem step_scan_zero (B : Language) (x : List Bool) (k : ℕ) (c : Fin k → Bool) (b : Bool)
    (hk : (Tape.init (x.map Γ.ofBool)).cells (k + 1) = Γ.zero) :
    witnessNTM.step (oracleOf B) b (scanCfg x k c) = some (scanRejectCfg x k c) := by
  have hq_head : (queryTapeScan k c).head = k + 1 := rfl
  have ho_head : ((Tape.init ([] : List Γ)).move Dir3.right).head = 1 := rfl
  have hq_read : (queryTapeScan k c).cells (queryTapeScan k c).head = Γ.blank := by
    rw [hq_head]
    dsimp [queryTapeScan]
    have hnot0 : k + 1 ≠ 0 := by omega
    have hnotlt : ¬ (k + 1 - 1 < k) := by omega
    simp [hnot0, hnotlt]
  have ho_read : ((Tape.init ([] : List Γ)).move Dir3.right).cells
      ((Tape.init ([] : List Γ)).move Dir3.right).head = Γ.blank := by
    rw [ho_head]
    dsimp [Tape.move, Tape.init]
  have hq_stay : (queryTapeScan k c).writeAndMove Γ.blank Dir3.stay = queryTapeScan k c :=
    query_tape_blank_stay k c
  dsimp [OracleNTM.step, witnessNTM, scanCfg, scanRejectCfg, Tape.read, qw_scan, qw_halt, qw_query, qw_start, qw_accept, qw_reject]
  rw [hk, hq_read, ho_read]
  dsimp
  congr 1
  ext
  · rfl
  · rfl
  · rfl
  · exact congr_arg Tape.head hq_stay
  · exact congr_fun (congr_arg Tape.cells hq_stay) _
  · exact Fin.elim0 ‹Fin 0›
  · exact Fin.elim0 ‹Fin 0›
  · rfl
  · exact congr_fun output_tape_blank_step _

theorem step_scan_reject (B : Language) (x : List Bool) (k : ℕ) (c : Fin k → Bool) (b : Bool)
    (hk : (Tape.init (x.map Γ.ofBool)).cells (k + 1) = Γ.zero) :
    witnessNTM.step (oracleOf B) b (scanRejectCfg x k c) = some (haltScanRejectCfg x k c) := by
  have hq_head : (queryTapeScan k c).head = k + 1 := rfl
  have ho_head : ((Tape.init ([] : List Γ)).move Dir3.right).head = 1 := rfl
  have hq_read : (queryTapeScan k c).cells (queryTapeScan k c).head = Γ.blank := by
    rw [hq_head]
    dsimp [queryTapeScan]
    have hnot0 : k + 1 ≠ 0 := by omega
    have hnotlt : ¬ (k + 1 - 1 < k) := by omega
    simp [hnot0, hnotlt]
  have ho_read : ((Tape.init ([] : List Γ)).move Dir3.right).cells
      ((Tape.init ([] : List Γ)).move Dir3.right).head = Γ.blank := by
    rw [ho_head]
    dsimp [Tape.move, Tape.init]
  have hq_stay : (queryTapeScan k c).writeAndMove Γ.blank Dir3.stay = queryTapeScan k c :=
    query_tape_blank_stay k c
  dsimp [OracleNTM.step, witnessNTM, scanRejectCfg, haltScanRejectCfg, Tape.read, qw_reject, qw_halt, qw_query, qw_start, qw_accept, qw_scan]
  rw [hk, hq_read, ho_read]
  dsimp
  congr 1
  ext
  · rfl
  · rfl
  · rfl
  · exact congr_arg Tape.head hq_stay
  · exact congr_fun (congr_arg Tape.cells hq_stay) _
  · exact Fin.elim0 ‹Fin 0›
  · exact Fin.elim0 ‹Fin 0›
  · rfl
  · exact congr_fun output_tape_zero_step _

theorem acceptsInTime_congr (B : Language) (x : List Bool) {T1 T2 : ℕ} (h : T1 = T2) :
    witnessNTM.AcceptsInTime (oracleOf B) x T1 ↔
    witnessNTM.AcceptsInTime (oracleOf B) x T2 := by
  subst h
  rfl

theorem ofFn_getElem_eq (y : List Bool) :
    (List.ofFn fun i : Fin y.length => y[i.val]'i.isLt) = y := by
  apply List.ext_getElem
  · simp
  · intro i h1 h2
    simp

theorem trace_congr {n : ℕ} (m : OracleNTM n) (oracle : BooleanOracle)
    {T1 T2 : ℕ} (hT : T1 = T2) (choices1 : Fin T1 → Bool) (choices2 : Fin T2 → Bool)
    (hch : ∀ (i : ℕ) (h1 : i < T1) (h2 : i < T2), choices1 ⟨i, h1⟩ = choices2 ⟨i, h2⟩)
    (c : OracleCfg n m.Q) :
    m.trace oracle T1 choices1 c = m.trace oracle T2 choices2 c := by
  subst hT
  have : choices1 = choices2 := by
    ext ⟨i, hi⟩
    exact hch i hi hi
  subst this
  rfl

def witnessChoices (n : ℕ) (y : List Bool) (_hylen : y.length = n) : Fin (3 + n + 1) → Bool :=
  fun ⟨t, _ht⟩ =>
    if h : 1 ≤ t ∧ t ≤ n then y[t - 1]'(by omega)
    else false

theorem trace_three {n : ℕ} (m : OracleNTM n) (oracle : BooleanOracle)
    (choices : Fin 3 → Bool) (c c' : OracleCfg n m.Q)
    (hstep : m.step oracle (choices ⟨0, Nat.zero_lt_succ 2⟩) c = some c') :
    m.trace oracle 3 choices c =
      m.trace oracle 2 (fun i => choices ⟨i.val + 1, by omega⟩) c' :=
  trace_succ_of_step m oracle 2 choices c c' hstep

theorem trace_two {n : ℕ} (m : OracleNTM n) (oracle : BooleanOracle)
    (choices : Fin 2 → Bool) (c c' : OracleCfg n m.Q)
    (hstep : m.step oracle (choices ⟨0, Nat.zero_lt_succ 1⟩) c = some c') :
    m.trace oracle 2 choices c =
      m.trace oracle 1 (fun i => choices ⟨i.val + 1, by omega⟩) c' :=
  trace_succ_of_step m oracle 1 choices c c' hstep

theorem trace_one {n : ℕ} (m : OracleNTM n) (oracle : BooleanOracle)
    (choices : Fin 1 → Bool) (c c' : OracleCfg n m.Q)
    (hstep : m.step oracle (choices ⟨0, Nat.zero_lt_succ 0⟩) c = some c') :
    m.trace oracle 1 choices c = c' := by
  have h := trace_succ_of_step m oracle 0 choices c c' hstep
  rw [h]
  rfl

theorem acceptsInTime_of_mem (B : Language) (x : List Bool)
    (hx : ∀ b ∈ x, b = true) (y : List Bool) (hyB : y ∈ B) (hylen : y.length = x.length) :
    witnessNTM.AcceptsInTime (oracleOf B) x (x.length + 4) := by
  rw [← acceptsInTime_congr B x (by omega : 3 + x.length + 1 = x.length + 4)]
  use witnessChoices x.length y hylen
  dsimp
  have hstep0 : witnessNTM.step (oracleOf B)
      ((witnessChoices x.length y hylen) ⟨0, Nat.zero_lt_succ (3 + x.length)⟩)
      (witnessNTM.initCfg x) = some (c1 x) :=
    step_init B x _
  have htrace0 := trace_succ_of_step witnessNTM (oracleOf B) (3 + x.length)
    (witnessChoices x.length y hylen) (witnessNTM.initCfg x) (c1 x) hstep0
  rw [htrace0]
  have hc1_scan : c1 x = scanCfg x 0 (fun ⟨i, _hi⟩ => y[i]'(by omega)) := by
    rw [c1_eq_scanCfg_zero]
    congr 1
    ext ⟨i, hi⟩
    omega
  rw [hc1_scan]
  let choices' := fun i : Fin (3 + x.length) =>
    (witnessChoices x.length y hylen) ⟨i.val + 1, by omega⟩
  have hch : ∀ (i : ℕ) (hi : i < x.length), choices' ⟨i, by omega⟩ = y[0 + i]'(by omega) := by
    intro i hi
    dsimp [choices', witnessChoices]
    have h1 : 1 ≤ i + 1 := by omega
    have h2 : i + 1 ≤ x.length := by omega
    simp [h1, h2]
  have hscan := trace_scan_steps B x hx y hylen x.length 0 (by omega) 3 choices' hch
  rw [hscan]
  have hcfg_eq := scanCfg_congr (x := x) (y := y) (by omega) (by omega : 0 + x.length = x.length)
  rw [hcfg_eq]
  let choices'' := fun i : Fin 3 => choices' ⟨i.val + x.length, by omega⟩
  have hstep_blank : witnessNTM.step (oracleOf B) (choices'' ⟨0, Nat.zero_lt_succ 2⟩)
      (scanCfg x x.length (fun ⟨i, _hi⟩ => y[i]'(by omega))) =
      some (queryCfg x (fun ⟨i, _hi⟩ => y[i]'(by omega))) :=
    step_scan_blank B x (fun ⟨i, _hi⟩ => y[i]'(by omega)) _
  have htrace_blank := trace_three witnessNTM (oracleOf B) choices''
    (scanCfg x x.length (fun ⟨i, _hi⟩ => y[i]'(by omega)))
    (queryCfg x (fun ⟨i, _hi⟩ => y[i]'(by omega))) hstep_blank
  rw [htrace_blank]
  let choices''' := fun i : Fin 2 => choices'' ⟨i.val + 1, by omega⟩
  have hy_ofFn : (List.ofFn (n := x.length) (fun ⟨i, _hi⟩ => y[i]'(by omega))) ∈ B := by
    have h_eq : (List.ofFn (n := x.length) (fun ⟨i, _hi⟩ => y[i]'(by omega))) = y := by
      apply List.ext_getElem
      · simp [hylen]
      · intro i h1 h2
        simp
    rw [h_eq]
    exact hyB
  have hstep_query : witnessNTM.step (oracleOf B) (choices''' ⟨0, Nat.zero_lt_succ 1⟩)
      (queryCfg x (fun ⟨i, _hi⟩ => y[i]'(by omega))) =
      some (acceptCfg x (fun ⟨i, _hi⟩ => y[i]'(by omega))) :=
    step_query_accept B x (fun ⟨i, _hi⟩ => y[i]'(by omega)) _ hy_ofFn
  have htrace_query := trace_two witnessNTM (oracleOf B) choices'''
    (queryCfg x (fun ⟨i, _hi⟩ => y[i]'(by omega)))
    (acceptCfg x (fun ⟨i, _hi⟩ => y[i]'(by omega))) hstep_query
  rw [htrace_query]
  let choices'''' := fun i : Fin 1 => choices''' ⟨i.val + 1, by omega⟩
  have hstep_acc : witnessNTM.step (oracleOf B) (choices'''' ⟨0, Nat.zero_lt_succ 0⟩)
      (acceptCfg x (fun ⟨i, _hi⟩ => y[i]'(by omega))) =
      some (haltAcceptCfg x (fun ⟨i, _hi⟩ => y[i]'(by omega))) :=
    step_accept B x (fun ⟨i, _hi⟩ => y[i]'(by omega)) _
  have htrace_acc := trace_one witnessNTM (oracleOf B) choices''''
    (acceptCfg x (fun ⟨i, _hi⟩ => y[i]'(by omega)))
    (haltAcceptCfg x (fun ⟨i, _hi⟩ => y[i]'(by omega))) hstep_acc
  rw [htrace_acc]
  exact ⟨rfl, rfl⟩

theorem trace_all_ones (B : Language) (x : List Bool) (hx : ∀ b ∈ x, b = true)
    (choices : Fin (x.length + 4) → Bool) :
    witnessNTM.trace (oracleOf B) (x.length + 4) choices (witnessNTM.initCfg x) =
      if List.ofFn (fun (i : Fin x.length) => choices ⟨i.val + 1, by omega⟩) ∈ B
      then haltAcceptCfg x (fun (i : Fin x.length) => choices ⟨i.val + 1, by omega⟩)
      else haltRejectCfg x (fun (i : Fin x.length) => choices ⟨i.val + 1, by omega⟩) := by
  let c : Fin x.length → Bool := fun (i : Fin x.length) => choices ⟨i.val + 1, by omega⟩
  change witnessNTM.trace (oracleOf B) (x.length + 4) choices (witnessNTM.initCfg x) =
    if List.ofFn c ∈ B then haltAcceptCfg x c else haltRejectCfg x c
  have hT : x.length + 4 = 3 + x.length + 1 := by omega
  have htr_congr := trace_congr witnessNTM (oracleOf B) hT
    choices (fun i => choices ⟨i.val, by omega⟩) (fun _ _ _ => rfl) (witnessNTM.initCfg x)
  rw [htr_congr]
  have hstep0 : witnessNTM.step (oracleOf B)
      ((fun i : Fin (3 + x.length + 1) => choices ⟨i.val, by omega⟩) ⟨0, Nat.zero_lt_succ (3 + x.length)⟩)
      (witnessNTM.initCfg x) = some (c1 x) :=
    step_init B x _
  have htrace0 := trace_succ_of_step witnessNTM (oracleOf B) (3 + x.length)
    (fun i => choices ⟨i.val, by omega⟩) (witnessNTM.initCfg x) (c1 x) hstep0
  rw [htrace0]
  let choices' := fun i : Fin (3 + x.length) =>
    (fun i : Fin (3 + x.length + 1) => choices ⟨i.val, by omega⟩) ⟨i.val + 1, by omega⟩
  let y := List.ofFn c
  have hylen : y.length = x.length := by simp [y]
  have hc1_scan : c1 x = scanCfg x 0 (fun ⟨i, _hi⟩ => y[i]'(by omega)) := by
    rw [c1_eq_scanCfg_zero]
    congr 1
    ext ⟨i, hi⟩
    omega
  rw [hc1_scan]
  have hch : ∀ (i : ℕ) (hi : i < x.length), choices' ⟨i, by omega⟩ = y[0 + i]'(by omega) := by
    intro i hi
    dsimp [choices', y, c]
    simp
  have hscan := trace_scan_steps B x hx y hylen x.length 0 (by omega) 3 choices' hch
  rw [hscan]
  have hcfg_eq := scanCfg_congr (x := x) (y := y) (by omega) (by omega : 0 + x.length = x.length)
  rw [hcfg_eq]
  have hc_scan : (scanCfg x x.length fun ⟨i, _hi⟩ => y[i]'(by omega)) = scanCfg x x.length c := by
    congr 1
    ext ⟨i, hi⟩
    dsimp [y]
    simp
  rw [hc_scan]
  let choices'' := fun i : Fin 3 => choices' ⟨i.val + x.length, by omega⟩
  have hstep_blank : witnessNTM.step (oracleOf B) (choices'' ⟨0, Nat.zero_lt_succ 2⟩)
      (scanCfg x x.length c) = some (queryCfg x c) :=
    step_scan_blank B x c _
  have htrace_blank := trace_three witnessNTM (oracleOf B) choices''
    (scanCfg x x.length c) (queryCfg x c) hstep_blank
  rw [htrace_blank]
  let choices''' := fun i : Fin 2 => choices'' ⟨i.val + 1, by omega⟩
  by_cases hB : List.ofFn c ∈ B
  · simp only [hB, ite_true]
    have hstep_query : witnessNTM.step (oracleOf B) (choices''' ⟨0, Nat.zero_lt_succ 1⟩)
        (queryCfg x c) = some (acceptCfg x c) :=
      step_query_accept B x c _ hB
    have htrace_query := trace_two witnessNTM (oracleOf B) choices'''
      (queryCfg x c) (acceptCfg x c) hstep_query
    rw [htrace_query]
    let choices'''' := fun i : Fin 1 => choices''' ⟨i.val + 1, by omega⟩
    have hstep_acc : witnessNTM.step (oracleOf B) (choices'''' ⟨0, Nat.zero_lt_succ 0⟩)
        (acceptCfg x c) = some (haltAcceptCfg x c) :=
      step_accept B x c _
    have htrace_acc := trace_one witnessNTM (oracleOf B) choices''''
      (acceptCfg x c) (haltAcceptCfg x c) hstep_acc
    rw [htrace_acc]
  · simp only [hB, ite_false]
    have hstep_query : witnessNTM.step (oracleOf B) (choices''' ⟨0, Nat.zero_lt_succ 1⟩)
        (queryCfg x c) = some (rejectCfg x c) :=
      step_query_reject B x c _ hB
    have htrace_query := trace_two witnessNTM (oracleOf B) choices'''
      (queryCfg x c) (rejectCfg x c) hstep_query
    rw [htrace_query]
    let choices'''' := fun i : Fin 1 => choices''' ⟨i.val + 1, by omega⟩
    have hstep_rej : witnessNTM.step (oracleOf B) (choices'''' ⟨0, Nat.zero_lt_succ 0⟩)
        (rejectCfg x c) = some (haltRejectCfg x c) :=
      step_reject B x c _
    have htrace_rej := trace_one witnessNTM (oracleOf B) choices''''
      (rejectCfg x c) (haltRejectCfg x c) hstep_rej
    rw [htrace_rej]

theorem trace_not_all_ones (B : Language) (x : List Bool)
    (k : ℕ) (hk : k < x.length) (hprev : ∀ (j : ℕ) (hj : j < k), x[j] = true) (hfalse : x[k] = false)
    (choices : Fin (x.length + 4) → Bool) :
    witnessNTM.trace (oracleOf B) (x.length + 4) choices (witnessNTM.initCfg x) =
      haltScanRejectCfg x k (fun (i : Fin k) => choices ⟨i.val + 1, by omega⟩) := by
  let c : Fin k → Bool := fun (i : Fin k) => choices ⟨i.val + 1, by omega⟩
  change witnessNTM.trace (oracleOf B) (x.length + 4) choices (witnessNTM.initCfg x) =
    haltScanRejectCfg x k c
  have hT1 : x.length + 4 = (x.length + 3) + 1 := by omega
  have htr_congr1 := trace_congr witnessNTM (oracleOf B) hT1
    choices (fun i => choices ⟨i.val, by omega⟩) (fun _ _ _ => rfl) (witnessNTM.initCfg x)
  rw [htr_congr1]
  have hstep0 : witnessNTM.step (oracleOf B)
      ((fun i : Fin ((x.length + 3) + 1) => choices ⟨i.val, by omega⟩) ⟨0, Nat.zero_lt_succ (x.length + 3)⟩)
      (witnessNTM.initCfg x) = some (c1 x) :=
    step_init B x _
  have htrace0 := trace_succ_of_step witnessNTM (oracleOf B) (x.length + 3)
    (fun i => choices ⟨i.val, by omega⟩) (witnessNTM.initCfg x) (c1 x) hstep0
  rw [htrace0]
  let choices' := fun i : Fin (x.length + 3) => choices ⟨i.val + 1, by omega⟩
  let y := List.ofFn (fun i : Fin x.length => choices ⟨i.val + 1, by omega⟩)
  have hylen : y.length = x.length := by simp [y]
  have hc1_scan : c1 x = scanCfg x 0 (fun ⟨i, _hi⟩ => y[i]'(by omega)) := by
    rw [c1_eq_scanCfg_zero]
    congr 1
    ext ⟨i, hi⟩
    omega
  rw [hc1_scan]
  let T_rem := x.length + 3 - k
  have hT2 : x.length + 3 = T_rem + k := by omega
  have htr_congr2 := trace_congr witnessNTM (oracleOf B) hT2
    choices' (fun i => choices' ⟨i.val, by omega⟩) (fun _ _ _ => rfl)
    (scanCfg x 0 (fun ⟨i, _hi⟩ => y[i]'(by omega)))
  rw [htr_congr2]
  have hch : ∀ (i : ℕ) (hi : i < k),
      (fun i : Fin (T_rem + k) => choices' ⟨i.val, by omega⟩) ⟨i, by omega⟩ = y[0 + i]'(by omega) := by
    intro i hi
    dsimp [choices', y]
    simp
  have hscan := trace_scan_steps_prefix B x y hylen k 0 (by omega)
    (fun j hj => hprev j (by omega)) T_rem (fun i => choices' ⟨i.val, by omega⟩) hch
  rw [hscan]
  have hcfg_eq := scanCfg_congr (x := x) (y := y) (by omega) (by omega : 0 + k = k)
  rw [hcfg_eq]
  have hc_scan : (scanCfg x k fun ⟨i, _hi⟩ => y[i]'(by omega)) = scanCfg x k c := by
    congr 1
    ext ⟨i, hi⟩
    dsimp [y, c]
    simp
  rw [hc_scan]
  let choices_rem := fun i : Fin T_rem => choices' ⟨i.val + k, by omega⟩
  have hT_rem_pos : T_rem = (T_rem - 1) + 1 := by omega
  have htr_congr3 := trace_congr witnessNTM (oracleOf B) hT_rem_pos
    choices_rem (fun i => choices_rem ⟨i.val, by omega⟩) (fun _ _ _ => rfl)
    (scanCfg x k c)
  rw [htr_congr3]
  have hcell_zero : (Tape.init (x.map Γ.ofBool)).cells (k + 1) = Γ.zero :=
    zero_init_cell x k hk hfalse
  have hstep_zero : witnessNTM.step (oracleOf B)
      ((fun i : Fin ((T_rem - 1) + 1) => choices_rem ⟨i.val, by omega⟩) ⟨0, Nat.zero_lt_succ (T_rem - 1)⟩)
      (scanCfg x k c) = some (scanRejectCfg x k c) :=
    step_scan_zero B x k c _ hcell_zero
  have htrace_zero := trace_succ_of_step witnessNTM (oracleOf B) (T_rem - 1)
    (fun i => choices_rem ⟨i.val, by omega⟩) (scanCfg x k c) (scanRejectCfg x k c) hstep_zero
  rw [htrace_zero]
  let choices_rem2 := fun i : Fin (T_rem - 1) => choices_rem ⟨i.val + 1, by omega⟩
  have hT_rem2_pos : T_rem - 1 = (T_rem - 2) + 1 := by omega
  have htr_congr4 := trace_congr witnessNTM (oracleOf B) hT_rem2_pos
    choices_rem2 (fun i => choices_rem2 ⟨i.val, by omega⟩) (fun _ _ _ => rfl)
    (scanRejectCfg x k c)
  rw [htr_congr4]
  have hstep_rej : witnessNTM.step (oracleOf B)
      ((fun i : Fin ((T_rem - 2) + 1) => choices_rem2 ⟨i.val, by omega⟩) ⟨0, Nat.zero_lt_succ (T_rem - 2)⟩)
      (scanRejectCfg x k c) = some (haltScanRejectCfg x k c) :=
    step_scan_reject B x k c _ hcell_zero
  have htrace_rej := trace_succ_of_step witnessNTM (oracleOf B) (T_rem - 2)
    (fun i => choices_rem2 ⟨i.val, by omega⟩) (scanRejectCfg x k c) (haltScanRejectCfg x k c) hstep_rej
  rw [htrace_rej]
  let choices_rem3 := fun i : Fin (T_rem - 2) => choices_rem2 ⟨i.val + 1, by omega⟩
  have hhalt : witnessNTM.halted (haltScanRejectCfg x k c) := rfl
  exact trace_of_halted witnessNTM (oracleOf B) (T_rem - 2) choices_rem3 (haltScanRejectCfg x k c) hhalt

theorem witnessNTM_allPathsHalt (B : Language) :
    witnessNTM.AllPathsHaltIn (oracleOf B) (fun n => n + 4) := by
  intro x choices
  rcases first_false_or_all_ones x with hx | ⟨k, hk, hprev, hfalse⟩
  · have htr := trace_all_ones B x hx choices
    rw [htr]
    split_ifs <;> rfl
  · have htr := trace_not_all_ones B x k hk hprev hfalse choices
    rw [htr]
    rfl

theorem witnessNTM_decides (B : Language) :
    ∀ x, x ∈ unaryWitnessLang B ↔ witnessNTM.AcceptsInTime (oracleOf B) x (x.length + 4) := by
  intro x
  constructor
  · intro hx
    obtain ⟨hx_ones, y, hyB, hylen⟩ := hx
    exact acceptsInTime_of_mem B x hx_ones y hyB hylen
  · intro ⟨choices, hconj⟩
    obtain ⟨_hhalt, hout⟩ := hconj
    rcases first_false_or_all_ones x with hx | ⟨k, hk, hprev, hfalse⟩
    · have htr := trace_all_ones B x hx choices
      rw [htr] at hout
      split_ifs at hout with hB
      · refine ⟨hx, List.ofFn (fun (i : Fin x.length) => choices ⟨i.val + 1, by omega⟩), hB, ?_⟩
        simp
      · dsimp [haltRejectCfg] at hout
        cases hout
    · have htr := trace_not_all_ones B x k hk hprev hfalse choices
      rw [htr] at hout
      dsimp [haltScanRejectCfg] at hout
      cases hout

theorem unaryWitnessLang_mem_NPRel (B : Language) :
    unaryWitnessLang B ∈ NPRel B := by
  use 0, 1, witnessNTM, fun n => n + 4
  refine ⟨⟨witnessNTM_allPathsHalt B, witnessNTM_decides B⟩, witnessNTM_time_bigO⟩

#print axioms unaryWitnessLang_mem_NPRel


end Stage3A

open Stage3A in
#print axioms PRel_subset_NPRel
open Stage3A in
#print axioms P_subset_PRel
open Stage3A in
#print axioms NP_subset_NPRel
open Stage3A in
#print axioms oracleTMToTM_step
open Stage3A in
#print axioms oracleTMToTM_reachesIn
open Stage3A in
#print axioms unpack_step
open Stage3A in
#print axioms unpack_trace_of_step_sim
open Stage3A in
#print axioms PRel_empty_subset_P_of_step_sim
open Stage3A in
#print axioms NPRel_empty_subset_NP_of_step_sim
open Stage3A in
#print axioms NPRel_empty_eq_NP_of_step_sim

open Stage3A in
#print axioms unaryWitnessLang_mem_NPRel
