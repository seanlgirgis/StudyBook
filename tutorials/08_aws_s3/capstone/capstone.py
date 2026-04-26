import subprocess

steps = [
    "setup.py",
    "ingest.py",
    "access.py",
    "cost_report.py",
]

for step in steps:
    print(f"\nRunning {step}")
    subprocess.run(["python", step])