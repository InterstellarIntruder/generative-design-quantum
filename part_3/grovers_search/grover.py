import cirq
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import sys

def oracle_two_public_rooms(circuit, qubits):
    """
    Marks the 'val' qubit if and only if exactly two of the four room qubits are |1>.
    Ignores adjacency. We do not use 'count' anymore.
    """
    # Unpack qubits: first 4 are rooms, 5th is val, 6th is an unused ancilla
    q0, q1, q2, q3, val, _unused_count = qubits

    # We will systematically flip `val` for each pattern of exactly-two-ones
    two_public_patterns = [
        (1, 1, 0, 0),
        (1, 0, 1, 0),
        (1, 0, 0, 1),
        (0, 1, 1, 0),
        (0, 1, 0, 1),
        (0, 0, 1, 1)
    ]

    def flip_val_if_pattern(pattern):
        """
        Multi-controlled approach:
          - For each qubit supposed to be 0, apply an X before the controlled gate
            (which effectively makes "control=1" happen only if original was |0>).
          - Then do a 4-controlled X on `val`.
          - Finally uncompute the X's you applied.
        """
        # 1) X on all qubits that must be 0
        for i, bit_val in enumerate(pattern):
            if bit_val == 0:
                circuit.append(cirq.X(qubits[i]))
        
        # 2) Multi-controlled NOT on val (i.e., flip val if all controls are 1)
        circuit.append(cirq.X(val).controlled_by(q0, q1, q2, q3))
        
        # 3) Undo those X gates
        for i, bit_val in enumerate(pattern):
            if bit_val == 0:
                circuit.append(cirq.X(qubits[i]))

    # Apply the above for each pattern that has exactly two 1's
    for pat in two_public_patterns:
        flip_val_if_pattern(pat)

def build_grover_circuit(num_iterations):
    """
    Builds a Grover circuit to find layouts with exactly 2 public rooms.
    """
    qubits = cirq.LineQubit.range(6)  # q0, q1, q2, q3, val, count (but 'count' unused)
    circuit = cirq.Circuit()
    
    # 1) Initialize room qubits in superposition
    circuit.append(cirq.H.on_each(*qubits[:4]))
    
    # 2) Grover iterations
    for _ in range(num_iterations):
        # --- Oracle step ---
        oracle_two_public_rooms(circuit, qubits)
        
        # --- Diffusion step ---
        circuit.append(cirq.H.on_each(*qubits[:4]))
        circuit.append(cirq.X.on_each(*qubits[:4]))
        # 4-controlled Z on the 4 room qubits:
        circuit.append(cirq.H(qubits[3]).controlled_by(*qubits[:3]))
        circuit.append(cirq.X.on_each(*qubits[:4]))
        circuit.append(cirq.H.on_each(*qubits[:4]))
    
    # 3) Measure the room qubits
    circuit.append(cirq.measure(*qubits[:4], key='result'))
    return circuit

# Create a log file with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
log_filename = f'grover_results_{timestamp}.txt'

# Redirect stdout to both console and file with UTF-8 encoding
class Logger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, 'w', encoding='utf-8')  # Add UTF-8 encoding

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()

    def flush(self):
        self.terminal.flush()
        self.log.flush()

sys.stdout = Logger(log_filename)

# Run and plot results
print("GROVER'S ALGORITHM FOR ROOM LAYOUT OPTIMIZATION")
print("=" * 50)
print("\nProblem Configuration:")
print("- 4 rooms in a row")
print("- Looking for layouts with exactly 2 public rooms")
print("- Public room = [P], Private room = [_]")
print("\nAll possible 4-bit strings that have exactly two 1s are valid solutions.\n")

iterations_to_try = [1, 2, 3]
all_results = {}

print("Starting algorithm runs...\n")

for iters in iterations_to_try:
    print(f"\nRunning with {iters} iteration{'s' if iters > 1 else ''}:")
    print("-" * 40)
    
    simulator = cirq.Simulator()
    circuit = build_grover_circuit(iters)
    result = simulator.run(circuit, repetitions=100)
    all_results[iters] = result.histogram(key='result')
    
    # Print detailed results for this iteration
    counts = all_results[iters]
    total_counts = sum(counts.values())
    
    print(f"\nResults from {total_counts} measurements:")
    for state, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        binary = format(state, '04b')
        visual = ''.join(['[P]' if b=='1' else '[_]' for b in binary])
        
        # Calculate properties
        num_public = binary.count('1')
        # We won't require adjacency. We'll just note if there are two publics.
        is_valid = (num_public == 2)
        
        print(f"\nLayout: {visual}")
        print(f"Binary: {binary}")
        print(f"Found: {count} times ({count/total_counts*100:.1f}%)")
        print("Analysis:")
        print(f"  Public rooms: {num_public} {'✓' if num_public==2 else '✗'}")
        print(f"  Overall: {'VALID' if is_valid else 'invalid'}")

# Create and save visualization
plt.figure(figsize=(20, 8))
states = [format(i, '04b') for i in range(16)]
# Exactly-two-public states:
valid_states = [
    '1100', '1010', '1001',
    '0110', '0101', '0011'
]

for i, iters in enumerate(iterations_to_try):
    plt.subplot(1, 3, i+1)
    counts = all_results[iters]
    data = [counts.get(int(state, 2), 0) for state in states]
    
    bars = plt.bar(range(len(states)), data)
    for idx, state in enumerate(states):
        # Color green if exactly two 1s, else gray
        bars[idx].set_color('green' if state in valid_states else 'lightgray')
    
    plt.title(f'{iters} Iteration{"s" if iters > 1 else ""}', fontsize=14)
    plt.xticks(range(len(states)), [f'|{s}⟩' for s in states], rotation=45, fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    
    # Add room layout above each bar with non-zero count
    for idx, count in enumerate(data):
        if count > 0:
            binary = states[idx]
            visual = '[' + ']['.join('P' if b=='1' else '_' for b in binary) + ']'
            plt.text(idx, count, visual, 
                     ha='center', va='bottom', 
                     fontsize=10,
                     rotation=45)

plt.tight_layout()
plt.suptitle('Distribution of Results with Different Numbers of Grover Iterations\n'
             'Green bars = Valid states (2 public rooms)\n'
             '[P] = public room, [_] = private room', 
             y=1.05, 
             fontsize=16)

plot_filename = f'grover_plot_{timestamp}.png'
plt.savefig(plot_filename, bbox_inches='tight', dpi=300)
plt.close()

print(f"\nResults have been saved to:")
print(f"- Log file: {log_filename}")
print(f"- Plot: {plot_filename}")
