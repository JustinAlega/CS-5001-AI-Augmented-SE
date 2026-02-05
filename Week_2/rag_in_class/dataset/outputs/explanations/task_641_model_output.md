# Model output for task_641

## Model
- devstral-small-2:24b-cloud

## Original Code:

def is_nonagonal(n): 
	return int(n * (7 * n - 5) / 2) 

## Refactored Code:

```python
def is_nonagonal(n):
    """Calculate the nth nonagonal number.

    Args:
        n: The position in the sequence of nonagonal numbers.

    Returns:
        The nth nonagonal number.
    """
    return int(n * (7 * n - 5) / 2)
```

- Preserved the exact mathematical formula for nonagonal numbers
- Added a docstring to explain the function's purpose, arguments, and return value
- Maintained the same input/output behavior as the original
- Kept the integer conversion to ensure whole number results
- Improved readability with consistent formatting and spacing
- Ensured the function remains pure (no side effects)
- Maintained the same parameter name for clarity
- Kept the function signature unchanged to avoid breaking changes
