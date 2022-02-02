"""Data I/O: Import and export data to other useable formats."""
import csv
from pathlib import Path

from model import Job


def import_csv(filename, base_dir=Path("data/")):
    """Converts CSV files with the relevant data (see columns below) to
    a list of Jobs.
    """
    datafile = base_dir / filename
    with open(datafile, "r", newline="", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        return [
            Job(
                line["part number"],
                int(line["quantity"]),
                float(line["cycle"]),
                int(line["cavities"]),
                float(line["due date"]),
                line["mold"],
                line["material"],
                [int(num) for num in line["machines"].split(",")],
                float(line["setup"]),
                float(line["teardown"])
            ) for i, line in enumerate(reader, start=2)
        ]


def export_csv(schedule, fitness, time_elapsed, filename, base_dir=Path("results/")):
    """Exports a generated schedule to CSV in a format where each machine
    has its jobs listed with start and end dates in order of operation.
    Each machine separated by a blank line.
    """
    outfile = base_dir / filename
    with open(outfile, "w") as csvfile:
        fieldnames = ["part number", "due date", "material", "start", "end"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for machine in schedule:
            writer.writerow({"part number": f"Machine {machine.number}"})
            for assignment in machine.queue:
                writer.writerow({
                    "part number": assignment.job.number,
                    "due date": assignment.job.due_date,
                    "material": assignment.job.material,
                    "start": assignment.start,
                    "end": assignment.end,
                })
            writer.writerow({})
        writer.writerow({})
        writer.writerow({
            "part number": "Total fitness:",
            "due date": fitness
        })
        writer.writerow({
            "part number": "Time elapsed:",
            "due date": time_elapsed
        })