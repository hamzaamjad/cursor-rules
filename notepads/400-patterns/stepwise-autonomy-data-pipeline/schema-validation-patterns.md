# Schema Validation Patterns for Data Pipelines

This notepad contains comprehensive schema validation patterns and implementation examples for ensuring data integrity throughout pipeline processing. These patterns extend the stepwise-autonomy principle to data-specific verification requirements.

## Input Schema Verification

Robust data pipelines begin with thorough input validation to catch data quality issues early in the processing chain. The following patterns demonstrate comprehensive approaches to verifying incoming data meets expected specifications.

### Required Column Verification

```python
def verify_required_columns(df, required_cols):
    """
    Verify all required columns are present with expected names.
    
    Args:
        df: Input DataFrame
        required_cols: List of column names that must be present
        
    Returns:
        bool: True if all columns present
        
    Raises:
        ValueError: If any required columns are missing
    """
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return True
```

### Data Type Validation

```python
def validate_column_types(df, type_specifications):
    """
    Verify column data types match expectations.
    
    Args:
        df: DataFrame to validate
        type_specifications: Dict of {column_name: expected_dtype}
        
    Returns:
        List[str]: Validation issues found
    """
    issues = []
    
    for col, expected_type in type_specifications.items():
        if col not in df.columns:
            issues.append(f"Column {col} not found")
            continue
            
        actual_type = df[col].dtype
        
        # Handle flexible type matching
        if expected_type == 'datetime':
            if not pd.api.types.is_datetime64_any_dtype(actual_type):
                issues.append(f"Column {col} expected datetime, got {actual_type}")
        elif expected_type == 'numeric':
            if not pd.api.types.is_numeric_dtype(actual_type):
                issues.append(f"Column {col} expected numeric, got {actual_type}")
        elif expected_type == 'string':
            if not pd.api.types.is_string_dtype(actual_type):
                issues.append(f"Column {col} expected string, got {actual_type}")
                
    return issues
```

### Completeness Validation

```python
def validate_data_completeness(df, completeness_rules):
    """
    Verify data completeness according to business rules.
    
    Args:
        df: DataFrame to validate
        completeness_rules: Dict of {column_name: max_null_percentage}
        
    Returns:
        Dict[str, float]: Columns exceeding null thresholds
    """
    violations = {}
    
    for col, max_null_pct in completeness_rules.items():
        if col not in df.columns:
            continue
            
        null_pct = (df[col].isna().sum() / len(df)) * 100
        
        if null_pct > max_null_pct:
            violations[col] = null_pct
            
    return violations
```

## Output Schema Verification

Output validation ensures that pipeline transformations produce data conforming to downstream expectations. These patterns verify both structural integrity and business logic compliance.

### Metric Range Validation

```python
def validate_metric_ranges(df, metric_ranges):
    """
    Validate metrics are within expected ranges.
    
    Args:
        df: DataFrame to check
        metric_ranges: Dict of {column_name: (min_val, max_val)}
        
    Returns:
        List[str]: Validation issues found
    """
    issues = []
    
    for col, (min_val, max_val) in metric_ranges.items():
        if col not in df.columns:
            continue
            
        col_min = df[col].min()
        col_max = df[col].max()
        
        if col_min < min_val:
            issues.append(f"Column {col} has value {col_min} below minimum {min_val}")
            
        if col_max > max_val:
            issues.append(f"Column {col} has value {col_max} above maximum {max_val}")
            
    return issues
```

### Uniqueness Verification

```python
def verify_unique_constraints(df, unique_columns):
    """
    Verify uniqueness constraints are maintained.
    
    Args:
        df: DataFrame to validate
        unique_columns: List of column names or lists of column combinations
        
    Returns:
        Dict[str, int]: Columns with duplicate counts
    """
    duplicate_info = {}
    
    for col_spec in unique_columns:
        if isinstance(col_spec, str):
            col_spec = [col_spec]
            
        duplicates = df.duplicated(subset=col_spec).sum()
        
        if duplicates > 0:
            duplicate_info[','.join(col_spec)] = duplicates
            
    return duplicate_info
```

## Integration Patterns

These validation patterns integrate seamlessly with the stepwise-autonomy protocol through structured verification checkpoints. Each validation function returns clear success/failure indicators that guide pipeline execution decisions.

The patterns support both fail-fast and warning-based approaches, allowing pipelines to adapt their strictness based on business requirements and data criticality. Comprehensive logging ensures that validation results feed into monitoring and alerting systems for operational visibility.