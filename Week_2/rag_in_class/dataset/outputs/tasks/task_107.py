def count_hexadecimal_digits_in_range(start, end):
    """Count the number of hexadecimal digits (A-F) in the decimal representation of numbers from start to end (inclusive)."""
    count = 0
    for number in range(start, end + 1):
        if 10 <= number <= 15:
            count += 1
        elif number > 15:
            current = number
            while current != 0:
                if current % 16 >= 10:
                    count += 1
                current = current // 16
    return count
