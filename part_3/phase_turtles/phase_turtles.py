import cirq
import numpy as np
import random
from drawing_utils import QuantumVisualizer
from PIL import Image, ImageGrab
import io

class QuantumWalkAgent:
    def __init__(self):
        """
        Initialize the agent for a quantum-inspired random walk.
        """
        # Quantum setup
        self.qubit = cirq.GridQubit(0, 0)
        self.simulator = cirq.Simulator()
        self.visualizer = QuantumVisualizer()
        self.frames = []  # Store frames for GIF

    def create_quantum_circuit(self):
        """Create a quantum circuit using phase interference patterns."""
        circuit = cirq.Circuit()
        
        # Step 1: Create initial superposition with controlled amplitude
        # Ry(π/2) creates an equal superposition of |0⟩ and |1⟩
        # This gives each state an equal initial amplitude of 1/√2
        amplitude_angle = np.pi/2  # Equal superposition
        circuit.append(cirq.ry(amplitude_angle)(self.qubit))
        
        # Step 2: Add phase rotation - this will affect the walking direction
        # Z-rotation adds a relative phase between |0⟩ and |1⟩
        # This phase difference will be converted to amplitude difference by the Hadamard
        phase_angle = random.uniform(0, 2*np.pi)
        circuit.append(cirq.Z(self.qubit)**(phase_angle/(2*np.pi)))
        
        # Step 3: Convert phase to measurable amplitude
        # The Hadamard gate converts phase differences into amplitude differences
        # through quantum interference:
        # - When phases align: constructive interference increases amplitude
        # - When phases oppose: destructive interference decreases amplitude
        circuit.append(cirq.H(self.qubit))
        
        return circuit

    def simulate_quantum_circuit(self):
        """Simulate the quantum circuit and extract interference pattern."""
        circuit = self.create_quantum_circuit()
        result = self.simulator.simulate(circuit)
        state_vector = result.final_state_vector
        
        # The final state vector shows how phase differences were converted to amplitudes:
        # - Higher amplitude in |0⟩ means constructive interference occurred there
        # - Lower amplitude in |1⟩ means destructive interference occurred there
        # The squared magnitudes of these amplitudes give measurement probabilities
        prob_0 = np.abs(state_vector[0])**2
        phase = np.angle(state_vector[0])
        
        # Measurement follows the Born rule:
        # - Probability of measuring |0⟩ = |amplitude_0|²
        # - Probability of measuring |1⟩ = |amplitude_1|²
        measured_state = '0' if random.random() < prob_0 else '1'
        
        # Log quantum state information
        print("\nQuantum State Information:")
        print(f"State Vector: {state_vector}")
        print(f"Amplitude |0⟩: {np.abs(state_vector[0]):.4f}")
        print(f"Amplitude |1⟩: {np.abs(state_vector[1]):.4f}")
        print(f"Phase |0⟩: {np.angle(state_vector[0], deg=True):.2f}°")
        print(f"Phase |1⟩: {np.angle(state_vector[1], deg=True):.2f}°")
        print(f"Measured State: |{measured_state}⟩")
        print("-" * 50)
        
        return prob_0, phase

    def take_quantum_step(self, max_step_length=50):
        """Use interference pattern to control turtle movement."""
        probability, phase = self.simulate_quantum_circuit()
        self.visualizer.visualize_step(probability, phase, max_step_length)
        
        # Capture frame after each step using ImageGrab
        # Get the turtle window boundaries
        canvas = self.visualizer.screen.getcanvas()
        x = canvas.winfo_rootx()
        y = canvas.winfo_rooty()
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        # Capture the screen region of the turtle window
        frame = ImageGrab.grab(bbox=(x, y, x + width, y + height))
        self.frames.append(frame)

    def save_animation(self, filename='quantum_walk.gif'):
        """Save the captured frames as an animated GIF."""
        if self.frames:
            # Save the frames as an animated GIF
            self.frames[0].save(
                filename,
                save_all=True,
                append_images=self.frames[1:],
                duration=100,  # Duration for each frame in milliseconds
                loop=0
            )
            print(f"Animation saved as {filename}")

    def run(self, steps=100):
        """Perform the quantum random walk for a given number of steps."""
        for _ in range(steps):
            self.take_quantum_step()

def main():
    """Run the quantum-inspired random walk simulation."""
    agent = QuantumWalkAgent()
    agent.visualizer.setup_turtle()

    # Run the quantum random walk
    agent.run(steps=200)

    # Save the animation
    agent.save_animation()

    # Keep the screen open until clicked
    agent.visualizer.cleanup()

if __name__ == "__main__":
    main()

"""
Example Quantum State Analysis:
-----------------------------
Consider this specific quantum state measurement:
    Amplitude |0⟩: 0.9708
    Amplitude |1⟩: 0.2398
    Phase |0⟩: 13.87°
    Phase |1⟩: -76.13°
    Measured State: |0⟩

This shows:
1. Strong constructive interference for |0⟩ (amplitude 0.9708)
   - Probability of measuring |0⟩ = 0.9708² ≈ 94.2%

2. Destructive interference for |1⟩ (amplitude 0.2398)
   - Probability of measuring |1⟩ = 0.2398² ≈ 5.7%

3. Phase difference between states:
   - |0⟩ phase: 13.87°
   - |1⟩ phase: -76.13°
   - Difference: ~90° (phase differences near 90° or 270° create maximum interference,
     while 0° or 180° create minimal interference)

4. Result: State |0⟩ was measured, matching the high probability
   from constructive interference.
"""
