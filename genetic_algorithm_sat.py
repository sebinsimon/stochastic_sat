import random
import numpy as np
import logging


class GeneticAlgorithmSAT:
    def __init__(self, num_variables, clauses, population_size=100, generations=1000, mutation_rate=0.01):
        self.num_variables = num_variables
        self.clauses = clauses
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.population = self._initialise_population()

    def _initialise_population(self):
        return np.random.randint(2, size=(self.population_size, self.num_variables))

    def _fitness(self, individual):
        score = 0
        for clause in self.clauses:
            clause_satisfied = any(
                (literal > 0 and individual[abs(literal) -1] == 1) or
                (literal < 0 and individual[abs(literal) -1] == 0)
                for literal in clause
            )
            if clause_satisfied:
                score += 1
        return score

    def _selection(self, fitnesses):
        # select individuals for the next gen using tournament selection
        selected = []

        for _ in range(self.population_size):
            tournament = random.sample(range(self.population_size), 3)
            selected.append(max(tournament, key=lambda i: fitnesses[i]))
        return self.population[selected]

    def _crossover(self, parent1, parent2):
        # Perform uniform crossover between 2 parents
        mask = np.random.randint(self.num_variables) < 0.5
        child1 = np.where(mask, parent1, parent2)
        child2 = np.where(mask, parent2, parent1)
        return child1, child2

    def _mutate(self, individual):
        # Mutate an individual
        mutation_mask = np.random.randint(self.num_variables) < self.mutation_rate
        individual[mutation_mask] = 1 - individual[mutation_mask]
        return individual

    def run(self):
        best_solution = None
        best_fitness = -1

        for generation in range(self.generations):
            fitnesses = [self._fitness(individual) for individual in self.population]
            max_fitness = max(fitnesses)

            if max_fitness > best_fitness:
                best_fitness = max_fitness
                best_solution = self.population[np.argmax(fitnesses)]

            if best_fitness == len(self.clauses):
                logging.info(f"Perfect solution found in gen {generation}")
                break

            selected_population = self._selection(fitnesses)
            new_population = []

            for i in range(0, self.population_size, 2):
                parent1 = selected_population[i]
                parent2 = selected_population[i + 1]
                child1, child2 = self._crossover(parent1, parent2)
                new_population.append(self._mutate(child1))
                new_population.append(self._mutate(child2))

            self.population = np.array(new_population)

        return best_solution, best_fitness
