# Algorithm Explanation

## 1. Data Preprocessing
### Gap Filling
Motion capture data often contains gaps due to marker occlusion. We use **linear interpolation** to fill gaps in the timeseries data.

### Noise Filtering
Raw marker data contains high-frequency noise from sensor jitter. We apply a **4th-order Butterworth Low-Pass Filter** with a cutoff frequency of **6 Hz**. This frequency is chosen to preserve human movement (typically < 6Hz) while eliminating sensor noise.

## 2. Geometric Assessment (NASM Criteria)

### Coordinate System
- **X-axis**: Lateral/Medial (Left/Right)
- **Y-axis**: Vertical (Up/Down)
- **Z-axis**: Anterior/Posterior (Forward/Backward)

### Metrics Calculation

#### 1. Knee Valgus / Varus (Anterior View)
We evaluate the alignment of the leg in the **Frontal Plane (XY)**.
- **Vectors**: 
    - Thigh Vector ($V_{thigh}$): Knee - Hip
    - Shank Vector ($V_{shank}$): Ankle - Knee
- **Calculation**: We calculate the 2D angle between $V_{thigh}$ and $V_{shank}$.
- **Interpretation**: An angle significantly greater than 0 degrees indicates deviation from the neutral alignment.

#### 2. Low Back Arch (Lateral View)
We evaluate the curvature of the spine in the **Sagittal Plane (YZ)**.
- **Vectors**:
    - Pelvic Segment ($V_{pelvis}$): Waist - Hip Center
    - Thoracic Segment ($V_{thoracic}$): Torso - Waist
- **Calculation**: Simple angle between the two segments.
- **Interpretation**: Higher angles indicate greater lumbar extension (lordosis).

#### 3. Torso Forward Lean (Lateral View)
We evaluate the inclination of the torso relative to the vertical line.
- **Vectors**:
    - Trunk Vector ($V_{trunk}$): Torso - Waist
    - Vertical Vector ($V_{vert}$): [0, 1]
- **Calculation**: Angle between $V_{trunk}$ and $V_{vert}$ in the YZ plane.
- **Interpretation**: Larger angles indicate excessive forward lean.
