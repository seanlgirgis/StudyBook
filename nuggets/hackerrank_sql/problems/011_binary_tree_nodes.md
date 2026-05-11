# 011 - Binary Tree Nodes

## Source

HackerRank SQL - Advanced Select

## Problem Summary

Given a `BST` table with columns `N` and `P`, where `N` is a node value and `P` is the parent of `N`, classify each node as `Root`, `Inner`, or `Leaf`. Output each node value and its type ordered by `N`.

## Schema

`BST`
- `N Integer`
- `P Integer`

## Accepted Solution

```sql
SELECT
    N,
    CASE
        WHEN P IS NULL THEN 'Root'
        WHEN N NOT IN (
            SELECT P
            FROM BST
            WHERE P IS NOT NULL
        ) THEN 'Leaf'
        ELSE 'Inner'
    END AS NodeType
FROM BST
ORDER BY N;
```

## Provided Solution Reviewed

The provided SQL solution is correct and should pass.

### What is good

- `CASE` is used to classify each node.
- `P IS NULL` correctly identifies the root node.
- `N NOT IN (SELECT P FROM BST WHERE P IS NOT NULL)` identifies leaf nodes.
- The subquery checks whether a node ever appears as a parent.
- `WHERE P IS NOT NULL` avoids `NULL` issues with `NOT IN`.
- `ELSE 'Inner'` correctly classifies all remaining nodes.
- `ORDER BY N` outputs nodes in ascending order.

## Plain-English Explanation

The `BST` table stores each node `N` and its parent `P`.

A root node has no parent, so:
`P IS NULL`

A leaf node has no children. In this table, a node has children if its value appears in the `P` column for some other row.

So if `N` does not appear in the non-null parent list, it is a leaf:
`N NOT IN (SELECT P FROM BST WHERE P IS NOT NULL)`

Any node that is not root and not leaf is an inner node.

## Important Learning Notes

- `CASE` lets SQL return different labels based on conditions.
- Root means parent is `NULL`.
- Leaf means the node is never used as another node's parent.
- Inner means the node has both a parent and at least one child.
- `NOT IN` with `NULL` can be dangerous, so filter `NULL` out of the subquery.
- `ORDER BY N` is required to sort by node value.

## Sample Input Idea

`N | P`
`1 | 2`
`3 | 2`
`6 | 8`
`9 | 8`
`2 | 5`
`8 | 5`
`5 | NULL`

## Sample Output

`1 Leaf`
`2 Inner`
`3 Leaf`
`5 Root`
`6 Leaf`
`8 Inner`
`9 Leaf`

## Mistakes / Reminders

- Do not classify only by `P IS NULL` and `P IS NOT NULL`.
- A node with a parent can still be `Inner` if it has children.
- A node is `Leaf` only if it never appears in the `P` column.
- Always exclude `NULL` in the `NOT IN` subquery.
- Do not forget `ORDER BY N`.
- Keep exact output labels: `Root`, `Leaf`, `Inner`.
