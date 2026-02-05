def remove_column(matrix, column_index):
    """Remove the specified column from each row in the matrix.

    Args:
        matrix: A list of lists representing a matrix.
        column_index: The index of the column to remove.

    Returns:
        The matrix with the specified column removed from each row.
    """
    return [row[:column_index] + row[column_index + 1:] for row in matrix]
