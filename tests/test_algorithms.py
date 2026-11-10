
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

    def test_result_metrics(self):
        result = simulate_fifo([1, 1, 2], 2)

        self.assertEqual(result["total_references"], 3)
        self.assertEqual(result["page_hits"], 1)
        self.assertEqual(result["page_faults"], 2)
        self.assertEqual(result["hit_rate"], round(1 / 3, 4))
        self.assertEqual(result["fault_rate"], round(2 / 3, 4))

    def test_frame_history(self):
        result = simulate_fifo([1, 2, 1], 2)

        self.assertEqual(result["history"][0]["frames"], [1])
        self.assertEqual(result["history"][1]["frames"], [1, 2])
        self.assertEqual(result["history"][2]["frames"], [1, 2])
        self.assertTrue(result["history"][2]["hit"])

    def test_optimal_replaces_page_not_used_again(self):
        result = simulate_optimal([1, 2, 3, 1, 2, 4], 3)

        self.assertEqual(result["history"][5]["frames"], [4, 2, 3])
        self.assertEqual(result["page_faults"], 4)


if __name__ == "__main__":
    unittest.main()
