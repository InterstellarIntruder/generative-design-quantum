flowchart TD
    A[Start: Room Configuration Inputs] --> B{Check q0 and q1: Are both public spaces?}
    B -->|Yes| C[Set a_adj0 = 1]
    B -->|No| D[Skip setting a_adj0]

    C --> E{Check q2 and q3: Are both public spaces?}
    D --> E

    E -->|Yes| F[Set a_adj1 = 1]
    E -->|No| G[Skip setting a_adj1]

    F --> H{Compute XOR: Is exactly one pair public spaces?}
    G --> H

    H -->|Yes| I[Set val = 1 - Valid Configuration]
    H -->|No| J[Set val = 0 - Invalid Configuration]

    I --> K[Uncompute: Reset a_adj0, a_adj1, and a_xor]
    J --> K

    K --> L[Output Result: val = 1 - Valid or val = 0 - Invalid]
    L --> M[End]
