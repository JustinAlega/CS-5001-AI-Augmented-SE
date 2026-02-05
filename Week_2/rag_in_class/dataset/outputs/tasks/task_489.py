def frequency_of_largest(n, arr):
    if not arr:
        return 0

    max_value = arr[0]
    frequency = 1

    for value in arr[1:]:
        if value > max_value:
            max_value = value
            frequency = 1
        elif value == max_value:
            frequency += 1

    return frequency
