import cirq
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def create_interference_circuit(phase_angle, amplitude_angle):
    """Creates circuit showing smooth quantum interference (saddle shape)"""
    qubit = cirq.GridQubit(0, 0)
    circuit = cirq.Circuit()
    circuit.append(cirq.ry(amplitude_angle)(qubit))
    circuit.append(cirq.Z(qubit)**(phase_angle/(2*np.pi)))
    circuit.append(cirq.H(qubit))
    return circuit

def create_grover_circuit(oracle_phase, num_iterations):
    """Creates Grover-style circuit showing why saddle disappears
    
    Key differences that eliminate saddle shape:
    1. Always starts with H gate (fixed initial amplitude)
    2. Uses π phase flip instead of smooth rotation
    3. Diffusion operator reflects about mean
    """
    qubit = cirq.GridQubit(0, 0)
    circuit = cirq.Circuit()
    
    # Initial superposition ALWAYS π/2 rotation (H gate)
    # - Unlike smooth case where we vary initial amplitude
    # - This eliminates one dimension of the saddle
    circuit.append(cirq.H(qubit))
    
    # Grover iterations
    for _ in range(int(num_iterations)):
        # Oracle: Binary phase flip (π), not smooth rotation
        # - Only values that matter are 0 and π
        # - Eliminates smooth phase dependence
        circuit.append(cirq.Z(qubit)**(oracle_phase/np.pi))
        
        # Diffusion: Reflection about mean
        # - Creates sharp transitions
        # - Not smooth interference pattern
        circuit.append(cirq.H(qubit))
        circuit.append(cirq.Z(qubit))
        circuit.append(cirq.H(qubit))
    
    return circuit

# Create parameters
phases = np.linspace(0, 2*np.pi, 50)
amplitudes = np.linspace(0, np.pi, 50)
phase_grid, amplitude_grid = np.meshgrid(phases, amplitudes)

# Initialize probability arrays
smooth_probs = np.zeros_like(phase_grid)
grover_probs = np.zeros_like(phase_grid)

# Simulate both circuits
simulator = cirq.Simulator()
for i, amp in enumerate(amplitudes):
    for j, phase in enumerate(phases):
        # Simulate smooth interference
        circuit1 = create_interference_circuit(phase, amp)
        result1 = simulator.simulate(circuit1)
        smooth_probs[i, j] = np.abs(result1.final_state_vector[0])**2
        
        # Simulate Grover-style circuit
        circuit2 = create_grover_circuit(phase, amp * 2 / np.pi)  # Scale iterations
        result2 = simulator.simulate(circuit2)
        grover_probs[i, j] = np.abs(result2.final_state_vector[0])**2

# Create visualization
fig = plt.figure(figsize=(15, 6))

# Plot 1: Smooth Interference (Saddle)
ax1 = fig.add_subplot(121, projection='3d')
surf1 = ax1.plot_surface(phase_grid, amplitude_grid, smooth_probs, 
                        cmap='viridis', alpha=0.8)
ax1.set_xlabel('Phase (radians)')
ax1.set_ylabel('Amplitude Rotation (radians)')
ax1.set_zlabel('Probability of |0⟩')
ax1.set_title('Smooth Quantum Interference\n(Saddle Shape)')

# Plot 2: Grover-style Interference
ax2 = fig.add_subplot(122, projection='3d')
surf2 = ax2.plot_surface(phase_grid, amplitude_grid, grover_probs, 
                        cmap='viridis', alpha=0.8)
ax2.set_xlabel('Oracle Phase (radians)')
ax2.set_ylabel('Number of Iterations\n(scaled from amplitude)')
ax2.set_zlabel('Probability of |0⟩')
ax2.set_title('Grover-style Interference\n(Amplitude Amplification)')

# Add π labels to both plots
for ax in [ax1, ax2]:
    ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
    ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
    ax.set_yticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
    ax.set_yticklabels(['0', 'π/4', 'π/2', '3π/4', 'π'])
    ax.view_init(elev=20, azim=45)

# Add colorbars
fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=5)
fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=5)

plt.tight_layout()
plt.show()

"""
Why No Saddle Shape in Grover:

1. Fixed Initial State:
   - Smooth case: Variable initial amplitude creates saddle
   - Grover: Always starts with H gate (fixed π/2 rotation)
   
2. Binary Phase Flip:
   - Smooth case: Continuous phase rotation creates waves
   - Grover: Only uses π phase flip (binary effect)
   
3. Reflection Operation:
   - Smooth case: Direct interference of phases
   - Grover: Reflects about mean (geometric operation)
   
4. Purpose:
   - Smooth case: Shows natural quantum behavior
   - Grover: Engineered to amplify specific states
"""