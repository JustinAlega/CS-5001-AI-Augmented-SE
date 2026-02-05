def generate_matrix(n):
    if n <= 0:
        return []

    matrix = [[0 for _ in range(n)] for _ in range(n)]
    row_start, row_end = 0, n - 1
    col_start, col_end = 0, n - 1
    current = 1

    while current <= n * n:
        # Fill top row from left to right
        for c in range(col_start, col_end + 1):
            matrix[row_start][c] = current
            current += 1
        row_start += 1

        # Fill right column from top to bottom
        for r in range(row_start, row_end + 1):
            matrix[r][col_end] = current
            current += 1
        col_end -= 1

        # Fill bottom row from right to left
        for c in range(col_end, col_start - 1, -1):
            matrix[row_end][c] = current
            current += 1
        row_end -= 1

        # Fill left column from bottom to top
        for r in range(row_end, row_start - 1, -1):
            matrix[r][col_start] = current
            current += 1
        col_start += 1

    return matrix
