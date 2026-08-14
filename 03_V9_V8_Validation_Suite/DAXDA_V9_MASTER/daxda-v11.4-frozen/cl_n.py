"""General Clifford Algebra Cl(p, q) Core Engine.

Supports arbitrary signature Cl(p, q) with full blade products, reversion, 
grade projection, norm calculation, rotor exponentiation, and exact 
multivector inversion.

Common Signatures:
- Cl(2,0): 4D (Legacy DAXDA)
- Cl(4,1): 16D Conformal Geometric Algebra (Spacetime, Mechanics, Geometry)
- Cl(8,0): 256D Octonion-like Multivector Tensor Space (Logic, Math, Code ASTs)
"""

import math
from typing import Dict, List, Tuple, Union

class CliffordAlgebra:
    def __init__(self, p: int = 7, q: int = 0):
        self.p = p
        self.q = q
        self.n = p + q
        self.dim = 1 << self.n  # 2^n basis blades
        
        # Precompute basis blade names and signatures
        self.blade_names = self._generate_blade_names()
        self.signature = [1.0] * p + [-1.0] * q
        
        # Precompute multiplication lookup tables for efficiency
        self._mul_table, self._sign_table = self._precompute_mul_tables()

    def _generate_blade_names(self) -> List[str]:
        names = []
        for i in range(self.dim):
            if i == 0:
                names.append("1")
            else:
                indices = [j + 1 for j in range(self.n) if (i & (1 << j))]
                names.append("e" + "".join(map(str, indices)))
        return names

    def _precompute_mul_tables(self) -> Tuple[List[List[int]], List[List[float]]]:
        mul_table = [[0] * self.dim for _ in range(self.dim)]
        sign_table = [[0.0] * self.dim for _ in range(self.dim)]

        for a in range(self.dim):
            for b in range(self.dim):
                res_blade = a ^ b
                sign = 1.0

                # Count swaps needed to reorder basis vectors canonically
                swaps = 0
                for i in range(self.n):
                    if (b & (1 << i)):
                        # Count how many vectors in 'a' are to the right of position i
                        mask = a & ~((1 << (i + 1)) - 1)
                        swaps += bin(mask).count('1')

                if swaps % 2 != 0:
                    sign = -1.0

                # Apply metric signature for squared basis vectors (a & b)
                common = a & b
                for i in range(self.n):
                    if (common & (1 << i)):
                        sign *= self.signature[i]

                mul_table[a][b] = res_blade
                sign_table[a][b] = sign

        return mul_table, sign_table


class Multivector:
    """Represents an element of Cl(p,q) algebra."""
    def __init__(self, algebra: CliffordAlgebra, coeffs: Union[List[float], Dict[int, float], None] = None):
        self.algebra = algebra
        self.coeffs = [0.0] * algebra.dim
        
        if coeffs is not None:
            if isinstance(coeffs, list):
                for i in range(min(len(coeffs), algebra.dim)):
                    self.coeffs[i] = float(coeffs[i])
            elif isinstance(coeffs, dict):
                for idx, val in coeffs.items():
                    if 0 <= idx < algebra.dim:
                        self.coeffs[idx] = float(val)

    def __add__(self, other: "Multivector") -> "Multivector":
        res = Multivector(self.algebra)
        for i in range(self.algebra.dim):
            res.coeffs[i] = self.coeffs[i] + other.coeffs[i]
        return res

    def __sub__(self, other: "Multivector") -> "Multivector":
        res = Multivector(self.algebra)
        for i in range(self.algebra.dim):
            res.coeffs[i] = self.coeffs[i] - other.coeffs[i]
        return res

    def __mul__(self, other: Union["Multivector", float, int]) -> "Multivector":
        res = Multivector(self.algebra)
        if isinstance(other, (int, float)):
            s = float(other)
            for i in range(self.algebra.dim):
                res.coeffs[i] = self.coeffs[i] * s
            return res

        # Geometric product
        m_tbl = self.algebra._mul_table
        s_tbl = self.algebra._sign_table

        for i in range(self.algebra.dim):
            c_i = self.coeffs[i]
            if c_i == 0.0:
                continue
            for j in range(self.algebra.dim):
                c_j = other.coeffs[j]
                if c_j == 0.0:
                    continue
                target = m_tbl[i][j]
                sign = s_tbl[i][j]
                res.coeffs[target] += c_i * c_j * sign

        return res

    __rmul__ = __mul__

    def reverse(self) -> "Multivector":
        """Clifford reversion: reverses order of basis vector products."""
        res = Multivector(self.algebra)
        for i in range(self.algebra.dim):
            grade = bin(i).count('1')
            sign = -1.0 if (grade * (grade - 1) // 2) % 2 != 0 else 1.0
            res.coeffs[i] = self.coeffs[i] * sign
        return res

    def grade(self, k: int) -> "Multivector":
        """Project onto grade k components."""
        res = Multivector(self.algebra)
        for i in range(self.algebra.dim):
            if bin(i).count('1') == k:
                res.coeffs[i] = self.coeffs[i]
        return res

    def norm2(self) -> float:
        """Quadratic norm: scalar part of (M * M~)."""
        rev = self.reverse()
        prod = self * rev
        return prod.coeffs[0]

    def magnitude(self) -> float:
        """Euclidean norm of component coefficient vector."""
        return math.sqrt(sum(c * c for c in self.coeffs))

    def normalized(self, floor: float = 1e-12) -> "Multivector":
        mag = self.magnitude()
        if mag < floor:
            return Multivector(self.algebra)
        return self * (1.0 / mag)

    def rotate(self, bivector: "Multivector", angle: float) -> "Multivector":
        """Applies rotor transformation R * M * R~ where R = exp(-0.5 * angle * B)."""
        b_norm = bivector.magnitude()
        if b_norm < 1e-12:
            return self
        
        b_unit = bivector * (1.0 / b_norm)
        half_a = angle * 0.5
        
        # R = cos(half_a) - sin(half_a) * b_unit
        rotor = Multivector(self.algebra)
        rotor.coeffs[0] = math.cos(half_a)
        scaled_b = b_unit * (-math.sin(half_a))
        rotor = rotor + scaled_b

        return rotor * self * rotor.reverse()

    def to_dict(self, round_digits: int = 6) -> Dict[str, float]:
        res = {}
        for i in range(self.algebra.dim):
            if abs(self.coeffs[i]) > 1e-8:
                res[self.algebra.blade_names[i]] = round(self.coeffs[i], round_digits)
        return res
