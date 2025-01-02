# Quantum Turtle Graphics

A creative visualization tool that combines quantum computing concepts with turtle graphics to generate unique generative art patterns.

## Overview

This tutorial contains two examples that demonstrate fundamental quantum computing concepts through visual art:

### 1. Quantum Turtle
The Quantum Turtle uses quantum superposition and measurement to create mesmerizing visual patterns. As it moves, it visualizes:

- Quantum superposition states using branching paths
- Quantum measurement outcomes through color-coded trails
- Quantum randomness via the path choices

The visualization shows:
- Magenta paths: Possible |0⟩ state direction (+45 degrees)
- Yellow paths: Possible |1⟩ state direction (-45 degrees) 
- Cyan paths: The actual measured path taken

### 2. Entangled Turtles
The Entangled Turtles demonstrate quantum entanglement by using two quantum turtles that move in perfect correlation:

- Quantum entanglement through synchronized turtle movements
- Bell state superposition using branching paths
- Perfect correlation between entangled qubits

The visualization shows:
- Dark magenta paths: Possible |0⟩ state direction for both qubits
- Dark yellow paths: Possible |1⟩ state direction for both qubits
- Blue/Green paths: The actual measured paths taken by the entangled pair

## Technical Implementation

The project uses Cirq, Google's quantum computing framework, to simulate quantum behavior:

### Quantum Turtle Implementation:
- **Quantum Circuit**: Creates a single qubit circuit using `cirq.GridQubit(0, 0)`
- **Hadamard Gate**: Applies H-gates to create quantum superposition states
- **State Visualization**: 
  - Calculates quantum amplitudes from the final state vector
  - Probability of |0⟩ and |1⟩ states determines path transparency
  - Each quantum walk creates a branching pattern showing both potential paths

### Entangled Turtles Implementation:
- **Bell State Creation**:
  1. Creates two qubits and applies Hadamard (H) gate to first qubit
  2. Uses CNOT gate to entangle the qubits
  3. Creates the Bell state: (|00⟩ + |11⟩)/√2
- **Entanglement Visualization**:
  - Measures both qubits in the computational basis
  - Shows perfect correlation in measurement outcomes
  - Both turtles always take matching paths due to entanglement

## Requirements

- Python 3.7+
- cirq
- numpy
- pillow (PIL)
- turtle (included in Python standard library)
