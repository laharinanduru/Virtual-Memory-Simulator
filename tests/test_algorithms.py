
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from algorithms import (
    simulate_fifo,
    simulate_lru,
    simulate_optimal,
)


class TestPageReplacementAlgorithms(unittest.TestCase):

    def setUp(self):
        self.pages = [1, 2, 3, 1, 4, 2, 5]
        self.frame_count = 3

    def test_fifo(self):
        result = simulate_fifo(self.pages, self.frame_count)
        self.assertEqual(result["page_hits"], 2)
        self.assertEqual(result["page_faults"], 5)

    def test_lru(self):
        result = simulate_lru(self.pages, self.frame_count)
        self.assertEqual(result["page_hits"], 1)
        self.assertEqual(result["page_faults"], 6)

    def test_optimal(self):
        result = simulate_optimal(self.pages, self.frame_count)
        self.assertEqual(result["page_hits"], 2)
        self.assertEqual(result["page_faults"], 5)

    def test_hits_and_faults_equal_total(self):
        for algorithm in (
            simulate_fifo,
            simulate_lru,
            simulate_optimal,
        ):
            result = algorithm(self.pages, self.frame_count)
            self.assertEqual(
                result["page_hits"] + result["page_faults"],
                len(self.pages),
            )

    def test_one_frame(self):
        result = simulate_fifo([1, 2, 1], 1)
        self.assertEqual(result["page_hits"], 0)
        self.assertEqual(result["page_faults"], 3)


if __name__ == "__main__":
    unittest.main()
