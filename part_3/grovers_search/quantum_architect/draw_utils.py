import matplotlib.pyplot as plt
import sys
from datetime import datetime

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

def setup_logging():
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f'grover_results_{timestamp}.txt'
    sys.stdout = Logger(log_filename)
    return timestamp, log_filename

def print_header():
    print("GROVER'S ALGORITHM (Option 2) FOR NON-OVERLAPPING ADJACENCY")
    print("=" * 50)
    print("\nWe have 4 room-qubits in a row. We want states that satisfy:")
    print("- Exactly 2 public rooms (i.e. exactly two 1s).")
    print("- Exactly one adjacency pair, but *only* in (q0,q1) or (q2,q3).")
    print("Hence valid states are 1100 and 0011 only.")
    print("We build the oracle to check both conditions inside the circuit.")
    print("\nStarting runs...")

def print_results(counts, iters):
    total = sum(counts.values())
    print(f"\n{'-'*10} Running with {iters} Grover iteration{'s' if iters>1 else ''} {'-'*10}")
    print(f"Results from {total} shots:")
    for state, cnt in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        bstr = format(state, '04b')
        visual = ''.join('[P]' if c=='1' else '[_]' for c in bstr)
        is_valid = (bstr in ['1100', '0011'])
        print(f"  {bstr} -> {visual}, Count = {cnt} ({cnt/total*100:.1f}%) "
              f"{'VALID' if is_valid else 'invalid'}")

def plot_results(all_results, iterations_to_try, timestamp):
    plt.figure(figsize=(18, 6))
    states = [format(i, '04b') for i in range(16)]
    valid_states = ['1100', '0011']

    for idx, iters in enumerate(iterations_to_try):
        plt.subplot(1, 3, idx+1)
        counts = all_results[iters]
        data = [counts.get(int(s,2), 0) for s in states]
        bars = plt.bar(range(16), data)
        for i, s in enumerate(states):
            bars[i].set_color('lightblue' if s in valid_states else 'lightblue')
        plt.title(f"{iters} Grover iteration{'s' if iters>1 else ''}")
        plt.xticks(range(16), states, rotation=45)
        plt.ylabel('Frequency')
        for i, val in enumerate(data):
            if val > 0:
                label = ''.join('■' if c=='1' else '□' for c in states[i])
                plt.text(i, val, label, ha='center', va='bottom', rotation=45)

    plt.suptitle("Distribution of Results with Different Numbers of Grover Iterations\n"
                 "■ = public room, □ = private room",
                 fontsize=14)
    plt.tight_layout()

    plot_filename = f'grover_plot_{timestamp}.png'
    plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
    plt.close()
    return plot_filename
