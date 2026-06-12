import unittest
from main import calculate_energy_financials


class TestEnergyFinancials(unittest.TestCase):

    def test_empty_devices_list(self):
        result = calculate_energy_financials([])
        self.assertEqual(result, (0.0, 0.0, 0.0))

    def test_financials_with_discount(self):
        devices = [
            {
                "id": "M01",
                "location": "A",
                "old_index": 0,
                "new_index": 60000,
                "status": "Normal"
            }
        ]

        total_kwh, discount, final_cost = calculate_energy_financials(devices)

        self.assertEqual(total_kwh, 60000)
        self.assertEqual(discount, 3)
        self.assertEqual(final_cost, 174600000)

    def test_financials_no_discount(self):
        devices = [
            {
                "id": "M01",
                "location": "A",
                "old_index": 0,
                "new_index": 10000,
                "status": "Normal"
            }
        ]

        total_kwh, discount, final_cost = calculate_energy_financials(devices)

        self.assertEqual(total_kwh, 10000)
        self.assertEqual(discount, 0)
        self.assertEqual(final_cost, 30000000)


if __name__ == "__main__":
    unittest.main()