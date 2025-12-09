import unittest
import numpy as np
import pandas as pd
from src.nasm_metrics import NASMMetrics

class TestNASMMetrics(unittest.TestCase):
    def setUp(self):
        self.metrics = NASMMetrics()

    def test_angle_2d(self):
        # 90 degrees
        v1 = np.array([1, 0])
        v2 = np.array([0, 1])
        angle = self.metrics._angle_2d(v1, v2)
        self.assertAlmostEqual(angle, 90.0)
        
        # 180 degrees
        v1 = np.array([1, 0])
        v2 = np.array([-1, 0])
        angle = self.metrics._angle_2d(v1, v2)
        self.assertAlmostEqual(angle, 180.0)
        
        # 0 degrees
        v1 = np.array([1, 0])
        v2 = np.array([1, 0])
        angle = self.metrics._angle_2d(v1, v2)
        self.assertAlmostEqual(angle, 0.0)

    def test_knee_valgus_straight(self):
        # Straight leg in 2D
        row = pd.Series({
            'l_hip_x': 0, 'l_hip_y': 100, 
            'l_knee_x': 0, 'l_knee_y': 50,
            'l_ankle_x': 0, 'l_ankle_y': 0
        })
        angle = self.metrics.calculate_knee_valgus_angle(row, 'l')
        # Thigh vector: (0, -50). Shank vector: (0, -50). Angle should be 0.
        self.assertAlmostEqual(angle, 0.0)

    def test_knee_valgus_inward(self):
        # Knee inward (Valgus). 
        # Hip (0, 100), Knee (10, 50) -> Inward relative to straight line?
        # Wait, if hip=0, ankle=0, then knee at x=10 is "Inward" (towards other leg if on left).
        # Actually x=0 is usually midline? Let's assume Left Leg is at x=-something.
        # But purely vector-wise:
        # Thigh: Knee - Hip = (10, -50).
        # Shank: Ankle - Knee = (-10, -50).
        # Angle between (10, -50) and (-10, -50).
        # Should be some angle.
        row = pd.Series({
            'l_hip_x': 0, 'l_hip_y': 100, 
            'l_knee_x': 10, 'l_knee_y': 50, 
            'l_ankle_x': 0, 'l_ankle_y': 0
        })
        angle = self.metrics.calculate_knee_valgus_angle(row, 'l')
        self.assertGreater(angle, 0)
        print(f"\nTest Valgus Angle: {angle}")

if __name__ == '__main__':
    unittest.main()
