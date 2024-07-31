import os
import random
import logging
from collections import defaultdict

def generate_hard_3sat(num_variables, num_clauses, folder_path, num_files):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i in range(num_files):
        file_path = os.path.join(folder_path, f'cnf_{i+1}.cnf')
        clauses = set()
        variable_occurrences = defaultdict(int)

        while len(clauses) < num_clauses:
            clause = set()
            while len(clause) < 3:
                literal = random.randint(1, num_variables)
                if random.choice([True, False]):
                    literal = -literal
                clause.add(literal)

            clause = tuple(sorted(clause))  # Sort to prevent duplicates
            if clause not in clauses:
                clauses.add(clause)
                for literal in clause:
                    variable_occurrences[abs(literal)] += 1

        # Convert set of clauses to a list of lists
        clauses = [list(clause) for clause in clauses]

        # Ensure a balanced occurrence of variables
        for var in range(1, num_variables + 1):
            positive_count = sum(1 for clause in clauses for lit in clause if lit == var)
            negative_count = sum(1 for clause in clauses for lit in clause if lit == -var)

            while abs(positive_count - negative_count) > 1:
                for clause in clauses:
                    if var in clause and positive_count > negative_count:
                        clause[clause.index(var)] = -var
                        positive_count -= 1
                        negative_count += 1
                        break
                    elif -var in clause and negative_count > positive_count:
                        clause[clause.index(-var)] = var
                        positive_count += 1
                        negative_count -= 1
                        break

        with open(file_path, 'w') as f:
            f.write(f'p cnf {num_variables} {num_clauses}\n')
            for clause in clauses:
                f.write(' '.join(map(str, clause)) + ' 0\n')
        logging.info(f'Generated hard CNF file: {file_path}')
