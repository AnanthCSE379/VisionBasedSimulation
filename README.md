# VisionBasedSimulation

### **Objective**

Developing a high-frequency communication bridge between a Python-based controller and the CoppeliaSim physics engine. This project focuses on the **Cyber-Physical** challenge of marshalling raw simulation data into processed visual feedback for real-time control logic.

### **Core Features**

* **Synchronous ZMQ Handshaking:** Utilizes the ZeroMQ Remote API to establish a low-latency, request-reply communication pattern with the simulation core.
* **Raw Buffer Reconstruction:** Implements a pipeline using `NumPy` and `OpenCV` to transform raw 1D byte-arrays from vision sensors into structured 3D image matrices.
* **Vision-in-the-Loop Control:** Differential drive kinematics with real-time edge detection feedback (Canny Filter), demonstrating a fundamental autonomous navigation loop.

---

### **Dependencies & Prerequisites**

#### **1. Simulation Environment**

* **CoppeliaSim V4.5+** (Required for the `zmqRemoteAPI`).
* The ZMQ Add-on must be enabled (standard in recent versions).

#### **2. Python Environment**

You will need the following libraries:

```bash
pip install coppeliasim-zmqremoteapi-client opencv-python numpy

```

> **Note on ZMQ Dependency:** Unlike the legacy Remote API, this project uses the modern **ZMQ Remote API Client**. Ensure the port matches the one specified in the script (default: `23000`).

---

### **Execution**

1. Open CoppeliaSim and load your scene (ensure the objects `/RRwheel_motor`, `/RLwheel_motor`, and `/visionSensor` exist).
2. Press the **Play** button in CoppeliaSim or let the script handle the simulation start.
3. Run the controller:
```bash
python VisionBasedSimulation.py

```


4. **Emergency Stop:** Press `q` in the OpenCV window to trigger a "Negotiated Stop" where velocities are reset to zero before the socket closes.

---

### **Technical Implementation Details**

* **Color Space Conversion:** Re-ordered simulation RGB buffers to BGR for OpenCV compatibility.
* **Temporal Consistency:** Managed loop timing to ensure image processing latency does not cause "Stale Data" commands to the actuator joints.

---
