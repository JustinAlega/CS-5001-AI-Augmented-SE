def number_of_substrings(input_string: str) -> int:
    """Calculate the number of possible substrings in a given string.

    The number of substrings in a string of length n is given by the formula n*(n+1)/2.

    Args:
        input_string: The input string for which to calculate substrings.

    Returns:
        The count of possible substrings as an integer.
    """
    length = len(input_string)
    return length * (length + 1) // 2
