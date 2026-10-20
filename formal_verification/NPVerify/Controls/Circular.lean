import Mathlib
-- Circular: assumes the goal as a hypothesis. Kernel accepts it, but it is vacuous and must be flagged.
theorem ctrl_circ (P : Prop) (h : P) : P := h
-- Cheating with sorry: kernel accepts with warning; axiom audit must catch sorryAx.
theorem ctrl_sorry : ∀ n : ℕ, n = n + 1 := by sorry
#print axioms ctrl_sorry
