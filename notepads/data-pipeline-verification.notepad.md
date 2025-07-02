# Data Pipeline Verification Procedures

## Schema Validation

### Input Schema Verification
- **Required Columns**
  - Verify all required columns are present with expected names
  - Check for case sensitivity issues in column names
  - Example:
    ```python
    def verify_required_columns(df, required_cols):
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        return True
    ```

- **Data Type Verification**
  - Confirm data types match expectations
  - Pay special attention to:
    - Date/time columns (proper datetime objects, not strings)
    - Numeric columns (appropriate precision)
    - Categorical columns (proper encoding)
  - Example:
    ```python
    def verify_column_types(df, type_dict):
        """
        Verify column types match expected types
        
        Args:
            df: DataFrame to check
            type_dict: Dict of {column_name: expected_type}
                where expected_type can be 'int', 'float', 'datetime', etc.
        """
        for col, expected_type in type_dict.items():
            if col not in df.columns:
                continue
                
            if expected_type == 'datetime':
                if not pd.api.types.is_datetime64_any_dtype(df[col]):
                    raise TypeError(f"Column {col} should be datetime, got {df[col].dtype}")
            elif str(df[col].dtype) != expected_type:
                raise TypeError(f"Column {col} should be {expected_type}, got {df[col].dtype}")
    ```

- **Completeness Check**
  - Verify expected row count matches based on source
  - Check for null values in critical columns
  - Example:
    ```python
    def check_completeness(df, critical_cols, expected_row_count=None):
        """Check dataframe for completeness"""
        issues = []
        
        # Check row count if expected count provided
        if expected_row_count and len(df) != expected_row_count:
            issues.append(f"Expected {expected_row_count} rows, got {len(df)}")
            
        # Check for nulls in critical columns
        for col in critical_cols:
            null_count = df[col].isna().sum()
            if null_count > 0:
                issues.append(f"Column {col} has {null_count} null values")
                
        return issues
    ```

### Output Schema Verification

- **Shape Validation**
  - Verify output dimensions are as expected
  - Check for duplicate records
  - Example:
    ```python
    def validate_output_shape(df, min_rows=None, max_rows=None, unique_cols=None):
        """Validate shape of output dataframe"""
        issues = []
        
        # Check min/max row counts
        if min_rows and len(df) < min_rows:
            issues.append(f"Output has too few rows: {len(df)} < {min_rows}")
            
        if max_rows and len(df) > max_rows:
            issues.append(f"Output has too many rows: {len(df)} > {max_rows}")
            
        # Check for duplicates on specified columns
        if unique_cols:
            dupe_count = len(df) - len(df.drop_duplicates(subset=unique_cols))
            if dupe_count > 0:
                issues.append(f"Found {dupe_count} duplicate rows based on {unique_cols}")
                
        return issues
    ```

- **Data Range Validation**
  - Verify calculated metrics are within expected ranges
  - Flag outliers for review
  - Example:
    ```python
    def validate_metric_ranges(df, metric_ranges):
        """
        Validate metrics are within expected ranges
        
        Args:
            df: DataFrame to check
            metric_ranges: Dict of {column_name: (min_val, max_val)}
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

## Transformation Logic Verification

### Business Logic Validation

- **Aggregation Accuracy**
  - Verify aggregations match expected totals
  - Example:
    ```python
    def verify_aggregation(df, group_cols, agg_col, expected_total):
        """Verify aggregation sums to expected total"""
        actual_total = df.groupby(group_cols)[agg_col].sum().sum()
        if not math.isclose(actual_total, expected_total, rel_tol=1e-5):
            raise ValueError(f"Aggregation total {actual_total} doesn't match expected {expected_total}")
    ```

- **Calculated Field Validation**
  - Manually verify calculated fields for sample records
  - Test boundary cases and special values
  - Example:
    ```python
    def verify_calculated_field(df, input_cols, output_col, calculation_func):
        """
        Verify a calculated field matches expected output
        
        Args:
            df: DataFrame with data
            input_cols: List of columns used in calculation
            output_col: Column containing result
            calculation_func: Function that takes inputs and returns expected output
        """
        # Take a sample for verification
        sample = df.sample(min(100, len(df)))
        
        for _, row in sample.iterrows():
            inputs = [row[col] for col in input_cols]
            expected = calculation_func(*inputs)
            actual = row[output_col]
            
            if not pd.isna(expected) and not pd.isna(actual):
                if not math.isclose(actual, expected, rel_tol=1e-5):
                    raise ValueError(
                        f"Calculation mismatch for row {row.name}: "
                        f"expected {expected}, got {actual}"
                    )
    ```

- **Null Handling Verification**
  - Check how nulls propagate through calculations
  - Verify that null handling aligns with business requirements
  - Example:
    ```python
    def verify_null_handling(df, calc_col, input_cols):
        """Verify null handling in calculations"""
        # Check if nulls in inputs lead to nulls in output as expected
        for input_col in input_cols:
            null_inputs = df[df[input_col].isna()]
            if not null_inputs.empty:
                if not null_inputs[calc_col].isna().all():
                    logger.warning(
                        f"Found {null_inputs[calc_col].notna().sum()} non-null values in "
                        f"{calc_col} where {input_col} is null"
                    )
    ```

### Time-based Calculation Verification

- **Time Zone Consistency**
  - Verify all datetime operations use consistent time zones
  - Check for daylight saving time handling
  - Example:
    ```python
    def verify_timezone_consistency(df, datetime_cols):
        """Verify timezone consistency across datetime columns"""
        for col in datetime_cols:
            if col not in df.columns:
                continue
                
            # Check if timezone info exists and is consistent
            tz_info = df[col].dt.tz
            if tz_info is None:
                logger.warning(f"Column {col} has no timezone information")
            
            # Check for mixed timezones
            sample_tzs = df.sample(min(100, len(df)))[col].apply(
                lambda x: x.tzinfo if not pd.isna(x) else None
            ).unique()
            
            if len(sample_tzs) > 1:
                logger.error(f"Column {col} has mixed timezone information: {sample_tzs}")
    ```

- **Period Calculations**
  - Verify period-over-period calculations correctly align dates
  - Example:
    ```python
    def verify_period_calculations(df, date_col, value_col, period_col):
        """Verify period-over-period calculations"""
        # Group by period
        period_df = df.groupby(period_col)[value_col].sum().reset_index()
        
        # Verify no periods are missing
        periods = period_df[period_col].unique()
        min_period = min(periods)
        max_period = max(periods)
        expected_periods = pd.date_range(min_period, max_period, freq='M')
        
        if len(periods) != len(expected_periods):
            logger.error(f"Missing periods detected. Expected {len(expected_periods)}, got {len(periods)}")
    ```

## Performance Verification

### Query Optimization

- **Execution Plan Analysis**
  - Review query execution plans for full table scans or other inefficiencies
  - Example:
    ```sql
    EXPLAIN ANALYZE
    SELECT * FROM fact_orders
    JOIN dim_customers ON fact_orders.customer_id = dim_customers.id
    WHERE order_date > '2024-01-01'
    ```

- **Index Utilization**
  - Verify appropriate indexes are being used
  - Example check:
    ```sql
    SELECT 
      relname as table_name,
      indexrelname as index_name,
      idx_scan as index_scans,
      idx_tup_read as tuples_read,
      idx_tup_fetch as tuples_fetched
    FROM pg_stat_all_indexes
    WHERE schemaname = 'analytics'
    ORDER BY idx_scan DESC;
    ```

### Memory Utilization

- **Peak Memory Monitoring**
  - Monitor memory usage during pipeline execution
  - Example:
    ```python
    @contextmanager
    def memory_usage_monitor():
        """Monitor memory usage during a code block"""
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        yield
        
        end_memory = process.memory_info().rss / 1024 / 1024  # MB
        peak_memory = end_memory - start_memory
        
        logger.info(f"Peak memory usage: {peak_memory:.2f} MB")
    
    # Usage:
    with memory_usage_monitor():
        result_df = transform_function(input_df)
    ```

- **Chunking Verification**
  - Verify chunking implementation for large dataset operations
  - Example:
    ```python
    def process_in_chunks(df, chunk_size, process_func):
        """Process a dataframe in chunks to manage memory"""
        results = []
        
        for i in range(0, len(df), chunk_size):
            chunk = df.iloc[i:i+chunk_size]
            chunk_result = process_func(chunk)
            results.append(chunk_result)
            
            # Log progress
            logger.info(f"Processed chunk {i//chunk_size + 1} of {math.ceil(len(df)/chunk_size)}")
        
        # Combine results
        if isinstance(results[0], pd.DataFrame):
            return pd.concat(results, ignore_index=True)
        else:
            return results
    ```

## Research Integration

### Applying Research Findings

- **Documentation Alignment**
  - Document how research findings influenced implementation
  - Example:
    ```python
    """
    Revenue Forecasting Model
    
    This implementation is based on research findings from the
    'Revenue Forecasting Comparison' Perplexity research (2024-04-28),
    which identified Prophet as the optimal model for our use case,
    balancing accuracy and implementation complexity.
    
    Key parameters (seasonality_mode, changepoint_prior_scale) were
    selected based on hyperparameter testing documented in the research.
    """
    ```

- **Decision Point Transparency**
  - Document decision points with clear rationale based on research
  - Example decision log:
    ```
    ## 2024-04-29: Selected xgboost for churn prediction
    
    Research from Perplexity (see perplexity-research-churn-models.md)
    compared 5 algorithms for our customer churn use case. XGBoost was
    selected because:
    
    1. Highest F1 score (0.82) on validation data
    2. Good balance of precision (0.79) and recall (0.85)
    3. Reasonable training time (3-5 minutes on full dataset)
    4. Native feature importance output aligns with explainability requirements
    
    Runner-up was Random Forest (F1: 0.78) which will be kept as fallback.
    ```

### Validation Against Research

- **Metric Alignment**
  - Verify implemented solution achieves metrics identified in research
  - Example:
    ```python
    def validate_against_research_metrics(model, test_data, expected_metrics):
        """
        Validate model performance against metrics identified in research
        
        Args:
            model: Trained model
            test_data: Test dataset
            expected_metrics: Dict of expected metric values from research
        """
        predictions = model.predict(test_data.features)
        
        # Calculate actual metrics
        actual_metrics = {
            'accuracy': accuracy_score(test_data.labels, predictions),
            'f1': f1_score(test_data.labels, predictions),
            'precision': precision_score(test_data.labels, predictions),
            'recall': recall_score(test_data.labels, predictions)
        }
        
        # Compare with expected metrics
        for metric, expected in expected_metrics.items():
            actual = actual_metrics[metric]
            
            # Allow slight variation from research results
            if abs(actual - expected) > 0.05:
                logger.warning(
                    f"{metric} of {actual:.2f} differs significantly "
                    f"from research finding of {expected:.2f}"
                )
            else:
                logger.info(
                    f"{metric} of {actual:.2f} aligns with "
                    f"research finding of {expected:.2f}"
                )
    ```

## Reference Files
@stepwise-autonomy.mdc
@sql-correctness.mdc
@sql-performance.mdc
@datascience-repro.mdc
