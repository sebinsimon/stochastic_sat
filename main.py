import time
from dimacs_parser import parse_dimacs
from genetic_algorithm_sat import GeneticAlgorithmSAT


def main():
    file_path = 'example.cnf'
    num_variables, clauses = parse_dimacs(file_path)

    ga_solver = GeneticAlgorithmSAT(num_variables, clauses, population_size=100, generations=1000, mutation_rate=0.01)

    start_time = time.time()
    best_solution, best_fitness = ga_solver.run()
    end_time = time.time()

    runtime = end_time - start_time

    print(f'Best solution: {best_solution}')
    print(f'Fitness of the best solution: {best_fitness}')
    print(f'Runtime: {runtime:.4f} seconds')


if __name__ == '__main__':
    main()
