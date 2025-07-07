# Implementation Patterns for Stepwise Autonomy

## Pattern Overview
This guide provides concrete implementation patterns for applying stepwise autonomy across various task complexity levels.

## Simple Task Patterns

### Direct Execution Pattern
```python
def handle_simple_task(task):
    """Minimal overhead for predictable operations"""
    # 1. Quick validation
    if not validate_inputs(task):
        return error_response("Invalid inputs")
    
    # 2. Direct execution
    result = execute_operation(task)
    
    # 3. Basic verification
    if verify_result(result):
        return success_response(result)
    else:
        return retry_once(task)
```

### Single-Step Operations
- File formatting
- Variable renaming
- Simple calculations
- Direct API calls with known parameters

## Moderate Task Patterns

### Staged Execution Pattern
```python
def handle_moderate_task(task):
    """Structured approach with checkpoints"""
    plan = create_execution_plan(task)
    
    for stage in plan.stages:
        # Execute stage
        result = execute_stage(stage)
        
        # Verify before proceeding
        if not verify_stage_result(result):
            plan = adapt_plan(plan, stage, result)
        
        # Update progress
        update_task_progress(task, stage)
    
    return compile_results(plan)
```

### Multi-Step Workflows
- Feature implementation across 2-3 files
- Database migrations with validation
- API integration with error handling
- Refactoring with test coverage

## Complex Task Patterns

### Tree of Thoughts Pattern
```python
def handle_complex_task(task):
    """Multi-path exploration for high-stakes operations"""
    # Generate solution paths
    paths = generate_solution_paths(task, count=5)
    
    # Evaluate each path
    evaluations = []
    for path in paths:
        score = evaluate_path_promise(path)
        evaluations.append((score, path))
    
    # Select best path
    best_path = max(evaluations, key=lambda x: x[0])[1]
    
    # Execute with comprehensive verification
    return execute_with_rollback(best_path)
```

### Cross-System Coordination
- Microservice deployments
- Data pipeline modifications
- Infrastructure changes
- Security updates

## Error Recovery Patterns

### Graceful Degradation
```python
def recover_from_error(error, context):
    """Systematic error recovery"""
    if error.type == "network":
        return retry_with_backoff(context, max_attempts=3)
    elif error.type == "validation":
        return request_clarification(context)
    elif error.type == "resource":
        return try_alternative_approach(context)
    else:
        return escalate_to_user(error, context)
```

### Rollback Strategies
- Checkpoint-based recovery
- Transaction-style operations
- State preservation techniques
- Partial success handling

## Tool Usage Patterns

### MCP Service Selection
```python
def select_optimal_tool(operation):
    """Choose the best tool for the job"""
    if operation.type == "documentation":
        return use_context7_mcp()
    elif operation.type == "research":
        return use_perplexity_mcp()
    elif operation.type == "file_operation":
        return use_desktop_commander()
    else:
        return use_default_api()
```

### Tool Composition
- Sequential tool chains
- Parallel tool execution
- Fallback tool strategies
- Tool result aggregation

## Verification Patterns

### Multi-Level Verification
```python
def verify_implementation(result, requirements):
    """Comprehensive verification strategy"""
    checks = [
        syntax_validation(result),
        logic_verification(result, requirements),
        integration_testing(result),
        performance_validation(result)
    ]
    
    return all(checks) and user_acceptance_test(result)
```

### Verification Depth by Complexity
- **Simple**: Syntax check only
- **Moderate**: Syntax + unit tests
- **Complex**: Full test suite + integration

## Performance Optimization

### Token Efficiency
```python
def optimize_token_usage(task):
    """Minimize token consumption"""
    # Use context trimming for large inputs
    if estimate_tokens(task) > THRESHOLD:
        task = apply_context_trimming(task)
    
    # Batch similar operations
    if has_repetitive_operations(task):
        task = batch_operations(task)
    
    return task
```

### Processing Optimization
- Early termination conditions
- Cached result reuse
- Parallel processing where safe
- Progressive enhancement

## Best Practices

1. **Always verify assumptions** before execution
2. **Maintain clear audit trails** for complex tasks
3. **Prefer explicit over implicit** in all operations
4. **Design for failure** with recovery strategies
5. **Measure and optimize** based on actual performance

## Common Pitfalls

- Over-engineering simple tasks
- Under-verifying complex operations
- Ignoring edge cases in moderate tasks
- Assuming tool availability without checking
- Neglecting user communication needs
