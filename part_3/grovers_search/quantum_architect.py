import cirq

def oracle_for_2_adj_public(circuit, qubits):
    """
    Oracle that marks states with exactly 2 adjacent public rooms
    in a 3-room layout. For example:
    ■■□ (110) - Valid: First two rooms are public
    □■■ (011) - Valid: Last two rooms are public 
    ■□■ (101) - Invalid: Public rooms not adjacent
    """
    q0, q1, q2, val = qubits  # 3 data qubits + 1 ancilla
    
    # Mark pattern 110 (first two rooms public)
    # We want q0=1, q1=1, q2=0, so we flip q2 first
    circuit.append(cirq.X(q2))           # q2 must be 0
    circuit.append(cirq.TOFFOLI(q0, q1, val))
    circuit.append(cirq.X(q2))
    
    # Mark pattern 011 (last two rooms public) 
    # We want q0=0, q1=1, q2=1, so we flip q0 first
    circuit.append(cirq.X(q0))           # q0 must be 0
    circuit.append(cirq.TOFFOLI(q1, q2, val))
    circuit.append(cirq.X(q0))
    
    # Phase flip marked states using controlled-Z
    circuit.append(cirq.CZ(val, q0))
    
    # Uncompute everything in reverse order to clean up
    circuit.append(cirq.X(q0))
    circuit.append(cirq.TOFFOLI(q1, q2, val))
    circuit.append(cirq.X(q0))
    
    circuit.append(cirq.X(q2))
    circuit.append(cirq.TOFFOLI(q0, q1, val))
    circuit.append(cirq.X(q2))

def build_grover_circuit():
    """
    Builds a quantum circuit that finds room arrangements with exactly 2 adjacent public rooms.
    
    The circuit uses:
    - 3 qubits to represent rooms (public=1, private=0)
    - 1 auxiliary qubit for marking valid states
    - 2 Grover iterations to amplify the valid states
    """
    # Create 4 qubits: 3 for rooms + 1 auxiliary 
    qubits = cirq.LineQubit.range(4)
    q0, q1, q2, val = qubits
    circuit = cirq.Circuit()
    
    # Step 1: Put all room combinations in superposition
    # This creates equal probability of all 8 possible arrangements
    circuit.append(cirq.H.on_each(q0, q1, q2))
    
    # Step 2: Two Grover iterations to amplify valid states
    for _ in range(2):
        # Oracle marks valid states (110 and 011)
        oracle_for_2_adj_public(circuit, qubits)
        
        # Diffusion operator amplifies marked states
        circuit.append(cirq.H.on_each(q0, q1, q2))
        circuit.append(cirq.X.on_each(q0, q1, q2))
        circuit.append(cirq.H(q2).controlled_by(q0, q1))
        circuit.append(cirq.X.on_each(q0, q1, q2))
        circuit.append(cirq.H.on_each(q0, q1, q2))
    
    # Step 3: Measure the result
    circuit.append(cirq.measure(q0, q1, q2, key='result'))
    return circuit

# Run the quantum circuit 100 times
simulator = cirq.Simulator()
circuit = build_grover_circuit()
result = simulator.run(circuit, repetitions=100)

# Show results with visual representation
print("\nRoom Arrangements Found:")
print("(■ = public space, □ = private space)")
print("-" * 40)

# Process and display results
# Valid arrangements should be 110 and 011
counts = result.histogram(key='result')
for state, count in counts.items():
    # Convert state number to binary string and visual layout
    binary = format(state, f'0{3}b')
    visual = ''.join(['■' if b=='1' else '□' for b in binary])
    
    # Check if this is a valid arrangement
    is_valid = binary in ['110', '011']
    validity = "VALID!" if is_valid else "Invalid"
    
    # Display the results
    print(f"Layout: {visual}")
    print(f"Found {count} times")
    print(f"Binary: {binary} - {validity}")
    print("-" * 40)

# The quantum algorithm should show higher counts for 110 and 011
# compared to other arrangements, demonstrating quantum advantage
# in finding valid room layouts
