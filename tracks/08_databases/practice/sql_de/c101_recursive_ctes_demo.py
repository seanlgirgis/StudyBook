# Story:
# Recursive CTEs walk a hierarchy level by level: anchor rows, then recursive expansion.

EMPLOYEES = [
    {"id": 1, "name": "Ava", "manager_id": None},
    {"id": 2, "name": "Ben", "manager_id": 1},
    {"id": 3, "name": "Cara", "manager_id": 1},
    {"id": 4, "name": "Drew", "manager_id": 2},
    {"id": 5, "name": "Eli", "manager_id": 2},
    {"id": 6, "name": "Fay", "manager_id": 3},
    {"id": 7, "name": "Gus", "manager_id": 4},
]


def _index_by_manager(rows):
    by_manager = {}
    for row in rows:
        by_manager.setdefault(row["manager_id"], []).append(row)
    return by_manager


def recursive_cte_simulation(rows):
    """
    This mirrors a recursive CTE:
    - Anchor: manager_id is None (top of the tree).
    - Recursive member: join previous level to find children.
    """
    by_manager = _index_by_manager(rows)
    anchor = by_manager.get(None, [])

    results = []
    frontier = [{"level": 0, "path": row["name"], **row} for row in anchor]
    visited = set()

    step = 0
    while frontier:
        print("=" * 72)
        print(f"Step {step}: frontier (rows produced by this recursion level)")
        for row in frontier:
            print(
                {
                    "level": row["level"],
                    "id": row["id"],
                    "name": row["name"],
                    "manager_id": row["manager_id"],
                    "path": row["path"],
                }
            )

        results.extend(frontier)
        next_frontier = []
        for row in frontier:
            if row["id"] in visited:
                continue
            visited.add(row["id"])
            for child in by_manager.get(row["id"], []):
                next_frontier.append(
                    {
                        "level": row["level"] + 1,
                        "path": f"{row['path']} -> {child['name']}",
                        **child,
                    }
                )

        frontier = next_frontier
        step += 1

    return results


def run_recursive_cte_demo():
    print("=" * 72)
    print("Raw table (employees with manager_id):")
    for row in EMPLOYEES:
        print(row)

    print("=" * 72)
    print("Scenario: build an org chart by walking the hierarchy.")
    print("Mental model: anchor rows, then repeatedly expand to children.")

    hierarchy = recursive_cte_simulation(EMPLOYEES)

    print("=" * 72)
    print("Final result (like the recursive CTE output):")
    for row in hierarchy:
        print(
            {
                "level": row["level"],
                "name": row["name"],
                "manager_id": row["manager_id"],
                "path": row["path"],
            }
        )

    print("=" * 72)
    print("Interpretation:")
    print("- Anchor produced the CEO (level 0).")
    print("- Each recursion step joined prior rows to their direct reports.")
    print("- Recursion stopped when no new children were found.")
    print("- The path shows the full chain from the root to each node.")


if __name__ == "__main__":
    run_recursive_cte_demo()

# Takeaway:
# Recursive CTEs are SQL loops for hierarchies: seed, expand, stop.
