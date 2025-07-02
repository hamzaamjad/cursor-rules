# Pantheon Workflow Playbook

This notepad contains detailed procedural instructions and best practices for common development workflows within the Pantheon ecosystem. It is intended to be referenced by various Cursor Rules to provide more in-depth guidance.

## 1. Handling Complex Structured Data File Edits (e.g., YAML, JSON)

When partial edits to complex structured data files (e.g., YAML, JSON, intricate XML) using `edit_file` prove unreliable (e.g., resulting in malformed files or unintended content duplication/loss), adopt the following more robust **read-parse-modify-serialize-rewrite** strategy:

1.  **Read**: Use `mcp_desktop_commander_read_file` to read the entire file content.
    *Example*: `mcp_desktop_commander_read_file(path="/path/to/your/config.yaml")`
2.  **Parse**: Parse the content into an in-memory data structure.
    *   For YAML: Use `yaml.safe_load()` (requires `PyYAML` library).
    *   For JSON: Use `json.loads()`.
    *   *Note*: Ensure the execution environment has access to necessary parsing libraries.
3.  **Modify**: Programmatically modify the Python data structure (dictionary, list, etc.).
4.  **Serialize**: Serialize the modified data structure back into its string representation.
    *   For YAML: `yaml.dump()`
    *   For JSON: `json.dumps()`
5.  **Rewrite**: Use `mcp_desktop_commander_write_file` to write the entire new string content back to the file, overwriting it. This is generally safer than `edit_file` for entire content replacement.
    *Example*: `mcp_desktop_commander_write_file(path="/path/to/your/config.yaml", content=new_yaml_string)`

This pattern is the preferred method when high fidelity and structural integrity are critical for such files.

## 2. Ensuring File System Interaction Stability

When a workflow involves writing a file and then immediately reading or executing it with a separate tool or subprocess, stability issues (e.g., "file not found," access errors) can occur despite reported successful writes. This can be due to file system latencies, aggressive file watchers, or dispatch mechanisms.

**Verification Protocol:**

1.  **Explicit Check**: *Between the write and the subsequent read/execute operation*, explicitly verify file existence and accessibility using a simple, direct method:
    *   `mcp_desktop_commander_read_file(path="/abs/path/to/file")`: Attempting a quick read can confirm accessibility.
    *   Python one-liner via `run_terminal_cmd` or `mcp_desktop_commander_execute_command`:
        ```python
        # Command for run_terminal_cmd:
        # python3 -c "from pathlib import Path; p = Path('/abs/path/to/file'); print(p.exists() and p.is_file())"
        ```
2.  **Query for Background Processes**: Be aware of and, if issues persist, query the user about potential background processes (e.g., file watchers, dispatchers like `dispatch_bridge.py` in Pantheon) that might monitor and alter files in shared directories (e.g., dispatch queues). Such processes can cause files to be moved or deleted unexpectedly.

## 3. Python Script Execution Best Practices (Packaged Scripts)

For executing Python scripts that are part of a package structure (i.e., use relative imports like `from . import foo` or `from package import bar`):

1.  **Set CWD**: Ensure the Current Working Directory (CWD) for the execution command is set to the project's root directory (the one containing the top-level package directory).
    *   Example: If script is `/Users/user/project/my_package/module.py`, CWD should be `/Users/user/project/`.
    *   When using `run_terminal_cmd` or `mcp_desktop_commander_execute_command`, prefix with `cd /path/to/project_root && ...` if unsure about the shell's current state.
2.  **Execute as Module**: Execute the script as a module using `python3 -m package.module ...`.
    *   Example: `python3 -m my_package.module --arg1 value1`
    *   This ensures Python's import system can correctly resolve internal package paths.
3.  **Avoid Direct Path Execution**: Avoid direct execution like `python3 path/to/package/module.py` if it leads to `ModuleNotFoundError` for internal imports.

*Referenced from learnings in Transmutation Phase III.* 