import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app import app


class TestFlaskAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/api/health")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Backend is running", response.get_json()["status"])

    def test_tutor_page_fault(self):
        response = self.client.post(
            "/api/tutor",
            json={"question": "page fault"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("answer", data)
        self.assertTrue(len(data["answer"]) > 0)
        self.assertIn("page", data["answer"].lower())

    def test_tutor_empty_question(self):
        response = self.client.post(
            "/api/tutor",
            json={"question": ""}
        )
        self.assertEqual(response.status_code, 400)

    def test_analyze(self):
        response = self.client.post(
            "/api/analyze",
            json={
                "question": "Which algorithm performed best?",
                "comparison": [
                    {"algorithm": "FIFO", "page_faults": 5, "page_hits": 2, "fault_rate": 71.4},
                    {"algorithm": "LRU", "page_faults": 6, "page_hits": 1, "fault_rate": 85.7},
                    {"algorithm": "OPTIMAL", "page_faults": 4, "page_hits": 3, "fault_rate": 57.1}
                ]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("answer", data)
        self.assertIn("OPTIMAL", data["answer"])

    def test_simulate(self):
        response = self.client.post(
            "/api/simulate",
            json={
                "pages": [1, 2, 3, 1, 4],
                "frames": 3,
                "algorithm": "FIFO"
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["algorithm"], "FIFO")
        self.assertIn("page_faults", data)

    def test_simulate_8bit_addresses(self):
        # 8-bit binary addresses: 4-bit page + 4-bit offset
        # "00010010" -> Page 1, Offset 2
        # "00100011" -> Page 2, Offset 3
        response = self.client.post(
            "/api/simulate",
            json={
                "addresses": ["00010010", "00100011", "00010100"],
                "frames": 3,
                "algorithm": "LRU"
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("translations", data)
        self.assertEqual(data["translations"][0]["page_number"], 1)
        self.assertEqual(data["translations"][0]["offset"], 2)
        self.assertIn("physical_address", data["history"][0])

    def test_compare_custom_selected_algorithms_with_pages(self):
        response = self.client.post(
            "/api/compare",
            json={
                "pages": [1, 2, 3, 1, 4, 2],
                "frames": 3,
                "algorithms": ["FIFO", "LRU"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["selected_algorithms"], ["FIFO", "LRU"])
        self.assertIn("FIFO", data["comparison"])
        self.assertIn("LRU", data["comparison"])
        self.assertNotIn("OPTIMAL", data["comparison"])

    def test_compare_custom_selected_algorithms_with_addresses(self):
        response = self.client.post(
            "/api/compare",
            json={
                "addresses": ["00010000", "00100000", "00010000"],
                "frames": 2,
                "algorithms": ["LRU", "OPTIMAL"]
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["selected_algorithms"], ["LRU", "OPTIMAL"])
        self.assertIn("LRU", data["comparison"])
        self.assertIn("OPTIMAL", data["comparison"])
        self.assertIn("translations", data)


if __name__ == "__main__":
    unittest.main()
