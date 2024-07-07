import re

def parse_dimacs(file_path):
    with open(file_path, 'r') as file:
        content = file.readlines()

    clauses = []
    num_variables = 0
    for line in content:
        if line.startswith('c'):
            continue
        elif line.startswith('p'):
            parts = re.split(r'\s+', line.strip())
            num_variables = int(parts[2])
        else:
            parts = re.split(r'\s+', line.strip())
            clause = [int(x) for x in parts if x != '0']
            clauses.append(clause)

    return num_variables, clauses
