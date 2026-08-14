import math, unittest
from cl20 import MV

class TestCl20(unittest.TestCase):
    def test_basis_squares(self):
        self.assertEqual(MV(e1=1)*MV(e1=1), MV(s=1))
        self.assertEqual(MV(e2=1)*MV(e2=1), MV(s=1))
        self.assertEqual(MV(e12=1)*MV(e12=1), MV(s=-1))
    def test_anticommutation(self):
        self.assertEqual(MV(e1=1)*MV(e2=1), MV(e12=1))
        self.assertEqual(MV(e2=1)*MV(e1=1), MV(e12=-1))
    def test_reversion(self):
        x=MV(1,2,3,4)
        self.assertEqual(x.reverse(),MV(1,2,3,-4))
    def test_rotor_preserves_vector_norm(self):
        v=MV(e1=2,e2=-3); r=v.rotate(math.pi/3)
        self.assertAlmostEqual(v.norm2(),r.norm2(),places=10)

if __name__=="__main__": unittest.main()

