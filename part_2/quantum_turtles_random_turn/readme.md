# Quantum Turtle Graphics - random turn

A creative visualization tool that combines quantum computing concepts with turtle graphics to generate unique generative art patterns.

## Overview

The Quantum Turtle uses quantum superposition and measurement to create mesmerizing visual patterns. As it moves, it visualizes:

- Quantum superposition states using branching paths
- Quantum measurement outcomes through color-coded trails
- Quantum randomness via both path choices and rotation angles

The visualization shows:
- Magenta paths: Possible |0⟩ state direction (+45 degrees)
- Yellow paths: Possible |1⟩ state direction (-45 degrees) 
- Cyan paths: The actual measured path taken

## Technical Implementation

The project uses Cirq, Google's quantum computing framework, to simulate quantum behavior:

- **Quantum Circuit**: Creates multiple qubits:
  - One qubit for movement direction using `cirq.GridQubit(0, 4)`
  - Four rotation qubits using `cirq.GridQubit(0, 0)` through `cirq.GridQubit(0, 3)`
- **Hadamard Gates**: Applied to all qubits to create quantum superposition states
- **Binary-Encoded Rotation**: 
  - Uses 4 qubits to encode 16 possible rotation angles
  - Converts quantum measurements to angles between 0° and 360°
  - Each step's rotation is determined by quantum measurement
- **State Visualization**: 
  - Calculates quantum amplitudes from the final state vector
  - Probability of |0⟩ and |1⟩ states determines path transparency
  - Each quantum walk creates a branching pattern showing both potential paths

The main pattern is created by:
1. Initializing a quantum circuit with movement and rotation qubits
2. Applying superposition (H-gate) to all qubits
3. Measuring the quantum states
4. Converting rotation qubit measurements to angles
5. Drawing branching paths based on movement probabilities
6. Applying quantum-determined rotation

## Binary-Encoded Rotation Explained

The quantum rotation system uses 4 qubits to create random angles through binary encoding:

- Each qubit represents a binary digit (0 or 1)
- With 4 qubits, we can represent numbers from 0 to 15 (2⁴ - 1)
- Example binary representations:
  - 0000 = 0
  - 0001 = 1
  - 0010 = 2
  - 1111 = 15

The measured binary number is converted to an angle by:
1. Reading the qubits as a binary number (0-15)
2. Dividing by 16 to get a fraction between 0 and 0.9375
3. Multiplying by 360° to get a final angle

For example:
- If qubits measure to 0110 (binary 6):
  - 6/16 = 0.375
  - 0.375 * 360° = 135°
- If qubits measure to 1111 (binary 15):
  - 15/16 = 0.9375
  - 0.9375 * 360° = 337.5°

This creates 16 evenly-spaced possible rotation angles between 0° and 360°, each determined by quantum measurement.

## Requirements

- Python 3.7+
- cirq
- numpy
- pillow (PIL)
- turtle (included in Python standard library)
