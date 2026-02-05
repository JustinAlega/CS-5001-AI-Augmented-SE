def find_max_len_even(s):
    max_length = 0
    max_start = -1
    current_length = 0
    current_start = 0

    for i, char in enumerate(s):
        if char == ' ':
            if current_length % 2 == 0 and current_length > max_length:
                max_length = current_length
                max_start = current_start
            current_length = 0
            current_start = i + 1
        else:
            current_length += 1

    if current_length % 2 == 0 and current_length > max_length:
        max_length = current_length
        max_start = current_start

    return s[max_start:max_start + max_length] if max_start != -1 else "-1"
