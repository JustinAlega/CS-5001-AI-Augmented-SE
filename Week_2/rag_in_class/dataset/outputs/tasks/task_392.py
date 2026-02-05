def get_max_sum(n):
    if n == 0:
        return 0
    if n == 1:
        return 1

    dp = [0] * (n + 1)
    dp[0], dp[1] = 0, 1

    for i in range(2, n + 1):
        max_val = i
        for divisor in [2, 3, 4, 5]:
            max_val = max(max_val, dp[i // divisor] + dp[i % divisor])
        dp[i] = max_val

    return dp[n]
