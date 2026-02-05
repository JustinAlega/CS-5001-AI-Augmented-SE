# Model output for task_558

## Model
- devstral-small-2:24b-cloud

## Original Code:

def digit_distance_nums(n1, n2):
         return sum(map(int,str(abs(n1-n2))))

## Refactored Code:

```python
def digit_distance_nums(n1, n2):
    """Calculate the sum of digits in the absolute difference between two numbers."""
    difference = abs(n1 - n2)
    return sum(int(digit) for digit in str(difference))
```

- Preserved exact behavior as validated by tests
- Improved readability with descriptive variable name
- Used generator expression instead of map for clarity
- Added docstring to explain function purpose
- Maintained same input/output contract
- Kept the same mathematical logic
- Simplified the code structure
- Ensured same performance characteristics
- Made the code more maintainable for future changes
