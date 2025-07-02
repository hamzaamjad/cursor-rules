# Data Analytics Code Patterns

## Data Transformation Pattern

```python
def transform_revenue_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transform revenue data for analysis.
    
    Args:
        df: DataFrame containing raw revenue data
            Required columns: ['date', 'customer_id', 'amount']
            
    Returns:
        DataFrame with transformed data and additional metrics
        
    Raises:
        ValueError: If required columns are missing
    """
    # Validate input
    required_cols = ['date', 'customer_id', 'amount']
    if not all(col in df.columns for col in required_cols):
        raise ValueError(f"Missing required columns. Required: {required_cols}")
        
    # Convert date to datetime if needed
    if not pd.api.types.is_datetime64_any_dtype(df['date']):
        df['date'] = pd.to_datetime(df['date'])
        
    # Add calculated columns
    result = df.copy()
    result['month'] = result['date'].dt.to_period('M')
    result['quarter'] = result['date'].dt.to_period('Q')
    result['year'] = result['date'].dt.year
    
    # Group and calculate metrics
    result['customer_monthly_total'] = (
        result.groupby(['customer_id', 'month'])['amount']
        .transform('sum')
    )
    
    # Calculate year-over-year growth
    result['prev_year_amount'] = (
        result.groupby(['customer_id', result['date'].dt.month])['amount']
        .transform(lambda x: x.shift(1))
    )
    
    result['yoy_growth'] = (
        (result['amount'] - result['prev_year_amount']) / 
        result['prev_year_amount'].replace(0, float('nan'))
    )
    
    # Log transformations for debugging
    logger.info(f"Transformed revenue data shape: {result.shape}")
    logger.debug(f"Sample transformed data:\n{result.head(2)}")
    
    return result
```

## Data Validation Pattern

```python
def validate_dataset(df: pd.DataFrame, schema: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """Validate a DataFrame against a schema definition.
    
    Args:
        df: DataFrame to validate
        schema: Dict containing column specs with required format:
               {
                   "column_name": {
                       "dtype": str|int|float|bool|datetime,
                       "required": bool,
                       "unique": bool,
                       "range": (min, max) | None,
                       "allowed_values": List[Any] | None
                   }
               }
            
    Returns:
        Tuple containing (is_valid, list_of_validation_errors)
    """
    errors = []
    
    # Check for required columns
    required_cols = [col for col, specs in schema.items() 
                    if specs.get("required", False)]
    missing_cols = [col for col in required_cols if col not in df.columns]
    
    if missing_cols:
        errors.append(f"Missing required columns: {missing_cols}")
    
    # Check column types and constraints
    for col, specs in schema.items():
        if col not in df.columns:
            continue
            
        # Type validation
        expected_type = specs.get("dtype")
        if expected_type:
            if expected_type == "datetime":
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    errors.append(f"Column '{col}' should be datetime type")
            elif not df[col].dtype == expected_type:
                errors.append(f"Column '{col}' should be {expected_type} type")
        
        # Uniqueness validation
        if specs.get("unique", False) and df[col].duplicated().any():
            errors.append(f"Column '{col}' contains duplicate values")
            
        # Range validation
        if specs.get("range") and not df[col].isna().all():
            min_val, max_val = specs["range"]
            if df[col].min() < min_val or df[col].max() > max_val:
                errors.append(f"Column '{col}' has values outside range {specs['range']}")
                
        # Allowed values validation
        if specs.get("allowed_values") and not df[col].isna().all():
            invalid_vals = df[col][~df[col].isin(specs["allowed_values"])].unique()
            if len(invalid_vals) > 0:
                errors.append(f"Column '{col}' contains invalid values: {invalid_vals}")
    
    return len(errors) == 0, errors
```

## Data Pipeline Code Review Checklist

### Performance
- [ ] Uses vectorized operations instead of loops for pandas operations
- [ ] Avoids multiple GroupBy operations on the same dimensions
- [ ] Employs appropriate chunking for large datasets
- [ ] Considers memory usage for large transformations
- [ ] Uses appropriate indexes for database operations

### Maintainability
- [ ] Functions have clear, specific purposes aligned with business concepts
- [ ] Type hints used consistently
- [ ] Follows naming conventions (see Airflow pattern below)
- [ ] Documentation covers intent, not just mechanics
- [ ] Unit tests cover edge cases (null handling, empty datasets)

### Error Handling
- [ ] Input validation occurs early
- [ ] Specific exceptions with clear messages
- [ ] Graceful handling of missing or malformed data
- [ ] Appropriate logging at different levels
- [ ] Avoids silent failures

### Common Airflow Pattern Naming Conventions

For DAGs and operators:
```python
# Generally follow: {source}_to_{destination}_{action}_{frequency}

# Examples:
dag_id = 'salesforce_to_snowflake_load_daily'
task_id = 'transform_customer_data'
```

## Common Data Analytics Anti-patterns

1. **Premature Aggregation**
   - Problem: Aggregating data too early in the pipeline
   - Impact: Loss of drill-down capability, hindered analysis
   - Solution: Maintain granular data as long as possible, aggregate at query time

2. **String-based Date Operations**
   - Problem: Manipulating dates as strings
   - Impact: Performance degradation, timezone issues, errors
   - Solution: Convert to datetime objects immediately, use proper date operations

3. **Lack of Data Type Enforcement**
   - Problem: Not enforcing data types 
   - Impact: Subtle calculation errors, performance issues
   - Solution: Explicitly convert and validate types early in process

4. **Silent Null Handling**
   - Problem: Operations that silently handle nulls in unexpected ways
   - Impact: Incorrect analyses, misleading results
   - Solution: Explicitly handle nulls, document behavior, validate output

5. **Dashboard-driven Development**
   - Problem: Creating data models solely for specific dashboards
   - Impact: Data silos, inconsistent definitions, maintenance overhead
   - Solution: Develop semantic layer with business-aligned definitions

## Reference Files
@python-clean-code.mdc
@datascience-repro.mdc
