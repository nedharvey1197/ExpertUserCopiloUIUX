# Code Commenting Best Practices

## General Principles

1. **Document Why, Not What**
   - Good: `// Calculate risk score based on patient history and current symptoms`
   - Bad: `// Add 1 to counter`

2. **Keep Comments Up to Date**
   - Update comments when code changes
   - Remove outdated comments
   - Use version control to track comment changes

3. **Use Clear, Concise Language**
   - Write in complete sentences
   - Use proper grammar
   - Avoid abbreviations unless standard

## Frontend Documentation

### File-Level Documentation
```typescript
/**
 * @fileoverview Description of the file's purpose and contents
 * @module path/to/file
 * @author [Author Name]
 * @created [Date]
 * @last-modified [Date]
 * @version 1.0.0
 */

// Import statements...

/**
 * @component ComponentName
 * @description Brief description of the component's purpose
 * @example
 * ```jsx
 * <ComponentName prop1="value" />
 * ```
 */
```

### Component Documentation
```typescript
/**
 * @component ComponentName
 * @description Detailed description of the component
 * @param {Object} props - Component props
 * @param {string} props.name - Description of name prop
 * @param {number} [props.age] - Optional age prop
 * @returns {JSX.Element} Rendered component
 * @example
 * ```jsx
 * <ComponentName name="John" age={30} />
 * ```
 */
const ComponentName = ({ name, age }) => {
  // Component implementation
};
```

### Hook Documentation
```typescript
/**
 * @hook useCustomHook
 * @description Description of the hook's purpose
 * @param {string} param1 - Description of first parameter
 * @param {Object} [options] - Optional configuration object
 * @returns {Object} Description of return value
 * @example
 * ```typescript
 * const result = useCustomHook('value', { option: true });
 * ```
 */
const useCustomHook = (param1, options = {}) => {
  // Hook implementation
};
```

### Function Documentation
```typescript
/**
 * @function functionName
 * @description Description of the function's purpose
 * @param {Type} paramName - Parameter description
 * @returns {Type} Description of return value
 * @throws {ErrorType} Description of when this error is thrown
 * @example
 * ```typescript
 * const result = functionName(param);
 * ```
 */
const functionName = (param) => {
  // Function implementation
};
```

## Backend Documentation

### File-Level Documentation
```python
"""
File: module_name.py
Description: Detailed description of the module's purpose
Author: [Author Name]
Created: [Date]
Last Modified: [Date]
Version: 1.0.0

This module handles [specific functionality].
"""

# Import statements...

class ClassName:
    """
    Class description and purpose.
    
    This class handles [specific functionality] and provides methods for [operations].
    
    Attributes:
        attr1 (type): Description of first attribute
        attr2 (type): Description of second attribute
    
    Example:
        >>> instance = ClassName()
        >>> instance.method()
    """
```

### Class Documentation
```python
class ClassName:
    """
    Class description and purpose.
    
    This class handles [specific functionality] and provides methods for [operations].
    
    Attributes:
        attr1 (type): Description of first attribute
        attr2 (type): Description of second attribute
    
    Example:
        >>> instance = ClassName()
        >>> instance.method()
    """
    
    def __init__(self, param1: str, param2: int = 0):
        """
        Initialize the class instance.
        
        Args:
            param1 (str): Description of first parameter
            param2 (int, optional): Description of second parameter. Defaults to 0.
        
        Raises:
            ValueError: Description of when this error is raised
        """
        pass
```

### Method Documentation
```python
def method_name(self, param1: str, param2: int = 0) -> bool:
    """
    Method description and purpose.
    
    This method performs [specific operation] and returns [result description].
    
    Args:
        param1 (str): Description of first parameter
        param2 (int, optional): Description of second parameter. Defaults to 0.
    
    Returns:
        bool: Description of return value
    
    Raises:
        ValueError: Description of when this error is raised
    
    Example:
        >>> instance = ClassName()
        >>> result = instance.method_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

### Function Documentation
```python
def function_name(param1: str, param2: int = 0) -> bool:
    """
    Function description and purpose.
    
    This function performs [specific operation] and returns [result description].
    
    Args:
        param1 (str): Description of first parameter
        param2 (int, optional): Description of second parameter. Defaults to 0.
    
    Returns:
        bool: Description of return value
    
    Raises:
        ValueError: Description of when this error is raised
    
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
    pass
```

## Inline Comments

### Frontend
```typescript
// Use single-line comments for brief explanations
const result = value * 2; // Double the value for calculation

/*
 * Use multi-line comments for complex explanations
 * that require multiple lines to explain
 */
const complexCalculation = (value) => {
  // Step 1: Validate input
  if (!value) {
    throw new Error('Value is required');
  }
  
  // Step 2: Perform calculation
  const result = value * 2;
  
  // Step 3: Apply business rules
  if (result > 100) {
    return 100; // Cap maximum value
  }
  
  return result;
};
```

### Backend
```python
# Use single-line comments for brief explanations
result = value * 2  # Double the value for calculation

# Use multi-line comments for complex explanations
# that require multiple lines to explain
def complex_calculation(value):
    # Step 1: Validate input
    if not value:
        raise ValueError('Value is required')
    
    # Step 2: Perform calculation
    result = value * 2
    
    # Step 3: Apply business rules
    if result > 100:
        return 100  # Cap maximum value
    
    return result
```

## Best Practices for Specific Cases

### Complex Algorithms
```typescript
/**
 * Implements the Smith-Waterman algorithm for local sequence alignment.
 * 
 * @param {string} seq1 - First sequence to align
 * @param {string} seq2 - Second sequence to align
 * @returns {Object} Alignment result with score and aligned sequences
 * 
 * @example
 * const result = smithWaterman("ACGT", "ACCT");
 * console.log(result.score); // 2
 */
function smithWaterman(seq1, seq2) {
  // Initialize scoring matrix
  const matrix = Array(seq1.length + 1)
    .fill()
    .map(() => Array(seq2.length + 1).fill(0));
  
  // Fill scoring matrix
  for (let i = 1; i <= seq1.length; i++) {
    for (let j = 1; j <= seq2.length; j++) {
      // Calculate match/mismatch score
      const match = seq1[i - 1] === seq2[j - 1] ? 2 : -1;
      
      // Calculate maximum score from previous positions
      matrix[i][j] = Math.max(
        matrix[i - 1][j - 1] + match,  // Diagonal (match/mismatch)
        matrix[i - 1][j] - 1,          // Up (gap)
        matrix[i][j - 1] - 1,          // Left (gap)
        0                              // No alignment
      );
    }
  }
  
  // Rest of implementation...
}
```

### API Endpoints
```python
@router.post("/api/v1/trials")
async def create_trial(trial: TrialCreate) -> TrialResponse:
    """
    Create a new clinical trial.
    
    This endpoint creates a new clinical trial in the system and returns
    the created trial with its assigned ID.
    
    Args:
        trial (TrialCreate): Trial creation data including:
            - name (str): Trial name
            - description (str): Trial description
            - start_date (date): Planned start date
            - status (str): Initial trial status
    
    Returns:
        TrialResponse: Created trial data including:
            - id (int): Assigned trial ID
            - created_at (datetime): Creation timestamp
            - [other fields...]
    
    Raises:
        HTTPException(400): If trial data is invalid
        HTTPException(409): If trial name already exists
    
    Example:
        >>> response = await create_trial({
        ...     "name": "COVID-19 Vaccine Trial",
        ...     "description": "Phase 3 clinical trial",
        ...     "start_date": "2024-01-01",
        ...     "status": "planned"
        ... })
        >>> print(response.id)
        123
    """
    # Implementation...
```

### State Management
```typescript
/**
 * Custom hook for managing trial form state
 * 
 * @param {Object} initialData - Initial form data
 * @returns {Object} Form state and handlers
 * 
 * @example
 * const { values, errors, handleChange, handleSubmit } = useTrialForm({
 *   name: '',
 *   description: ''
 * });
 */
const useTrialForm = (initialData) => {
  // State management implementation...
};
```

## Tools and Automation

### Frontend
- ESLint with JSDoc plugin
- TypeDoc for documentation generation
- VSCode JSDoc snippets

### Backend
- pylint for Python code style
- Sphinx for documentation generation
- VSCode Python docstring snippets

## Review Checklist

1. Documentation Completeness
   - [ ] File-level documentation
   - [ ] Component/class documentation
   - [ ] Method/function documentation
   - [ ] Parameter descriptions
   - [ ] Return value descriptions
   - [ ] Examples provided

2. Documentation Quality
   - [ ] Clear and concise language
   - [ ] Proper formatting
   - [ ] Up-to-date with code
   - [ ] No redundant comments
   - [ ] Examples are working

3. Code Organization
   - [ ] Logical grouping
   - [ ] Consistent style
   - [ ] Clear separation of concerns
   - [ ] Proper indentation
   - [ ] No commented-out code 