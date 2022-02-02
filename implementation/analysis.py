"""Analysis: a quickly changing module containing analysis functions
for outputting data for plotting.  The goal was to enable me to reuse
functionality during multiple tests, but a lot of the tests required
small tweaks to the functions as I went, so not all analysis cases
are correct or well-preserved all the time.
"""

import csv
import time
from pathlib import Path
import random

from data_io import import_csv, export_csv
from scheduler import generate_initial_solution, generate_random_solution, stochastic_descent, dna_fitness, simulated_annealing

TESTCASES = ["baseline", "heavy", "late", "light"]


def run_csv_testcase(name, algorithm):
    """Helper function to run a single test case using default i=100"""
    if name not in TESTCASES:
        raise ValueError(f"{name} not in {TESTCASES}")
    start_time = time.perf_counter()
    jobs = import_csv(f"{name}-jobs.csv")
    initial = generate_random_solution(jobs)
    result, fitness = algorithm(initial, 8)
    export_csv(result, fitness,  time.perf_counter() - start_time, f"{name}-output.csv")


def stochastic_descent_stop_iter_experiment():
    """Test out what stop iteration value works best by trying a bunch and
    seeing where the benefits stop paying off.
    """
    resultfile = Path("results/stochastic-descent-stop-iters.csv")
    with open(resultfile, "w") as csvfile:
        fieldnames = ["testcase", "iteration", "fitness"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        iterations = [5, 10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 750000, 1000000]
        for testcase in TESTCASES:
            for trial in range(5):
                print(f"Running trial {trial + 1} of '{testcase}' case.")
                datapoints = {it: 0 for it in iterations}
                start_time = time.perf_counter()
                jobs = import_csv(f"{testcase}-jobs.csv")
                initial = generate_random_solution(jobs)
                _result, _fitness = stochastic_descent(initial, 8, 1000001, datapoints)
                stop_time = time.perf_counter()
                
                for iteration, fitness in datapoints.items():
                    writer.writerow({
                        "testcase": testcase,
                        "iteration": iteration,
                        "fitness": fitness,
                    })


def simulated_annealing_stop_iter_experiment():
    """Test out what stop iteration value works best by trying a bunch and
    seeing where the benefits stop paying off.
    """
    resultfile = Path("results/simulated-annealing-stop-iters.csv")
    with open(resultfile, "w") as csvfile:
        fieldnames = ["testcase", "iteration", "fitness"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        iterations = [5, 10, 50, 100, 500, 1000, 5000, 10000, 50000, 100000, 500000, 750000, 1000000]
        for testcase in TESTCASES:
            for trial in range(5):
                print(f"Running trial {trial + 1} of '{testcase}' case.")
                datapoints = {it: 0 for it in iterations}
                start_time = time.perf_counter()
                jobs = import_csv(f"{testcase}-jobs.csv")
                initial = generate_random_solution(jobs)
                _result, _fitness = simulated_annealing(initial, 8, 10000, 0.89, 1000001, datapoints)
                stop_time = time.perf_counter()
                
                for iteration, fitness in datapoints.items():
                    writer.writerow({
                        "testcase": testcase,
                        "iteration": iteration,
                        "fitness": fitness,
                    })


def simulated_annealing_t0_calculation():
    """Try to find a good initial temperature for SA."""
    resultfile = Path("results/sa-t0.csv")
    with open(resultfile, "w") as csvfile:
        fieldnames = ["random delta", "sorted delta"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        jobs = import_csv("baseline-jobs.csv")
        for _ in range(1000):
            random_initial = generate_random_solution(jobs)
            sorted_initial = generate_initial_solution(jobs)
            random_f0 = dna_fitness(random_initial, 8)
            sorted_f0 = dna_fitness(sorted_initial, 8)
            a, b = random.sample(range(len(random_initial)), 2)
            random_initial[a], random_initial[b] = random_initial[b], random_initial[a]
            sorted_initial[a], sorted_initial[b] = sorted_initial[b], sorted_initial[a]
            random_f1 = dna_fitness(random_initial, 8)
            sorted_f1 = dna_fitness(sorted_initial, 8)
            writer.writerow({
                "random delta": random_f0 - random_f1,
                "sorted delta": sorted_f0 - sorted_f1,
            })


def simulated_annealing_alpha():
    """Try to find a good alpha for SA"""
    jobs = import_csv("late-jobs.csv")
    outfile = Path("results/sa-alpha-late.csv")
    with open(outfile, "w") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["alpha", "fitness", "final temp"])
        writer.writeheader()

        for alpha in [val / 100 for val in range(60, 100)]:
            print("testing alpha:", alpha)
            initial = generate_initial_solution(jobs)
            for _ in range(30):
                schedule, fitness, t_final = simulated_annealing(initial, 8, 10000, alpha, 10000)
                writer.writerow({"alpha": alpha, "fitness": fitness, "final temp": t_final})


def test_greedy_only():
    """Check and see if the initial solution is noticably worse that
    the SD solution after iterations."""
    for testcase in TESTCASES:
        jobs = import_csv(f"{testcase}-jobs.csv")
        initial = generate_initial_solution(jobs)
        print(f"'{testcase}' initial solution fitness: {dna_fitness(initial, 8)}")
        

def run_simulated_annealing():
    """Quick run of SA to see if it works."""
    for testcase in TESTCASES:
        jobs = import_csv(f"{testcase}-jobs.csv")
        initial = generate_initial_solution(jobs)
        schedule, fitness, _t = simulated_annealing(initial, 8, 10000, .89, 750)
        print(testcase, fitness)



def compare_sa_sd_with_random_and_sorted_initials():
    """Seeing whether random or sorted starting conditions work better."""
    iteration_values = [100, 500, 1000, 5000, 10000, 50000, 100000]
    resultfile = Path("results/sa-sd-random-and-sorted-baseline.csv")
    with open(resultfile, "w") as csvfile:
        fieldnames = ["algorithm", "testcase", "start type", "iteration", "fitness"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        sd = lambda initial, datapoints: stochastic_descent(initial, 8, 100001, datapoints)
        sd.name = "SD"
        sa = lambda initial, datapoints: simulated_annealing(initial, 8, 10000, .89, 100001, datapoints)
        sa.name = "SA"
        generate_initial_solution.name = "sorted"
        generate_random_solution.name = "random"
        for testcase in TESTCASES:
            if testcase != "baseline":
                continue
            for algo in [sd, sa]:
                for startcase in [generate_initial_solution, generate_random_solution]:
                    print(f"Starting '{testcase}' with '{startcase.name}' and '{algo.name}'...")
                    averages = {it: 0 for it in iteration_values}
                    row = {
                        "algorithm": "SD" if algo == sd else "SA",
                        "testcase": testcase,
                        "start type": "random" if startcase == generate_random_solution else "sorted"
                    }
                    for sample in range(3):
                        fitnesses = {it: 0 for it in iteration_values}
                        jobs = import_csv(f"{testcase}-jobs.csv")
                        initial = startcase(jobs)
                        result, fitness = algo(initial, fitnesses)
                        for it, score in fitnesses.items():
                            averages[it] += score
                        print(sample)
                    
                    for it, fitness in averages.items():
                        row["iteration"] = it
                        row["fitness"] = fitness/3
                        writer.writerow(row)


def final_results():
    """Generating the final results data for all testcases."""
    resultfile = Path("results/final_results.csv")
    with open(resultfile, "w") as csvfile:
        fieldnames = ["algorithm", "testcase", "fitness", "duration"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        sd = lambda initial: stochastic_descent(initial, 8, 50000)
        sa = lambda initial: simulated_annealing(initial, 8, 10000, .89, 100000)
        for algo in [sd, sa]:
            for testcase in TESTCASES:
                jobs = import_csv(f"{testcase}-jobs.csv")
                fitnesses = []
                durations = []
                row = {"algorithm": "SD" if algo == sd else "SA", "testcase": testcase}
                for trial in range(5):
                    print(f"'{row}' trial {trial + 1}...")
                    start_time = time.perf_counter()
                    if testcase == "light":
                        initial = generate_initial_solution(jobs)
                    else:
                        initial = generate_random_solution(jobs)
                    _result, fitness = algo(initial)
                    row["duration"] = time.perf_counter() - start_time
                    row["fitness"] = fitness
                    writer.writerow(row)