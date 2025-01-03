import cirq
from draw_utils import setup_logging, print_header, print_results, plot_results

##############################################################################
# ORACLE: The oracle is a quantum operation that "marks" solutions by flipping
# a target qubit when it sees a valid state. In this case, we're looking for:
# - Exactly 2 ones (public rooms) out of 4 qubits
# - Exactly 1 pair of adjacent ones, but only in windows (q0,q1) or (q2,q3)
##############################################################################
def oracle_count_nonoverlapping_adjacency(circuit, qubits):
    """
    Oracle implementation using ancilla (helper) qubits to check conditions.
    
    Qubit layout:
      qubits[0..3] = room qubits q0,q1,q2,q3 (main computation qubits)
      qubits[4]    = oracle/val qubit (flipped when solution found)
      qubits[5..8] = ancillas: helper qubits that start and end in |0⟩ state
                     - a_count: marks if exactly 2 rooms are public
                     - a_adj0: marks if (q0,q1) are both 1
                     - a_adj1: marks if (q2,q3) are both 1
                     - a_xor: helps check for exactly one adjacent pair
    """

    q0, q1, q2, q3, val = qubits[:5]
    a_count, a_adj0, a_adj1, a_xor = qubits[5:9]

    #-----------------------------------------------------------------------
    # STEP 1: Mark a_count=1 if exactly 2-of-4
    #         We'll do this by toggling a_count for each pattern of 2-of-4:
    #         1100, 1010, 1001, 0110, 0101, 0011.
    #         (We do not check adjacency here; this is purely "2-of-4".)
    #-----------------------------------------------------------------------
    two_of_four_patterns = [
        (1,1,0,0),
        (1,0,1,0),
        (1,0,0,1),
        (0,1,1,0),
        (0,1,0,1),
        (0,0,1,1),
    ]
    for pattern in two_of_four_patterns:
        # 1A) X on qubits that must be 0
        for i, bit_val in enumerate(pattern):
            if bit_val == 0:
                circuit.append(cirq.X(qubits[i]))
        # 1B) 4-controlled toggle of a_count
        circuit.append(cirq.X(a_count).controlled_by(q0, q1, q2, q3))
        # 1C) Uncompute the X's
        for i, bit_val in enumerate(pattern):
            if bit_val == 0:
                circuit.append(cirq.X(qubits[i]))

    #-----------------------------------------------------------------------
    # STEP 2: a_adj0 = 1 if (q0,q1) = (1,1)
    #-----------------------------------------------------------------------
    circuit.append(cirq.X(a_adj0).controlled_by(q0, q1))

    #-----------------------------------------------------------------------
    # STEP 3: a_adj1 = 1 if (q2,q3) = (1,1)
    #-----------------------------------------------------------------------
    circuit.append(cirq.X(a_adj1).controlled_by(q2, q3))

    #-----------------------------------------------------------------------
    # STEP 4: a_xor = a_adj0 XOR a_adj1
    #         We'll do that with two CNOTs.  a_xor starts at 0, so final = adj0^adj1.
    #         a_xor = 0 ^ a_adj0 ^ a_adj1 = a_adj0 XOR a_adj1
    #-----------------------------------------------------------------------
    circuit.append(cirq.CNOT(a_adj0, a_xor))
    circuit.append(cirq.CNOT(a_adj1, a_xor))

    #-----------------------------------------------------------------------
    # STEP 5: Flip val if (a_count=1) AND (a_xor=1).
    #         In Cirq, "controlled_by(a_count,a_xor)" means
    #         "apply X(val) if both a_count,a_xor are 1."
    #-----------------------------------------------------------------------
    circuit.append(cirq.X(val).controlled_by(a_count, a_xor))

    #-----------------------------------------------------------------------
    # STEP 6: UNCOMPUTE all ancillas to return them to |0>.
    #         Reverse steps 4..2..1 in that order.
    #-----------------------------------------------------------------------
    # Uncompute the XOR:
    circuit.append(cirq.CNOT(a_adj1, a_xor))
    circuit.append(cirq.CNOT(a_adj0, a_xor))

    # Uncompute adjacency:
    circuit.append(cirq.X(a_adj1).controlled_by(q2, q3))
    circuit.append(cirq.X(a_adj0).controlled_by(q0, q1))

    # Uncompute the "2-of-4" counting:
    for pattern in reversed(two_of_four_patterns):
        for i, bit_val in enumerate(pattern):
            if bit_val == 0:
                circuit.append(cirq.X(qubits[i]))
        circuit.append(cirq.X(a_count).controlled_by(q0, q1, q2, q3))
        for i, bit_val in enumerate(pattern):
            if bit_val == 0:
                circuit.append(cirq.X(qubits[i]))


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
        oracle_count_nonoverlapping_adjacency(circuit, qubits)

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
    result = simulator.run(circuit, repetitions=1000)
    # Count the frequency of each output state
    counts = result.histogram(key='result')
    all_results[iters] = counts
    print_results(counts, iters)

plot_filename = plot_results(all_results, iterations_to_try, timestamp)

print(f"\nSaved log to {log_filename}")
print(f"Saved plot to {plot_filename}")
