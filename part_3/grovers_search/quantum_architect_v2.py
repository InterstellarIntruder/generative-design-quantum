import cirq
import matplotlib.pyplot as plt
from datetime import datetime
import sys

##############################################################################
# ORACLE: Count how many 1s you have (must be 2) AND
#         check adjacency in the two disjoint windows (q0,q1) and (q2,q3),
#         then flip the "val" qubit if and only if
#         ( exactly 2 total ) AND ( exactly 1 pair of adjacent 1s ).
##############################################################################
def oracle_count_nonoverlapping_adjacency(circuit, qubits):
    """
    We assume:
      qubits[0..3] = room qubits q0,q1,q2,q3
      qubits[4]    = oracle/val qubit
      qubits[5..8] = ancillas: a_count, a_adj0, a_adj1, a_xor  (all start in |0>)
    Steps:
      1) Mark a_count=1 if exactly 2 of the 4 room qubits are 1.
      2) Mark a_adj0=1 if (q0,q1) are both 1.
      3) Mark a_adj1=1 if (q2,q3) are both 1.
      4) Compute a_xor = a_adj0 XOR a_adj1.
      5) Multi-controlled flip of val if (a_count=1) AND (a_xor=1).
      6) Uncompute steps 4..1 so all ancillas return to |0>.
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
    We now have 9 qubits total:
        4 "room" qubits: q0, q1, q2, q3
        1 "val" qubit:   q4
        4 ancillas:      q5 = a_count, q6 = a_adj0, q7 = a_adj1, q8 = a_xor
    We'll perform standard Grover iterations:
      - put the 4 "room" qubits into H-superposition
      - repeated Oracle + Diffusion
      - measure the 4 room qubits
    """
    qubits = cirq.LineQubit.range(9)
    q0, q1, q2, q3 = qubits[:4]
    val = qubits[4]

    circuit = cirq.Circuit()

    # Step A: put the 4 room-qubits into superposition
    circuit.append(cirq.H.on_each(q0, q1, q2, q3))

    # Step B: run the requested number of Grover iterations
    for _ in range(num_iterations):
        # --- Oracle step ---
        oracle_count_nonoverlapping_adjacency(circuit, qubits)

        # --- Diffusion step (on q0..q3 only) ---
        circuit.append(cirq.H.on_each(q0, q1, q2, q3))
        circuit.append(cirq.X.on_each(q0, q1, q2, q3))
        # 4-controlled Z (on the highest qubit q3):
        circuit.append(cirq.H(q3).controlled_by(q0, q1, q2))
        circuit.append(cirq.X.on_each(q0, q1, q2, q3))
        circuit.append(cirq.H.on_each(q0, q1, q2, q3))

    # Step C: measure the 4 room-qubits
    circuit.append(cirq.measure(q0, q1, q2, q3, key='result'))

    return circuit


##############################################################################
# SCRIPT MAIN: logging, running, printing, plotting
##############################################################################

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_filename = f'grover_results_{timestamp}.txt'

class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, 'w', encoding='utf-8')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = Logger(log_filename)

print("GROVER'S ALGORITHM (Option 2) FOR NON-OVERLAPPING ADJACENCY")
print("=" * 50)
print("\nWe have 4 room-qubits in a row. We want states that satisfy:")
print("- Exactly 2 public rooms (i.e. exactly two 1s).")
print("- Exactly one adjacency pair, but *only* in (q0,q1) or (q2,q3).")
print("Hence valid states are 1100 and 0011 only.")
print("We build the oracle to check both conditions inside the circuit.")
print("\nStarting runs...")

iterations_to_try = [1, 2, 3]
all_results = {}

for iters in iterations_to_try:
    print(f"\n{'-'*10} Running with {iters} Grover iteration{'s' if iters>1 else ''} {'-'*10}")
    simulator = cirq.Simulator()
    circuit = build_grover_circuit(iters)
    result = simulator.run(circuit, repetitions=1000)
    counts = result.histogram(key='result')
    all_results[iters] = counts

    total = sum(counts.values())
    print(f"Results from {total} shots:")
    for state, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        bstr = format(state, '04b')
        visual = ''.join('[P]' if c=='1' else '[_]' for c in bstr)
        # Check if it's one of our 2 valid states
        is_valid = (bstr in ['1100', '0011'])
        print(f"  {bstr} -> {visual}, Count = {cnt} ({cnt/total*100:.1f}%) "
              f"{'VALID' if is_valid else 'invalid'}")

# Let's plot the distribution
plt.figure(figsize=(18, 6))
states = [format(i, '04b') for i in range(16)]
valid_states = ['1100', '0011']

for idx, iters in enumerate(iterations_to_try):
    plt.subplot(1, 3, idx+1)
    counts = all_results[iters]
    data = [counts.get(int(s,2), 0) for s in states]
    bars = plt.bar(range(16), data)
    for i, s in enumerate(states):
        bars[i].set_color('green' if s in valid_states else 'lightgray')
    plt.title(f"{iters} Grover iteration{'s' if iters>1 else ''}")
    plt.xticks(range(16), states, rotation=45)
    plt.ylabel('Frequency')
    for i, val in enumerate(data):
        if val > 0:
            label = ''.join('[P]' if c=='1' else '[_]' for c in states[i])
            plt.text(i, val, label, ha='center', va='bottom', rotation=45)

plt.suptitle("Grover’s Algorithm Results: Exactly 2 public rooms + Non-overlapping adjacency windows\n"
             "Valid states = 1100, 0011 (green bars)",
             fontsize=14)
plt.tight_layout()

plot_filename = f'grover_plot_{timestamp}.png'
plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
plt.close()

print(f"\nSaved log to {log_filename}")
print(f"Saved plot to {plot_filename}")
