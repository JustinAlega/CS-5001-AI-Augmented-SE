# Model output for task_395

## Model
- devstral-small-2:24b-cloud

## Original Code:

def first_non_repeating_character(str1):
  char_order = []
  ctr = {}
  for c in str1:
    if c in ctr:
      ctr[c] += 1
    else:
      ctr[c] = 1 
      char_order.append(c)
  for c in char_order:
    if ctr[c] == 1:
      return c
  return None

## Refactored Code:

```python
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
```

- Renamed parameters and variables for clarity (e.g., `str1` to `s`, `ctr` to `char_counts`)
- Added a docstring to explain the function's purpose
- Maintained the same logic and behavior as the original implementation
- Kept the same return structure (returns the first non-repeating character or None)
- Preserved the order of operations (counting first, then checking in order)
- Used consistent naming conventions throughout
- Improved readability by using more descriptive variable names
- Ensured the function still passes all existing tests
