# Mold Shop Problem

Author: Ryan Palo\
Date: 3/16/2021

## Overview

This is the Master's Thesis that I put together for my Master's in Computer Science with a focus in Intelligent Systems for Lewis University.  

I work at a injection molding shop, and we get tons of orders placed on a weekly basis.  The turnaround time for these jobs is on the order of a few days to a few weeks, and, based on factors out of our control (catastrophic tool crashes, machine failures, sick employees, material shortages, etc.), the molding schedule needs completely scrapped and redone regularly.  This schedule is an assignment of which jobs will run on which machines on which days.  

Tired of doing this scheduling by hand--and in dire need of a Master's Thesis--I decided to use my AI classes as a spring board into developing a software tool that finds at least a "pretty good" solution to our schedule much faster than I could by hand.

Right on time, as I was in the final days of finishing my thesis, we hired a production manager who handles the scheduling using Excel Spreadsheets quite effectively, negating the need for the entire exercise.

But, search trees earn degrees, so I finished it up, documented it, and here we are.

Enclosed in this repository, you'll find my final Thesis, my presentation slides, and the source code to my solution in Python.

Everything below this point are notes that I took during research and development.  For the actual decisions made, rationales, and results, please refer to the final report.

## The Algorithm

1. Build an initial solution
2. Calculate its fitness.
3. Generate one or more neighbor states.
4. Calculate their fitnesses.
5. Using some local search algorithm, select the next state from the neighbors.
6. Return to 3.  Repeat until the local search algorithm calls a stop.

## The Data

The data can be found in test-cases.xlsx.  I took realistic jobs based on a real molding schedule and used those for the baseline case.  Then I generated the light, heavy, and late cases by shifting due dates to control how much extra time (or not) we had to finish all the work.  Within that spreadsheet, I also manually scheduled out the work to get a benchmark for how long it takes a human to optimize a schedule like this.  The "jobs" tabs in the spreadsheet were individually exported to CSV into the "data" folder for my program's analysis.  The program outputs to CSV files in the "results" folder, which I then compiled into graphs and charts.

## The Pieces

### 1. Generating an Initial Solution

Simplest: order by due date and then by increasing run-time.

Need to restrict invalid solutions which include:

- Running over-mold before substrates

### 2. Calculating Fitness

Major metric: days late.

Additional factors:

- Material changeover?
  - How much penalty?  1 day?
  - Should it be a secondary fitness score?
  - Or maybe only for secondary-level customers?
- Customer priority? (Multi-level?)

Do we want to prioritize for even machine loading?  E.g. penalize uneven machine loading?  Or can we expect the algorithm to level for us.  I suppose it doesn't matter if our fitness is good.

Do we want to penalize/limit earliness?

### 3. Generating Neighbor States

Research recommends mutating items in the queue, switching their positions.

Mutation methods:

- random?
- generate all?
- subproblem?
- somehow generate likely improvement neighbors?

### 4. Local Search (Selecting Next State, How Many Neighbors, etc.)

Could be any.  Need to track and tune whatever variables.  Options:

- stochastic descent (simplest)
- simulated annealing: start temp, alpha
- tabu search: need more research
- beam search: how many beams?  How many neighbors?
- particle swarm: how many particles?  Gravity constant?

### 5. Stopping Condition

Options:

- Fixed number of iterations (would need testing)
- minimal change a.k.a. convergence (would need an error value)

### 6. Generating Schedules from Solutions (the List Algorithm)

We go through the solution (list of jobs) and, one by one, assign each job to a machine.  Jobs will have a set of machines they can run on.

## Todos

- Job durations: fudge-factor, risk factor, plan in downtime?
- Jobs can be multi-shift
- Lots of date things to handle.  Weekends, holidays.
- Possibly which employees are working?
- Factor in deburring/other post-processing before due date?
- Prerequisite jobs (over-molding)