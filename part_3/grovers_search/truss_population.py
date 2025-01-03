import numpy as np

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
