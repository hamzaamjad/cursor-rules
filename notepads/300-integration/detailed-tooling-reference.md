# Detailed Tooling Reference

## Complete Tool Comparison Matrix

### File System Operations

| Task | MCP Desktop Commander | Default API | Recommendation |
|------|---------------------|-------------|----------------|
| **Create/Write File** | `write_file` - Supports URLs, images, chunking | `edit_file` - Basic text | MCP for advanced features |
| **Append to File** | `write_file` mode='append' | `edit_file` | MCP for explicit control |
| **Surgical Edit** | `edit_block` - Precise diffs, validation | `edit_file` - Context-aware | MCP for precision, API for context |
| **Read Full File** | `read_file` - URLs, images, pagination | `read_file` should_read_entire=True | MCP for URLs/images |
| **Read Partial** | `read_file` offset/length | `read_file` lines | API for simplicity |
| **List Directory** | `list_directory` - Detailed metadata | `list_dir` - Basic | MCP for details |
| **Create Directory** | `create_directory` | - | MCP only |
| **Move/Rename** | `move_file` | - | MCP only |
| **File Info** | `get_file_info` - Full metadata | - | MCP only |
| **Delete File** | - | `delete_file` | API only |

### Search Operations

| Task | Tool | Features | Use When |
|------|------|----------|----------|
| **Code Pattern Search** | `mcp_desktop_commander_search_code` | Ripgrep, regex, context lines | Complex patterns, performance |
| **Basic Grep** | `default_api.grep_search` | Simple patterns | Quick searches |
| **File Name Search** | `mcp_desktop_commander_search_files` | Fuzzy, timeout control | Finding files |
| **Semantic Search** | `default_api.Codebase` | Conceptual understanding | High-level queries |
| **Web Search** | `default_api.web_search` | General queries | Quick lookups |
| **Research** | `mcp_perplexity-ask` | Deep research, citations | Complex research |

### Process & Execution

| Task | Tool | Features | Use When |
|------|------|----------|----------|
| **Execute Command** | `mcp_desktop_commander_execute_command` | Timeout, session mgmt, shell selection | Complex scripts, long-running |
| **Simple Command** | `default_api.run_terminal_cmd` | Direct execution | One-shot commands |
| **List Processes** | `mcp_desktop_commander_list_processes` | PID, CPU, memory | System monitoring |
| **Kill Process** | `mcp_desktop_commander_kill_process` | By PID | Process management |
| **Session Management** | `read_output`, `force_terminate` | Persistent sessions | Interactive tasks |

### Specialized MCP Servers

#### GitHub Integration
- `create_repository` - Initialize repos
- `push_files` - Multi-file commits
- `create_issue` - Issue tracking
- `create_pull_request` - PR workflow
- `search_code` - Cross-repo search

#### Memory Management
- `create_entities` - Store concepts
- `create_relations` - Link entities
- `add_observations` - Update knowledge
- `search_nodes` - Query memory
- `read_graph` - Full knowledge view

#### API Integrations
- **Slack**: Message operations, channel management
- **Notion**: Page/database operations
- **Redshift**: SQL execution, data export
- **Context7**: Live library documentation
- **Chroma**: Vector database operations

### Tool Selection Decision Tree

```
Need to work with files?
├─ Creating new file?
│  ├─ From URL/with images? → mcp_desktop_commander_write_file
│  └─ Simple text? → Either tool works
├─ Editing existing file?
│  ├─ Precise small changes? → mcp_desktop_commander_edit_block
│  └─ Larger contextual edits? → default_api.edit_file
├─ Reading file?
│  ├─ From URL or image? → mcp_desktop_commander_read_file
│  ├─ Specific lines? → default_api.read_file
│  └─ Full file? → Either tool works
└─ File operations?
   ├─ Move/rename/info? → mcp_desktop_commander_*
   └─ Delete? → default_api.delete_file

Need to search?
├─ Code patterns/regex? → mcp_desktop_commander_search_code
├─ Simple text search? → default_api.grep_search
├─ Conceptual search? → default_api.Codebase
└─ Web search?
   ├─ Quick lookup? → default_api.web_search
   └─ Deep research? → mcp_perplexity-ask

Need to execute?
├─ Complex/long-running? → mcp_desktop_commander_execute_command
├─ Simple one-shot? → default_api.run_terminal_cmd
└─ Process management? → mcp_desktop_commander_*_process
```

### Performance Considerations

1. **Latency**: MCP tools may have additional overhead
2. **Features**: MCP tools often provide richer functionality
3. **Reliability**: Default API tools are battle-tested
4. **Cost**: Check current pricing for default_api usage

### Best Practices

1. **Absolute Paths**: Always use full paths with MCP tools
2. **Error Handling**: Verify operations, check exit codes
3. **Batching**: Group related operations when possible
4. **Tool Limits**: Monitor 25-call session limit for default_api
5. **Fallbacks**: Have alternative approaches ready

### Integration Patterns

```python
# Example: Robust file editing with verification
def safe_edit_file(path, old_content, new_content):
    # Try precise edit first
    try:
        result = mcp_desktop_commander_edit_block(
            file_path=path,
            old_string=old_content,
            new_string=new_content
        )
        if result.success:
            return True
    except:
        pass
    
    # Fallback to full rewrite
    return mcp_desktop_commander_write_file(
        path=path,
        content=new_content,
        mode='rewrite'
    )
```

### Version Compatibility

- Desktop Commander: v0.6.0+
- Default API: Cursor 0.40.0+
- Context7: Latest
- Perplexity: Pro features required

### Troubleshooting

| Issue | Solution |
|-------|----------|
| MCP timeout | Increase timeout_ms parameter |
| File not found | Use absolute paths |
| Permission denied | Check file permissions |
| Tool limit reached | Reset session or use MCP alternatives |
| Encoding issues | Specify UTF-8 explicitly |