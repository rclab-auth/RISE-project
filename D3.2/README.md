# Bridge Damage Assessment

The **BridgeDamageAssessment** class provides a structured framework for **assessing structural damage** in reinforced concrete (R/C) bridges using **OpenSeesPy** and **finite element modeling (FEM)**.

### 🚀 Features:
- Collects acceleration data from **sensors**.
- Applies **signal processing** (baseline correction, Lanczos resampling, Butterworth filtering).
- Performs **Dynamic Mode Decomposition (DMD)** to extract modal properties.
- Uses **Particle Swarm Optimization (PSO)** to update FEM parameters.
- Computes **damage indicators** based on structural variations.
- Conducts **pushover analysis** for seismic capacity evaluation.
- Provides **visualization** of detected damage.

---

## 🔧 Installation
To run this project, install the necessary dependencies:

```bash
pip install numpy matplotlib openseespy
```

Make sure you have **OpenSeesPy** installed for finite element analysis.


## Usage
### 1️⃣ **Initialize the Class**
The class requires an **OpenSeesPy-based FEM model function** as input.

```python
from BridgeDamageAssessment import BridgeDamageAssessment

# Define an FEM model function
def my_fem_model(param1, param2, param3):
    import openseespy.opensees as ops
    ops.wipe()
    ops.model("basic", "-ndm", 2, "-ndf", 3)
    # Add nodes, materials, and elements here...

# Initialize the class
bridge = BridgeDamageAssessment(my_fem_model)
```



### 2️⃣ **Load Acceleration Data**
Provide raw sensor data as a **NumPy array**:

```python
import numpy as np

# Simulated acceleration data (replace with real sensor readings)
accel_data = np.random.rand(5, 100)  # 5 sensors, 100 time steps

# Load the data into the class
bridge.collect_acceleration_data(accel_data)
```



### 3️⃣ **Preprocess Signals**
Applies baseline correction, resampling, and band-pass filtering.

```python
bridge.preprocess_signals()
```



### 4️⃣ **Perform Dynamic Mode Decomposition (DMD)**
Extract modal properties from the processed data.

```python
bridge.dynamic_mode_decomposition(rank=10)
```



### 5️⃣ **Update the Model (Optimization)**
Refines FEM parameters using **Particle Swarm Optimization (PSO)**.

```python
bridge.model_update()
```



### 6️⃣ **Detect Structural Damage**
Compute **variation ratios** to identify damage.

```python
bridge.damage_detection()
```



### 7️⃣ **Perform Pushover Analysis**
Evaluate **displacement capacity** and **damage index (DI)**.

```python
bridge.pushover_analysis()
```



### 8️⃣ **Visualize Damage Indicators**
Plot the computed **damage variations**.

```python
bridge.plot_damage_indicators()
```
---

## 📌 Requirements
- **Python 3.9+**
- **NumPy**
- **Matplotlib**
- **OpenSeesPy**


## 📝 Notes:
- Replace `my_fem_model()` with your actual **OpenSeesPy FEM model**.
- Ensure **sensor data** is provided in **NumPy array format**.
- Modify **PSO parameters** if needed for model optimization.

