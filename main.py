import os
import time
import logging
from dimacs_parser import parse_dimacs
from genetic_algorithm_sat import GeneticAlgorithmSAT
from cnf_generator import generate_hard_3sat

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    """
    Main function to run the SAT solver on multiple CNF files.
    Generates CNF files if not enough exist, solves them using a genetic algorithm,
    and reports the best overall solution.
    """

    folder_path = 'cnf_files'
    num_files = 30

    # Check if CNF files already exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    cnf_files = [f for f in os.listdir(folder_path) if f.endswith('.cnf')]

    if len(cnf_files) < num_files:
        # If not enough CNF files exist, generate them
        generate_hard_3sat(num_variables=50, num_clauses=200, folder_path=folder_path, num_files=num_files)
        cnf_files = [f for f in os.listdir(folder_path) if f.endswith('.cnf')]

    best_overall_solution = None
    best_overall_fitness = -1
    best_overall_runtime = float('inf')
    best_overall_file = ''

    # Read and solve CNF files
    for cnf_file in cnf_files:
        file_path = os.path.join(folder_path, cnf_file)
        num_variables, clauses = parse_dimacs(file_path)

        ga_solver = GeneticAlgorithmSAT(num_variables, clauses, population_size=100, generations=1000,
                                        mutation_rate=0.01)

        start_time = time.time()
        best_solution, best_fitness = ga_solver.run()
        end_time = time.time()
        runtime = end_time - start_time

        logging.info(f'File: {cnf_file}')
        logging.info(f'Best solution: {best_solution}')
        logging.info(f'Fitness of the best solution: {best_fitness}')
        logging.info(f'Runtime: {runtime:.4f} seconds\n')

        if best_fitness > best_overall_fitness or (
                best_fitness == best_overall_fitness and runtime < best_overall_runtime):
            best_overall_solution = best_solution
            best_overall_fitness = best_fitness
            best_overall_runtime = runtime
            best_overall_file = cnf_file

    logging.info('Overall Best solution:')
    logging.info(f'File: {best_overall_file}')
    logging.info(f'Best solution: {best_overall_solution}')
    logging.info(f'Fitness of the best solution: {best_overall_fitness}')
    logging.info(f'Runtime: {best_overall_runtime:.4f} seconds\n')


if __name__ == '__main__':
    main()
