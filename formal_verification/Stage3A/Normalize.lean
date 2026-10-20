import Complexitylib.Stage3.Defs
import Complexitylib.Models.TuringMachine.Oracle.Defs

namespace Complexity

namespace OracleTM

variable {n : ℕ}

/-- Canonical equivalence between an oracle TM's states and `Fin (Fintype.card m.Q)`. -/
noncomputable def stateEquiv (m : OracleTM n) : m.Q ≃ Fin (Fintype.card m.Q) :=
  @Fintype.equivFin m.Q m.finQ

/-- Normalize an OracleTM to state space `Fin (Fintype.card m.Q)`. -/
noncomputable def normalize (m : OracleTM n) : OracleTM n where
  Q := Fin (Fintype.card m.Q)
  decEq := inferInstance
  finQ := inferInstance
  qstart := m.stateEquiv m.qstart
  qhalt := m.stateEquiv m.qhalt
  queryTransition := fun q =>
    (m.queryTransition (m.stateEquiv.symm q)).map fun (yesState, noState) =>
      (m.stateEquiv yesState, m.stateEquiv noState)
  localTransition := fun q iHead qHead wHeads oHead =>
    let t := m.localTransition (m.stateEquiv.symm q) iHead qHead wHeads oHead
    { nextState := m.stateEquiv t.nextState
      queryWrite := t.queryWrite
      workWrites := t.workWrites
      outputWrite := t.outputWrite
      inputDir := t.inputDir
      queryDir := t.queryDir
      workDirs := t.workDirs
      outputDir := t.outputDir }
  localTransition_right_of_start := fun q iHead qHead wHeads oHead =>
    m.localTransition_right_of_start (m.stateEquiv.symm q) iHead qHead wHeads oHead

/-- Configuration embedding: map a config with original states to normalized states. -/
noncomputable def normalizeCfg (m : OracleTM n) (c : OracleCfg n m.Q) : OracleCfg n (m.normalize.Q) where
  state := m.stateEquiv c.state
  input := c.input
  query := c.query
  work := c.work
  output := c.output

/-- Stepping the normalized OracleTM commutes with configuration normalization. -/
theorem normalize_step_comm (m : OracleTM n) (oracle : BooleanOracle)
    (c : OracleCfg n m.Q) :
    m.normalize.step oracle (m.normalizeCfg c) = (m.step oracle c).map m.normalizeCfg := by
  dsimp [step, normalize, normalizeCfg]
  by_cases h : c.state = m.qhalt
  · simp [h, Option.map]
  · have hne : m.stateEquiv c.state ≠ m.stateEquiv m.qhalt := by
      intro heq
      exact h (m.stateEquiv.injective heq)
    simp only [h, hne, ↓reduceIte]
    simp only [Equiv.symm_apply_apply]
    cases hq : m.queryTransition c.state with
    | some yesNo =>
        rcases yesNo with ⟨yesState, noState⟩
        dsimp only [Option.map]
        split_ifs <;> rfl
    | none =>
        dsimp only [Option.map]
        rfl

/-- Multi-step execution is preserved by normalization. -/
theorem normalize_reachesIn (m : OracleTM n) (oracle : BooleanOracle) {t : ℕ}
    {c c' : OracleCfg n m.Q} (h : m.reachesIn oracle t c c') :
    m.normalize.reachesIn oracle t (m.normalizeCfg c) (m.normalizeCfg c') := by
  induction h with
  | zero => exact .zero
  | step hstep _ ih =>
    exact .step (by rw [normalize_step_comm, hstep]; rfl) ih

/-- Halting is preserved by normalization. -/
theorem normalize_halted (m : OracleTM n) (c : OracleCfg n m.Q) :
    m.normalize.halted (m.normalizeCfg c) ↔ m.halted c := by
  simp only [OracleTM.halted, normalizeCfg, normalize, stateEquiv]
  constructor
  · intro h; exact m.stateEquiv.injective h
  · intro h; rw [h]

/-- Output tape is preserved by normalization. -/
theorem normalize_output (m : OracleTM n) (c : OracleCfg n m.Q) :
    (m.normalizeCfg c).output = c.output := rfl

/-- Initial configuration is preserved by normalization. -/
theorem normalize_initCfg (m : OracleTM n) (x : List Bool) :
    m.normalizeCfg (m.initCfg x) = m.normalize.initCfg x := by
  simp [normalizeCfg, OracleTM.initCfg, OracleCfg.init, normalize]

/-- Normalized OracleTM decides the same language in the same time. -/
theorem normalize_decidesInTime (m : OracleTM n) (oracle : BooleanOracle)
    {L : Language} {T : ℕ → ℕ} (h : m.DecidesInTime oracle L T) :
    m.normalize.DecidesInTime oracle L T := by
  intro x
  obtain ⟨c', t, ht, hreach, hhalt, hmem, hnmem⟩ := h x
  refine ⟨m.normalizeCfg c', t, ht, ?_, ?_, ?_, ?_⟩
  · rw [← normalize_initCfg]; exact normalize_reachesIn m oracle hreach
  · rwa [normalize_halted]
  · intro hx; rw [normalize_output]; exact hmem hx
  · intro hx; rw [normalize_output]; exact hnmem hx

end OracleTM

end Complexity
