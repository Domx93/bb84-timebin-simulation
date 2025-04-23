#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2025-04-22

Author: Domenico Ribezzo
"""
import numpy as np
import matplotlib.pyplot as plt

# Parameters
num_states = 100000
state_duration = 2e-9
bin_offset = 1e-9
jitter_std = 40e-12
total_time = num_states * state_duration  # for example 10000 * 2ns


# Alice: bases and bits
alice_bases = np.random.randint(0, 2, size=num_states)   # 0=Z, 1=X
alice_bits = np.random.randint(0, 2, size=num_states)

# Bob: bases
bob_bases = np.random.randint(0, 2, size=num_states)

# Output
timestamps = []

for i in range(num_states):
    t0 = i * state_duration
    ab = alice_bases[i]
    bb = bob_bases[i]
    bit = alice_bits[i]

    if ab == 0:
        # Alice in Z basis → sends early (0) or late (1)
        emission_delay = bit * bin_offset

        if bb == 0:
            # Bob in Z basis → measures arrival time → jitter for simulating real setup
            detector=1
            ts = t0 + emission_delay + np.random.normal(0, jitter_std)
        else:
            # Bob in X basis → not coherent interferece → random click in one detector 
            detector=np.random.choice([2,3])
            ts = t0 + (np.random.randint(0, 2) * bin_offset) + np.random.normal(0, jitter_std)

    else:
        # Alice in X basis → sends |+⟩ o |−⟩
        # Wavefunction has two bins: early + late
        # Detector 2 for 0-phase and detector 3 for pi-phase

        if bb == 0:
            # Bob in Z basis → detection in early or late with 50% probability
            delay = np.random.choice([0, bin_offset])
            ts = t0 + delay + np.random.normal(0, jitter_std)
            detected_bit = int(delay == bin_offset)
            detector=1
        else:
            # Bob in X basis → good interferometric measurement
            # |+⟩ → output 0 (detector 2), |−⟩ → output 1 (detector 3)
            emission_delay =  bin_offset
            ts = t0 + emission_delay + np.random.normal(0, jitter_std)
            if (bit==0):
                detector=2
            else:
                detector=3

    timestamps.append([float(ts),int(detector)])


# Number of noise events
num_noise_events = 10000

# Generate random timestamps uniformly distributed
noise_times = np.random.uniform(0, total_time, size=num_noise_events)

# Choose a random detector for each event
noise_detectors = np.random.randint(1, 4, size=num_noise_events)

# Combine in Nx2 array
noise_events = np.column_stack((noise_times, noise_detectors))

# Unite and order timestamps
timestamps = np.vstack([timestamps, noise_events])
timestamps = timestamps[timestamps[:, 0].argsort()]

#shift USEFUL TO DO
timestamps[:, 0] += 500e-12 #shift for better visualization 
timestamps[:, 0] = np.mod(timestamps[:, 0], total_time) #avoid problems due to shift

#extract times
times = timestamps[:, 0]

# Plot hisogram
plt.hist(times % state_duration * 1e12, bins=200, alpha=0.7)
plt.xlabel("Time window (ps)")
plt.ylabel("Counts")
plt.title("Time-bin BB84 - Simulation")
plt.grid(True)
plt.show()
