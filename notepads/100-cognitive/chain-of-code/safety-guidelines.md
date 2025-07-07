# Safety Guidelines for Chain of Code

## Execution Sandboxing

### Core Safety Principles
1. **No filesystem access**: Block all file I/O operations
2. **No network calls**: Prevent external connections
3. **Resource limits**: Cap CPU, memory, and time
4. **Namespace isolation**: Restricted execution environment

### Python Sandbox Implementation
```python
import ast
import sys
import resource
import signal

class SafeExecutor:
    """Secure code execution environment"""
    
    BANNED_IMPORTS = {
        'os', 'sys', 'subprocess', 'socket', 'requests',
        'urllib', 'pathlib', 'shutil', '__builtins__'
    }
    
    BANNED_FUNCTIONS = {
        'eval', 'exec', 'compile', '__import__',
        'open', 'input', 'file'
    }
    
    def __init__(self, time_limit=5, memory_limit_mb=100):
        self.time_limit = time_limit
        self.memory_limit_mb = memory_limit_mb
    
    def validate_code(self, code_string):
        """Static analysis for dangerous patterns"""
        try:
            tree = ast.parse(code_string)
        except SyntaxError as e:
            return False, f"Syntax error: {e}"
        
        for node in ast.walk(tree):
            # Check imports
            if isinstance(node, ast.Import):
                for name in node.names:
                    if name.name.split('.')[0] in self.BANNED_IMPORTS:
                        return False, f"Forbidden import: {name.name}"
            
            # Check function calls
            if isinstance(node, ast.Name) and node.id in self.BANNED_FUNCTIONS:
                return False, f"Forbidden function: {node.id}"
        
        return True, "Code validated"
    
    def execute_safe(self, code_string):
        """Execute code with safety constraints"""
        # Validate first
        valid, msg = self.validate_code(code_string)
        if not valid:
            return {'error': msg, 'safe': False}
        
        # Set resource limits
        resource.setrlimit(resource.RLIMIT_CPU, (self.time_limit, self.time_limit))
        resource.setrlimit(resource.RLIMIT_AS, 
                         (self.memory_limit_mb * 1024 * 1024, -1))
        
        # Create restricted namespace
        safe_globals = {
            '__builtins__': {
                'len': len, 'range': range, 'str': str, 'int': int,
                'float': float, 'list': list, 'dict': dict, 'set': set,
                'sum': sum, 'min': min, 'max': max, 'abs': abs,
                'round': round, 'sorted': sorted, 'enumerate': enumerate,
                'zip': zip, 'map': map, 'filter': filter, 'print': print
            },
            'math': __import__('math'),
            'datetime': __import__('datetime'),
            'json': __import__('json'),
            're': __import__('re')
        }
        
        try:
            exec(code_string, safe_globals)
            return {
                'result': safe_globals.get('result', 'No result variable'),
                'safe': True
            }
        except Exception as e:
            return {'error': str(e), 'safe': True}
```

### JavaScript Sandbox
```javascript
// Browser-based sandboxing with Web Workers
class SafeJSExecutor {
    constructor(timeLimit = 5000, memoryLimit = 100) {
        this.timeLimit = timeLimit;
        this.memoryLimit = memoryLimit;
    }
    
    async executeInWorker(code) {
        // Create sandboxed worker
        const workerCode = `
            // Remove dangerous globals
            self.XMLHttpRequest = undefined;
            self.fetch = undefined;
            self.WebSocket = undefined;
            self.importScripts = undefined;
            
            // Execute user code
            try {
                ${code}
                self.postMessage({success: true, result: result});
            } catch (e) {
                self.postMessage({success: false, error: e.message});
            }
        `;
        
        const blob = new Blob([workerCode], {type: 'application/javascript'});
        const worker = new Worker(URL.createObjectURL(blob));
        
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                worker.terminate();
                reject(new Error('Execution timeout'));
            }, this.timeLimit);
            
            worker.onmessage = (e) => {
                clearTimeout(timeout);
                worker.terminate();
                resolve(e.data);
            };
            
            worker.onerror = (e) => {
                clearTimeout(timeout);
                worker.terminate();
                reject(e);
            };
        });
    }
}
```

## Input Validation

### Type Safety
```python
def validate_numeric_input(value, min_val=None, max_val=None):
    """Ensure numeric inputs are within safe bounds"""
    try:
        num = float(value)
        if math.isnan(num) or math.isinf(num):
            raise ValueError("Invalid numeric value")
        if min_val is not None and num < min_val:
            raise ValueError(f"Value below minimum: {min_val}")
        if max_val is not None and num > max_val:
            raise ValueError(f"Value above maximum: {max_val}")
        return num
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid input: {e}")
```

### Size Limits
```python
MAX_ARRAY_SIZE = 10000
MAX_STRING_LENGTH = 100000
MAX_RECURSION_DEPTH = 100

def validate_data_size(data):
    """Prevent memory exhaustion attacks"""
    if isinstance(data, (list, tuple)):
        if len(data) > MAX_ARRAY_SIZE:
            raise ValueError(f"Array too large: {len(data)} > {MAX_ARRAY_SIZE}")
    elif isinstance(data, str):
        if len(data) > MAX_STRING_LENGTH:
            raise ValueError(f"String too long: {len(data)} > {MAX_STRING_LENGTH}")
    elif isinstance(data, dict):
        if len(data) > MAX_ARRAY_SIZE:
            raise ValueError(f"Dictionary too large: {len(data)} > {MAX_ARRAY_SIZE}")
```

## Error Handling

### Safe Error Messages
```python
def sanitize_error_message(error):
    """Remove sensitive information from errors"""
    # Don't expose system paths
    error_str = str(error)
    error_str = re.sub(r'/[\w/]+/', '<path>/', error_str)
    
    # Don't expose internal state
    error_str = re.sub(r'at 0x[\w]+', 'at <address>', error_str)
    
    # Limit length
    if len(error_str) > 200:
        error_str = error_str[:200] + '...[truncated]'
    
    return error_str
```

### Graceful Failure
```python
def safe_execution_wrapper(func):
    """Decorator for safe function execution"""
    def wrapper(*args, **kwargs):
        try:
            # Set alarm for timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)  # 5 second timeout
            
            result = func(*args, **kwargs)
            signal.alarm(0)  # Cancel alarm
            
            return {'success': True, 'result': result}
            
        except MemoryError:
            return {'success': False, 'error': 'Memory limit exceeded'}
        except RecursionError:
            return {'success': False, 'error': 'Maximum recursion depth exceeded'}
        except Exception as e:
            return {'success': False, 'error': sanitize_error_message(e)}
        finally:
            signal.alarm(0)
    
    return wrapper
```

## Resource Monitoring

### Memory Tracking
```python
import tracemalloc

class MemoryMonitor:
    def __init__(self, limit_mb=100):
        self.limit_bytes = limit_mb * 1024 * 1024
        tracemalloc.start()
    
    def check_memory(self):
        current, peak = tracemalloc.get_traced_memory()
        if current > self.limit_bytes:
            raise MemoryError(f"Memory usage exceeded: {current / 1024 / 1024:.1f}MB")
        return current
    
    def get_usage_report(self):
        current, peak = tracemalloc.get_traced_memory()
        return {
            'current_mb': current / 1024 / 1024,
            'peak_mb': peak / 1024 / 1024,
            'limit_mb': self.limit_bytes / 1024 / 1024
        }
```

### CPU Usage Control
```python
import time
import threading

class CPULimiter:
    def __init__(self, max_cpu_percent=50):
        self.max_cpu_percent = max_cpu_percent
        self.active = False
    
    def limit_cpu(self, func, *args, **kwargs):
        """Execute function with CPU throttling"""
        work_time = self.max_cpu_percent / 100
        sleep_time = (100 - self.max_cpu_percent) / 100
        
        def throttled_execution():
            start = time.time()
            while self.active:
                # Work phase
                work_start = time.time()
                func(*args, **kwargs)
                work_duration = time.time() - work_start
                
                # Sleep phase
                if work_duration < work_time:
                    time.sleep(sleep_time)
        
        self.active = True
        thread = threading.Thread(target=throttled_execution)
        thread.start()
        
        return thread
```

## Security Checklist

### Pre-execution Validation
- [ ] Code parsed successfully
- [ ] No forbidden imports detected
- [ ] No dangerous function calls
- [ ] Input sizes within limits
- [ ] Numeric values in valid ranges

### Runtime Protection
- [ ] Execution timeout configured
- [ ] Memory limits enforced
- [ ] CPU usage monitored
- [ ] Network access blocked
- [ ] File system access prevented

### Post-execution Cleanup
- [ ] Worker processes terminated
- [ ] Temporary resources freed
- [ ] Memory usage reset
- [ ] Error messages sanitized
- [ ] Results validated

## Common Attack Vectors

### Denial of Service
```python
# Attack: Infinite loop
while True: pass  # Prevented by timeout

# Attack: Memory exhaustion
x = [0] * 10**10  # Prevented by memory limits

# Attack: Fork bomb
import os
while True: os.fork()  # Prevented by import blocking
```

### Information Disclosure
```python
# Attack: File system probe
import os
os.listdir('/')  # Blocked by import restrictions

# Attack: Network scanning
import socket
socket.gethostbyname('example.com')  # Blocked by import restrictions
```

## Best Practices

1. **Principle of Least Privilege**: Only allow necessary operations
2. **Defense in Depth**: Multiple layers of protection
3. **Fail Secure**: Errors should result in denied access
4. **Regular Updates**: Keep security measures current
5. **Monitoring**: Log and analyze execution patterns

## Emergency Response

### Kill Switch Implementation
```python
class EmergencyStop:
    def __init__(self):
        self.emergency = False
    
    def trigger(self):
        """Emergency stop all executions"""
        self.emergency = True
        # Kill all worker processes
        os.system("pkill -f 'worker_process'")
        # Clear execution queue
        execution_queue.clear()
        # Log incident
        logger.critical("Emergency stop triggered")
```

### Incident Logging
```python
def log_security_event(event_type, details):
    """Log security-relevant events"""
    event = {
        'timestamp': datetime.now().isoformat(),
        'type': event_type,
        'details': details,
        'severity': get_severity(event_type)
    }
    
    # Log to secure location
    with open('/var/log/chain_of_code_security.log', 'a') as f:
        f.write(json.dumps(event) + '\n')
    
    # Alert if critical
    if event['severity'] == 'critical':
        send_security_alert(event)
```
