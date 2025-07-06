# Performance Monitoring Patterns for Data Pipelines

This notepad provides comprehensive performance monitoring and optimization patterns for data pipeline implementations. These patterns ensure efficient resource utilization and enable proactive identification of performance bottlenecks.

## Memory Utilization Monitoring

Effective memory management is critical for data pipeline performance, particularly when processing large datasets. The following patterns demonstrate systematic approaches to monitoring and optimizing memory usage throughout pipeline execution.

### Context Manager for Memory Monitoring

```python
from contextlib import contextmanager
import psutil
import os
import logging

logger = logging.getLogger(__name__)

@contextmanager
def memory_usage_monitor():
    """
    Monitor memory usage during a code block execution.
    
    Usage:
        with memory_usage_monitor():
            result_df = transform_function(input_df)
    """
    process = psutil.Process(os.getpid())
    start_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    yield
    
    end_memory = process.memory_info().rss / 1024 / 1024  # MB
    peak_memory = end_memory - start_memory
    
    logger.info(f"Peak memory usage: {peak_memory:.2f} MB")
    
    # Alert if memory usage exceeds threshold
    if peak_memory > 1000:  # 1GB threshold
        logger.warning(f"High memory usage detected: {peak_memory:.2f} MB")
```

### Chunked Processing Pattern

```python
def process_large_dataset_in_chunks(input_path, output_path, transform_func, chunk_size=10000):
    """
    Process large datasets in manageable chunks to control memory usage.
    
    Args:
        input_path: Path to input data
        output_path: Path for output data
        transform_func: Function to apply to each chunk
        chunk_size: Number of rows per chunk
    """
    total_rows = 0
    
    # Process in chunks
    for chunk_num, chunk_df in enumerate(pd.read_csv(input_path, chunksize=chunk_size)):
        with memory_usage_monitor():
            # Apply transformation
            transformed_chunk = transform_func(chunk_df)
            
            # Write results
            mode = 'w' if chunk_num == 0 else 'a'
            header = chunk_num == 0
            transformed_chunk.to_csv(output_path, mode=mode, header=header, index=False)
            
            total_rows += len(chunk_df)
            logger.info(f"Processed chunk {chunk_num + 1} ({total_rows} rows total)")
```

## Query Performance Optimization

Database query performance significantly impacts overall pipeline efficiency. These patterns provide systematic approaches to identifying and resolving query performance issues.

### Query Execution Plan Analysis

```sql
-- Analyze query execution plan for optimization opportunities
EXPLAIN ANALYZE
SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) as order_count,
    SUM(o.total_amount) as total_revenue
FROM 
    fact_orders o
    JOIN dim_customers c ON o.customer_id = c.id
WHERE 
    o.order_date >= '2024-01-01'
    AND c.customer_status = 'active'
GROUP BY 
    c.customer_id, c.customer_name
HAVING 
    COUNT(o.order_id) > 5;
```

### Query Performance Monitoring Wrapper

```python
import time
from functools import wraps

def monitor_query_performance(query_name):
    """
    Decorator to monitor query execution time and log performance metrics.
    
    Args:
        query_name: Descriptive name for the query being monitored
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                logger.info(f"Query '{query_name}' completed in {execution_time:.2f} seconds")
                
                # Alert on slow queries
                if execution_time > 30:  # 30 second threshold
                    logger.warning(f"Slow query detected: '{query_name}' took {execution_time:.2f} seconds")
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"Query '{query_name}' failed after {execution_time:.2f} seconds: {str(e)}")
                raise
                
        return wrapper
    return decorator

# Usage example
@monitor_query_performance("customer_aggregation")
def get_customer_metrics(connection, start_date):
    query = """
    SELECT customer_id, COUNT(*) as purchase_count, SUM(amount) as total_spent
    FROM transactions
    WHERE transaction_date >= %s
    GROUP BY customer_id
    """
    return pd.read_sql(query, connection, params=[start_date])
```

## Pipeline Execution Monitoring

Comprehensive pipeline monitoring enables proactive identification of performance degradation and system issues. These patterns provide holistic visibility into pipeline execution characteristics.

### Pipeline Performance Metrics Collector

```python
class PipelineMetricsCollector:
    """
    Collect and report comprehensive metrics for pipeline execution.
    """
    
    def __init__(self, pipeline_name):
        self.pipeline_name = pipeline_name
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'steps': {},
            'memory_peaks': [],
            'row_counts': {},
            'errors': []
        }
    
    def start_pipeline(self):
        self.metrics['start_time'] = time.time()
        logger.info(f"Pipeline '{self.pipeline_name}' started")
    
    def start_step(self, step_name):
        self.metrics['steps'][step_name] = {
            'start_time': time.time(),
            'memory_start': psutil.Process().memory_info().rss / 1024 / 1024
        }
    
    def end_step(self, step_name, row_count=None):
        if step_name not in self.metrics['steps']:
            return
            
        step_metrics = self.metrics['steps'][step_name]
        step_metrics['end_time'] = time.time()
        step_metrics['duration'] = step_metrics['end_time'] - step_metrics['start_time']
        step_metrics['memory_end'] = psutil.Process().memory_info().rss / 1024 / 1024
        step_metrics['memory_used'] = step_metrics['memory_end'] - step_metrics['memory_start']
        
        if row_count:
            self.metrics['row_counts'][step_name] = row_count
        
        logger.info(f"Step '{step_name}' completed in {step_metrics['duration']:.2f}s, "
                   f"used {step_metrics['memory_used']:.2f}MB memory")
    
    def end_pipeline(self):
        self.metrics['end_time'] = time.time()
        total_duration = self.metrics['end_time'] - self.metrics['start_time']
        
        logger.info(f"Pipeline '{self.pipeline_name}' completed in {total_duration:.2f}s")
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive performance report."""
        report = f"\n{'='*60}\n"
        report += f"Pipeline Performance Report: {self.pipeline_name}\n"
        report += f"{'='*60}\n"
        report += f"Total Duration: {self.metrics['end_time'] - self.metrics['start_time']:.2f}s\n"
        report += f"\nStep Performance:\n"
        
        for step_name, step_metrics in self.metrics['steps'].items():
            report += f"  - {step_name}: {step_metrics['duration']:.2f}s, "
            report += f"{step_metrics['memory_used']:.2f}MB memory\n"
        
        logger.info(report)
        return report
```

## Integration with Monitoring Systems

These performance monitoring patterns integrate seamlessly with enterprise monitoring solutions through standardized metrics export. The patterns support integration with Prometheus, Grafana, DataDog, and other monitoring platforms through metric exposition endpoints and standardized logging formats.

The systematic collection of performance metrics enables trend analysis, capacity planning, and proactive optimization of data pipeline infrastructure. By maintaining historical performance baselines, teams can quickly identify performance regressions and validate the impact of optimization efforts.