#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-04-23

Author: Domenico Ribezzo
"""


import numpy as np
import matplotlib.pyplot as plt

"""
YOU NEED TO RUN data_generator.py BEFORE. IT USES THE SAME VARIABLE. 
YOU CAN ALSO SAVE THEM AND IMPORT 
'alice_bases, bob_bases, alice_bits, timestamps' HERE
"""

# Extract detector channel and time-of-arrival (TOA) from timestamps
channel = timestamps[:, 1]
toa = timestamps[:, 0]  # TOA stands for time-of-arrival

# Identify indices where Alice used Z or X basis
base_Z = np.where(alice_bases == 0)[0]
base_X = np.where(alice_bases == 1)[0]

# Analyze timestamps
click_pos = np.asarray(np.floor_divide(toa, 2e-9), dtype=int)
# → Indicates in which 2 ns time-slot (i.e., in which quantum state) the click occurred

click_val = np.mod(toa, 2e-9)
# → Indicates the position within the 2 ns state: <1 ns means |E⟩, >1 ns means |L⟩

# Sifting: keep only events where Alice and Bob used the same basis
match_mask = alice_bases[click_pos] == bob_bases[click_pos]
matching_positions = click_pos[match_mask]

# Mask for clicks in base Z
base_z_mask = np.isin(click_pos[match_mask], base_Z)

# Keep only sifted positions
sifted_pos = click_pos[match_mask]
sifted_z_pos = sifted_pos[base_z_mask]

# Visualize the click positions (|E⟩ or |L⟩) for Z-basis
plt.hist(click_val[np.isin(click_pos, sifted_z_pos)], bins=100)

# Digitize the measured Z-basis clicks (0 for |E⟩, 1 for |L⟩)
click_z = click_val[np.isin(click_pos, sifted_z_pos)]
det_z = (click_z >= 1e-9).astype(int)


# Get the true values sent by Alice in those positions
real_value = alice_bits[click_pos[np.isin(click_pos, sifted_z_pos)]]

# Calculate the Quantum Bit Error Rate (QBER)
qberz = len(np.where(det_z != real_value)[0]) / len(det_z)
print(f"QBER_Z: {qberz:.3%}")


##LET'S DO THE SAME FOR x BASIS

# Mask for clicks in base X (positions where Alice used X and matched with Bob)
base_x_mask = np.isin(click_pos[match_mask], base_X)

# Keep only sifted positions for X basis
sifted_x_pos = sifted_pos[base_x_mask]

# Create a global mask for sifted X clicks that are in the late bin
global_mask = np.isin(click_pos, sifted_x_pos) & (click_val > 1e-9)

# Extract the channels and decode the bits (2 → 0, 3 → 1)
channel_x = channel[global_mask]
det_x = (channel_x == 3).astype(int)  # only channel 3 gives bit 1

# Get the original bits from Alice at those positions
real_value = alice_bits[click_pos[global_mask]]

# Calculate QBER for base X
qberx = np.mean(det_x != real_value)
print(f"QBER_X: {qberx:.3%}")

####FINALLY WE CALCULATE THE SECURE KEY RATE

#Shannon entropy definition
def H2(q):
    """Binary entropy function h2(q)"""
    if q == 0 or q == 1:
        return 0.0
    return -q * np.log2(q) - (1 - q) * np.log2(1 - q)

#secure key rate. 0.5 is the sifting, qberz bit-flip error rate, qberx phase-flip error rate
skr=(0.5*num_states*(1-H2(qberz)-H2(qberx)))/total_time
print(f"secure key rate: {int(skr)} bps")

#more precise, also dark count detections are included
skr=((len(det_z)+len(det_x))*(1-H2(qberz)-H2(qberx)))/total_time
print(f"secure key rate: {int(skr)} bps")