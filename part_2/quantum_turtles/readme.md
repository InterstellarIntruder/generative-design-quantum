# Quantum Turtle Graphics

A creative visualization tool that combines quantum computing concepts with turtle graphics to generate unique generative art patterns.

## Overview

The Quantum Turtle uses quantum superposition and measurement to create mesmerizing visual patterns. As it moves, it visualizes:

- Quantum superposition states using branching paths
- Quantum measurement outcomes through color-coded trails
- Quantum randomness via the path choices

The visualization shows:
- Magenta paths: Possible |0⟩ state direction (+45 degrees)
- Yellow paths: Possible |1⟩ state direction (-45 degrees) 
- Cyan paths: The actual measured path taken

## Technical Implementation

The project uses Cirq, Google's quantum computing framework, to simulate quantum behavior:

- **Quantum Circuit**: Creates a single qubit circuit using `cirq.GridQubit(0, 0)`
- **Hadamard Gate**: Applies H-gates to create quantum superposition states
- **State Visualization**: 
  - Calculates quantum amplitudes from the final state vector
  - Probability of |0⟩ and |1⟩ states determines path transparency
  - Each quantum walk creates a branching pattern showing both potential paths

The main pattern is created by:
1. Initializing a quantum circuit
2. Applying superposition (H-gate)
3. Simulating the quantum state
4. Drawing branching paths based on quantum probabilities
5. Rotating and repeating to create circular patterns

## Requirements

- Python 3.7+
- cirq
- numpy
- pillow (PIL)
- turtle (included in Python standard library)
