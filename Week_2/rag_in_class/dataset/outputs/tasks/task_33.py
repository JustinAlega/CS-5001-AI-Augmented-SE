def decimal_to_binary(n):
    """Convert a decimal number to its binary representation as an integer.

    Args:
        n: A non-negative integer to convert.

    Returns:
        The binary representation of n as an integer (e.g., 5 becomes 101).
    """
    binary_number = 0
    position = 0

    while n != 0:
        remainder = n % 2
        binary_number += remainder * (10 ** position)
        n //= 2
        position += 1

    return binary_number
