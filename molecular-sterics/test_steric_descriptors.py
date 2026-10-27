"""Local unit tests with mock descriptor calculators; NOT scientific benchmarks."""
import unittest
from steric_descriptors import compute_descriptors, find_metal_index, parse_indices


class FakeBuried:
    def __init__(self, elements, coords, index, excluded_atoms=None, radius=None):
        assert index == 1 and excluded_atoms == [4] and radius == 3.5
        self.fraction_buried_volume = 0.42


class FakeCone:
    def __init__(self, elements, coords, index):
        assert index == 1 and list(elements) == ["Pd", "P", "C"]
        self.cone_angle = 120.0


class TestMorfeusAdapter(unittest.TestCase):
    def test_indices(self):
        self.assertEqual(parse_indices("2,3"), [2, 3])
        with self.assertRaises(ValueError):parse_indices("2,2")
        self.assertEqual(find_metal_index(["Pd", "P", "C"], "Pd"), 1)

    def test_call_pattern(self):
        x = compute_descriptors(["Pd", "P", "C", "H"], [(0,0,0)]*4,
                                "Pd", "2,3", 3.5, FakeBuried, FakeCone)
        self.assertEqual(x["buried_volume_percent"], 42.0)
        self.assertEqual(x["cone_angle_degrees"], 120.0)


if __name__ == "__main__": unittest.main()
