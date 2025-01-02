# Entangled Turtles Graphics

A creative visualization tool that demonstrates quantum entanglement through synchronized turtle graphics, creating mesmerizing patterns that showcase one of quantum mechanics' most mysterious phenomena.

## Overview

The Entangled Turtles demonstrate quantum entanglement by using two quantum turtles that move in perfect correlation. The visualization shows:

- Quantum entanglement through synchronized turtle movements
- Bell state superposition using branching paths
- Quantum measurement collapse via color-coded trails
- Perfect correlation between entangled qubits

The visualization includes:
- Dark magenta paths: Possible |0⟩ state direction (+45 degrees) for both qubits
- Dark yellow paths: Possible |1⟩ state direction (-45 degrees) for both qubits
- Blue/Green paths: The actual measured paths taken by the entangled qubits

## Technical Implementation

The project uses Cirq to create and simulate entangled quantum states:

- **Quantum Circuit**: Creates two qubits using `cirq.GridQubit(0, 0)` and `cirq.GridQubit(0, 1)`
- **Bell State Creation**:
  1. Applies Hadamard (H) gate to first qubit for superposition
  2. Uses CNOT gate to entangle the qubits
  3. Creates the Bell state: (|00⟩ + |11⟩)/√2
- **State Visualization**: 
  - Measures both qubits in the computational basis
  - Shows perfect correlation in measurement outcomes
  - Both turtles always take matching paths due to entanglement

The entanglement pattern is created by:
1. Creating a Bell state with H and CNOT gates
2. Measuring both qubits
3. Drawing quantum possibilities as faint branching paths
4. Moving both turtles according to measurement results
5. Rotating and repeating to create symmetric patterns

## Key Quantum Concepts

- **Quantum Entanglement**: When two qubits are entangled, their states become correlated in a way that can't be explained by classical physics
- **Bell States**: The fundamental resource in quantum teleportation and quantum cryptography
- **Measurement Correlation**: Measuring one entangled qubit instantly determines the state of the other
- **Einstein's "Spooky Action"**: The seemingly instantaneous influence between entangled particles

## Requirements

- Python 3.7+
- cirq
- numpy
- pillow (PIL)
- turtle (included in Python standard library)