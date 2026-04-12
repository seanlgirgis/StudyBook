def pass_one():
    out = [[0 for _ in range(len(matrix[0]))] for _ in range(len(matrix))]
    for r in range(len(matrix)):
        for c in range(len(matrix[0])):
            if matrix[r][c] == "1":       # ← cell is 1
                val = 1
                if r > 0:
                    val += out[r-1][c]
            else:                          # ← cell is 0, same indent as outer if
                val = 0
            out[r][c] = val
    print(out)
    return out



matrix = [
    ["1","1","1","0","0"],
    ["1","0","1","1","1"],
    ["1","1","1","1","1"],
    ["1","0","0","1","0"]
]
print(maximalRectangle(pass_one))  # expected 6