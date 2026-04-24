import unittest
from src.packet_drop import simulate

class TestPacketDrop(unittest.TestCase):
def test_simulation_runs(self):
result = simulate(10, 0.5)
self.assertEqual(len(result), 10)

if **name** == "**main**":
unittest.main()
