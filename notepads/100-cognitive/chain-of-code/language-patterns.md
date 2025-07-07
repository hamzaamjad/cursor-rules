# Language Selection Patterns for Chain of Code

## Language Selection Matrix

| Problem Type | Primary Language | Fallback | Rationale |
|--------------|-----------------|----------|-----------|
| Data Analysis | Python | JavaScript | NumPy/Pandas ecosystem |
| String Processing | Python/Regex | JavaScript | Built-in string methods |
| Mathematical | Python | JavaScript | Math libraries, precision |
| Set Operations | SQL | Python | Declarative efficiency |
| Async Logic | JavaScript | Python | Native async/await |
| State Machines | Python | JavaScript | Class-based modeling |
| Pattern Matching | Regex | Python | Domain-specific syntax |

## Python Patterns

### Data Transformation
```python
# Optimal for tabular data operations
import pandas as pd
import numpy as np

def analyze_sales_data(df):
    """Chain of Code for sales analysis"""
    # Explicit calculations
    df['profit_margin'] = (df['revenue'] - df['costs']) / df['revenue']
    df['quarter'] = pd.to_datetime(df['date']).dt.quarter
    
    # Verifiable aggregations
    quarterly_summary = df.groupby('quarter').agg({
        'revenue': 'sum',
        'profit_margin': 'mean',
        'units_sold': 'sum'
    })
    
    # Include verification
    assert quarterly_summary['revenue'].sum() == df['revenue'].sum()
    return quarterly_summary
```

### Mathematical Operations
```python
# Precision and clarity for complex calculations
from decimal import Decimal, getcontext
import math

def calculate_compound_interest(principal, rate, time, n=12):
    """Precise financial calculations"""
    # Set precision for financial accuracy
    getcontext().prec = 10
    
    p = Decimal(str(principal))
    r = Decimal(str(rate))
    t = Decimal(str(time))
    
    # Explicit formula: A = P(1 + r/n)^(nt)
    amount = p * (1 + r/n) ** (n * t)
    
    # Verification with alternative calculation
    alternative = p * Decimal(math.e) ** (r * t)  # Continuous compounding
    
    return {
        'compound_amount': float(amount),
        'continuous_amount': float(alternative),
        'total_interest': float(amount - p)
    }
```

## JavaScript Patterns

### Async Operations
```javascript
// Natural for promise-based workflows
async function processUserRequests(userIds) {
    // Parallel processing with clear flow
    const results = await Promise.all(
        userIds.map(async (id) => {
            try {
                const user = await fetchUser(id);
                const permissions = await fetchPermissions(user.roleId);
                return { userId: id, permissions, status: 'success' };
            } catch (error) {
                return { userId: id, error: error.message, status: 'failed' };
            }
        })
    );
    
    // Verification
    const successCount = results.filter(r => r.status === 'success').length;
    console.log(`Processed ${successCount}/${userIds.length} successfully`);
    
    return results;
}
```

### DOM Manipulation
```javascript
// Browser-specific logic
function calculateViewportCoverage(elements) {
    const viewport = {
        width: window.innerWidth,
        height: window.innerHeight
    };
    
    const coverage = elements.map(el => {
        const rect = el.getBoundingClientRect();
        const visible = {
            width: Math.max(0, Math.min(rect.right, viewport.width) - Math.max(rect.left, 0)),
            height: Math.max(0, Math.min(rect.bottom, viewport.height) - Math.max(rect.top, 0))
        };
        
        return {
            element: el.id,
            visibleArea: visible.width * visible.height,
            totalArea: rect.width * rect.height,
            coveragePercent: (visible.width * visible.height) / (rect.width * rect.height) * 100
        };
    });
    
    return coverage;
}
```

## SQL Patterns

### Set-Based Operations
```sql
-- Declarative approach for complex queries
WITH monthly_sales AS (
    SELECT 
        DATE_TRUNC('month', order_date) as month,
        customer_id,
        SUM(total_amount) as monthly_total,
        COUNT(*) as order_count
    FROM orders
    WHERE order_date >= '2024-01-01'
    GROUP BY 1, 2
),
customer_metrics AS (
    SELECT
        customer_id,
        AVG(monthly_total) as avg_monthly_spend,
        STDDEV(monthly_total) as spend_variance,
        MAX(monthly_total) as peak_month
    FROM monthly_sales
    GROUP BY customer_id
)
SELECT 
    cm.*,
    CASE 
        WHEN avg_monthly_spend > 1000 AND spend_variance < 200 THEN 'Premium Stable'
        WHEN avg_monthly_spend > 1000 THEN 'Premium Variable'
        WHEN avg_monthly_spend > 500 THEN 'Standard'
        ELSE 'Basic'
    END as customer_segment
FROM customer_metrics cm
ORDER BY avg_monthly_spend DESC;
```

## Regex Patterns

### Complex Pattern Matching
```python
import re

def extract_structured_data(text):
    """Parse semi-structured text with regex"""
    patterns = {
        'phone': r'(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
        'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        'currency': r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)',
        'date': r'(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})|(\d{4}[-/]\d{1,2}[-/]\d{1,2})'
    }
    
    extracted = {}
    for name, pattern in patterns.items():
        matches = re.findall(pattern, text)
        extracted[name] = matches
    
    # Validation
    for phone in extracted.get('phone', []):
        formatted = f"({phone[0]}) {phone[1]}-{phone[2]}"
        assert len(phone[0]) == 3 and len(phone[1]) == 3 and len(phone[2]) == 4
    
    return extracted
```

## Multi-Language Patterns

### Polyglot Solutions
```python
def generate_multi_language_solution(problem_type, data):
    """Select optimal language for each component"""
    
    if problem_type == 'data_pipeline':
        # SQL for extraction
        sql_extract = """
        SELECT * FROM source_table
        WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'
        """
        
        # Python for transformation
        python_transform = """
import pandas as pd
df = pd.read_sql(sql_query, connection)
df['normalized_value'] = (df['value'] - df['value'].mean()) / df['value'].std()
        """
        
        # JavaScript for visualization
        js_visualize = """
const chart = new Chart(ctx, {
    type: 'line',
    data: transformedData,
    options: { responsive: true }
});
        """
        
        return {
            'extract': sql_extract,
            'transform': python_transform,
            'visualize': js_visualize
        }
```

## Language-Specific Optimizations

### Python: Vectorization
```python
# Leverage NumPy for performance
import numpy as np

# Bad: Loop-based
def calculate_distances_slow(points):
    distances = []
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            dist = np.sqrt((points[i][0]-points[j][0])**2 + 
                          (points[i][1]-points[j][1])**2)
            distances.append(dist)
    return distances

# Good: Vectorized
def calculate_distances_fast(points):
    points = np.array(points)
    # Broadcasting for all pairwise differences
    diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    distances = np.sqrt((diff ** 2).sum(axis=2))
    return distances[np.triu_indices_from(distances, k=1)]
```

### JavaScript: Functional Patterns
```javascript
// Leverage functional programming
const processTransactions = (transactions) => {
    return transactions
        .filter(t => t.status === 'completed')
        .map(t => ({
            ...t,
            fee: t.amount * 0.02,
            netAmount: t.amount * 0.98
        }))
        .reduce((acc, t) => ({
            totalFees: acc.totalFees + t.fee,
            totalNet: acc.totalNet + t.netAmount,
            count: acc.count + 1
        }), { totalFees: 0, totalNet: 0, count: 0 });
};
```

## Selection Decision Tree

```python
def select_language(task):
    """Decision tree for language selection"""
    
    # Primary criteria
    if task.involves_dom or task.is_browser_based:
        return "javascript"
    
    if task.is_data_query or task.involves_aggregation:
        return "sql"
    
    if task.is_pattern_matching and task.complexity == "simple":
        return "regex"
    
    # Secondary criteria
    if task.requires_precision or task.involves_math:
        return "python"
    
    if task.is_async or task.involves_promises:
        return "javascript"
    
    # Default to Python for general computation
    return "python"
```

## Best Practices

1. **Match language to domain**: Use SQL for set operations, not loops
2. **Leverage built-ins**: Each language's standard library is optimized
3. **Avoid translation**: Don't force idioms from one language to another
4. **Clarity over cleverness**: Readable code is verifiable code
5. **Test in target environment**: Ensure code runs where intended
