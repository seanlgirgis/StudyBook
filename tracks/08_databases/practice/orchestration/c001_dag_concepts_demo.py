# Story:
# A daily finance report is built by multiple tasks. One wrong order breaks the whole run.


TASKS = {
    "extract_orders": {"deps": [], "desc": "pull raw orders from the source"},
    "extract_payments": {"deps": [], "desc": "pull raw payments from the source"},
    "transform_sales": {
        "deps": ["extract_orders", "extract_payments"],
        "desc": "join orders + payments into sales facts",
    },
    "validate_report": {
        "deps": ["transform_sales"],
        "desc": "quality check totals before publishing",
    },
    "publish_report": {
        "deps": ["validate_report"],
        "desc": "ship the report to the dashboard",
    },
    "notify_slack": {
        "deps": ["publish_report"],
        "desc": "announce completion to stakeholders",
    },
}


def _describe_dag(tasks):
    print("DAG nodes:")
    for name, info in tasks.items():
        print(f"- {name}: {info['desc']}")
    print("DAG edges (dependencies):")
    for name, info in tasks.items():
        if info["deps"]:
            for dep in info["deps"]:
                print(f"- {dep} -> {name}")
        else:
            print(f"- {name} has no upstream deps")


def _can_run(task_name, status, tasks):
    for dep in tasks[task_name]["deps"]:
        if status.get(dep) != "success":
            return False
    return True


def _run_task(task_name, status, tasks):
    if not _can_run(task_name, status, tasks):
        missing = [dep for dep in tasks[task_name]["deps"] if status.get(dep) != "success"]
        print(f"[BLOCKED] {task_name} waits on {missing}")
        return False
    print(f"[RUN] {task_name} -> success")
    status[task_name] = "success"
    return True


def _topological_order(tasks):
    incoming = {name: set(info["deps"]) for name, info in tasks.items()}
    ready = [name for name, deps in incoming.items() if not deps]
    order = []
    while ready:
        node = ready.pop(0)
        order.append(node)
        for candidate, deps in incoming.items():
            if node in deps:
                deps.remove(node)
                if not deps and candidate not in order and candidate not in ready:
                    ready.append(candidate)
    return order


def run_dag_concepts_demo():
    print("=" * 72)
    print("Scenario: daily finance report DAG")
    _describe_dag(TASKS)

    print("=" * 72)
    print("Attempt 1: run tasks in a human-guessed order (fails first)")
    status = {}
    guessed_order = [
        "publish_report",
        "transform_sales",
        "extract_orders",
        "extract_payments",
        "validate_report",
        "notify_slack",
    ]
    for task in guessed_order:
        _run_task(task, status, TASKS)

    print("=" * 72)
    print("Why that failed:")
    print("- A DAG (Directed Acyclic Graph) enforces dependencies.")
    print("- A task is blocked until every upstream dependency succeeds.")

    print("=" * 72)
    print("Attempt 2: compute a topological order (valid DAG execution order)")
    topo_order = _topological_order(TASKS)
    print("Topological order:", topo_order)
    print("This order is constrained because downstream tasks depend on upstream outputs.")

    print("=" * 72)
    print("Execute in topological order:")
    status = {}
    for task in topo_order:
        _run_task(task, status, TASKS)

    print("=" * 72)
    print("Summary:")
    print("- DAG = tasks + dependency edges.")
    print("- Blocked tasks prove why order matters.")
    print("- Topological order is the safe execution plan.")


if __name__ == "__main__":
    run_dag_concepts_demo()

# Takeaway: DAGs make dependencies explicit so downstream tasks wait for upstream success.
