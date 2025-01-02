import cirq
import numpy as np
from drawing_utils import TurtleDrawer

class QuantumEntanglement:
    def __init__(self):
        """
        Initialize a QuantumEntanglement visualization class.
        
        This class demonstrates quantum entanglement, one of the most fascinating
        phenomena in quantum mechanics. When two qubits are entangled, their states
        become correlated in such a way that the state of one qubit instantly
        determines the state of the other, regardless of the distance between them.
        
        Einstein called this "spooky action at a distance" because it seemed to
        violate classical physics principles.
        
        Components:
        - Two turtles represent the entangled qubits
        - Blue turtle (drawer1) and Green turtle (drawer2) move in perfect sync
        - Their synchronized movement demonstrates quantum correlation
        """
        self.drawer1 = TurtleDrawer(color="blue")  # Turtle for qubit 1
        self.drawer2 = TurtleDrawer(color="green")  # Turtle for qubit 2

        # Create two qubits that we will entangle
        # In quantum computing, qubits are the basic unit of information
        # While classical bits can only be 0 or 1, qubits can be in a superposition of both
        self.qubit1 = cirq.GridQubit(0, 0)
        self.qubit2 = cirq.GridQubit(0, 1)

        # Initialize a quantum circuit to hold our operations
        self.circuit = cirq.Circuit()

    def create_entanglement(self):
        """
        Creates entanglement between the two qubits using Hadamard and CNOT gates.
        
        The process of creating entanglement:
        1. Hadamard Gate (H):
           - Applied to qubit1
           - Creates superposition: |0⟩ → (|0⟩ + |1⟩)/√2
           - Now qubit1 is in equal superposition of 0 and 1
        
        2. CNOT Gate (Controlled-NOT):
           - Uses qubit1 as control and qubit2 as target
           - If qubit1 is |0⟩, qubit2 stays the same
           - If qubit1 is |1⟩, qubit2 flips
           
        Result:
        Creates the Bell state: (|00⟩ + |11⟩)/√2
        This means the qubits are now entangled - measuring one instantly determines the other!
        """
        # Step 1: Create superposition of qubit1
        self.circuit.append(cirq.H(self.qubit1))
        
        # Step 2: Entangle the qubits using CNOT
        self.circuit.append(cirq.CNOT(self.qubit1, self.qubit2))
        
    def measure_entangled_states(self):
        """
        Measures the entangled states of both qubits and visualizes possible paths.
        
        Key Quantum Concepts Demonstrated:
        1. Quantum Measurement:
           - Collapses the superposition into a definite state
           - Before measurement, both paths are possible (shown in faint colors)
           - After measurement, only one path is taken (shown in bright color)
        
        2. Entanglement Properties:
           - Both qubits always measure to the same value
           - If qubit1 is 0, qubit2 is 0
           - If qubit1 is 1, qubit2 is 1
           - This perfect correlation is a signature of quantum entanglement
        
        3. Quantum Circuit Reset:
           - We need to reset and recreate entanglement each time
           - Measurement destroys the quantum state
           - This mirrors real quantum computers where qubits must be reinitialized
        """
        # Reset the circuit for a fresh start
        self.circuit = cirq.Circuit()
        
        # Recreate the entanglement
        self.create_entanglement()
        
        # Add measurement operations for both qubits
        self.circuit.append(cirq.measure(self.qubit1, key='q1'))
        self.circuit.append(cirq.measure(self.qubit2, key='q2'))

        # Simulate the circuit using Cirq's quantum simulator
        simulator = cirq.Simulator()
        result = simulator.run(self.circuit, repetitions=1)
        measurement_q1 = result.measurements['q1'][0][0]
        measurement_q2 = result.measurements['q2'][0][0]

        # Set probabilities based on measurement outcomes
        # In entangled state, both qubits always give same result
        prob_0 = 1.0 if measurement_q1 == 0 else 0.0
        prob_1 = 1.0 if measurement_q1 == 1 else 0.0

        # Visualize quantum paths for both turtles
        # The faint paths show quantum possibilities before measurement
        # The bright path shows the actual outcome after measurement
        distance = 50
        self.drawer1.draw_quantum_paths(prob_0, prob_1, distance)
        self.drawer2.draw_quantum_paths(prob_0, prob_1, distance)

def main():
    """
    Creates an artistic visualization of quantum entanglement.
    
    The visualization shows:
    - Two turtles representing entangled qubits
    - Quantum possibilities as faint magenta/yellow paths
    - Actual measured states as bright blue/green paths
    - Perfect correlation between the two turtles' movements
    
    This creates a beautiful pattern that would be impossible
    to achieve with classical physics alone - it's a unique
    signature of quantum mechanics in action!
    """
    qe = QuantumEntanglement()
    qe.create_entanglement()

    # Position the turtles symmetrically
    qe.drawer1.setup_initial_position(-100, 50)
    qe.drawer2.setup_initial_position(-100, -50)

    # Start recording frames for GIF - only need to record one turtle
    # since they move in perfect sync due to entanglement
    qe.drawer1.start_gif_recording()

    # Create pattern through repeated measurements of entangled state
    for _ in range(100):  # 100 steps for a complete pattern
        qe.measure_entangled_states()
        # Rotate to create circular patterns
        qe.drawer1.rotate(36)  # 360/10 degrees
        qe.drawer2.rotate(36)
        # Capture frame for GIF animation
        qe.drawer1.capture_frame()

    # Save visualizations
    qe.drawer1.save_drawing_as_png("entanglement_turtles.png")
    qe.drawer1.save_as_gif("entanglement_turtles.gif")

    # Keep the window open until clicked
    qe.drawer1.screen.exitonclick()

if __name__ == "__main__":
    main()
