# Story:
# The team chains transformations and expects work to happen immediately.
# In Spark, nothing runs until an action triggers execution.


RAW_ORDERS = [
    {"order_id": "o1", "customer": "Ava", "amount": 120.0, "status": "paid"},
    {"order_id": "o2", "customer": "Ben", "amount": 85.0, "status": "paid"},
    {"order_id": "o3", "customer": "Ava", "amount": 25.0, "status": "refund"},
    {"order_id": "o4", "customer": "Cara", "amount": 200.0, "status": "paid"},
    {"order_id": "o5", "customer": "Ben", "amount": 15.0, "status": "paid"},
]


class LazyPipeline:
    def __init__(self, rows):
        self._rows = rows
        self._steps = []

    def filter(self, label, fn):
        print(f"Define transformation: filter ({label})")
        self._steps.append(("filter", label, fn))
        return self

    def map(self, label, fn):
        print(f"Define transformation: map ({label})")
        self._steps.append(("map", label, fn))
        return self

    def group_sum(self, label, key_fn, value_fn):
        print(f"Define transformation: group_sum ({label})")
        self._steps.append(("group_sum", label, (key_fn, value_fn)))
        return self

    def collect(self):
        print("Action: collect -> start execution")
        data = list(self._rows)
        for step_type, label, payload in self._steps:
            print(f"Executing {step_type}: {label}")
            if step_type == "filter":
                data = [row for row in data if payload(row)]
            elif step_type == "map":
                data = [payload(row) for row in data]
            elif step_type == "group_sum":
                key_fn, value_fn = payload
                totals = {}
                for row in data:
                    key = key_fn(row)
                    totals[key] = totals.get(key, 0.0) + value_fn(row)
                data = [
                    {"customer": key, "total_amount": round(value, 2)}
                    for key, value in totals.items()
                ]
        print("Execution complete.")
        return data


def _print_rows(label, rows):
    print(label)
    for row in rows:
        print(row)


def run_lazy_evaluation_demo():
    print("=" * 72)
    print("Scenario: build a pipeline for paid revenue per customer")
    _print_rows("Raw orders:", RAW_ORDERS)

    print("=" * 72)
    print("Transformations are defined first (no work yet)")
    pipeline = (
        LazyPipeline(RAW_ORDERS)
        .filter("amount > 50 and status = paid", lambda row: row["amount"] > 50 and row["status"] == "paid")
        .map("select customer, amount", lambda row: {"customer": row["customer"], "amount": row["amount"]})
        .group_sum("sum amount by customer", lambda row: row["customer"], lambda row: row["amount"])
    )

    print("Nothing has executed yet. No results until an action is called.")

    print("=" * 72)
    print("Action triggers execution")
    results = pipeline.collect()
    _print_rows("Collected results:", results)

    print("=" * 72)
    print("Summary:")
    print("- Transformations build a plan and stay lazy.")
    print("- Actions (collect, count, show) trigger execution.")
    print("- Nothing happens until an action runs.")


if __name__ == "__main__":
    run_lazy_evaluation_demo()

# Takeaway: Spark transformations are lazy; only actions execute the plan.