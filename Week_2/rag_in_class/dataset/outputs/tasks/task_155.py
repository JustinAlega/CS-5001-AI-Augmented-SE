def even_bit_toggle_number(n):
    """Toggle all even-indexed bits (0-based) in the binary representation of n.

    Args:
        n: Integer to process

    Returns:
        Integer with even-indexed bits toggled
    """
    result = 0
    bit_position = 0

    # Process each bit in the number
    temp = n
    while temp > 0:
        if bit_position % 2 == 1:  # Even-indexed bits (0-based)
            result |= 1 << bit_position
        bit_position += 1
        temp >>= 1

    return n ^ result
