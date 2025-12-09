import numpy as np
import pandas as pd

class NASMMetrics:
    def __init__(self):
        # Coordinate System Assumptions based on context:
        # Y is Up (Vertical)
        # Z is Forward (Sagittal depth)
        # X is Lateral (Frontal width)
        pass

    def _angle_2d(self, v1, v2):
        """Angle between two 2D vectors in degrees (always positive)."""
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        
        if norm_v1 < 1e-6 or norm_v2 < 1e-6:
            return 0.0
            
        unit_v1 = v1 / norm_v1
        unit_v2 = v2 / norm_v2
        
        dot_product = np.dot(unit_v1, unit_v2)
        dot_product = np.clip(dot_product, -1.0, 1.0)
        return np.degrees(np.arccos(dot_product))

    def _signed_angle_2d(self, v1, v2):
        """
        Calculates signed angle from v1 to v2 in 2D.
        Returns degrees. Positive is CCW rotation from v1 to v2.
        """
        x1, y1 = v1
        x2, y2 = v2
        
        # atan2(y, x)
        # angle of v1: theta1
        # angle of v2: theta2
        # diff: theta2 - theta1
        # However, for vectors, use cross product analog for sign
        # dot = |a||b|cos(theta)
        # det = |a||b|sin(theta) = x1*y2 - x2*y1
        
        dot = x1*x2 + y1*y2
        det = x1*y2 - y1*x2
        
        angle = np.degrees(np.arctan2(det, dot))
        return angle

    def calculate_knee_valgus_angle(self, row, side='l'):
        """
        Calculates Knee Frontal Plane Angle.
        Inward (Medial) movement is VALGUS.
        Outward (Lateral) movement is VARUS.
        
        We calculate the angle deviation from a straight leg.
        Vectors: Thigh (Hip->Knee), Shank (Knee->Ankle).
        
        For LEFT leg (Subject's Left):
          - Hip is approx negative X (if mid=0).
          - Valgus (Knee In) means Knee X > Hip line.
          - We want positive for Valgus.
          
        Metric: Signed angle between Thigh vector (pointing down) and Shank vector (pointing down).
        """
        hip = row[[f'{side}_hip_x', f'{side}_hip_y']].values
        knee = row[[f'{side}_knee_x', f'{side}_knee_y']].values
        ankle = row[[f'{side}_ankle_x', f'{side}_ankle_y']].values
        
        # Vectors pointing DOWN
        vec_thigh = knee - hip
        vec_shank = ankle - knee
        
        # Calculate signed angle
        # Note: In standard screen coordinates (Y up, X right), 
        # For Left Leg: Valgus (Inward) means Knee goes Right (towards X=0). 
        # This implies Shank is rotated CCW relative to Thigh extension?
        # Let's say Thigh is straight down (0, -1). 
        # If valgus, Knee is right, Ankle is relative Left of Knee? No.
        # Hip (Fixed) -> Knee (In/Right) -> Ankle (Fixed on ground relative to hip width usually).
        # Actually foot position acts as anchor.
        # If Knee moves In, the angle (Hip-Knee-Ankle) < 180 on lateral side.
        
        # Let's use simpler deviation logic for sign, but full angle for magnitude.
        angle_mag = self._angle_2d(vec_thigh, vec_shank)
        
        # Determine Sign (Inward/Outward)
        # Construct a vector from Hip to Ankle
        vec_leg_line = ankle - hip
        
        # Cross product (2D) of LegLine vs Vector(Hip->Knee)
        # If Knee is to the 'Left' or 'Right' of the Hip-Ankle line.
        cross_val = np.cross(vec_leg_line, (knee - hip))
        
        # Sign convention:
        # Left Leg: Inward is towards +X (Right).
        # Vector Hip->Ankle roughly points Down.
        # If Knee is to the Right of this line, Cross Product (X*Y - Y*X) direction?
        # Let's assume standard Pose:
        # Left Hip (-10, 100), Left Ankle (-10, 0). Line is (0, -100).
        # Knee Inward: (-5, 50). Vector Hip->Knee (5, -50).
        # Cross: (0 * -50) - (-100 * 5) = 500 => Positive.
        # Right Leg: Hip (10, 100), Ankle (10, 0). Line (0, -100).
        # Knee Inward: (5, 50). Vector Hip->Knee (-5, -50).
        # Cross: (0 * -50) - (-100 * -5) = -500 => Negative.
        
        if side == 'l':
            # For Left Leg, Cross > 0 is Inward (Valgus)
            sign = 1.0 if cross_val > 0 else -1.0
        else:
            # For Right Leg, Cross < 0 is Inward (Valgus)
            sign = 1.0 if cross_val < 0 else -1.0
            
        return angle_mag * sign

    def calculate_lumbar_curvature(self, row):
        """
        Estimates Lumbar Extension/Flexion in Sagittal Plane (YZ).
        Angle between Pelvis vector and Lumbar/Thoracic vector.
        
        Vectors from Lateral View (Z is Forward, Y is Up).
        Pelvis defined by Hip -> Waist? Or vertical reference?
        NASM "Low Back Arch" is excessive Extension (Lordosis).
        "Low Back Rounds" is Flexion.
        
        We use Hip->Waist (Lower Back) and Waist->Torso (Upper Back).
        If they align perfectly = 0.
        If Arching (Lordosis): Waist is pushed Forward? Or rather, the angle closes posteriorly.
        """
        # Hips center Z, Y (Sagittal 2D)
        hy = (row['l_hip_y'] + row['r_hip_y']) / 2
        hz = (row['l_hip_z'] + row['r_hip_z']) / 2
        
        # Using Y as vertical axis (0), Z as horizontal axis (1)
        hip = np.array([hz, hy]) 
        waist = row[['waist_z', 'waist_y']].values
        torso = row[['torso_z', 'torso_y']].values
        
        # Vector 1: Hip -> Waist (Lower segment)
        v_lower = waist - hip
        
        # Vector 2: Waist -> Torso (Upper segment)
        v_upper = torso - waist
        
        angle_mag = self._angle_2d(v_lower, v_upper)
        
        # Sign? 
        # Arching (Lordosis) -> Belly forward.
        # If subject faces +Z.
        # Hip to Waist goes Up. Waist to Torso goes Up.
        # If Arched, Waist is Anterior (more +Z) relative to Hip/Torso line.
        # Cross product 2D (Z-Y plane):
        # v_lower (dz1, dy1), v_upper (dz2, dy2)
        # Cross = dz1*dy2 - dy1*dz2
        
        # Example: Straight (0, 1), (0, 1) -> Cross 0.
        # Arching: Hip(0,0), Waist(1, 1), Torso(0, 2). 
        # v_lower(1,1), v_upper(-1, 1).
        # Cross: 1*1 - 1*(-1) = 2 > 0.
        # So Positive Cross = Arching (if facing +Z).
        
        cross_val = np.cross(v_lower, v_upper)
        
        # Assuming Data Z is forward.
        sign = 1.0 if cross_val > 0 else -1.0
        
        return angle_mag * sign

    def calculate_torso_lean(self, row):
        """
        Calculates Torso Forward Lean.
        Angle of Torso (Waist->Torso) relative to Vertical.
        Sagittal Plane (YZ).
        """
        waist = row[['waist_z', 'waist_y']].values
        torso = row[['torso_z', 'torso_y']].values
        
        trunk_vec = torso - waist
        
        # Vertical Up in YZ plane (Z=0, Y=1)
        vertical_vec = np.array([0, 1]) 
        
        angle = self._angle_2d(trunk_vec, vertical_vec)
        
        # Direction: Forward vs Backward?
        # If Forward Lean, Z increases as Y increases (if facing Z).
        # trunk (dz, dy). If dz > 0 => Forward.
        
        sign = 1.0 if trunk_vec[0] > 0 else -1.0
        
        return angle * sign

    def process_subject(self, df):
        """
        Calculates metrics for all frames.
        Returns DataFrame of metrics.
        """
        results = {
            'l_knee_angle': [],    # +Valgus (In), -Varus (Out)
            'r_knee_angle': [],    # +Valgus (In), -Varus (Out)
            'lumbar_extension': [],# +Arch, -Round
            'torso_lean': []       # +Forward, -Backward
        }
        
        for idx, row in df.iterrows():
            results['l_knee_angle'].append(self.calculate_knee_valgus_angle(row, 'l'))
            results['r_knee_angle'].append(self.calculate_knee_valgus_angle(row, 'r'))
            results['lumbar_extension'].append(self.calculate_lumbar_curvature(row))
            results['torso_lean'].append(self.calculate_torso_lean(row))
            
        return pd.DataFrame(results)
