# Playbook: Iterative Data Analysis for Complex Queries

**Purpose:** To guide AI agents in conducting tangible, data-driven analysis when initial queries return large or complex datasets, ensuring a structured, verifiable, and iterative approach.

**When to Use:**
*   When a Redshift query (or other data retrieval method) returns a substantial number of rows (e.g., > 50-100) that require detailed pattern identification, aggregation, or subset analysis to derive meaningful insights.
*   When a high-level conceptual review of a large dataset is insufficient to meet user requirements for data-driven progress.
*   When the analysis involves multiple potential hypotheses that need to be tested against different facets of the data.

**Core Principles:**
*   **Tangibility:** Prioritize concrete data manipulation and observation over purely conceptual reasoning.
*   **Modularity:** Break down complex analysis into smaller, manageable steps.
*   **Verifiability:** Ensure each step produces a clear, reviewable output.
*   **Iteration:** Allow for refinement of hypotheses and further focused investigation based on intermediate findings.
*   **Tool-Assistance:** Leverage available tools (file system operations, code execution, sequential thinking) to manage and execute the analysis.

**Workflow Steps:**

1.  **Initial Query & Data Persistence (Input: SQL Query):**
    *   Execute the primary data retrieval query using the appropriate tool (e.g., `mcp_redshift_mcp_execute_sql`).
    *   **Action:** Upon successful execution, immediately save the full raw results to a temporary, structured file within the workspace (e.g., `/Users/USERNAME/.digital_twin/temp/query_results_[timestamp_or_task_id].json` or `.csv`).
        *   *Tool (Ideal for Efficiency):* If available, use a specialized tool like `mcp_redshift_mcp_execute_sql_to_file` to save results directly from the database to a file on the server where the MCP runs. This avoids ingesting large datasets into the agent's context.
        *   *Tool (Alternative):* If direct-to-file is not available, ingest results via `mcp_redshift_mcp_execute_sql`, then use `mcp_desktop_commander_write_file` to persist.
        *   *Rationale:* Persists data, allows for offline/iterative analysis, and enables use of various data processing tools.
    *   Confirm file creation and briefly report a summary (e.g., number of rows retrieved, file path).

2.  **Handling Very Large Query Results (e.g., >100KB for `mcp_desktop_commander_read_file`):**
    *   **Challenge:** If the persisted query result file is too large for direct ingestion into the agent's context using tools like `mcp_desktop_commander_read_file`.
    *   **Preferred Strategy (If `execute_sql_to_file` was used):** The data is already persisted. Proceed to Step 3 (Iterative Segmental Analysis) using focused SQL queries for summarization/sampling if local file processing isn't feasible due to tool limitations for large file reads.
    *   **Alternative Strategy 1 (Focused SQL Summaries/Sampling):** If the goal is primarily summarization or identifying specific patterns that can be expressed in SQL, it's often more efficient to run further, more targeted SQL queries against the database to extract only the necessary aggregated data or specific sample rows, rather than attempting to process a very large local file without robust local code execution tools.
    *   **Alternative Strategy 2 (Server-Side File Splitting - Advanced/If Necessary):** If the full dataset *must* be processed locally (e.g., for complex non-SQL transformations) and is too large for a single read, and no server-side chunking/streaming tool is available directly via MCP: Consider using `mcp_desktop_commander_execute_command` to invoke system utilities (e.g., `split` on Linux/macOS, or PowerShell equivalents for Windows) to break the persisted large file (e.g., a large JSONL or CSV) into smaller, individually readable chunks. Then, iteratively read and process each chunk using `mcp_desktop_commander_read_file` and conceptual/Python-like logic. *Note: This approach adds significant complexity and should be a fallback.* 

3.  **High-Level Data Profiling (Input: Saved Data File - if readable, or via SQL against source):**
    *   **Action:** Perform a quick profiling of the dataset to understand its basic structure and dimensions.
        *   If the file is readable: Use `mcp_desktop_commander_read_file` (or part of it if it supports range reads and the initial segment is small enough).
        *   If the file is too large: Run simple SQL `COUNT(*)`, `SELECT DISTINCT` on key columns, or `SUM()`/`AVG()` on numerical columns directly against the source table(s) for the relevant query window.
        *   Identify key columns, data types, and potentially unique value counts for categorical fields or ranges for numerical fields.
    *   **Output:** Brief summary of data structure.

4.  **Iterative Segmental Analysis (Input: Saved Data File - if chunkable/readable, SQL queries, Analysis Plan):**
    *   **Action (Planning):** Based on the task objectives and initial data profile, outline a sub-plan for analyzing the data in focused segments or subsets. This sub-plan can be managed using `mcp_sequential_thinking_sequentialthinking`.
        *   Example Sub-Plan Thought: "Analyze 'Category X' items: Craft SQL to filter data for Category X, identify top 5 patterns in 'Field Y', calculate aggregate 'Value Z'."
    *   **Action (Execution per Segment):**
        *   **Filtering & Analysis (SQL-first approach for large data):** Prioritize crafting specific SQL queries (using `mcp_redshift_mcp_execute_sql` or similar) to perform filtering, aggregation, pattern identification directly on the database server.
            *   *Tool (Alternative for smaller, local files):* If data is chunked and locally readable, Python script execution via a code interpreter tool (if available) using Pandas, or conceptual analysis on samples.
        *   **Documentation:** For each segment analyzed, document:
            *   The SQL query or filtering criteria used.
            *   Concrete observations and patterns (e.g., "For 'Partially Settled (Review)' items where `recon_trans_type` is 'Check Row', SQL query aggregating by `is_perfectly_netted_at_installment` showed 100% are perfectly netted.").
            *   Illustrative examples (specific transaction IDs and relevant field values) obtained via targeted SQL `LIMIT` queries if needed.
            *   Save intermediate findings or summarized/aggregated data subsets from SQL to new temporary files if complex or for later synthesis, ideally using `mcp_redshift_mcp_execute_sql_to_file`.

5.  **Hypothesis Refinement & Further Investigation (Input: Segmental Findings):**
    *   **Action:** Review the findings from segmental analysis.
        *   Do the findings confirm or refute initial hypotheses?
        *   Do new patterns or questions emerge?
    *   If necessary, propose and (with permission) execute new, highly targeted SQL queries to explore these refined questions or newly identified patterns.
    *   Return to Step 1 (Data Persistence - ideally with `execute_sql_to_file`) for any new query results.

6.  **Synthesize Overall Conclusions (Input: All Segmental Findings & Supplemental Query Results):**
    *   **Action:** Consolidate all documented findings from the iterative analysis.
    *   Identify overarching themes, confirm primary root causes with supporting data examples, and quantify impacts where possible (e.g., "Carrier X accounts for Y% of aged payable value from June-Dec 2024 based on aggregated SQL results.").
    *   Update primary reports (e.g., root cause analysis document) with these data-driven conclusions, replacing or augmenting earlier conceptual findings.
        *   *Tool:* `mcp_desktop_commander_edit_block` or `default_api.edit_file`.

7.  **Clean Up (Optional):**
    *   Consider deleting temporary data files if no longer needed and workspace hygiene is a concern.
        *   *Tool:* `mcp_desktop_commander_delete_file` (if available and appropriate).

**Orchestration with `mcp_sequential_thinking_sequentialthinking`:**

*   **Main Task:** The overall user request can be the primary sequence of thoughts.
*   **Data Analysis as a Sub-Sequence:** A complex data analysis directive (like D1 in the Restricted Cash project) can itself become a series of thoughts within the main sequence. For instance:
    *   Thought X: "Begin D1: Root Cause Analysis. Plan to analyze 3 main categories. Total sub-thoughts for D1: ~15"
    *   Thought X.1: "Execute Query E3.D for detailed unsettled items (Jan-Mar 2025)."
    *   Thought X.2: "Save E3.D results to `/temp/e3d_results.json`."
    *   Thought X.3: "Analyze 'Partially Settled (Review)' items from `e3d_results.json`: Filter, identify netting patterns for first 20 items."
    *   Thought X.4: "Document initial findings for 'Partially Settled (Review)' items."
    *   ... and so on for other categories and analytical steps.

By following this playbook, AI agents can provide a more transparent, verifiable, and robustly data-driven analytical process, aligning better with user expectations for tangible progress on complex data tasks.
