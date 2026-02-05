# Model output for task_927

## Model
- devstral-small-2:24b-cloud

## Original Code:

class Node: 
	def __init__(self, data): 
		self.data = data 
		self.left = None
		self.right = None
def max_height(node): 
	if node is None: 
		return 0 ; 
	else : 
		left_height = max_height(node.left) 
		right_height = max_height(node.right) 
		if (left_height > right_height): 
			return left_height+1
		else: 
			return right_height+1

## Refactored Code:

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def max_height(node):
    if node is None:
        return 0
    left_height = max_height(node.left)
    right_height = max_height(node.right)
    return max(left_height, right_height) + 1
```

- Simplified the conditional logic by using `max()` function
- Improved code formatting and readability with consistent indentation
- Removed unnecessary `else` clause after `if` when returning
- Maintained the same behavior as the original implementation
- Kept the same function signature and return types
- Preserved the recursive approach for calculating tree height
- Ensured all test cases continue to pass
- Reduced cognitive complexity by eliminating nested conditionals
