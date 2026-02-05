def smallest_divisor(n):
    """Return the smallest divisor of n greater than 1."""
    if n % 2 == 0:
        return 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return i
        i += 2
    return n
