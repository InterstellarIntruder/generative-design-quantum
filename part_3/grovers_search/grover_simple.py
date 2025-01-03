import numpy as np
import cirq

# Each design is represented as: [num_nodes, total_length, max_stress]
truss_designs = [
    [4, 120, 250],  # Design 1
    [5, 150, 200],  # Design 2
    [6, 180, 180],  # Design 3
    [4, 130, 220],  # Design 4
    [5, 160, 190],  # Design 5
    [6, 200, 150],  # Design 6
    [4, 140, 210],  # Design 7
    [5, 170, 170]   # Design 8
]

def calculate_fitness(design, target_stress=200):
    """
    Fitness function that considers:
    1. How close the stress is to target
    2. Minimizing total length
    3. Preferring fewer nodes for simplicity
    
    Lower fitness score is better
    """
    num_nodes, total_length, max_stress = design
    
    # Calculate components of fitness
    stress_diff = abs(max_stress - target_stress)
    length_penalty = total_length / 100  # Normalize length
    node_penalty = num_nodes * 10       # Penalty for complexity
    
    # Combined fitness (lower is better)
    fitness = stress_diff + length_penalty + node_penalty
    
    return fitness

# Calculate fitness for each design
for i, design in enumerate(truss_designs):
    fitness = calculate_fitness(design)
    print(f"Design {i+1}: {design} - Fitness: {fitness:.2f}")

# Number of qubits needed to represent 8 designs (2³ = 8)
num_qubits = 3
qubits = cirq.LineQubit.range(num_qubits)
fitness_qubits = [cirq.LineQubit(i + num_qubits) for i in range(num_qubits)]

def oracle_for_best_design(circuit, qubits, fitness_qubits):
    """
    Oracle that marks the design(s) with lowest fitness score
    """
    # Calculate and store all fitness values
    fitness_values = [calculate_fitness(design) for design in truss_designs]
    min_fitness = min(fitness_values)
    
    # Convert design index to binary and mark if it has minimum fitness
    aux = cirq.LineQubit(2 * num_qubits)
    for i, fitness in enumerate(fitness_values):
        if abs(fitness - min_fitness) < 1e-6:  # Check for minimum fitness
            # Convert i to binary and mark that state
            binary = format(i, f'0{num_qubits}b')
            # XOR current state with target state
            for j, bit in enumerate(binary):
                if bit == '0':
                    circuit.append(cirq.X(qubits[j]))
            
            # Mark the state
            circuit.append(cirq.Z(qubits[0]).controlled_by(*qubits[1:]))
            
            # Uncompute XORs
            for j, bit in enumerate(binary):
                if bit == '0':
                    circuit.append(cirq.X(qubits[j]))

def build_grover_circuit():
    circuit = cirq.Circuit()
    
    # Initialize in superposition
    circuit.append(cirq.H.on_each(*qubits))
    
    # Single Grover iteration (can be adjusted)
    num_iterations = 1
    
    for _ in range(num_iterations):
        # Apply oracle
        oracle_for_best_design(circuit, qubits, fitness_qubits)
        
        # Apply diffusion operator
        circuit.append(cirq.H.on_each(*qubits))
        circuit.append(cirq.X.on_each(*qubits))
        circuit.append(cirq.H(qubits[-1]).controlled_by(*qubits[:-1]))
        circuit.append(cirq.X.on_each(*qubits))
        circuit.append(cirq.H.on_each(*qubits))
    
    # Measure
    circuit.append(cirq.measure(*qubits, key='result'))
    return circuit

# Run the circuit
simulator = cirq.Simulator()
circuit = build_grover_circuit()
result = simulator.run(circuit, repetitions=100)

# Process and print results
counts = result.histogram(key='result')
print("\nMeasurement Results:")
for state, count in counts.items():
    binary = format(state, f'0{num_qubits}b')
    design = truss_designs[state]
    fitness = calculate_fitness(design)
    print(f"Design {state+1} (State: {binary}): {count} times")
    print(f"Parameters: {design}")
    print(f"Fitness: {fitness:.2f}\n")
