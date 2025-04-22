# BB84 Time-bin Simulation

This repository contains a Python script that simulates detection events in a quantum key distribution (QKD) experiment using the BB84 protocol with **time-bin encoding**.

The simulation is designed for educational purposes and can be used as a basis for laboratory exercises in quantum optics or quantum information.

## 📋 Overview

The script generates a list of timestamped detection events resulting from a BB84 time-bin setup. It includes:

- Random bit and basis generation for Alice and Bob
- Time-of-arrival based detection (Z basis)
- Interference-based detection (X basis)
- Gaussian timing jitter to simulate realistic detector response
- Background noise events (uncorrelated random detections)
- Final histogram plotting of detection events within a single quantum state window (two time-bins)

The output simulates what an experiment might produce, and can be analyzed to extract bit values, sift keys, calculate QBER or visibility, and extract secure key rate.

## 📂 Files

- `generate_data.py` — The main script that generates and plots detection events

## ▶️ How to Run

This script requires Python 3 and the following packages:
- `numpy`
- `matplotlib`

You can install the dependencies with:

```bash
pip install numpy matplotlib
```

Then run the script:

python generate_data.py

## 🛠️ Parameters and Output Structure

### Adjustable Parameters

The following parameters can be modified at the top of the script to explore different simulation conditions:

| Parameter        | Description                                                                 | Default Value   |
|------------------|-----------------------------------------------------------------------------|-----------------|
| `num_states`      | Number of quantum states sent by Alice (i.e., number of time-bins)         | `100000`        |
| `state_duration`  | Duration of each time-bin (in seconds)                                     | `2e-9` (2 ns)   |
| `bin_offset`      | Time separation between early and late bins (defines the qubit encoding)   | `1e-9` (1 ns)   |
| `jitter_std`      | Standard deviation of Gaussian timing jitter (simulates detector noise)    | `40e-12` (40 ps)|
| `num_noise_events`| Number of uncorrelated background noise events                             | `10000`         |

These parameters affect the **density of events**, **temporal resolution**, and **signal-to-noise ratio** in the output.

### Encoding Variables

The quantum information in the simulation is encoded through the following arrays:

| Variable         | Shape           | Description                                                              |
|------------------|-----------------|--------------------------------------------------------------------------|
| `alice_bases`    | `(num_states,)` | Basis chosen by Alice for each qubit: `0 = Z`, `1 = X`                   |
| `alice_bits`     | `(num_states,)` | Bit chosen by Alice to encode: `0` or `1`                                |
| `bob_bases`      | `(num_states,)` | Basis chosen by Bob for measurement: `0 = Z`, `1 = X`                    |

These arrays define the **ideal quantum communication** process:

- If `alice_bases[i] == bob_bases[i]`, the measurement is meaningful (i.e., they used the same basis).
- If the bases differ, the result is random, as in real QKD.

These variables are not directly included in the final `timestamps` array, but can be used to analyze QBER (Quantum Bit Error Rate) or visibility of interference.
If you plan to use these arrays for downstream analysis, you can save them using `numpy.save()` or `numpy.savez()` for later loading.


### Output: `timestamps` array

The final output of the simulation is stored in a NumPy array called `timestamps`, which is a 2D array with shape `(N, 2)`:

timestamps[i, 0] → timestamp in seconds (float); timestamps[i, 1] → detector number (1, 2, or 3)


- **Detector 1**: Time-of-arrival detection (Z basis)
- **Detector 2/3**: Time of interferometric detection (X basis), distinguishing phase 0 vs π 
- The timestamps are sorted chronologically.
- Noise events are randomly interleaved and indistinguishable from valid detections without additional metadata.
