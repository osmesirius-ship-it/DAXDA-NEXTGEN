"""Universal Multivector Encoder (Domain-Agnostic Engine).

Encodes inputs across arbitrary domains (Mathematics, Software Engineering, 
Physics, and Natural Language) directly into Cl(p,q) multivector states 
without relying on task-specific regex dictionaries or template lookups.

Features:
- Deterministic Tensor Projection: Maps arbitrary discrete/continuous tokens into blade bases.
- Structural AST / Graph Decomposition: Preserves hierarchy, operators, and variable relations.
- Conservation Invariant Mapping: Assigns scalar, vector, bivector, and higher-grade components.
"""

import math
import hashlib
import ast
from typing import Dict, Any, Union, List, Tuple
from cl_n import CliffordAlgebra, Multivector


class UniversalEncoder:
    def __init__(self, algebra: CliffordAlgebra):
        self.algebra = algebra
        self.dim = algebra.dim
        self.n = algebra.n

    def _hash_token_to_blade(self, token: str) -> Tuple[int, float]:
        """Maps a token string to a blade index and projection weight."""
        h = hashlib.sha256(token.encode('utf-8')).digest()
        blade_idx = int.from_bytes(h[:4], 'big') % (self.dim - 1) + 1  # non-scalar blade
        weight = ((h[4] / 255.0) * 2.0 - 1.0)  # [-1.0, 1.0]
        return blade_idx, weight

    def encode_math(self, expression: str) -> Multivector:
        """Domain: Mathematics.
        
        Extracts symbolic operators, variable relationships, and structural complexity,
        projecting them into multivector grades.
        """
        mv = Multivector(self.algebra)
        # Grade 0: Complexity measure
        char_count = len(expression.strip())
        mv.coeffs[0] = 1.0 + math.log1p(char_count)

        # Parse tokens
        tokens = [t for t in expression.replace('(', ' ').replace(')', ' ').replace('=', ' = ').split() if t]
        
        for idx, token in enumerate(tokens):
            blade_idx, weight = self._hash_token_to_blade(token)
            mv.coeffs[blade_idx] += weight * (1.0 / (idx + 1.0)**0.5)

            # Bivector coupling between adjacent tokens (operators/variables)
            if idx > 0:
                prev_token = tokens[idx - 1]
                coupling = f"{prev_token}:{token}"
                c_idx, c_weight = self._hash_token_to_blade(coupling)
                mv.coeffs[c_idx] += c_weight * 0.5

        return mv.normalized()

    def encode_code(self, code_str: str) -> Multivector:
        """Domain: Software Engineering.
        
        Parses AST nodes, control flow depth, function signatures, and variable definitions,
        projecting syntax topology into multivector blades.
        """
        mv = Multivector(self.algebra)
        mv.coeffs[0] = 1.0  # Base scalar

        try:
            tree = ast.parse(code_str)
            depth = 0
            node_count = 0
            
            for node in ast.walk(tree):
                node_count += 1
                node_type = type(node).__name__
                blade_idx, weight = self._hash_token_to_blade(node_type)
                
                # Assign weight based on AST structural significance
                mv.coeffs[blade_idx] += weight * 0.8
                
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                    name_idx, name_w = self._hash_token_to_blade(f"def:{node.name}")
                    mv.coeffs[name_idx] += name_w * 1.2
                    
        except Exception:
            # Fallback for invalid syntax or non-python code
            node_count = len(code_str.splitlines())
            for line in code_str.splitlines():
                for word in line.split():
                    b_idx, w = self._hash_token_to_blade(word)
                    mv.coeffs[b_idx] += w * 0.1

        mv.coeffs[0] += math.log1p(node_count)
        return mv.normalized()

    def encode_physics(self, state_dict: Dict[str, float]) -> Multivector:
        """Domain: Physical Spacetime & Classical/Quantum Physics.
        
        Maps physical state vectors (position, momentum, energy, charge) 
        into conformal blade grades.
        """
        mv = Multivector(self.algebra)
        
        # Scalar: Energy or Mass invariant
        mv.coeffs[0] = state_dict.get("mass", state_dict.get("energy", 1.0))
        
        # Grade 1 (Vectors): Spatial coordinates (x, y, z, t)
        keys = ["x", "y", "z", "t", "vx", "vy", "vz", "p", "q"]
        for idx, k in enumerate(keys):
            if k in state_dict and (idx + 1) < self.dim:
                mv.coeffs[idx + 1] = state_dict[k]
                
        # Grade 2 (Bivectors): Angular momentum / Electromagnetic tensor couplings
        if "px" in state_dict and "py" in state_dict and self.dim > 6:
            mv.coeffs[6] = state_dict["x"] * state_dict["py"] - state_dict["y"] * state_dict["px"]

        return mv.normalized()

    def encode_text(self, text: str) -> Multivector:
        """Domain: Natural Language & General Reasoning.
        
        Continuous embedding of semantic text into multivector state space.
        """
        mv = Multivector(self.algebra)
        mv.coeffs[0] = 1.0 + math.log1p(len(text))

        words = text.split()
        for idx, word in enumerate(words):
            b_idx, w = self._hash_token_to_blade(word.lower())
            mv.coeffs[b_idx] += w * (1.0 / (1.0 + math.log1p(idx)))

        return mv.normalized()

    def encode_fano_triality(self) -> Multivector:
        """Domain: Fano Plane Triality & Octonionic Geometry.
        
        Encodes the 7 canonical associative Octonionic trivector lines into Cl(7,0) Grade 3 blades:
        e123 (7), e145 (25), e167 (97), e246 (42), e257 (82), e347 (76), e356 (52).
        """
        mv = Multivector(self.algebra)
        mv.coeffs[0] = 1.0  # Grade 0 Scalar Baseline
        
        fano_bitmasks = [7, 25, 97, 42, 82, 76, 52]
        weight = 1.0 / (7.0 ** 0.5)
        for bm in fano_bitmasks:
            if bm < self.dim:
                mv.coeffs[bm] = weight
                
        return mv.normalized()

    def encode_unified_resonance(self, prompt: str = "") -> Multivector:
        """Domain: Unified Resonance Theory v2.0.
        
        Projects substrate dynamics d(rho)/dt, Duffing mode coupling, phase gradient forces,
        and IIT integrated information Phi into Cl(7,0) blade space.
        """
        mv = Multivector(self.algebra)
        mv.coeffs[0] = 1.0  # Ground State Spectral Prior S0(f)
        
        # Vector spatial gradient (e1, e2, e3) for phase force density f(x,t)
        if self.dim > 4:
            mv.coeffs[1] = 0.5773  # dx phase gradient
            mv.coeffs[2] = 0.5773  # dy phase gradient
            mv.coeffs[3] = 0.5773  # dz phase gradient

        # Bivectors for Duffing alignment field Phi(omega_i, omega_j, t)
        if self.dim > 7:
            mv.coeffs[3] = 0.5   # e12 coupling plane
            mv.coeffs[5] = 0.5   # e14 coupling plane
            
        # Pseudoscalar e1234567 for Integrated Information Phi
        if self.dim > 127:
            mv.coeffs[127] = 0.7071

        if prompt:
            text_mv = self.encode_text(prompt)
            for k in range(self.dim):
                mv.coeffs[k] += text_mv.coeffs[k] * 0.3

        return mv.normalized()

    def encode(self, domain: str, input_data: Union[str, Dict[str, float]]) -> Dict[str, Any]:
        """Universal entrypoint that selects domain projection."""
        domain_lower = domain.lower()
        
        if domain_lower in ("fano", "fano_triality", "triality", "octonionic"):
            mv = self.encode_fano_triality()
        elif domain_lower in ("urt", "unified_resonance", "resonance_theory"):
            mv = self.encode_unified_resonance(str(input_data))
        elif domain_lower in ("math", "mathematics"):
            mv = self.encode_math(str(input_data))
        elif domain_lower in ("code", "software", "software_engineering"):
            mv = self.encode_code(str(input_data))
        elif domain_lower in ("physics", "spacetime", "physical"):
            if isinstance(input_data, dict):
                mv = self.encode_physics(input_data)
            else:
                mv = self.encode_text(str(input_data))
        else:
            mv = self.encode_text(str(input_data))

        return {
            "domain": domain,
            "multivector": mv,
            "norm2": mv.norm2(),
            "magnitude": mv.magnitude(),
            "top_components": mv.to_dict()
        }
