# Quantum Turtle

import cirq
import numpy as np
from drawing_utils import TurtleDrawer

class QuantumTurtle:
    def __init__(self):
        """
        Initialize a QuantumTurtle that combines quantum computing with visualization.
        
        This class demonstrates fundamental quantum computing concepts through visual art:
        - Quantum superposition: A qubit existing in multiple states simultaneously
        - Quantum measurement: The act of observing a quantum state
        - Quantum randomness: The inherently probabilistic nature of quantum mechanics
        """
        # Initialize our drawing utilities for visualization
        self.drawer = TurtleDrawer()
        
        # In quantum computing, a qubit is the fundamental unit (like a bit in classical computing)
        # While a classical bit can only be 0 or 1, a qubit can be in a superposition of both!
        # Here we create a single qubit at position (0,0) on a grid
        self.qubit = cirq.GridQubit(0, 4)  # Move main qubit to avoid overlap
        
        # Create multiple qubits for binary encoding of rotation
        self.rotation_qubits = [cirq.GridQubit(0, i) for i in range(4)]  # 4 qubits for 16 possible angles
        
        # A quantum circuit is a sequence of quantum operations (gates) applied to qubits
        # It's like a program for our quantum computer
        self.circuit = cirq.Circuit()

    def add_superposition(self):
        """
        Adds a Hadamard (H) gate to create quantum superposition.
        
        The Hadamard gate is one of the most fundamental quantum gates. It creates
        an equal superposition of |0⟩ and |1⟩ states:
        
        |0⟩ -> (|0⟩ + |1⟩)/√2  (equal superposition)
        |1⟩ -> (|0⟩ - |1⟩)/√2
        
        This means our qubit is simultaneously in both 0 and 1 states until measured!
        The probability of measuring either state is exactly 50%.
        """
        self.circuit.append(cirq.H(self.qubit))
        
    def quantum_walk(self, steps: int, distance: float = 50):
        """
        Performs a quantum walk with quantum-determined rotation angles.
        Each step now includes both movement and rotation determination.
        """
        # Reset circuit
        self.circuit = cirq.Circuit()
        
        # Put movement qubit into superposition
        self.add_superposition()
        
        # Add superposition for rotation qubits
        for qubit in self.rotation_qubits:
            self.circuit.append(cirq.H(qubit))
        
        # Measure all qubits
        self.circuit.append(cirq.measure(*self.rotation_qubits, key='rotation'))
        self.circuit.append(cirq.measure(self.qubit, key='movement'))
        
        # Run the circuit
        simulator = cirq.Simulator()
        result = simulator.run(self.circuit, repetitions=1)
        
        # Get movement measurement
        movement = result.measurements['movement'][0][0]
        
        # Calculate rotation angle from binary measurement
        rotation_bits = result.measurements['rotation'][0]
        rotation_value = sum(bit << i for i, bit in enumerate(rotation_bits))
        rotation_angle = (rotation_value / 16) * 360  # Convert to angle between 0 and 360
        
        # Set probabilities based on movement measurement
        prob_0 = 1.0 if movement == 0 else 0.0
        prob_1 = 1.0 if movement == 1 else 0.0
        
        # Draw the quantum paths
        self.drawer.draw_quantum_paths(prob_0, prob_1, distance)
        
        # Apply the quantum-determined rotation
        self.drawer.rotate(rotation_angle)

def main():
    """
    Creates a quantum-inspired artistic pattern using quantum superposition
    to determine the path of a turtle.
    
    This demonstrates how quantum randomness and superposition can be used
    to create unique artistic patterns that would be difficult to achieve
    with classical random number generators.
    """
    # Initialize our quantum turtle
    qt = QuantumTurtle()
    
    # Set up starting position
    qt.drawer.setup_initial_position(-100, 0)
    
    # Start recording frames for GIF
    qt.drawer.start_gif_recording()
    
    # Create a pattern by repeating quantum walks
    for _ in range(100):
        qt.quantum_walk(steps=1)
        # Remove the fixed rotation as it's now handled in quantum_walk
        qt.drawer.capture_frame()
    
    # Save both PNG and GIF versions of our quantum art
    qt.drawer.save_drawing_as_png()
    qt.drawer.save_as_gif()
    
    # Keep the window open until clicked
    qt.drawer.screen.exitonclick()

if __name__ == "__main__":
    main()

