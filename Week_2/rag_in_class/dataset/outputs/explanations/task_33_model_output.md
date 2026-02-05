# Model output for task_33

## Model
- devstral-small-2:24b-cloud

## Original Code:

def decimal_To_Binary(N): 
    B_Number = 0
    cnt = 0
    while (N != 0): 
        rem = N % 2
        c = pow(10,cnt)  
        B_Number += rem*c  
        N //= 2 
        cnt += 1
    return B_Number  

## Refactored Code:

```python
def decimal_to_binary(n):
    """Convert a decimal number to its binary representation as an integer.

    Args:
        n: A non-negative integer to convert.

    Returns:
        The binary representation of n as an integer (e.g., 5 becomes 101).
    """
    binary_number = 0
    position = 0

    while n != 0:
        remainder = n % 2
        binary_number += remainder * (10 ** position)
        n //= 2
        position += 1

    return binary_number
```

- Renamed function to follow snake_case convention (`decimal_To_Binary` → `decimal_to_binary`)
- Renamed variables to be more descriptive (`B_Number` → `binary_number`, `cnt` → `position`)
- Added a docstring to explain the function's purpose, arguments, and return value
- Improved code formatting and spacing for better readability
- Maintained the exact same logic and behavior as the original implementation
- Ensured the function still handles edge cases (like 0) correctly
- Kept the same return type (integer representation of binary)
