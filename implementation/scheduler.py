"""Scheduler: All of the main logic for generating initial solutions,
generating machine schedules, and the local search algorithms can be
found here.
"""

import random
from math import exp

from model import Job, Assignment, Machine

def stochastic_descent(initial, num_machines, iterations=100, datapoints=None):
    """Stochastic Descent local search algorithm.  Randomly generate a
    neighbor state, and, if it's better than our original, update to that
    state.  Essentially greedy.  Prone to getting stuck in local minima.
    """
    current = initial
    current_fitness = dna_fitness(current, num_machines)

    for i in range(iterations):
        a, b = random.sample(range(len(initial)), 2)
        current[a], current[b] = current[b], current[a]
        new_fitness = dna_fitness(current, num_machines)
        if new_fitness < current_fitness:
            current_fitness = new_fitness
        else:
            current[a], current[b] = current[b], current[a]
        
        if datapoints is not None and i in datapoints:
            datapoints[i] = current_fitness

    return generate_schedule(current, num_machines), current_fitness


def simulated_annealing(initial, num_machines, t0, alpha, iterations, datapoints=None):
    """Simulated annealing local search.  Stochastic descent but with a geometrically
    reducing probability of sometimes accepting worse neighbor solutions.
    Allows the algorithm to escape bad wells early and have a better chance
    of finding the global minimum before diving down towards it.
    """
    current = initial
    current_fitness = dna_fitness(initial, num_machines)
    t = t0
    for i in range(iterations):
        a, b = random.sample(range(len(initial)), 2)
        current[a], current[b] = current[b], current[a]
        new_fitness = dna_fitness(current, num_machines)
        if new_fitness < current_fitness:
            current_fitness = new_fitness
        elif random.random() < exp((current_fitness - new_fitness)/t):
            current_fitness = new_fitness
        else:
            current[a], current[b] = current[b], current[a]

        t *= alpha

        if datapoints is not None and i in datapoints:
            datapoints[i] = current_fitness
    return generate_schedule(current, num_machines), current_fitness


def generate_initial_solution(jobs):
    """Generates an initial solution that is sorted by due date and duration."""
    return sorted(jobs, key=initial_sort_key)


def generate_random_solution(jobs):
    """Generates an initial solution that is a random shuffling of jobs."""
    result = jobs[:]
    random.shuffle(result)
    return result


def initial_sort_key(job):
    return (job.due_date, job.duration)


def schedule_fitness(schedule, num_machines):
    """Calculate the fitness of a given schedule.
    
    Every day late for any job is +1 to fitness (big fitness is bad,
    this is a minimizing problem).  Every material switch is +0.5 days penalty.
    """
    penalty = 0
    for machine in schedule:
        loaded_material = None
        for assignment in machine:
            penalty += max(assignment.end - assignment.job.due_date, 0)
            if assignment.job.material != loaded_material:
                if loaded_material is not None:
                    penalty += 0.5
                loaded_material = assignment.job.material
    return penalty

def dna_fitness(solution, num_machines):
    """Given a DNA strand of jobs to work on, generate a schedule and
    return the fitness score of that schedule.
    """
    schedule = generate_schedule(solution, num_machines)
    return schedule_fitness(schedule, num_machines)


def generate_schedule(solution, num_machines):
    """Greedy algorithm.  Go through the list and assign each job to the
    first available machine that can work on it.

    Returns:
        list(Machine): Each machine with its queue (Machine 1 is 0th index)
    """
    machines = [Machine(i + 1) for i in range(num_machines)]
    for job in solution:
        machine = min(machines[i - 1] for i in job.machines)
        if not machine.queue or machine.queue[-1].job.mold != job.mold:
            changeover = True
            start_date = machine.open_date
        else:
            start_date = machine.open_date - machine.queue[-1].job.teardown
            changeover = False
        machine.add(Assignment(job, machine.number, machine.open_date, changeover))
    return machines