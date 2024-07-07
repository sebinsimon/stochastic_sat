import random
import numpy as np


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
        total_fitness = sum(fitnesses)
        probabilities = [f / total_fitness for f in fitnesses]
        selected_indices = np.random.choice(self.population_size, self.population_size, p=probabilities)
        return self.population[selected_indices]

    def _crossover(self, parent1, parent2):
        crossover_point = random.randint(1, self.num_variables - 1)
        child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
        child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
        return child1, child2

    def _mutate(self, individual):
        for i in range(self.num_variables):
            if random.random() < self.mutation_rate:
                individual[i] = 1 - individual[i]
        return individual

    def run(self):
        best_solution = None
        best_fitness =  -1

        for generation in range(self.generations):
            fitnesses = [self._fitness(individual) for individual in self.population]
            max_fitness = max(fitnesses)
            if max_fitness > best_fitness:
                best_fitness = max_fitness
                best_solution = self.population[np.argmax(fitnesses)]

            if best_fitness == len(self.clauses):
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
