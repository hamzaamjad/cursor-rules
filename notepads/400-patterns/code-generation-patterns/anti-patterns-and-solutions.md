# Anti-Patterns and Solutions for Code Generation

This notepad provides comprehensive documentation of common formatting errors in AI-generated code and their solutions. These patterns help prevent typical mistakes that occur when AI systems generate code without proper formatting awareness.

## Formatting Anti-Patterns

Formatting errors represent the most common issues in AI-generated code, often resulting from misunderstanding whitespace requirements or line continuation rules. The following anti-patterns demonstrate these issues with clear problem/solution pairs.

### Docstring and Comment Line Continuation

One of the most frequent errors involves placing code on the same line as docstrings or comments. This anti-pattern occurs when AI systems attempt to minimize line count without understanding Python's formatting requirements.

**Problem Pattern:**
```python
# BAD: Code on same line as docstring
def function():
    """Docstring."""    code_here()
    
# BAD: Code on same line as comment
# Comment    code_here()

# BAD: Multi-line docstring with immediate code
def complex_function():
    """
    This is a longer docstring.
    """result = calculate()  # Wrong!
```

**Solution Pattern:**
```python
# GOOD: Code on new line after docstring
def function():
    """Docstring."""
    code_here()
    
# GOOD: Code on new line after comment
# Comment
code_here()

# GOOD: Proper spacing after multi-line docstring
def complex_function():
    """
    This is a longer docstring.
    """
    result = calculate()  # Correct placement
```

### Missing Newlines Between Logical Blocks

Proper spacing between functions, classes, and logical sections improves code readability and follows Python conventions. AI systems often miss these spacing requirements when generating multiple components sequentially.

**Problem Pattern:**
```python
# BAD: No separation between functions
def func1():
    pass
def func2():
    pass
class MyClass:
    pass
def func3():
    pass

# BAD: Insufficient spacing in class definitions
class Example:
    def method1(self):
        pass
    def method2(self):
        pass
```

**Solution Pattern:**
```python
# GOOD: Two blank lines between top-level definitions
def func1():
    pass


def func2():
    pass


class MyClass:
    pass


def func3():
    pass

# GOOD: One blank line between class methods
class Example:
    def method1(self):
        pass
    
    def method2(self):
        pass
```

### Incorrect Indentation After Multiline Strings

Triple-quoted strings can confuse AI systems about the correct indentation level for subsequent code. This issue commonly occurs with module docstrings and class definitions.

**Problem Pattern:**
```python
# BAD: Wrong indentation after module docstring
"""Module docstring."""
    import os  # Wrong indentation

# BAD: Class definition indentation error
class MyClass:
    """
    Class docstring.
    """
        def __init__(self):  # Wrong indentation
            pass

# BAD: Function with multiline string
def process():
    data = """
    Multi-line data
    """
        result = parse(data)  # Wrong indentation
```

**Solution Pattern:**
```python
# GOOD: Correct module-level indentation
"""Module docstring."""

import os  # Correct indentation

# GOOD: Proper class method indentation
class MyClass:
    """
    Class docstring.
    """
    
    def __init__(self):  # Correct indentation
        pass

# GOOD: Maintained indentation after multiline string
def process():
    data = """
    Multi-line data
    """
    result = parse(data)  # Correct indentation
```

## Import Organization Anti-Patterns

Import statement organization frequently suffers in AI-generated code, leading to maintenance issues and potential circular dependencies.

**Problem Pattern:**
```python
# BAD: Mixed import styles and ordering
from os import path
import sys
from datetime import datetime
import os
import requests
from .utils import helper
import numpy as np
from . import config

# BAD: Star imports
from module import *
from another_module import *
```

**Solution Pattern:**
```python
# GOOD: Organized imports following PEP 8
# Standard library imports
import os
import sys
from datetime import datetime
from os import path

# Third-party imports
import numpy as np
import requests

# Local imports
from . import config
from .utils import helper

# GOOD: Explicit imports
from module import ClassA, ClassB, function1
from another_module import specific_function
```

## Continuation and Line Length Anti-Patterns

Managing line length and proper continuation represents another common challenge in AI-generated code.

**Problem Pattern:**
```python
# BAD: Excessive line length
result = some_very_long_function_name(argument1, argument2, argument3, argument4, argument5, argument6)

# BAD: Poor line breaking
long_string = "This is a very long string that continues for many characters without any consideration for readability or the recommended 79-character line limit in Python code"

# BAD: Incorrect continuation
if (condition1 and condition2 and
condition3):  # Wrong indentation
    pass
```

**Solution Pattern:**
```python
# GOOD: Proper line breaking for function calls
result = some_very_long_function_name(
    argument1, argument2, argument3,
    argument4, argument5, argument6
)

# GOOD: String continuation
long_string = (
    "This is a very long string that continues for many "
    "characters with proper consideration for readability "
    "and the recommended 79-character line limit"
)

# GOOD: Correct continuation indentation
if (condition1 and condition2 and
        condition3):  # Aligned continuation
    pass
```

## Class Definition Anti-Patterns

Class definitions often exhibit specific formatting issues when generated by AI systems.

**Problem Pattern:**
```python
# BAD: Missing proper spacing and organization
class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    @property
    def value(self):
        return self.x + self.y
    def method1(self):
        pass
    @staticmethod
    def static_method():
        pass
```

**Solution Pattern:**
```python
# GOOD: Properly organized class with spacing
class MyClass:
    """Class with proper organization."""
    
    def __init__(self, x, y):
        """Initialize with x and y values."""
        self.x = x
        self.y = y
    
    @property
    def value(self):
        """Calculate combined value."""
        return self.x + self.y
    
    def method1(self):
        """Regular instance method."""
        pass
    
    @staticmethod
    def static_method():
        """Static utility method."""
        pass
```

## Recovery Strategies for Formatting Errors

When formatting errors occur in generated code, systematic recovery strategies help restore proper structure without introducing new issues.

### Targeted Fix Approach

Apply specific corrections to identified patterns rather than attempting broad reformatting that might affect valid code. Use precise search and replace operations that target the exact anti-pattern.

### AST-Based Correction

When possible, use Abstract Syntax Tree (AST) based tools that understand Python's structure. Tools like `autopep8` and `black` can automatically fix many formatting issues while preserving code functionality.

### Validation After Correction

Always validate corrected code through multiple methods:
1. Syntax checking with `python -m py_compile`
2. Import testing to ensure module loading
3. Format verification with `black --check`
4. Functional testing of corrected components

### Progressive Correction

For files with multiple formatting issues, address problems in order of severity:
1. Fix syntax errors that prevent parsing
2. Correct indentation issues
3. Add proper spacing between blocks
4. Organize imports
5. Apply consistent formatting

These anti-patterns and solutions form the foundation for generating properly formatted Python code. By understanding and avoiding these common issues, AI systems can produce code that follows Python conventions and maintains readability.