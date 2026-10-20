import Complexitylib.Stage3.Clocked
import Complexitylib.Stage3.Normalize
import Mathlib.Data.Nat.Pairing

namespace Stage3Separation

open Complexity
open Stage3Spec

structure CanonicalClockedOracleTM where
  k : ℕ
  q : ℕ
  hq : 1 ≤ q
  qstart : Fin q
  qhalt : Fin q
  queryTransition : Fin q → Option (Fin q × Fin q)
  localTransition : Fin q → Γ → Γ → (Fin k → Γ) → Γ → OracleLocalTransition k (Fin q)
  localTransition_right_of_start :
    ∀ (s : Fin q) (inputHead queryHead : Γ) (workHeads : Fin k → Γ) (outputHead : Γ),
      let transition := localTransition s inputHead queryHead workHeads outputHead
      (inputHead = Γ.start → transition.inputDir = Dir3.right) ∧
      (queryHead = Γ.start → transition.queryDir = Dir3.right) ∧
      (∀ index, workHeads index = Γ.start → transition.workDirs index = Dir3.right) ∧
      (outputHead = Γ.start → transition.outputDir = Dir3.right)
  C : ℕ
  d : ℕ
  hC : 1 ≤ C

def CanonicalClockedOracleTM.toClockedOracleTM (M : CanonicalClockedOracleTM) : ClockedOracleTM where
  k := M.k
  m := {
    Q := Fin M.q
    decEq := inferInstance
    finQ := inferInstance
    qstart := M.qstart
    qhalt := M.qhalt
    queryTransition := M.queryTransition
    localTransition := M.localTransition
    localTransition_right_of_start := M.localTransition_right_of_start
  }
  C := M.C
  d := M.d
  hC := M.hC

theorem ClockedOracleTM.ext_same_k {k : ℕ} {m₁ m₂ : OracleTM k} {C₁ C₂ d₁ d₂ : ℕ}
    {hC₁ : 1 ≤ C₁} {hC₂ : 1 ≤ C₂}
    (hm : m₁ = m₂) (hC : C₁ = C₂) (hd : d₁ = d₂) :
    ({ k := k, m := m₁, C := C₁, d := d₁, hC := hC₁ } : ClockedOracleTM) =
    { k := k, m := m₂, C := C₂, d := d₂, hC := hC₂ } := by
  subst hm hC hd
  rfl

theorem OracleTM.ext_fin {k q : ℕ}
    {qs₁ qs₂ qh₁ qh₂ : Fin q}
    {qt₁ qt₂ : Fin q → Option (Fin q × Fin q)}
    {lt₁ lt₂ : Fin q → Γ → Γ → (Fin k → Γ) → Γ → OracleLocalTransition k (Fin q)}
    {hros₁ : ∀ (s : Fin q) (iHead qHead : Γ) (wHeads : Fin k → Γ) (oHead : Γ),
      let t := lt₁ s iHead qHead wHeads oHead
      (iHead = Γ.start → t.inputDir = Dir3.right) ∧
      (qHead = Γ.start → t.queryDir = Dir3.right) ∧
      (∀ index, wHeads index = Γ.start → t.workDirs index = Dir3.right) ∧
      (oHead = Γ.start → t.outputDir = Dir3.right)}
    {hros₂ : ∀ (s : Fin q) (iHead qHead : Γ) (wHeads : Fin k → Γ) (oHead : Γ),
      let t := lt₂ s iHead qHead wHeads oHead
      (iHead = Γ.start → t.inputDir = Dir3.right) ∧
      (qHead = Γ.start → t.queryDir = Dir3.right) ∧
      (∀ index, wHeads index = Γ.start → t.workDirs index = Dir3.right) ∧
      (oHead = Γ.start → t.outputDir = Dir3.right)}
    (hqs : qs₁ = qs₂) (hqh : qh₁ = qh₂) (hqt : qt₁ = qt₂) (hlt : lt₁ = lt₂) :
    ({ Q := Fin q, decEq := inferInstance, finQ := inferInstance,
       qstart := qs₁, qhalt := qh₁, queryTransition := qt₁, localTransition := lt₁,
       localTransition_right_of_start := hros₁ } : OracleTM k) =
    { Q := Fin q, decEq := inferInstance, finQ := inferInstance,
       qstart := qs₂, qhalt := qh₂, queryTransition := qt₂, localTransition := lt₂,
       localTransition_right_of_start := hros₂ } := by
  subst hqs hqh hqt hlt
  rfl

noncomputable def ClockedOracleTM.toCanonical (M : ClockedOracleTM) : CanonicalClockedOracleTM where
  k := M.k
  q := Fintype.card M.m.Q
  hq := by
    have : Nonempty M.m.Q := ⟨M.m.qstart⟩
    exact Fintype.card_pos
  qstart := M.m.stateEquiv M.m.qstart
  qhalt := M.m.stateEquiv M.m.qhalt
  queryTransition := M.normalize.m.queryTransition
  localTransition := M.normalize.m.localTransition
  localTransition_right_of_start := M.normalize.m.localTransition_right_of_start
  C := M.C
  d := M.d
  hC := M.hC

theorem toCanonical_toClockedOracleTM (M : ClockedOracleTM) :
    M.toCanonical.toClockedOracleTM = M.normalize := rfl

def encodeΓ : Γ → ℕ
  | .zero => 0
  | .one => 1
  | .blank => 2
  | .start => 3

def decodeΓ : ℕ → Γ
  | 0 => .zero
  | 1 => .one
  | 2 => .blank
  | _ => .start

theorem decodeΓ_encodeΓ (g : Γ) : decodeΓ (encodeΓ g) = g := by
  cases g <;> rfl

def encodeΓw : Γw → ℕ
  | .zero => 0
  | .one => 1
  | .blank => 2

def decodeΓw : ℕ → Γw
  | 0 => .zero
  | 1 => .one
  | _ => .blank

theorem decodeΓw_encodeΓw (g : Γw) : decodeΓw (encodeΓw g) = g := by
  cases g <;> rfl

def encodeDir3 : Dir3 → ℕ
  | .left => 0
  | .right => 1
  | .stay => 2

def decodeDir3 : ℕ → Dir3
  | 0 => .left
  | 1 => .right
  | _ => .stay

theorem decodeDir3_encodeDir3 (d : Dir3) : decodeDir3 (encodeDir3 d) = d := by
  cases d <;> rfl

def encodeNatListAux : List ℕ → ℕ
  | [] => 0
  | x :: xs => Nat.pair x (encodeNatListAux xs)

def decodeNatListAux : ℕ → ℕ → List ℕ
  | 0, _ => []
  | len + 1, code =>
      let p := Nat.unpair code
      p.1 :: decodeNatListAux len p.2

def encodeNatList (l : List ℕ) : ℕ :=
  Nat.pair l.length (encodeNatListAux l)

def decodeNatList (code : ℕ) : List ℕ :=
  let p := Nat.unpair code
  decodeNatListAux p.1 p.2

theorem decodeNatListAux_encodeNatListAux (l : List ℕ) :
    decodeNatListAux l.length (encodeNatListAux l) = l := by
  induction l with
  | nil => rfl
  | cons x xs ih =>
      dsimp [encodeNatListAux, decodeNatListAux]
      rw [Nat.unpair_pair]
      dsimp
      rw [ih]

theorem decodeNatList_encodeNatList (l : List ℕ) :
    decodeNatList (encodeNatList l) = l := by
  dsimp [encodeNatList, decodeNatList]
  rw [Nat.unpair_pair]
  dsimp
  exact decodeNatListAux_encodeNatListAux l

def encodeQueryOpt (q : ℕ) : Option (Fin q × Fin q) → ℕ
  | none => 0
  | some (y, n) => Nat.pair y.val n.val + 1

def decodeQueryOpt (q : ℕ) (code : ℕ) : Option (Fin q × Fin q) :=
  match code with
  | 0 => none
  | c + 1 =>
      let p := Nat.unpair c
      if hy : p.1 < q then
        if hn : p.2 < q then
          some (⟨p.1, hy⟩, ⟨p.2, hn⟩)
        else none
      else none

theorem decodeQueryOpt_encodeQueryOpt (q : ℕ) (opt : Option (Fin q × Fin q)) :
    decodeQueryOpt q (encodeQueryOpt q opt) = opt := by
  cases opt with
  | none => rfl
  | some yn =>
      rcases yn with ⟨y, n⟩
      dsimp [encodeQueryOpt, decodeQueryOpt]
      rw [Nat.unpair_pair]
      dsimp
      split_ifs with h1 h2 <;> [rfl; omega; omega]

def encodeQueryTable (q : ℕ) (qt : Fin q → Option (Fin q × Fin q)) : ℕ :=
  encodeNatList (List.ofFn fun s => encodeQueryOpt q (qt s))

def decodeQueryTable (q : ℕ) (code : ℕ) : Fin q → Option (Fin q × Fin q) :=
  fun s =>
    let l := decodeNatList code
    decodeQueryOpt q (l.getD s.val 0)

theorem decodeQueryTable_encodeQueryTable (q : ℕ) (qt : Fin q → Option (Fin q × Fin q)) :
    decodeQueryTable q (encodeQueryTable q qt) = qt := by
  funext s
  dsimp [encodeQueryTable, decodeQueryTable]
  rw [decodeNatList_encodeNatList]
  have hlen : s.val < (List.ofFn fun s : Fin q => encodeQueryOpt q (qt s)).length := by
    rw [List.length_ofFn]
    exact s.isLt
  rw [List.getD_eq_getElem?_getD]
  rw [List.getElem?_eq_getElem hlen]
  dsimp [Option.getD]
  rw [List.getElem_ofFn]
  exact decodeQueryOpt_encodeQueryOpt q (qt s)

def encodeAction (k q : ℕ) (act : OracleLocalTransition k (Fin q)) : ℕ :=
  Nat.pair act.nextState.val
    (Nat.pair (encodeΓw act.queryWrite)
      (Nat.pair (encodeNatList ((List.ofFn act.workWrites).map encodeΓw))
        (Nat.pair (encodeΓw act.outputWrite)
          (Nat.pair (encodeDir3 act.inputDir)
            (Nat.pair (encodeDir3 act.queryDir)
              (Nat.pair (encodeNatList ((List.ofFn act.workDirs).map encodeDir3))
                (encodeDir3 act.outputDir)))))))

def decodeAction (k q : ℕ) (hq : 1 ≤ q) (code : ℕ) : OracleLocalTransition k (Fin q) where
  nextState :=
    let s_val := (Nat.unpair code).1
    ⟨if s_val < q then s_val else 0, by dsimp [s_val]; split_ifs with h <;> omega⟩
  queryWrite := decodeΓw (Nat.unpair (Nat.unpair code).2).1
  workWrites := fun i =>
    let l := decodeNatList (Nat.unpair (Nat.unpair (Nat.unpair code).2).2).1
    decodeΓw (l.getD i.val 0)
  outputWrite := decodeΓw (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair code).2).2).2).1
  inputDir := decodeDir3 (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair code).2).2).2).2).1
  queryDir := decodeDir3 (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair code).2).2).2).2).2).1
  workDirs := fun i =>
    let l := decodeNatList (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair code).2).2).2).2).2).2).1
    decodeDir3 (l.getD i.val 0)
  outputDir := decodeDir3 (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair (Nat.unpair code).2).2).2).2).2).2).2

theorem decodeAction_encodeAction (k q : ℕ) (hq : 1 ≤ q) (act : OracleLocalTransition k (Fin q)) :
    decodeAction k q hq (encodeAction k q act) = act := by
  rcases act with ⟨ns, qw, ww, ow, id, qd, wd, od⟩
  dsimp [encodeAction, decodeAction]
  simp only [Nat.unpair_pair]
  have hs : (if ns.val < q then ns.val else 0) = ns.val := by
    split_ifs with h <;> [rfl; omega]
  have hnext : (⟨if ns.val < q then ns.val else 0, by split_ifs with h <;> omega⟩ : Fin q) = ns := by
    ext
    exact hs
  rw [decodeNatList_encodeNatList]
  rw [decodeNatList_encodeNatList]
  have hww : (fun i : Fin k => decodeΓw (((List.ofFn ww).map encodeΓw).getD i.val 0)) = ww := by
    funext i
    have hlen : i.val < ((List.ofFn ww).map encodeΓw).length := by
      rw [List.length_map, List.length_ofFn]
      exact i.isLt
    rw [List.getD_eq_getElem?_getD]
    rw [List.getElem?_eq_getElem hlen]
    dsimp [Option.getD]
    rw [List.getElem_map, List.getElem_ofFn]
    exact decodeΓw_encodeΓw _
  have hwd : (fun i : Fin k => decodeDir3 (((List.ofFn wd).map encodeDir3).getD i.val 0)) = wd := by
    funext i
    have hlen : i.val < ((List.ofFn wd).map encodeDir3).length := by
      rw [List.length_map, List.length_ofFn]
      exact i.isLt
    rw [List.getD_eq_getElem?_getD]
    rw [List.getElem?_eq_getElem hlen]
    dsimp [Option.getD]
    rw [List.getElem_map, List.getElem_ofFn]
    exact decodeDir3_encodeDir3 _
  rw [decodeΓw_encodeΓw, decodeΓw_encodeΓw, decodeDir3_encodeDir3, decodeDir3_encodeDir3, decodeDir3_encodeDir3]
  rw [hww, hwd, hnext]

def consW (g : Γ) {k : ℕ} (tail : Fin k → Γ) : Fin (k + 1) → Γ :=
  fun i =>
    if h : i.val = 0 then g
    else tail ⟨i.val - 1, by omega⟩

theorem consW_tail {k : ℕ} (w : Fin (k + 1) → Γ) :
    consW (w ⟨0, Nat.zero_lt_succ k⟩) (fun i => w ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩) = w := by
  funext i
  dsimp [consW]
  split_ifs with h
  · have : i = ⟨0, Nat.zero_lt_succ k⟩ := Fin.ext h
    subst this
    rfl
  · congr 1
    ext
    dsimp
    omega

def encodeKFun : (k : ℕ) → ((Fin k → Γ) → ℕ) → ℕ
  | 0, f => f fun i => i.elim0
  | k + 1, f =>
      Nat.pair (encodeKFun k (fun tail => f (consW .zero tail)))
        (Nat.pair (encodeKFun k (fun tail => f (consW .one tail)))
          (Nat.pair (encodeKFun k (fun tail => f (consW .blank tail)))
            (encodeKFun k (fun tail => f (consW .start tail)))))

def decodeKFun : (k : ℕ) → ℕ → (Fin k → Γ) → ℕ
  | 0, code => fun _ => code
  | k + 1, code => fun w =>
      let p := Nat.unpair code
      let q := Nat.unpair p.2
      let r := Nat.unpair q.2
      let f0 := decodeKFun k p.1
      let f1 := decodeKFun k q.1
      let f2 := decodeKFun k r.1
      let f3 := decodeKFun k r.2
      match w ⟨0, Nat.zero_lt_succ k⟩ with
      | .zero  => f0 (fun i => w ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)
      | .one   => f1 (fun i => w ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)
      | .blank => f2 (fun i => w ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)
      | .start => f3 (fun i => w ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)

theorem decodeKFun_encodeKFun (k : ℕ) (f : (Fin k → Γ) → ℕ) :
    decodeKFun k (encodeKFun k f) = f := by
  induction k with
  | zero =>
      funext w
      dsimp [encodeKFun, decodeKFun]
      congr 1
      funext i
      exact i.elim0
  | succ k' ih =>
      funext w
      dsimp [encodeKFun, decodeKFun]
      rw [Nat.unpair_pair]
      dsimp
      rw [Nat.unpair_pair]
      dsimp
      rw [Nat.unpair_pair]
      dsimp
      rw [ih (fun tail => f (consW Γ.zero tail))]
      rw [ih (fun tail => f (consW Γ.one tail))]
      rw [ih (fun tail => f (consW Γ.blank tail))]
      rw [ih (fun tail => f (consW Γ.start tail))]
      have hw := consW_tail w
      cases h0 : w ⟨0, Nat.zero_lt_succ k'⟩ <;> {
        have hcopy := hw
        rw [h0] at hcopy
        have htarget : (match w ⟨0, Nat.zero_lt_succ k'⟩ with
          | Γ.zero => f (consW Γ.zero fun i => w ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)
          | Γ.one => f (consW Γ.one fun i => w ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)
          | Γ.blank => f (consW Γ.blank fun i => w ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)
          | Γ.start => f (consW Γ.start fun i => w ⟨i.val + 1, Nat.succ_lt_succ i.isLt⟩)) = f w := by
          rw [h0]
          exact congrArg f hcopy
        exact htarget
      }

def encodeΓ4 (f : Γ → ℕ) : ℕ :=
  Nat.pair (f .zero) (Nat.pair (f .one) (Nat.pair (f .blank) (f .start)))

def decodeΓ4 (code : ℕ) : Γ → ℕ :=
  let p := Nat.unpair code
  let q := Nat.unpair p.2
  let r := Nat.unpair q.2
  fun g =>
    match g with
    | .zero  => p.1
    | .one   => q.1
    | .blank => r.1
    | .start => r.2

theorem decodeΓ4_encodeΓ4 (f : Γ → ℕ) : decodeΓ4 (encodeΓ4 f) = f := by
  funext g
  dsimp [encodeΓ4, decodeΓ4]
  rw [Nat.unpair_pair]
  dsimp
  rw [Nat.unpair_pair]
  dsimp
  rw [Nat.unpair_pair]
  dsimp
  cases g <;> rfl

def fixRightOfStart (k q : ℕ)
    (lt : Fin q → Γ → Γ → (Fin k → Γ) → Γ → OracleLocalTransition k (Fin q)) :
    Fin q → Γ → Γ → (Fin k → Γ) → Γ → OracleLocalTransition k (Fin q) :=
  fun s iHead qHead wHeads oHead =>
    let act := lt s iHead qHead wHeads oHead
    { act with
      inputDir := if iHead = Γ.start then Dir3.right else act.inputDir
      queryDir := if qHead = Γ.start then Dir3.right else act.queryDir
      workDirs := fun i => if wHeads i = Γ.start then Dir3.right else act.workDirs i
      outputDir := if oHead = Γ.start then Dir3.right else act.outputDir }

theorem fixRightOfStart_satisfies (k q : ℕ)
    (lt : Fin q → Γ → Γ → (Fin k → Γ) → Γ → OracleLocalTransition k (Fin q)) :
    ∀ (s : Fin q) (inputHead queryHead : Γ) (workHeads : Fin k → Γ) (outputHead : Γ),
      let transition := fixRightOfStart k q lt s inputHead queryHead workHeads outputHead
      (inputHead = Γ.start → transition.inputDir = Dir3.right) ∧
      (queryHead = Γ.start → transition.queryDir = Dir3.right) ∧
      (∀ index, workHeads index = Γ.start → transition.workDirs index = Dir3.right) ∧
      (outputHead = Γ.start → transition.outputDir = Dir3.right) := by
  intro s inputHead queryHead workHeads outputHead
  dsimp [fixRightOfStart]
  refine ⟨?_, ?_, ?_, ?_⟩
  · intro hi; simp [hi]
  · intro hq; simp [hq]
  · intro idx hw; simp [hw]
  · intro ho; simp [ho]

theorem fixRightOfStart_eq (k q : ℕ)
    (lt : Fin q → Γ → Γ → (Fin k → Γ) → Γ → OracleLocalTransition k (Fin q))
    (h : ∀ (s : Fin q) (inputHead queryHead : Γ) (workHeads : Fin k → Γ) (outputHead : Γ),
      let transition := lt s inputHead queryHead workHeads outputHead
      (inputHead = Γ.start → transition.inputDir = Dir3.right) ∧
      (queryHead = Γ.start → transition.queryDir = Dir3.right) ∧
      (∀ index, workHeads index = Γ.start → transition.workDirs index = Dir3.right) ∧
      (outputHead = Γ.start → transition.outputDir = Dir3.right)) :
    fixRightOfStart k q lt = lt := by
  funext s iHead qHead wHeads oHead
  dsimp [fixRightOfStart]
  have h_spec := h s iHead qHead wHeads oHead
  rcases h_spec with ⟨hi, hq, hw, ho⟩
  have hi_eq : (if iHead = Γ.start then Dir3.right else (lt s iHead qHead wHeads oHead).inputDir) =
      (lt s iHead qHead wHeads oHead).inputDir := by
    split_ifs with h_if <;> [exact (hi h_if).symm; rfl]
  have hq_eq : (if qHead = Γ.start then Dir3.right else (lt s iHead qHead wHeads oHead).queryDir) =
      (lt s iHead qHead wHeads oHead).queryDir := by
    split_ifs with h_if <;> [exact (hq h_if).symm; rfl]
  have hw_eq : (fun i => if wHeads i = Γ.start then Dir3.right else (lt s iHead qHead wHeads oHead).workDirs i) =
      (lt s iHead qHead wHeads oHead).workDirs := by
    funext i
    split_ifs with h_if <;> [exact (hw i h_if).symm; rfl]
  have ho_eq : (if oHead = Γ.start then Dir3.right else (lt s iHead qHead wHeads oHead).outputDir) =
      (lt s iHead qHead wHeads oHead).outputDir := by
    split_ifs with h_if <;> [exact (ho h_if).symm; rfl]
  rw [hi_eq, hq_eq, hw_eq, ho_eq]

def encodeLocal (k q : ℕ) (lt : Fin q → Γ → Γ → (Fin k → Γ) → Γ → OracleLocalTransition k (Fin q)) : ℕ :=
  encodeNatList (List.ofFn fun s =>
    encodeΓ4 fun iHead =>
      encodeΓ4 fun qHead =>
        encodeΓ4 fun oHead =>
          encodeKFun k fun wHeads =>
            encodeAction k q (lt s iHead qHead wHeads oHead))

def decodeLocalRaw (k q : ℕ) (hq : 1 ≤ q) (code : ℕ) :
    Fin q → Γ → Γ → (Fin k → Γ) → Γ → OracleLocalTransition k (Fin q) :=
  fun s iHead qHead wHeads oHead =>
    let slist := decodeNatList code
    let scode := slist.getD s.val 0
    let icode := decodeΓ4 scode iHead
    let qcode := decodeΓ4 icode qHead
    let ocode := decodeΓ4 qcode oHead
    let actCode := decodeKFun k ocode wHeads
    decodeAction k q hq actCode

def decodeLocal (k q : ℕ) (hq : 1 ≤ q) (code : ℕ) :
    Fin q → Γ → Γ → (Fin k → Γ) → Γ → OracleLocalTransition k (Fin q) :=
  fixRightOfStart k q (decodeLocalRaw k q hq code)

theorem decodeLocal_encodeLocal (k q : ℕ) (hq : 1 ≤ q)
    (lt : Fin q → Γ → Γ → (Fin k → Γ) → Γ → OracleLocalTransition k (Fin q))
    (hlt : ∀ (s : Fin q) (inputHead queryHead : Γ) (workHeads : Fin k → Γ) (outputHead : Γ),
      let transition := lt s inputHead queryHead workHeads outputHead
      (inputHead = Γ.start → transition.inputDir = Dir3.right) ∧
      (queryHead = Γ.start → transition.queryDir = Dir3.right) ∧
      (∀ index, workHeads index = Γ.start → transition.workDirs index = Dir3.right) ∧
      (outputHead = Γ.start → transition.outputDir = Dir3.right)) :
    decodeLocal k q hq (encodeLocal k q lt) = lt := by
  dsimp [decodeLocal]
  have hraw : decodeLocalRaw k q hq (encodeLocal k q lt) = lt := by
    funext s iHead qHead wHeads oHead
    dsimp [encodeLocal, decodeLocalRaw]
    rw [decodeNatList_encodeNatList]
    have hlen : s.val < (List.ofFn fun s : Fin q =>
        encodeΓ4 fun iHead =>
          encodeΓ4 fun qHead =>
            encodeΓ4 fun oHead =>
              encodeKFun k fun wHeads =>
                encodeAction k q (lt s iHead qHead wHeads oHead)).length := by
      rw [List.length_ofFn]
      exact s.isLt
    rw [List.getD_eq_getElem?_getD]
    rw [List.getElem?_eq_getElem hlen]
    dsimp [Option.getD]
    rw [List.getElem_ofFn]
    rw [decodeΓ4_encodeΓ4]
    rw [decodeΓ4_encodeΓ4]
    rw [decodeΓ4_encodeΓ4]
    rw [decodeKFun_encodeKFun]
    rw [decodeAction_encodeAction]
  rw [hraw]
  exact fixRightOfStart_eq k q lt hlt

def defaultClockedOracleTM : ClockedOracleTM where
  k := 0
  m := {
    Q := Fin 2
    decEq := inferInstance
    finQ := inferInstance
    qstart := ⟨0, by omega⟩
    qhalt := ⟨1, by omega⟩
    queryTransition := fun _ => none
    localTransition := fun _ _ _ _ _ =>
      { nextState := ⟨1, by omega⟩
        queryWrite := .blank
        workWrites := fun i => i.elim0
        outputWrite := .blank
        inputDir := .right
        queryDir := .right
        workDirs := fun i => i.elim0
        outputDir := .right }
    localTransition_right_of_start := by
      intro s iHead qHead wHeads oHead
      refine ⟨fun _ => rfl, fun _ => rfl, fun i _ => i.elim0, fun _ => rfl⟩
  }
  C := 1
  d := 0
  hC := Nat.le_refl 1

def encode (M : CanonicalClockedOracleTM) : ℕ :=
  Nat.pair M.k
    (Nat.pair M.q
      (Nat.pair M.qstart.val
        (Nat.pair M.qhalt.val
          (Nat.pair (encodeQueryTable M.q M.queryTransition)
            (Nat.pair (encodeLocal M.k M.q M.localTransition)
              (Nat.pair M.C M.d))))))

def makeDecodedTM (k q : ℕ) (hq : 1 ≤ q) (qstart_val qhalt_val : ℕ)
    (hstart : qstart_val < q) (hhalt : qhalt_val < q)
    (code_Q code_L C d : ℕ) (hC : 1 ≤ C) : ClockedOracleTM where
  k := k
  m := {
    Q := Fin q
    decEq := inferInstance
    finQ := inferInstance
    qstart := ⟨qstart_val, hstart⟩
    qhalt := ⟨qhalt_val, hhalt⟩
    queryTransition := decodeQueryTable q code_Q
    localTransition := decodeLocal k q hq code_L
    localTransition_right_of_start := fixRightOfStart_satisfies k q _
  }
  C := C
  d := d
  hC := hC

theorem makeDecodedTM_eq (M : CanonicalClockedOracleTM) :
    makeDecodedTM M.k M.q M.hq M.qstart.val M.qhalt.val M.qstart.isLt M.qhalt.isLt
      (encodeQueryTable M.q M.queryTransition)
      (encodeLocal M.k M.q M.localTransition)
      M.C M.d M.hC = M.toClockedOracleTM := by
  have hqs : (⟨M.qstart.val, M.qstart.isLt⟩ : Fin M.q) = M.qstart := rfl
  have hqh : (⟨M.qhalt.val, M.qhalt.isLt⟩ : Fin M.q) = M.qhalt := rfl
  have hqt := decodeQueryTable_encodeQueryTable M.q M.queryTransition
  have hlt := decodeLocal_encodeLocal M.k M.q M.hq M.localTransition M.localTransition_right_of_start
  apply ClockedOracleTM.ext_same_k
  · exact OracleTM.ext_fin hqs hqh hqt hlt
  · rfl
  · rfl

def decode (code : ℕ) : ClockedOracleTM :=
  let p1 := Nat.unpair code
  let k := p1.1
  let p2 := Nat.unpair p1.2
  let q := p2.1
  let p3 := Nat.unpair p2.2
  let qstart_val := p3.1
  let p4 := Nat.unpair p3.2
  let qhalt_val := p4.1
  let p5 := Nat.unpair p4.2
  let code_Q := p5.1
  let p6 := Nat.unpair p5.2
  let code_L := p6.1
  let p7 := Nat.unpair p6.2
  let C := p7.1
  let d := p7.2
  if hq : 1 ≤ q then
    if hstart : qstart_val < q then
      if hhalt : qhalt_val < q then
        if hC : 1 ≤ C then
          makeDecodedTM k q hq qstart_val qhalt_val hstart hhalt code_Q code_L C d hC
        else defaultClockedOracleTM
      else defaultClockedOracleTM
    else defaultClockedOracleTM
  else defaultClockedOracleTM

theorem decode_encode (M : CanonicalClockedOracleTM) :
    decode (encode M) = M.toClockedOracleTM := by
  dsimp only [encode, decode]
  rw [Nat.unpair_pair]
  dsimp only
  rw [Nat.unpair_pair]
  dsimp only
  rw [Nat.unpair_pair]
  dsimp only
  rw [Nat.unpair_pair]
  dsimp only
  rw [Nat.unpair_pair]
  dsimp only
  rw [Nat.unpair_pair]
  dsimp only
  rw [Nat.unpair_pair]
  dsimp only
  rw [dite_eq_left M.hq]
  rw [dite_eq_left M.qstart.isLt]
  rw [dite_eq_left M.qhalt.isLt]
  rw [dite_eq_left M.hC]
  exact makeDecodedTM_eq M

theorem canonical_representation_complete (M : ClockedOracleTM) :
    ∃ i : ℕ, ∀ (oracle : BooleanOracle) (L : Language),
      M.Decides oracle L → (decode i).Decides oracle L := by
  refine ⟨encode M.toCanonical, ?_⟩
  intro oracle L hdec
  rw [decode_encode]
  rw [toCanonical_toClockedOracleTM]
  exact M.normalize_decides oracle L hdec

theorem bgs_separation : ∃ B : Language, PRel B ≠ NPRel B := by
  refine ⟨bgsOracle decode, ?_⟩
  intro heq
  have hnot : unaryWitnessLang (bgsOracle decode) ∉ PRel (bgsOracle decode) := by
    intro hP
    rw [PRel_iff_exists_clocked] at hP
    obtain ⟨M, hM⟩ := hP
    obtain ⟨i, hi⟩ := canonical_representation_complete M
    have hdec_i := hi (oracleOf (bgsOracle decode)) (unaryWitnessLang (bgsOracle decode)) hM
    exact not_decides_stage decode i hdec_i
  have hin : unaryWitnessLang (bgsOracle decode) ∈ NPRel (bgsOracle decode) :=
    Stage3A.unaryWitnessLang_mem_NPRel (bgsOracle decode)
  rw [← heq] at hin
  exact hnot hin

end Stage3Separation
