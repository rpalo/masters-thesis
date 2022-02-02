import mold_shop

jobs = mold_shop.import_json("jobs.json")

def test_even_loading():
    these_jobs = jobs[:] + jobs[:]
    initial = mold_shop.generate_initial_solution(these_jobs)
    result = mold_shop.stochastic_descent(initial, 3)
    for machine in mold_shop.generate_schedule(result, 3):
        print(machine)
    print(mold_shop.fitness(result, 3))


def test_lots_of_jobs():
    these_jobs = jobs[:] * 20
    initial = mold_shop.generate_initial_solution(these_jobs)
    result = mold_shop.stochastic_descent(initial, 3)
    for machine in mold_shop.generate_schedule(result, 3):
        print(machine)


def test_material_change():
    these_jobs = [jobs[0], jobs[1], jobs[3]]
    these_jobs[0].machines = [1]
    initial = mold_shop.generate_initial_solution(these_jobs)
    result = mold_shop.stochastic_descent(initial, 3)
    for machine in mold_shop.generate_schedule(result, 3):
        print(machine)
    print(mold_shop.fitness(result, 3))

def test_jobs_csv():
    jobs = mold_shop.import_csv("jobs.csv")
    initial = mold_shop.generate_initial_solution(jobs)
    result = mold_shop.stochastic_descent(initial, 8)
    for machine in mold_shop.generate_schedule(result, 8):
        print(machine)
    print(mold_shop.fitness(result, 8))

if __name__ == "__main__":
    test_jobs_csv()