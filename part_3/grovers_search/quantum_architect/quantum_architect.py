import cirq
from draw_utils import setup_logging, print_header, print_results, plot_results

##############################################################################
# ORACLE: The oracle is a quantum operation that "marks" solutions by flipping
# a target qubit when it sees a valid state. In this case, we're looking for:
# - Exactly 2 ones (public rooms) out of 4 qubits
# - Exactly 1 pair of adjacent ones, but only in windows (q0,q1) or (q2,q3)
##############################################################################
def oracle_nonoverlapping_adjacency(circuit, qubits):
    """
    Simplified oracle that only checks for exactly one adjacent pair in allowed windows.
    
    Qubit layout:
      qubits[0..3] = room qubits q0, q1, q2, q3 (main computation qubits)
      qubits[4]    = oracle/val qubit (flipped when solution found)
      qubits[5..7] = ancillas:
                     - a_adj0: marks if (q0, q1) are both 1
                     - a_adj1: marks if (q2, q3) are both 1
                     - a_xor: helps check for exactly one adjacent pair
    
    What is an ancilla qubit?
      - An ancilla qubit is a helper or auxiliary qubit used in a quantum circuit to store 
        intermediate results or facilitate computations. 
      - Ancilla qubits are often initialized in the |0⟩ state and are "uncomputed" (reset to |0⟩) 
        after use to avoid unintended interference with the circuit's main computation.
    """
    q0, q1, q2, q3, val = qubits[:5]
    a_adj0, a_adj1, a_xor = qubits[5:8]  # We now need only 3 ancilla qubits

    # STEP 1: Check if (q0, q1) are both 1
    # The X gate on a_adj0 will be applied only if q0 and q1 are both |1>.
    # controlled_by is a function that applies a gate to a qubit only if a control qubit is in the |1> state.
    # append is a function that appends a quantum operation to the circuit
    # Example:
    #   Initial: q0 = 1, q1 = 1, a_adj0 = 0
    #   After:   a_adj0 = 1 (flipped because q0 and q1 are both 1)
    circuit.append(cirq.X(a_adj0).controlled_by(q0, q1))

    # STEP 2: Check if (q2, q3) are both 1
    # The X gate on a_adj1 will be applied only if q2 and q3 are both |1>.
    # Example:
    #   Initial: q2 = 1, q3 = 0, a_adj1 = 0
    #   After:   a_adj1 = 0 (unchanged because q2 and q3 are not both 1)
    circuit.append(cirq.X(a_adj1).controlled_by(q2, q3))

    # STEP 3: Compute the XOR (exclusive OR) of a_adj0 and a_adj1 using CNOT gates
    # XOR means the result is 1 if exactly one of the inputs is 1, otherwise it's 0.
    # Example:
    #   Initial: a_adj0 = 1, a_adj1 = 0, a_xor = 0
    #   First CNOT: a_xor = a_xor ⊕ a_adj0 = 0 ⊕ 1 = 1
    #   Second CNOT: a_xor = a_xor ⊕ a_adj1 = 1 ⊕ 0 = 1
    #   Final: a_xor = 1 (indicates exactly one adjacency was found)
    circuit.append(cirq.CNOT(a_adj0, a_xor))  # Add a_adj0 to a_xor
    circuit.append(cirq.CNOT(a_adj1, a_xor))  # Add a_adj1 to a_xor to complete XOR

    # STEP 4: Flip val if exactly one adjacency was found
    # If a_xor = 1 (indicating exactly one pair was found), flip val.
    # Example:
    #   Initial: a_xor = 1, val = 0
    #   After:   val = 1 (flipped because a_xor = 1)
    circuit.append(cirq.X(val).controlled_by(a_xor))

    # STEP 5: Uncompute ancillas (in reverse order to clean up the circuit)
    # Uncompute the XOR operation:
    #   Reverse the steps used to compute a_xor.
    circuit.append(cirq.CNOT(a_adj1, a_xor))
    circuit.append(cirq.CNOT(a_adj0, a_xor))
    
    # Uncompute a_adj1:
    #   Reverse the controlled X gate on a_adj1.
    circuit.append(cirq.X(a_adj1).controlled_by(q2, q3))
    
    # Uncompute a_adj0:
    #   Reverse the controlled X gate on a_adj0.
    circuit.append(cirq.X(a_adj0).controlled_by(q0, q1))


##############################################################################
# BUILD THE FULL GROVER CIRCUIT
##############################################################################
def build_grover_circuit(num_iterations):
    """
    Constructs Grover's algorithm circuit for our search problem.
    
    Grover's algorithm steps:
    1. Initialize qubits in superposition (equal probability of all states)
       using Hadamard gates (H)
    2. Repeat num_iterations times:
       a. Oracle: marks solution states by flipping a target qubit
       b. Diffusion: amplifies marked states (increases their probability)
    3. Measure the qubits to get the result
    
    The optimal number of iterations is approximately π/4 * sqrt(N/M),
    where N is total states (16) and M is number of solutions (2).
    In our case, that's about 2.2 iterations.
    """
    # Create 9 qubits in a line (indexed 0 through 8)
    qubits = cirq.LineQubit.range(9)
    q0, q1, q2, q3 = qubits[:4]  # Main computation qubits
    val = qubits[4]              # Oracle's target qubit

    circuit = cirq.Circuit()

    # Step A: Initialize superposition with Hadamard gates
    # H|0⟩ creates equal superposition (1/√2)(|0⟩ + |1⟩)
    circuit.append(cirq.H.on_each(q0, q1, q2, q3))

    # Step B: Grover iterations
    for _ in range(num_iterations):
        # Oracle marks solutions by flipping val qubit
        oracle_nonoverlapping_adjacency(circuit, qubits)

        # Diffusion operator (reflection about mean)
        # 1. H gates to change basis
        circuit.append(cirq.H.on_each(q0, q1, q2, q3))
        # 2. Phase flip about zero state
        circuit.append(cirq.X.on_each(q0, q1, q2, q3))
        # 3. Multi-controlled Z gate (phase flip if all qubits are 1)
        circuit.append(cirq.H(q3).controlled_by(q0, q1, q2))
        # 4. Undo X gates
        circuit.append(cirq.X.on_each(q0, q1, q2, q3))
        # 5. H gates to change back to computational basis
        circuit.append(cirq.H.on_each(q0, q1, q2, q3))

    # Step C: Measure the result
    # This collapses superposition into classical bits
    circuit.append(cirq.measure(q0, q1, q2, q3, key='result'))

    return circuit


##############################################################################
# SCRIPT MAIN: Run the quantum circuit multiple times with different iterations
##############################################################################

timestamp, log_filename = setup_logging()
print_header()

# Try different numbers of Grover iterations
# More iterations don't always mean better results due to
# the periodic nature of quantum amplitude amplification
iterations_to_try = [1, 2, 3]
all_results = {}

for iters in iterations_to_try:
    # Create a quantum simulator (since we don't have a real quantum computer)
    simulator = cirq.Simulator()
    circuit = build_grover_circuit(iters)
    # Run the circuit 1000 times to get a distribution of results
    result = simulator.run(circuit, repetitions=5000)
    # Count the frequency of each output state
    counts = result.histogram(key='result')
    all_results[iters] = counts
    print_results(counts, iters)

plot_filename = plot_results(all_results, iterations_to_try, timestamp)

print(f"\nSaved log to {log_filename}")
print(f"Saved plot to {plot_filename}")
