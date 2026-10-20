import Mathlib
theorem ctrl_true (a b : ℕ) : a + b = b + a := Nat.add_comm a b
#print axioms ctrl_true
