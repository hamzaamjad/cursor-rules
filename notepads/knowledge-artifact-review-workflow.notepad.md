# Workflow: Knowledge Artifact Review & Refinement (Rules/Notepads)

*Version: 1.0*
*Date: 2025-05-07* (Placeholder - Current Date)

## 1. Purpose

This document outlines the standard procedure for periodically reviewing and refining the Cursor Rules (`.cursor/rules/*.mdc`) and Notepads (`.cursor/notepads/*.notepad.md`) within the Pantheon project. The goal is to ensure alignment with the established strategy, maintain quality, remove redundancy, and adapt to evolving best practices or project needs.

## 2. Trigger

This workflow should be triggered periodically (e.g., quarterly) or when significant changes to Cursor features, project structure, or common operational patterns warrant a review.

## 3. Workflow Steps

1.  **Recall Strategy:**
    *   **Action:** Read and internalize the current strategy defined in `@.cursor/notepads/pantheon-knowledge-management.notepad.md`.
    *   **Purpose:** Refresh understanding of the criteria for Rules vs. Notepads.

2.  **Check for Updates:**
    *   **Action (Manual/Tool):** Review official Cursor documentation for Rules and Notepads. Check for new features, format changes, or updated best practices.
    *   **Tool:** `mcp_desktop_commander_read_file` with `isUrl=True` for `https://docs.cursor.com/context/rules` and `https://docs.cursor.com/beta/notepads`.
    *   **Purpose:** Ensure the internal strategy aligns with current external guidance.
    *   **(Optional) External Research:** If significant changes are suspected or specific issues arise, conduct targeted external research using `@.cursor/rules/perplexity-research-framework.mdc` and `@.cursor/notepads/perplexity-research-framework-details.notepad.md`.

3.  **Inventory Current Artifacts:**
    *   **Action:** List files in `.cursor/rules/` and `.cursor/notepads/`.
    *   **Tool:** `mcp_desktop_commander_list_directory`.
    *   **Purpose:** Get a complete overview of existing artifacts.

4.  **Review Artifacts Against Strategy:**
    *   **Action:** For each Rule (`.mdc`) and Notepad (`.notepad.md`):
        *   Assess alignment with its defined purpose (Rule = directive/constraint; Notepad = context/procedure).
        *   Check Rule conciseness (target < 500 lines).
        *   Verify Notepads use appropriate Markdown structure.
        *   Identify any `.md` (or other non-`.notepad.md`) files in `/notepads` that should be standardized.
        *   Read the content of files that seem misaligned, overly long, potentially redundant, or unclear based on filename.
    *   **Tool:** `mcp_desktop_commander_read_multiple_files` or `mcp_desktop_commander_read_file`.
    *   **Purpose:** Identify specific items needing changes.

5.  **Identify Discrepancies & Redundancy:**
    *   **Action:** Compile a list of issues identified in Step 4. Look for:
        *   Rules containing overly detailed procedures.
        *   Notepads containing only simple directives suitable for a Rule.
        *   Redundant content across multiple files (e.g., similar frameworks in both a Rule and Notepad).
        *   Files in `/notepads` not ending in `.notepad.md`.
        *   Outdated information or references.
    *   **Purpose:** Create a clear list of problems to address.

6.  **Formulate Proposed Changes:**
    *   **Action:** For each identified issue, propose a specific action (Rename, Refactor, Consolidate, Delete, Create). Justify each proposal based on the strategy in `@.cursor/notepads/pantheon-knowledge-management.notepad.md`.
    *   **Purpose:** Define a clear plan for improvement.

7.  **Execute Low-Risk Changes:**
    *   **Action:** Execute changes deemed high-confidence and low-risk (e.g., renaming files to `.notepad.md`, creating new artifacts based on clear definitions, simple refactors).
    *   **Tools:** `mcp_desktop_commander_write_file`, `mcp_desktop_commander_move_file`, `edit_file` (with caution, fallback to write_file if edits fail).
    *   **Verification:** Verify each change (e.g., list directory after move, read file after write/edit).
    *   **Purpose:** Implement straightforward improvements efficiently.

8.  **Address Complex Changes (If Any):**
    *   **Action:** For more complex refactoring or consolidation, break down into smaller, verifiable steps following `@.cursor/rules/stepwise-autonomy.mdc`. This might involve creating temporary files, detailed diffs, or more careful editing.
    *   **Purpose:** Handle complex updates methodically.

9.  **Commit & Push Changes:**
    *   **Action:** Add, commit, and push all changes to the appropriate Git branch (create a new one if necessary), following the workflow documented in `@.cursor/notepads/git-workflow-feature-branch.notepad.md`.
    *   **Tools:** `run_terminal_cmd` (for `git add`, `git commit`, `git push`, `git checkout -b`).
    *   **Purpose:** Persist the improvements in version control.

10. **Log & Update Memory:**
    *   **Action:** Create or update a record in shared memory (`pantheon/memory/shared/`) summarizing the review, changes made, and any pending actions.
    *   **Tool:** `mcp_desktop_commander_write_file`.
    *   **Purpose:** Maintain a historical record of knowledge management efforts.

## 4. Key Tools

*   `mcp_desktop_commander` (list_directory, read_file, write_file, move_file)
*   `run_terminal_cmd` (for Git operations)
*   `mcp_perplexity-ask` (optional research)
*   `edit_file` (optional, for simple edits)

## 5. References

*   `@.cursor/notepads/pantheon-knowledge-management.notepad.md` (Core Strategy)
*   `@.cursor/notepads/git-workflow-feature-branch.notepad.md` (Git Workflow)
*   `@.cursor/rules/stepwise-autonomy.mdc` (Complex Task Execution)
*   `@.cursor/rules/perplexity-research-framework.mdc` (Research Guidance)
