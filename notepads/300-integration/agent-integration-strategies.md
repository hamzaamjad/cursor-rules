# Agent Integration Strategies - Detailed Reference

## Complete Tool Comparison for Agent Operations

### File Editing Strategies

#### Strategy 1: Surgical Edit with edit_block
```python
# When to use: Small, precise changes
# Advantages: Exact matching, diff feedback

# Step 1: Read exact content
current = mcp_desktop_commander_read_file(path)
target_lines = extract_target_section(current)

# Step 2: Apply surgical edit
result = mcp_desktop_commander_edit_block(
    file_path=path,
    old_string=target_lines,
    new_string=modified_lines,
    expected_replacements=1
)

# Step 3: Verify
if not result.success:
    # Fallback to broader edit
    default_api.edit_file(path, broader_context_edit)
```

#### Strategy 2: Read-Parse-Modify-Write Pattern
```python
# When to use: Structured files (JSON, YAML, TOML)
# Advantages: Maintains structure integrity

import json
import yaml

def safe_modify_json(path, modifications):
    # Read
    content = mcp_desktop_commander_read_file(path)
    data = json.loads(content)
    
    # Modify
    for key, value in modifications.items():
        data = set_nested_value(data, key, value)
    
    # Write
    new_content = json.dumps(data, indent=2)
    mcp_desktop_commander_write_file(
        path=path,
        content=new_content,
        mode='rewrite'
    )
    
    # Verify
    verify = json.loads(mcp_desktop_commander_read_file(path))
    assert all(get_nested_value(verify, k) == v 
              for k, v in modifications.items())
```

### Complex Content Embedding Patterns

#### JSON String Escaping Reference
```python
# Single quotes in JSON values
json_str = '''{"message": "User's input"}'''  # Works

# Double quotes in JSON values - requires escaping
json_str = '{"message": "He said \\"Hello!\\""}'  # \\" for JSON

# In edit_file code_edit parameter
code_edit = '''
{
  "prompt": "Analyze the user\\'s request",
  "response": "The system said: \\"Processing\\""
}
'''

# Python string → JSON string escaping levels:
# Python needs \\\\ to produce \\ for JSON
# JSON needs \\ to escape quotes
```

#### File Reference Pattern (Preferred)
```json
// Instead of embedding large schemas
{
  "prompt": {
    "schema": {
      "type": "object",
      "properties": {
        // 500 lines of schema...
      }
    }
  }
}

// Use file references
{
  "prompt": {
    "schema_ref": "./schemas/prompt_schema.json"
  }
}
```

### Error Recovery Patterns

#### Pattern 1: Exponential Backoff with Alternating Strategies
```python
def resilient_edit(path, changes, max_attempts=5):
    strategies = [
        lambda: mcp_desktop_commander_edit_block(path, **changes),
        lambda: default_api.edit_file(path, changes['new_string']),
        lambda: full_rewrite_strategy(path, changes)
    ]
    
    for attempt in range(max_attempts):
        strategy = strategies[attempt % len(strategies)]
        try:
            if strategy() and verify_changes(path, changes):
                return True
        except Exception as e:
            log_error(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2 ** attempt)  # Exponential backoff
    
    return False
```

#### Pattern 2: State Checkpointing
```python
class FileEditCheckpoint:
    def __init__(self, path):
        self.path = path
        self.original = mcp_desktop_commander_read_file(path)
        self.checkpoints = [self.original]
    
    def apply_edit(self, edit_func):
        try:
            result = edit_func()
            new_state = mcp_desktop_commander_read_file(self.path)
            self.checkpoints.append(new_state)
            return result
        except:
            self.rollback()
            raise
    
    def rollback(self, to_checkpoint=-2):
        mcp_desktop_commander_write_file(
            path=self.path,
            content=self.checkpoints[to_checkpoint],
            mode='rewrite'
        )
```

### Multi-File Operation Patterns

#### Atomic Multi-File Updates
```python
def atomic_multi_file_update(file_operations):
    """
    file_operations: List of (path, content) tuples
    """
    completed = []
    try:
        for path, content in file_operations:
            mcp_desktop_commander_write_file(path, content)
            completed.append((path, content))
            
        # Verify all
        for path, expected in file_operations:
            actual = mcp_desktop_commander_read_file(path)
            if actual != expected:
                raise ValueError(f"Verification failed for {path}")
                
    except Exception as e:
        # Rollback completed operations
        for path, _ in completed:
            # Restore original or delete if new
            rollback_file(path)
        raise
```

#### Directory Structure Creation
```python
def create_project_structure(base_path, structure):
    """
    structure = {
        'src': {
            '__init__.py': '',
            'main.py': 'def main():\n    pass',
            'utils': {
                '__init__.py': '',
                'helpers.py': '# Utility functions'
            }
        },
        'tests': {
            'test_main.py': 'import pytest'
        }
    }
    """
    def create_recursive(current_path, items):
        for name, content in items.items():
            path = os.path.join(current_path, name)
            if isinstance(content, dict):
                mcp_desktop_commander_create_directory(path)
                create_recursive(path, content)
            else:
                mcp_desktop_commander_write_file(path, content)
    
    create_recursive(base_path, structure)
```

### Command Execution Patterns

#### Long-Running Commands with Progress
```python
def execute_with_progress(command, timeout_ms=30000):
    pid = mcp_desktop_commander_execute_command(
        command=command,
        timeout_ms=1000  # Initial short timeout
    )
    
    total_time = 0
    while total_time < timeout_ms:
        output = mcp_desktop_commander_read_output(
            pid=pid,
            timeout_ms=1000
        )
        if output.get('completed'):
            return output
        
        # Process incremental output
        if output.get('new_output'):
            process_progress(output['new_output'])
        
        total_time += 1000
    
    # Force terminate if still running
    mcp_desktop_commander_force_terminate(pid)
    raise TimeoutError(f"Command exceeded {timeout_ms}ms")
```

### Verification Patterns

#### Content Verification Matrix
| File Type | Verification Method | Success Criteria |
|-----------|-------------------|------------------|
| JSON | `json.loads()` succeeds | No parse errors |
| YAML | `yaml.safe_load()` succeeds | Valid structure |
| Python | `ast.parse()` succeeds | Syntax valid |
| Markdown | Check key sections exist | Headers present |
| Config | Validate against schema | Schema compliance |

#### Semantic Verification
```python
def verify_code_changes(path, expected_changes):
    """Verify changes at semantic level, not just text"""
    import ast
    
    content = mcp_desktop_commander_read_file(path)
    tree = ast.parse(content)
    
    # Check function additions
    functions = [n.name for n in ast.walk(tree) 
                if isinstance(n, ast.FunctionDef)]
    
    # Check class modifications
    classes = [n.name for n in ast.walk(tree) 
              if isinstance(n, ast.ClassDef)]
    
    # Verify expected changes
    for change in expected_changes:
        if change['type'] == 'add_function':
            assert change['name'] in functions
        elif change['type'] == 'modify_class':
            assert change['name'] in classes
```

### Performance Optimization

#### Batch Operations
```python
# Instead of multiple individual writes
for file in files:
    mcp_desktop_commander_write_file(file['path'], file['content'])

# Use multi-file push for version control
mcp_github_push_files(
    owner='user',
    repo='project',
    branch='main',
    files=[{'path': f['path'], 'content': f['content']} 
           for f in files],
    message='Batch update'
)
```

#### Caching Patterns
```python
class FileCache:
    def __init__(self):
        self.cache = {}
    
    def read_file(self, path):
        if path not in self.cache:
            self.cache[path] = {
                'content': mcp_desktop_commander_read_file(path),
                'timestamp': time.time()
            }
        return self.cache[path]['content']
    
    def invalidate(self, path):
        self.cache.pop(path, None)
```

### Security Patterns

#### Secret Filtering
```python
import re

PATTERNS = [
    r'api[_-]?key["\']?\s*[:=]\s*["\']?[\w-]+',
    r'password["\']?\s*[:=]\s*["\']?[\w-]+',
    r'token["\']?\s*[:=]\s*["\']?[\w-]+',
]

def filter_secrets(content):
    for pattern in PATTERNS:
        content = re.sub(pattern, '[REDACTED]', content, flags=re.I)
    return content

# Use in logging
def safe_log_content(path):
    content = mcp_desktop_commander_read_file(path)
    safe_content = filter_secrets(content)
    logger.info(f"File content: {safe_content}")
```

### Testing Integration

#### Test-Driven File Modifications
```python
def modify_with_tests(path, modifications, test_command):
    # Baseline test
    baseline = mcp_desktop_commander_execute_command(test_command)
    if baseline['exit_code'] != 0:
        raise ValueError("Tests failing before modifications")
    
    # Apply modifications
    apply_modifications(path, modifications)
    
    # Verify tests still pass
    result = mcp_desktop_commander_execute_command(test_command)
    if result['exit_code'] != 0:
        # Rollback and analyze
        rollback_file(path)
        analyze_test_failure(result['output'])
        raise ValueError("Modifications broke tests")
```

This comprehensive guide covers advanced patterns for reliable agent-based code modifications.