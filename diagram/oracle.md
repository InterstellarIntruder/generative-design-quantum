flowchart LR
    A[Superposition of room quibits with Hadamard gate] --> B{Check for adjacent spaces with <b>X</b> gate.}
    B -->|if - q0 & q1| C[Set <b>a_adj0</b> = 1]
    B -->|if - q2 & q3| D[Set <b>a_adj1</b> = 1]
    B -->|Otherwise| E[Skip <b>a_adj0</b> and <b>a_adj1</b>]

    C --> F{Compute XOR: Exactly one pair of public spaces?}
    D --> F
    E --> F

    F -->|Yes| G[val = 1: Valid]
    F -->|No| H[val = 0: Invalid]

    G --> I[Reset Variables & Output Result]
    H --> I
    I --> o(( ))

    %% Add a styled note with HTML-like syntax
    F -.-> N["<div style='font-style: italic; font-size: 14px;'>Note on XOR: We do this with CNOT it Outputs true if exactly one input is true, false otherwise</div>"]
