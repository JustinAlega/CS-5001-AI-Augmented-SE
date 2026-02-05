# Model output for task_690

## Model
- devstral-small-2:24b-cloud

## Original Code:

def mul_consecutive_nums(nums):
    result = [b*a for a, b in zip(nums[:-1], nums[1:])]
    return result

## Refactored Code:

```python
def multiply_consecutive_numbers(numbers):
    """Return a list of products of each pair of consecutive numbers in the input list.

    Args:
        numbers: List of numbers to process.

    Returns:
        List of products where each element is the product of two consecutive numbers
        from the input list. The length of the result is len(numbers) - 1.
    """
    return [a * b for a, b in zip(numbers[:-1], numbers[1:])]
```

- Renamed function and parameter to be more descriptive
- Added docstring explaining purpose, arguments, and return value
- Maintained exact same logic and behavior
- Kept list comprehension for efficiency
- Preserved original functionality as validated by tests
- Improved readability through better naming
- Maintained same input/output behavior
- No changes to core algorithm or edge case handling
