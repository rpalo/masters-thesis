"""Model: the data model for the analysis.

A Job holds all of the input data from the user, including what is required
and when.  (NOTE: Base units are *days* so all hourly values must be divided
by 8.)

An Assignment takes a job and includes info about which machine that job
should run on and when.

A machine keeps track of its own queue as well as the date that it comes
open.
"""


class Job:
    def __init__(self, number, qty, cycle, cavities, due_date, mold, material, machines, setup, teardown):
        self.number = number
        self.due_date = due_date
        self.mold = mold
        self.material = material
        self.machines = machines
        self.duration = qty * cycle / (3600 * 8 * cavities) + setup / 8 + teardown / 8
        self.setup = setup / 8
        self.teardown = teardown / 8

    def __repr__(self):
        return f"Job(number={self.number}, due_date={self.due_date}, material={self.material})"


class Assignment:
    def __init__(self, job, machine, start, changeover):
        self.job = job
        self.machine = machine
        self.start = start
        self.end = start + job.duration
        if not changeover:
            self.end -= job.setup

    def __repr__(self):
        return f"Assignment(job={self.job}, machine={self.machine}, start={self.start:.2f}, end={self.end:.2f})"


class Machine:
    def __init__(self, number):
        self.open_date = 0
        self.number = number
        self.queue = []

    def add(self, assignment):
        self.queue.append(assignment)
        self.open_date = assignment.end

    def __lt__(self, other):
        return self.open_date < other.open_date

    def __iter__(self):
        return iter(self.queue)

    def __repr__(self):
        return f"Machine(number={self.number},assignments={self.queue})"