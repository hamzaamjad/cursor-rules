# Stigmergic Implementation Examples

This notepad contains comprehensive implementation examples demonstrating stigmergic coordination patterns across various development contexts. These examples illustrate how environmental modifications enable indirect communication and emergent optimization in software development workflows.

## Environmental Marker Patterns

Environmental markers serve as the foundation of stigmergic coordination, providing indirect communication channels that reduce the need for explicit documentation and meetings. These patterns demonstrate practical approaches to leaving interpretable traces that guide subsequent development activities.

### TODO Pattern Evolution

The traditional TODO comment evolves into a rich information carrier that conveys category, priority, and context without requiring external tracking systems. This pattern enables developers to discover work naturally through code exploration rather than task management tools.

```python
# Traditional approach - minimal information
# TODO: Fix this later

# Stigmergic approach - rich environmental marker
# TODO(performance): Optimize query - currently 2.3s, target <500ms
# BREADCRUMB: Previous optimization attempted indexing (failed due to cardinality)
# SUCCESS_TRAIL: Caching reduced similar query from 1.8s to 200ms
```

### Status Markers in Naming Conventions

File naming conventions become communication channels that broadcast work state without requiring status meetings or documentation updates. This pattern creates immediately visible workflow states that guide team coordination.

```
# Workflow state indicators
feature.wip.js          # Work in progress - active development
feature.review.js       # Ready for review - implementation complete
feature.ready.js        # Review complete - ready for integration
feature.deprecated.js   # Marked for removal - includes sunset date

# Evolution trails
auth.v1.legacy.js      # Original implementation
auth.v2.oauth.js       # OAuth migration
auth.v3.jwt.wip.js     # Current JWT implementation in progress
```

## Pheromone-Like Signal Implementation

Pheromone signals strengthen or fade based on usage patterns, creating self-optimizing systems that naturally evolve toward efficiency. These implementation patterns demonstrate how to create signals that guide optimization efforts without central planning.

### Performance Pheromones

```javascript
// userService.js
function getUserProfile(userId) {
    // HOTPATH: 5000 calls/hour, 45ms avg, 120ms p99
    // OPTIMIZATION_SCENT: 80% calls use only name and email fields
    // CACHE_TRAIL: Redis caching reduced latency by 75%
    
    const startTime = performance.now();
    
    const user = await database.users.findById(userId);
    
    // PERFORMANCE_MARKER: Auto-updated by monitoring
    // Last 1000 calls: min=12ms, avg=45ms, max=320ms
    updatePerformanceTrail('getUserProfile', performance.now() - startTime);
    
    return user;
}

// Auto-generated performance trail (updates hourly)
// .cursor/performance-trails.json
{
    "getUserProfile": {
        "callFrequency": 5000,
        "avgLatency": 45,
        "p99Latency": 120,
        "lastOptimized": "2025-01-02",
        "optimizationPriority": "high"
    }
}
```

### Success and Warning Trails

```python
def process_payment(amount, currency, payment_method):
    """
    SUCCESS_RATE: 99.2% (last 10K transactions)
    FAILURE_PATTERNS: 
      - insufficient_funds: 45%
      - network_timeout: 30%
      - invalid_card: 25%
    """
    
    # WARNING_SCENT: Currency conversion issues with XOF
    # VERIFIED: Works correctly with negative amounts (refunds)
    # EDGE_CASE_TRAIL: Handles zero amounts for auth-only transactions
    
    try:
        result = payment_gateway.process(amount, currency, payment_method)
        
        # SUCCESS_PHEROMONE: Strengthen successful path
        record_success_trail('payment_process', payment_method)
        
        return result
        
    except PaymentException as e:
        # FAILURE_ATTRACTOR: Common failure point
        # RECOVERY_PATTERN: Retry with exponential backoff successful 70% of time
        record_failure_pattern('payment_process', e.type)
        raise
```

## Artifact-Based Communication

Artifact-based communication creates persistent environmental modifications that communicate complex state and decisions without requiring synchronous interaction. These patterns demonstrate how to structure artifacts for maximum communicative value.

### State File Pattern

```json
// .cursor/workflow-state.json
{
    "pipeline": {
        "current_stage": "data_validation",
        "stages_complete": ["ingestion", "cleaning"],
        "stages_pending": ["transformation", "loading"],
        "last_successful_run": "2025-01-02T10:30:00Z",
        "common_failures": {
            "schema_mismatch": 15,
            "timeout": 8,
            "memory_exceeded": 3
        },
        "optimization_opportunities": [
            {
                "stage": "cleaning",
                "issue": "Full table scan",
                "impact": "2.5 minutes added",
                "suggestion": "Add index on customer_id"
            }
        ]
    }
}
```

### Decision Log Pattern

```markdown
# Decision: Authentication Strategy
Date: 2025-01-02
Participants: @alice (security), @bob (backend), @carol (frontend)

## Context
Need to implement authentication for new API endpoints.

## Options Considered
1. **Session-based** - Traditional, stateful
   - Pros: Simple, well-understood
   - Cons: Scaling issues, mobile complexity
   
2. **JWT** - Stateless tokens
   - Pros: Scalable, mobile-friendly
   - Cons: Token size, revocation complexity
   
3. **OAuth2** - Delegated authorization
   - Pros: Industry standard, flexible
   - Cons: Complex implementation

## Decision: JWT with Refresh Tokens

### Rationale
- Stateless scaling aligns with microservices architecture
- Mobile apps need offline capability
- Refresh tokens solve revocation problem

### Implementation Markers
- SUCCESS_PATTERN: Used in user-service successfully
- INTEGRATION_POINT: Links with rate-limiter.ready.js
- MONITORING: Track token expiry patterns
```

## Self-Organizing Behaviors

Self-organizing behaviors emerge from simple rules that create complex, adaptive systems. These implementation patterns demonstrate how to design systems that naturally evolve toward optimal configurations.

### Auto-Indexing Pattern

```python
import os
from pathlib import Path

def auto_generate_index(directory, threshold=10):
    """
    Automatically generate index files when directories become complex.
    This reduces cognitive load for navigation.
    """
    path = Path(directory)
    items = list(path.iterdir())
    
    if len(items) > threshold:
        index_content = f"# Index for {path.name}\n\n"
        index_content += f"Generated: {datetime.now()}\n"
        index_content += f"Item count: {len(items)}\n\n"
        
        # Categorize items
        categories = {
            'modules': [],
            'tests': [],
            'docs': [],
            'configs': [],
            'other': []
        }
        
        for item in items:
            if item.name.endswith('_test.py'):
                categories['tests'].append(item)
            elif item.name.endswith('.md'):
                categories['docs'].append(item)
            elif item.name.endswith('.config'):
                categories['configs'].append(item)
            elif item.suffix == '.py':
                categories['modules'].append(item)
            else:
                categories['other'].append(item)
        
        # Write categorized index
        for category, items in categories.items():
            if items:
                index_content += f"\n## {category.title()}\n"
                for item in sorted(items):
                    # Add metadata markers
                    size = item.stat().st_size
                    modified = datetime.fromtimestamp(item.stat().st_mtime)
                    index_content += f"- {item.name} ({size} bytes, modified: {modified:%Y-%m-%d})\n"
        
        # Write index file
        index_path = path / "INDEX.md"
        index_path.write_text(index_content)
        
        # Leave emergence marker
        print(f"EMERGENCE: Auto-generated index for {path.name} (>{threshold} items)")
```

### Pattern Reinforcement

```javascript
// patternLibrary.js
class PatternLibrary {
    constructor() {
        this.patterns = new Map();
        this.usageCount = new Map();
    }
    
    recordPatternUsage(patternName, context) {
        // Strengthen frequently used patterns
        const count = (this.usageCount.get(patternName) || 0) + 1;
        this.usageCount.set(patternName, count);
        
        // Promote patterns that reach usage threshold
        if (count === 10) {
            this.promoteToRecommended(patternName);
            // EMERGENCE_MARKER: Pattern promoted due to frequent use
            console.log(`PATTERN_PROMOTION: ${patternName} now recommended`);
        }
        
        // Deprecate unused patterns
        this.checkForStalePatterns();
    }
    
    checkForStalePatterns() {
        const now = Date.now();
        const staleThreshold = 30 * 24 * 60 * 60 * 1000; // 30 days
        
        this.patterns.forEach((pattern, name) => {
            if (now - pattern.lastUsed > staleThreshold) {
                pattern.status = 'deprecated';
                // DECAY_MARKER: Pattern marked stale
                console.log(`PATTERN_DECAY: ${name} marked deprecated (unused 30+ days)`);
            }
        });
    }
}
```

## Integration Examples

These examples demonstrate how stigmergic patterns integrate with existing development workflows to create more efficient and self-organizing systems.

### Multi-Stage Pipeline Development

```python
# data_pipeline.stage_2_of_5.py
"""
PIPELINE_EVOLUTION:
  1. raw_ingestion.complete.py ✓
  2. data_cleaning.current.py ← YOU ARE HERE
  3. feature_engineering.pending.py
  4. model_training.pending.py
  5. deployment.pending.py

UPSTREAM_MARKERS:
  - INPUT: 1.2M records validated
  - SCHEMA: v2.3 (see schemas/customer_v2.3.json)
  - QUALITY: 98.5% complete records

CURRENT_STAGE_STATUS:
  - PROGRESS: [████████░░] 80%
  - BLOCKER: Handling inconsistent date formats
  - PERFORMANCE: 1000 records/sec (target: 1500)
"""

import pandas as pd
from pathlib import Path

def clean_customer_data():
    # BREADCRUMB: Previous stage stored data in parquet format
    input_path = Path(".cursor/pipeline/stage_1_output.parquet")
    
    # CHECKPOINT: Verify input exists and is recent
    if not input_path.exists():
        raise FileNotFoundError("MISSING_UPSTREAM: Run stage_1 first")
    
    if (datetime.now() - datetime.fromtimestamp(input_path.stat().st_mtime)).hours > 24:
        print("WARNING_SCENT: Input data >24 hours old")
    
    df = pd.read_parquet(input_path)
    
    # HOTPATH: This validation catches 90% of issues
    validation_issues = validate_data_quality(df)
    if validation_issues:
        # FAILURE_ATTRACTOR: Common failure point
        record_validation_failures(validation_issues)
    
    # Cleaning logic here...
    cleaned_df = perform_cleaning(df)
    
    # SUCCESS_TRAIL: Mark successful completion
    output_path = Path(".cursor/pipeline/stage_2_output.parquet")
    cleaned_df.to_parquet(output_path)
    
    # DOWNSTREAM_SIGNAL: Notify next stage
    Path(".cursor/pipeline/stage_2.complete").touch()
    
    # EMERGENCE_INDICATOR: Track cleaning patterns
    record_cleaning_patterns(df, cleaned_df)
    
    return cleaned_df
```

### Collaborative Feature Development

```javascript
// features/shoppingCart.evolution.js
/*
FEATURE_PHYLOGENY:
├── cartBasic.v1.js (2024-12-01) - Simple add/remove
├── cartPersistent.v2.js (2024-12-15) - Added localStorage
├── cartMultiCurrency.v3.js (2025-01-01) - Multi-currency support
└── cartOptimized.wip.js (current) - Performance optimization

CONTRIBUTOR_TRAILS:
- @alice: Security review ✓ (2025-01-02)
- @bob: Performance baseline (45ms avg)
- @carol: Accessibility audit pending

INTEGRATION_LANDSCAPE:
- DEPENDS_ON: userAuth.ready.js, inventory.v2.js
- USED_BY: checkout.wip.js, orderHistory.js
- CONFLICTS_WITH: legacyCart.js (deprecate by 2025-02-01)
*/

class ShoppingCart {
    constructor() {
        // DECISION_SCENT: Chose Map over Object for O(1) operations
        this.items = new Map();
        
        // PERFORMANCE_MARKER: Track operation latencies
        this.performanceTrail = [];
    }
    
    addItem(productId, quantity = 1) {
        // HOTPATH_INDICATOR: 80% of additions are single items
        const startTime = performance.now();
        
        // VALIDATION_CHECKPOINT: Moved here from checkout
        if (!this.validateProduct(productId)) {
            // FAILURE_PATTERN: Invalid products 2% of attempts
            this.recordFailure('invalid_product', productId);
            throw new Error('Invalid product');
        }
        
        // Core logic
        const current = this.items.get(productId) || 0;
        this.items.set(productId, current + quantity);
        
        // SUCCESS_PHEROMONE: Strengthen this path
        this.recordPerformance('addItem', performance.now() - startTime);
        
        // INTEGRATION_SIGNAL: Notify inventory service
        this.emitCartUpdate('item_added', productId, quantity);
    }
    
    // AUTO_GENERATED: Performance summary (updates hourly)
    getPerformanceSummary() {
        /*
        LAST_1000_OPERATIONS:
        - addItem: avg=12ms, p99=45ms
        - removeItem: avg=8ms, p99=22ms
        - calculateTotal: avg=34ms, p99=89ms
        
        OPTIMIZATION_OPPORTUNITIES:
        - calculateTotal called repeatedly with same items
        - Consider memoization (estimated 60% reduction)
        */
    }
}
```

These implementation examples demonstrate the practical application of stigmergic principles in software development. The patterns show how environmental modifications can create self-organizing systems that reduce communication overhead while improving development efficiency and code quality.