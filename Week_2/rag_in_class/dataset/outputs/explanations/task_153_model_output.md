# Model output for task_153

## Model
- devstral-small-2:24b-cloud

## Original Code:

def parabola_vertex(a, b, c): 
  vertex=(((-b / (2 * a)),(((4 * a * c) - (b * b)) / (4 * a))))
  return vertex

## Refactored Code:

```python
def parabola_vertex(a, b, c):
    """Calculate the vertex of a parabola given coefficients a, b, and c.

    Args:
        a: Coefficient of x^2 term (must not be zero)
        b: Coefficient of x term
        c: Constant term

    Returns:
        tuple: (x, y) coordinates of the parabola's vertex
    """
    x = -b / (2 * a)
    y = (4 * a * c - b ** 2) / (4 * a)
    return (x, y)
```

- Simplified the calculation by breaking it into two clear steps (x and y coordinates)
- Added docstring to explain the function's purpose, parameters, and return value
- Used more descriptive variable names (x, y instead of vertex tuple)
- Maintained the exact same mathematical calculations and return format
- Improved readability by removing nested parentheses
- Kept the same parameter order and function signature
- Preserved all mathematical operations exactly as in the original
- The function still returns a tuple of (x, y) coordinates
- All test cases should pass without modification
