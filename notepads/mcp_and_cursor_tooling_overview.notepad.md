# MCP and Cursor Tooling Overview

**Version**: 1.0
**Last Updated**: 2025-05-13
**Steward**: Nexus (for Hamza Amjad)

## Introduction

This document provides a detailed overview and comparison of the AI agent tooling available within this workspace. It covers Cursor's native `default_api` tools, the `mcp_desktop_commander_*` suite, and other Model Context Protocol (MCP) servers configured in `/Users/USERNAME/.digital_twin/config.json` [SK_ConfigJson].

For concise, actionable guidance on tool selection for AI agents, refer to the rule: `@Rule:available_tooling_guide.mdc`.

This compendium aims to serve as a comprehensive reference to understand the capabilities, nuances, and strategic selection of these tools for various development and analytical tasks.

## I. Cursor Native Tools (`default_api`)

These tools are provided by the Cursor environment and are generally available for agent use. Their usage might be subject to platform limits (e.g., 25 tool calls per session, extendable) and a potential shift in costing model (unconfirmed as of 2025-05-13, `default_api` tools may no longer have extra costs, which could elevate their preference if capabilities are equivalent to alternatives).

| Tool (`default_api`) | Description                                                                 | Key Parameters & Notes                                                                                                                               |
| :------------------- | :-------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| `read_file`          | Reads file contents.                                                        | `target_file`, `start_line_one_indexed`, `end_line_one_indexed_inclusive`, `should_read_entire_file`. Max 750 lines (max mode) / 250 lines otherwise. |
| `list_dir`           | Lists directory structure.                                                  | `relative_workspace_path`.                                                                                                                           |
| `Codebase`           | Performs semantic searches within the indexed codebase.                     | `query`. Relies on codebase indexing.                                                                                                                |
| `grep_search`        | Searches for exact keywords or regex patterns within files.                 | `query`, `include_pattern`, `exclude_pattern`, `case_sensitive`.                                                                                     |
| `file_search`        | Finds files by name using fuzzy matching.                                   | `query`.                                                                                                                                             |
| `web_search`         | Generates search queries and performs web searches.                         | `search_term`.                                                                                                                                       |
| `fetch_rules`        | Retrieves specific `.mdc` rule definitions from the workspace.                | `rule_names`.                                                                                                                                        |
| `edit_file`          | Suggests and applies file edits. Can also create new files.                 | `target_file`, `code_edit`, `instructions`. For edits, use `// ... existing code ...` for unchanged parts.                                         |
| `reapply`            | Reapplies the last `edit_file` attempt if it wasn't satisfactory.           | `target_file`.                                                                                                                                       |
| `delete_file`        | Deletes files.                                                              | `target_file`.                                                                                                                                       |
| `run_terminal_cmd`   | Executes terminal commands and monitors output.                             | `command`, `is_background`.                                                                                                                          |

**Discussion on `default_api` Costing:**
If it's confirmed that `default_api` tools no longer incur additional costs, their utility for basic, common tasks increases significantly. However, specialized MCP tools may still be preferred for their advanced features, configurability, or specific integrations, even if `default_api` becomes "free."

## II. Desktop Commander MCP (`mcp_desktop_commander_*`)

This MCP server ([SK_DesktopCommanderRepo]) offers a comprehensive suite of tools for interacting with the operating system, including advanced file operations, terminal control, and search capabilities. It often provides more granular control and richer features than `default_api` equivalents.

| Tool (`mcp_desktop_commander_*`) | Description                                                                | Key Parameters & Notes                                                                                                                                                                      |
| :------------------------------- | :------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `get_config`                     | Gets the Desktop Commander server's own configuration.                      | `random_string`. Reveals `blockedCommands`, `defaultShell`, `allowedDirectories`, `fileReadLineLimit`, `fileWriteLineLimit`, etc.                                                                |
| `set_config_value`               | Sets specific Desktop Commander server configuration values.                 | `key`, `value`. Important for security and operational parameters. Modify with caution in a separate chat.                                                                              |
| `execute_command`                | Executes terminal commands with advanced control.                          | `command`, `shell` (optional), `timeout_ms` (optional). Supports output streaming, background execution, PID for session management.                                                          |
| `read_output`                    | Reads new output from a running terminal session.                          | `pid`. Used with `execute_command`.                                                                                                                                                         |
| `force_terminate`                | Force-terminates a running terminal session.                               | `pid`. Used with `execute_command`.                                                                                                                                                         |
| `list_sessions`                  | Lists all active terminal sessions.                                        | `random_string`.                                                                                                                                                                            |
| `list_processes`                 | Lists all running processes with details.                                  | `random_string`.                                                                                                                                                                            |
| `kill_process`                   | Terminates a running process by PID.                                       | `pid`.                                                                                                                                                                                      |
| `read_file`                      | Reads local files or content from URLs.                                    | `path`, `isUrl` (optional). Supports text & images (images rendered visually). Line-based pagination (`offset`, `length`). Configurable `fileReadLineLimit` (default 1000 lines).         |
| `read_multiple_files`            | Reads multiple files simultaneously.                                       | `paths`.                                                                                                                                                                                    |
| `write_file`                     | Writes file contents, with options for rewrite or append.                  | `path`, `content`, `mode` (`rewrite` or `append`). Configurable `fileWriteLineLimit` (default 50 lines). Best for full file writes.                                                           |
| `create_directory`               | Creates a new directory or ensures it exists.                              | `path`. Mandate absolute paths for reliability.                                                                                                                                             |
| `list_directory`                 | Gets a detailed listing of files and directories.                          | `path`. Provides `[FILE]` and `[DIR]` prefixes.                                                                                                                                             |
| `move_file`                      | Moves or renames files and directories.                                    | `source`, `destination`. Mandate absolute paths.                                                                                                                                            |
| `search_files`                   | Finds files by name using case-insensitive substring matching.             | `path`, `pattern`, `timeoutMs` (optional).                                                                                                                                                  |
| `search_code`                    | Searches for text/code patterns within file contents using `ripgrep`.        | `path`, `pattern`, `contextLines`, `filePattern`, `ignoreCase`, `includeHidden`, `maxResults`, `timeoutMs`. Powerful alternative to `default_api.grep_search`.                                |
| `get_file_info`                  | Retrieves detailed metadata about a file or directory.                     | `path`. Includes size, timestamps, permissions, type.                                                                                                                                       |
| `edit_block`                     | Applies surgical text replacements to files.                               | `file_path`, `old_string`, `new_string`, `expected_replacements` (optional). Best for small, focused changes (<20% of file). Provides character-level diff feedback. Use with precise `old_string`. |

## III. Other Configured MCP Servers (from `config.json` [SK_ConfigJson])

This workspace is configured with several other MCP servers, each providing specialized tools:

*   **`mcp_memory_*` Tools (via `memory` server)**
    *   **Purpose**: Manages a persistent knowledge graph for the agent.
    *   **Key Tools**: `mcp_memory_create_entities`, `mcp_memory_create_relations`, `mcp_memory_add_observations`, `mcp_memory_delete_entities`, `mcp_memory_delete_observations`, `mcp_memory_delete_relations`, `mcp_memory_read_graph`, `mcp_memory_search_nodes`, `mcp_memory_open_nodes`.
    *   **Use Case**: Storing, retrieving, and reasoning about structured information over time.

*   **`mcp_sequential_thinking_sequentialthinking` (via `sequential_thinking` server)**
    *   **Purpose**: Enables dynamic and reflective problem-solving through a structured thinking process.
    *   **Use Case**: Breaking down complex tasks, planning with revision, maintaining context over multiple analytical steps.

*   **`mcp_fetch` (via `fetch` server, `mcp-server-fetch`)**
    *   **Purpose**: Provides specialized web content fetching from a known URL, primarily focused on converting HTML to Markdown for easier LLM consumption. Supports chunked reading and configurable `robots.txt` handling and User-Agent.
    *   **Key Tool**: `fetch`
        *   `url` (string, required): URL to fetch.
        *   `max_length` (integer, optional, default: 5000): Max characters to return.
        *   `start_index` (integer, optional, default: 0): Character index to start content extraction (for chunking).
        *   `raw` (boolean, optional, default: false): If true, returns raw content without Markdown conversion.
    *   **Use Case**: Ideal for ingesting and processing textual content from specific web pages for analysis by an LLM. Differentiated from `default_api.web_search` (which is for discovery) and `mcp_desktop_commander_read_file` (which is more general for URLs, including image rendering, but lacks Markdown conversion and specific text processing features of `mcp-server-fetch`).

*   **`mcp_time_*` Tools (via `time` server)**
    *   **Purpose**: Provides time and timezone conversion capabilities.
    *   **Key Tools**: `mcp_time_get_current_time`, `mcp_time_convert_time`.
    *   **Use Case**: Getting current timestamps (defaulting to `America/New_York` as per user instructions), converting times between timezones.

*   **`mcp_chroma_*` Tools (via `chroma` server)**
    *   **Purpose**: Interacts with a Chroma vector database.
    *   **Key Tools**: `mcp_chroma_create_collection`, `mcp_chroma_add_documents`, `mcp_chroma_query_documents`, `mcp_chroma_delete_documents`, `mcp_chroma_list_collections`, `mcp_chroma_get_collection_info`, etc.
    *   **Use Case**: Vector similarity search, RAG, managing document embeddings.

*   **`mcp_perplexity-ask_*` Tools (via `perplexity-ask` server)**
    *   **Purpose**: Leverages Perplexity AI for research and reasoning.
    *   **Key Tools**: `mcp_perplexity-ask_perplexity_ask` (general queries), `mcp_perplexity-ask_perplexity_research` (deep research), `mcp_perplexity-ask_perplexity_reason` (reasoning tasks).
    *   **Use Case**: Advanced web research, answering complex questions with citations, performing reasoning over information.

*   **`mcp_context7` Tools (via `context7` server)**
    *   **Purpose**: Provides up-to-date, version-specific documentation and code examples for software libraries.
    *   **Key Tools**: `get-library-docs`, `resolve-library-id` (typically used implicitly via `use context7` in prompt).
    *   **Use Case**: Enhancing code generation and analysis by providing LLMs with current library information, reducing errors from outdated training data.

*   **`mcp_redshift_*` Tools (via `redshift_mcp` server)**
    *   **Purpose**: Interacts with a Redshift database.
    *   **Key Tools**: `mcp_redshift_mcp_execute_sql`, `mcp_redshift_mcp_execute_sql_to_file` (as per [SK_RedshiftMCPScript]).
    *   **Use Case**: Executing SQL queries against Redshift, retrieving data, saving results to files.

*   **Service-Specific MCPs (General Purpose)**:
    *   **`slack` (`@modelcontextprotocol/server-slack`)**: For Slack integration (e.g., sending messages, reading channels, notifications). Specific tool names depend on the server's schema.
    *   **`github` (`@modelcontextprotocol/server-github`)**: For GitHub integration (e.g., managing issues, PRs, repository information). Specific tool names depend on the server's schema.
    *   **`notionApi` (`@notionhq/notion-mcp-server`)**: For Notion integration (e.g., creating/updating pages, databases). Specific tool names depend on the server's schema.
    *   **`dbt_mcp`**: For dbt (Data Build Tool) integration (e.g., running models, tests, listing sources). Specific tool names depend on the server's schema (likely custom).

## IV. Tool Selection Strategy & Comparative Insights

Choosing the right tool involves considering the task, desired level of control, specific features needed, and overarching workspace guidelines (e.g., `@Rule:80-20-prioritization`, `@Rule:cursor-agent-integration`, `@Rule:stepwise-autonomy`).

**General Hierarchy of Preference:**

1.  **Highly Specialized MCP Tool**: If an MCP server offers a tool tailored precisely for the task with clear advantages (e.g., `mcp_context7` for library docs, `mcp_chroma_query_documents` for vector search, `mcp_desktop_commander_edit_block` for surgical edits), it's usually the best first choice.
2.  **`mcp_desktop_commander_*` for OS/File System**: For general file system operations, terminal execution, and robust local search, `mcp_desktop_commander` tools are often more feature-rich and configurable than `default_api` equivalents.
3.  **`default_api` Tools**: Serve as a versatile baseline, especially if the (unconfirmed) cost neutrality is factored in. Good for simpler tasks or when specialized features of MCPs aren't required.

**Comparative Table Snippets (Illustrative):**

| Feature/Task         | `default_api.read_file`                                  | `mcp_desktop_commander_read_file`                                                                 | Recommendation Context                                                                                                |
| :------------------- | :------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------- |
| **Read Local File**  | Basic read, line limits (250/750).                       | Advanced: pagination, configurable line limits (default 1000), image support.                                     | `mcp_desktop_commander` for full/large files, images. `default_api` for quick partial reads of text.                |
| **Read URL**         | Not directly supported. Use `web_search` then parse.     | Directly supported (`isUrl=True`), handles text & images.                                                         | `mcp_desktop_commander` for direct URL content retrieval.                                                             |
| **Terminal Command** | `run_terminal_cmd` (basic execution)                     | `execute_command` (timeout, shell choice, PID, background, session mgt with `read_output`/`force_terminate`)    | `mcp_desktop_commander` for complex/long-running commands or specific shell needs. `default_api` for simple commands. |
| **File Editing**     | `edit_file` (general purpose, new files, context edits)    | `edit_block` (surgical, diffs), `write_file` (full rewrite/append)                                              | `write_file` for new/full replacement. `edit_block` for precise small changes. `edit_file` for general edits.       |
| **Code Search**      | `grep_search` (basic regex), `Codebase` (semantic)         | `search_code` (ripgrep - powerful patterns, context lines)                                                        | `search_code` for advanced text/regex search. `Codebase` for semantic. `grep_search` for simpler patterns.          |

## V. Conclusion & Future Considerations

This tooling landscape is dynamic. As new MCP servers emerge or existing ones are updated (like the recent `execute_sql_to_file` for `redshift_mcp`), and as platform details like `default_api` costing evolve, this overview should be revisited.

The primary goal is to empower AI agents with the best possible tools for any given task, maximizing their efficiency, reliability, and capability within Hamza Amjad's digital twin environment.

--- 
*This document should be considered a living map, to be updated as new territories are discovered and existing pathways change.* 
