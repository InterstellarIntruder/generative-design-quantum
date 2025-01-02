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
        self.qubit = cirq.GridQubit(0, 0)
        
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
        Performs a quantum walk by creating and measuring a superposition state.
        
        This method demonstrates several key quantum concepts:
        1. Creating superposition with the Hadamard gate
        2. Quantum measurement collapsing the superposition
        3. Quantum randomness in the measurement outcomes
        
        Args:
            steps: Number of steps in the quantum walk
            distance: Length of each step in turtle units
        
        The visualization shows:
        - Magenta path: Possible |0⟩ state direction (+45 degrees)
        - Yellow path: Possible |1⟩ state direction (-45 degrees)
        - Cyan path: The actual path taken after measurement
        
        Note on Circuit Reset:
        We reset the circuit at each step because:
        1. Quantum measurements are irreversible - they collapse the quantum state
        2. After measurement, the qubit is in a definite state (|0⟩ or |1⟩)
        3. To get a new superposition, we need to start fresh with a new circuit
        4. This mirrors real quantum computers where you need to reinitialize 
           qubits for each new computation
        """
        # Clear any previous circuit - we need a fresh start because:
        # - Previous measurements have collapsed our quantum state
        # - We want each step to start from a clean superposition
        # - This mirrors how real quantum computers work
        self.circuit = cirq.Circuit()
        
        # Put our qubit into superposition using the Hadamard gate
        self.add_superposition()
        
        # In quantum mechanics, measurement collapses the superposition
        # Once measured, the qubit is no longer in superposition
        # That's why we need a new circuit for each step!
        self.circuit.append(cirq.measure(self.qubit))
        
        # Create a quantum simulator and run our circuit
        simulator = cirq.Simulator()
        result = simulator.run(self.circuit, repetitions=1)
        
        # Get the measurement result (0 or 1)
        # After this measurement, our quantum state is "collapsed"
        # and can't be used for another step without resetting
        measurement = result.measurements['q(0, 0)'][0][0]
        
        # Set probabilities based on measurement outcome
        prob_0 = 1.0 if measurement == 0 else 0.0
        prob_1 = 1.0 if measurement == 1 else 0.0
        
        # Visualize the quantum state and its measurement
        self.drawer.draw_quantum_paths(prob_0, prob_1, distance)

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
    # Each walk creates a superposition and draws both possible paths
    for _ in range(100):  # 100 steps for a complete pattern
        qt.quantum_walk(steps=1)
        # Rotate 36 degrees (360/10) to create a circular pattern
        qt.drawer.rotate(36)
        # Capture frame for GIF animation
        qt.drawer.capture_frame()
    
    # Save both PNG and GIF versions of our quantum art
    qt.drawer.save_drawing_as_png()
    qt.drawer.save_as_gif()
    
    # Keep the window open until clicked
    qt.drawer.screen.exitonclick()

if __name__ == "__main__":
    main()

