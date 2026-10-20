/-
  Stage 3 DEFINITIONS (no sorry). Imported by both the quarantined spec
  (Stage3Spec/Spec.lean) and the proved probes (Stage3A/Probes.lean).
  Inherited from Complexitylib (Apache-2.0, add0aca8): OracleTM, OracleCfg,
  BooleanOracle, DTIME/NTIME/P/NP/FP/≤ₚ. NEW here: OracleNTM, oracleOf,
  PRel, NPRel, unaryWitnessLang.
-/
import Complexitylib.Models.TuringMachine.Oracle
import Complexitylib.Classes.Containments
import Complexitylib.Classes.NP.Reduction

open Complexity
open scoped Complexity

namespace Stage3Spec

/-! ## 1. NEW: nondeterministic oracle machine (mirrors `OracleTM` and `NTM`) -/

/-- NEW. Nondeterministic oracle TM. The choice bit selects the local transition;
query states are choice-independent and cost exactly one step (same convention
as `Complexity.OracleTM`). -/
structure OracleNTM (n : ℕ) where
  Q : Type
  [decEq : DecidableEq Q]
  [finQ : Fintype Q]
  qstart : Q
  qhalt : Q
  queryTransition : Q → Option (Q × Q)
  localTransition :
    Bool → Q → Γ → Γ → (Fin n → Γ) → Γ → OracleLocalTransition n Q
  localTransition_right_of_start :
    ∀ (b : Bool) (q : Q) (inputHead queryHead : Γ) (workHeads : Fin n → Γ)
      (outputHead : Γ),
      let transition :=
        localTransition b q inputHead queryHead workHeads outputHead
      (inputHead = Γ.start → transition.inputDir = Dir3.right) ∧
      (queryHead = Γ.start → transition.queryDir = Dir3.right) ∧
      (∀ index, workHeads index = Γ.start →
        transition.workDirs index = Dir3.right) ∧
      (outputHead = Γ.start → transition.outputDir = Dir3.right)

attribute [instance] OracleNTM.decEq OracleNTM.finQ

namespace OracleNTM

variable {n : ℕ}

/-- NEW. One step under choice bit `b`; `none` iff halted. -/
def step (m : OracleNTM n) (oracle : BooleanOracle) (b : Bool)
    (cfg : OracleCfg n m.Q) : Option (OracleCfg n m.Q) :=
  if cfg.state = m.qhalt then none
  else
    match m.queryTransition cfg.state with
    | some (yesState, noState) =>
        some { cfg with
          state := if oracle cfg.query.oracleQuery then yesState else noState }
    | none =>
        let t := m.localTransition b cfg.state cfg.input.read cfg.query.read
          (fun index => (cfg.work index).read) cfg.output.read
        some
          { state := t.nextState
            input := cfg.input.move t.inputDir
            query := cfg.query.writeAndMove t.queryWrite t.queryDir
            work := fun index => (cfg.work index).writeAndMove
              (t.workWrites index) (t.workDirs index)
            output := cfg.output.writeAndMove t.outputWrite t.outputDir }

/-- NEW. Run for exactly `T` choice bits (frozen once halted), as `NTM.trace`. -/
def trace (m : OracleNTM n) (oracle : BooleanOracle) :
    (T : ℕ) → (Fin T → Bool) → OracleCfg n m.Q → OracleCfg n m.Q
  | 0, _, c => c
  | T + 1, choices, c =>
    match m.step oracle (choices ⟨0, Nat.zero_lt_succ T⟩) c with
    | none => c
    | some c' => trace m oracle T (fun i => choices ⟨i.val + 1, by omega⟩) c'

abbrev initCfg (m : OracleNTM n) (x : List Bool) : OracleCfg n m.Q :=
  OracleCfg.init m.qstart x

abbrev halted (m : OracleNTM n) (c : OracleCfg n m.Q) : Prop :=
  c.state = m.qhalt

/-- NEW. Every choice sequence halts within `T(|x|)` steps. -/
def AllPathsHaltIn (m : OracleNTM n) (oracle : BooleanOracle) (T : ℕ → ℕ) : Prop :=
  ∀ x (choices : Fin (T x.length) → Bool),
    m.halted (m.trace oracle (T x.length) choices (m.initCfg x))

/-- NEW. Some choice sequence of length `T` halts with output cell 1 = `1`. -/
def AcceptsInTime (m : OracleNTM n) (oracle : BooleanOracle)
    (x : List Bool) (T : ℕ) : Prop :=
  ∃ choices : Fin T → Bool,
    let c' := m.trace oracle T choices (m.initCfg x)
    m.halted c' ∧ c'.output.cells 1 = Γ.one

/-- NEW. Mirrors `NTM.DecidesInTime`. -/
def DecidesInTime (m : OracleNTM n) (oracle : BooleanOracle)
    (L : Language) (T : ℕ → ℕ) : Prop :=
  m.AllPathsHaltIn oracle T ∧ (∀ x, x ∈ L ↔ m.AcceptsInTime oracle x (T x.length))

end OracleNTM

/-! ## 2. NEW: oracle as a language, relativized classes -/

open Classical in
/-- NEW. Characteristic function of an oracle language `A ⊆ {0,1}*`. -/
noncomputable def oracleOf (A : Language) : BooleanOracle :=
  fun q => decide (q ∈ A)

/-- NEW. `P^A`: deterministic oracle TM, time `O(n^d)`, one step per query. -/
def PRel (A : Language) : Set Language :=
  {L | ∃ (k d : ℕ) (m : OracleTM k) (f : ℕ → ℕ),
    m.DecidesInTime (oracleOf A) L f ∧ f =O (· ^ d)}

/-- NEW. `NP^A`: nondeterministic oracle TM, all paths time `O(n^d)`. -/
def NPRel (A : Language) : Set Language :=
  {L | ∃ (k d : ℕ) (m : OracleNTM k) (f : ℕ → ℕ),
    m.DecidesInTime (oracleOf A) L f ∧ f =O (· ^ d)}

/-- NEW. Separating witness language `L_B = {1^n : ∃ y ∈ B, |y| = n}`. -/
def unaryWitnessLang (B : Language) : Language :=
  {x | (∀ b ∈ x, b = true) ∧ ∃ y ∈ B, y.length = x.length}


end Stage3Spec
