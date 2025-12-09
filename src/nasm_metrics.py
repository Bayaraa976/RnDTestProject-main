import numpy as np
import pandas as pd

class NASMMetrics:
    def __init__(self):
        # Y is Up, Z is Forward, X is Lateral
        pass

    def _angle_2d(self, v1, v2):
        """Angle between two 2D vectors in degrees."""
        if np.linalg.norm(v1) < 1e-6 or np.linalg.norm(v2) < 1e-6:
            return 0.0
            
        unit_v1 = v1 / np.linalg.norm(v1)
        unit_v2 = v2 / np.linalg.norm(v2)
        dot_product = np.dot(unit_v1, unit_v2)
        # Numerical stability
        dot_product = np.clip(dot_product, -1.0, 1.0)
        angle = np.degrees(np.arccos(dot_product))
        return angle

    def calculate_knee_valgus_angle(self, row, side='l'):
        """
        Calculates Knee Valgus/Varus angle in Frontal Plane (XY).
        Angle between Thigh (Hip->Knee) and Shank (Knee->Ankle).
        Ideally approach 0 (straight line) or 180 depending on vector direction.
        Here we treat Hip->Knee and Knee->Ankle as vectors pointing down.
        So angle should be close to 0.
        """
        hip = row[[f'{side}_hip_x', f'{side}_hip_y']].values
        knee = row[[f'{side}_knee_x', f'{side}_knee_y']].values
        ankle = row[[f'{side}_ankle_x', f'{side}_ankle_y']].values
        
        # Vectors pointing DOWN
        vec_thigh = knee - hip
        vec_shank = ankle - knee
        
        angle = self._angle_2d(vec_thigh, vec_shank)
        return angle

    def calculate_lumbar_curvature(self, row):
        """
        Estimates Lumbar Curvature in Sagittal Plane (YZ).
        Angle between Pelvic alignment (Hip->Waist) and Thoracic alignment (Waist->Torso).
        """
        # Hips center
        hy = (row['l_hip_y'] + row['r_hip_y']) / 2
        hz = (row['l_hip_z'] + row['r_hip_z']) / 2
        
        hip_center = np.array([hy, hz]) # Y, Z
        waist = row[['waist_y', 'waist_z']].values
        torso = row[['torso_y', 'torso_z']].values
        
        # Vectors pointing UP
        v_lower = waist - hip_center
        v_upper = torso - waist
        
        angle = self._angle_2d(v_lower, v_upper)
        return angle

    def calculate_torso_lean(self, row):
        """
        Calculates Torso Forward Lean in Sagittal Plane (YZ).
        Angle of Torso (Waist->Torso) relative to Vertical Y ([1, 0] in YZ).
        """
        waist = row[['waist_y', 'waist_z']].values
        torso = row[['torso_y', 'torso_z']].values
        
        trunk_vec = torso - waist
        # Vertical Up in YZ plane is (1, 0) since Y is idx 0 here? 
        # Wait, Y is 'waist_y'. Z is 'waist_z'.
        # If I extract values as [y, z], then Y is index 0.
        vertical_vec = np.array([1, 0]) 
        
        angle = self._angle_2d(trunk_vec, vertical_vec)
        return angle

    def process_subject(self, df):
        """
        Calculates metrics for all frames.
        Returns DataFrame of metrics.
        """
        results = {
            'l_knee_angle': [],
            'r_knee_angle': [],
            'lumbar_angle': [],
            'torso_lean': []
        }
        
        for idx, row in df.iterrows():
            results['l_knee_angle'].append(self.calculate_knee_valgus_angle(row, 'l'))
            results['r_knee_angle'].append(self.calculate_knee_valgus_angle(row, 'r'))
            results['lumbar_angle'].append(self.calculate_lumbar_curvature(row))
            results['torso_lean'].append(self.calculate_torso_lean(row))
            
        return pd.DataFrame(results)
