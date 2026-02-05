def first_non_repeating_character(s):
    """Return the first non-repeating character in the string, or None if none exists."""
    char_order = []
    char_counts = {}

    for char in s:
        if char in char_counts:
            char_counts[char] += 1
        else:
            char_counts[char] = 1
            char_order.append(char)

    for char in char_order:
        if char_counts[char] == 1:
            return char

    return None
