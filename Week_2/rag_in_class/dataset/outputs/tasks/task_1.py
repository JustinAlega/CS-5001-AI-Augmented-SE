def min_cost(cost, m, n):
    """Calculate the minimum cost path from top-left to bottom-right of a cost matrix.

    Args:
        cost: 2D list representing the cost matrix
        m: row index of the target cell (0-based)
        n: column index of the target cell (0-based)

    Returns:
        Minimum cost to reach cell (m, n) from (0, 0)
    """
    # Initialize a DP table with the same dimensions as the cost matrix
    dp = [[0 for _ in range(len(cost[0]))] for _ in range(len(cost))]

    # Base case: starting cell cost
    dp[0][0] = cost[0][0]

    # Fill first column (only can come from above)
    for i in range(1, len(cost)):
        dp[i][0] = dp[i-1][0] + cost[i][0]

    # Fill first row (only can come from left)
    for j in range(1, len(cost[0])):
        dp[0][j] = dp[0][j-1] + cost[0][j]

    # Fill rest of the table
    for i in range(1, len(cost)):
        for j in range(1, len(cost[0])):
            dp[i][j] = min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]) + cost[i][j]

    return dp[m][n]
