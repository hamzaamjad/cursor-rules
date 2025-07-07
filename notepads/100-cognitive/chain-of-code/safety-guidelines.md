# Chain of Code Safety Guidelines

## Execution Sandbox Constraints

```python
# Allowed operations
SAFE_MODULES = {
    'math', 'statistics', 'itertools', 'collections',
    'datetime', 'json', 're', 'decimal', 'fractions'
}

# Blocked operations
BLOCKED_CALLS = {
    'open', 'file', 'subprocess', 'os.system',
    'eval', 'exec', '__import__', 'compile'
}
```

## Memory Limits

```python
import resource

def set_memory_limit(mb=100):
    """Enforce memory constraints for code execution."""
    resource.setrlimit(
        resource.RLIMIT_AS,
        (mb * 1024 * 1024, mb * 1024 * 1024)
    )
```

## Timeout Enforcement

```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Code execution exceeded 5s limit")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(5)  # 5 second limit
```

## Safe Execution Pattern

```python
def safe_execute(code_string, globals_dict=None):
    """Execute code with full safety constraints."""
    # Sanitize imports
    if any(blocked in code_string for blocked in BLOCKED_CALLS):
        raise SecurityError("Unsafe operation detected")
    
    # Create restricted namespace
    safe_globals = {
        '__builtins__': {
            name: __builtins__[name]
            for name in ['print', 'len', 'range', 'enumerate']
        }
    }
    safe_globals.update(globals_dict or {})
    
    # Execute with constraints
    try:
        exec(code_string, safe_globals)
    except Exception as e:
        return f"Execution error: {type(e).__name__}: {e}"
```

## Input Validation

```python
MAX_CODE_LENGTH = 10000
MAX_LINE_LENGTH = 500

def validate_code_input(code):
    if len(code) > MAX_CODE_LENGTH:
        raise ValueError(f"Code exceeds {MAX_CODE_LENGTH} character limit")
    
    lines = code.split('\n')
    if any(len(line) > MAX_LINE_LENGTH for line in lines):
        raise ValueError(f"Line exceeds {MAX_LINE_LENGTH} character limit")
```
