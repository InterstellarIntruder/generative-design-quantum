import cirq
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a single qubit at position (0,0) on a grid
qubit = cirq.GridQubit(0, 0)

def create_interference_circuit(phase_angle, amplitude_angle):
    """Creates a quantum circuit demonstrating phase interference with variable amplitude
    
    Args:
        phase_angle: Angle for phase rotation (Z gate), controls interference pattern
        amplitude_angle: Angle for amplitude rotation (Ry gate), controls superposition amount
    
    Returns:
        cirq.Circuit: Quantum circuit with the following steps:
        1. Ry rotation to create initial superposition
        2. Z rotation to add phase
        3. Hadamard to convert phase differences into measurable amplitudes
    """
    circuit = cirq.Circuit()
    
    # Step 1: Create initial superposition with Ry gate
    # - At amplitude_angle = 0: stay in |0⟩ state
    # - At amplitude_angle = π/2: equal superposition
    # - At amplitude_angle = π: go to |1⟩ state
    circuit.append(cirq.ry(amplitude_angle)(qubit))
    
    # Step 2: Add phase rotation with Z gate
    # - This rotates the state in the complex plane
    # - Phase differences will later create interference
    circuit.append(cirq.Z(qubit)**(phase_angle/(2*np.pi)))
    
    # Step 3: Add Hadamard gate
    # - Converts phase differences into amplitude differences
    # - Makes the phase interference measurable in computational basis
    circuit.append(cirq.H(qubit))
    
    return circuit

# Create ranges for our parameters
phases = np.linspace(0, 2*np.pi, 50)      # Phase angles from 0 to 2π
amplitudes = np.linspace(0, np.pi, 50)     # Amplitude angles from 0 to π
# Create 2D grids from our parameter ranges
phase_grid, amplitude_grid = np.meshgrid(phases, amplitudes)
# Initialize array to store measurement probabilities
probabilities = np.zeros_like(phase_grid)

# Create quantum simulator
simulator = cirq.Simulator()

# Simulate circuits for all combinations of phase and amplitude
for i, amplitude in enumerate(amplitudes):
    for j, phase in enumerate(phases):
        # Create and simulate circuit
        circuit = create_interference_circuit(phase, amplitude)
        result = simulator.simulate(circuit)
        # Get final state vector and calculate probability of |0⟩
        state = result.final_state_vector
        probabilities[i, j] = np.abs(state[0])**2  # |amplitude|² gives probability

# Create 3D visualization
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# Create surface plot
# - X-axis: phase angles
# - Y-axis: amplitude angles
# - Z-axis: probability of measuring |0⟩
# - Colors: represent probability (blue=low, yellow=high)
surf = ax.plot_surface(phase_grid, amplitude_grid, probabilities, 
                      cmap='viridis', alpha=0.8)

# Label axes and title
ax.set_xlabel('Phase (radians)')
ax.set_ylabel('Amplitude Rotation (radians)')
ax.set_zlabel('Probability of |0⟩')
ax.set_title('Phase Interference and Amplitude Effects')

# Add π-based labels for better readability
ax.set_xticks([0, np.pi/2, np.pi, 3*np.pi/2, 2*np.pi])
ax.set_xticklabels(['0', 'π/2', 'π', '3π/2', '2π'])
ax.set_yticks([0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi])
ax.set_yticklabels(['0', 'π/4', 'π/2', '3π/4', 'π'])

# Add colorbar to show probability scale
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)

# Set the viewing angle for best visualization
ax.view_init(elev=20, azim=45)

plt.tight_layout()
plt.show()

"""
Key Points for Students:

1. Amplitude Rotation (Ry gate):
   - Controls how much of the state is in superposition
   - Determines the maximum possible interference effect
   - At π/2, creates equal superposition for maximum interference

2. Phase Rotation (Z gate):
   - Adds a quantum phase difference
   - No effect until combined with Hadamard
   - Creates interference pattern when measured

3. Hadamard Gate (H):
   - Converts phase differences into measurable amplitudes
   - Essential for seeing interference effects
   - Without it, phase differences wouldn't be measurable

4. The Plot Shows:
   - Valleys: destructive interference
   - Peaks: constructive interference
   - Flat areas: no interference (when amplitude is 0 or π)
   - How amplitude controls interference strength
"""


"""
Key Connections to Grover's Algorithm:

1. Constructive Interference:
   - Our plot showed how phase + amplitude create peaks
   - Grover uses this to amplify solution states
   - Each iteration increases amplitude of solution

2. Phase Differences:
   - Our Z rotation created phase differences
   - Grover's oracle marks solutions with phase
   - Phase difference drives the amplitude amplification

3. Amplitude Control:
   - Our Ry showed how to distribute amplitude
   - Grover starts with equal superposition (like our π/2)
   - Then uses interference to move amplitude to solution
"""