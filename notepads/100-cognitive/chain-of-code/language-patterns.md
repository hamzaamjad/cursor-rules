# Chain of Code Language Patterns

## Language Selection Matrix

| Problem Type | Primary Language | Rationale |
|--------------|------------------|-----------|
| Data Analysis | Python | NumPy, Pandas, statistical libraries |
| Web Logic | JavaScript | Async handling, DOM manipulation |
| Set Operations | SQL | Native relational operations |
| Pattern Matching | Regex | Efficient text processing |
| System Scripts | Bash | Direct OS interaction |
| Math/Algorithms | Python/C++ | Performance + readability |

## Python Patterns

```python
# Arithmetic verification
def verify_calculation(operation, *args):
    """Generate test cases for arithmetic operations."""
    result = operation(*args)
    # Cross-verify with different approaches
    alternatives = [
        lambda: eval(f"{operation.__name__}{args}"),
        lambda: sum(args) if operation == add else None
    ]
    return all(alt() == result for alt in alternatives if alt())

# Data transformation
def transform_with_validation(data, pipeline):
    """Apply transformations with intermediate verification."""
    intermediate_results = []
    for step in pipeline:
        data = step(data)
        intermediate_results.append({
            'step': step.__name__,
            'sample': data[:5] if hasattr(data, '__getitem__') else data,
            'shape': getattr(data, 'shape', len(data))
        })
    return data, intermediate_results
```

## JavaScript Patterns

```javascript
// Async logic verification
async function verifyAsyncChain(operations) {
    const results = [];
    let data = null;
    
    for (const op of operations) {
        const startTime = performance.now();
        data = await op(data);
        results.push({
            operation: op.name,
            duration: performance.now() - startTime,
            output: JSON.stringify(data).slice(0, 100)
        });
    }
    
    return { finalResult: data, trace: results };
}

// State machine implementation
class VerifiableStateMachine {
    constructor(states, transitions) {
        this.states = states;
        this.transitions = transitions;
        this.history = [];
    }
    
    transition(event) {
        const allowed = this.transitions[this.state]?.[event];
        if (!allowed) throw new Error(`Invalid transition: ${this.state} -> ${event}`);
        
        this.history.push({ from: this.state, event, to: allowed });
        this.state = allowed;
        return this.state;
    }
}
```

## SQL Patterns

```sql
-- Set operations with verification
WITH source_counts AS (
    SELECT COUNT(*) as total FROM source_table
),
transformed AS (
    SELECT /* transformation logic */
    FROM source_table
),
result_counts AS (
    SELECT COUNT(*) as total FROM transformed
)
SELECT 
    s.total as source_records,
    r.total as result_records,
    s.total - r.total as dropped_records
FROM source_counts s, result_counts r;

-- Data integrity verification
SELECT 
    CASE 
        WHEN COUNT(DISTINCT id) = COUNT(*) THEN 'PASS: No duplicates'
        ELSE CONCAT('FAIL: ', COUNT(*) - COUNT(DISTINCT id), ' duplicates')
    END as uniqueness_check,
    CASE
        WHEN SUM(CASE WHEN critical_field IS NULL THEN 1 ELSE 0 END) = 0 THEN 'PASS: No nulls'
        ELSE CONCAT('FAIL: ', SUM(CASE WHEN critical_field IS NULL THEN 1 ELSE 0 END), ' nulls')
    END as completeness_check
FROM transformed_data;
```

## Regex Patterns

```python
# Pattern matching with verification
import re

def extract_with_verification(pattern, text, expected_groups):
    """Extract patterns with structure verification."""
    compiled = re.compile(pattern)
    matches = compiled.findall(text)
    
    verification = {
        'pattern_valid': bool(matches),
        'match_count': len(matches),
        'group_counts': [len(m) if isinstance(m, tuple) else 1 for m in matches],
        'sample_matches': matches[:3]
    }
    
    # Verify expected structure
    if expected_groups:
        verification['structure_valid'] = all(
            len(m) == expected_groups for m in matches if isinstance(m, tuple)
        )
    
    return matches, verification
```
