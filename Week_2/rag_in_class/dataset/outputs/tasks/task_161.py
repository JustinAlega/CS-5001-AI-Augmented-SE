def remove_elements(list1, list2):
    """Return a new list containing elements from list1 that are not in list2.

    Args:
        list1: The source list to filter elements from.
        list2: The list of elements to exclude from list1.

    Returns:
        A new list with elements from list1 that are not present in list2.
    """
    return [x for x in list1 if x not in list2]
