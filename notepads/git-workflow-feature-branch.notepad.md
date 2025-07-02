# Git Workflow: Feature Branch Creation & Push

*Version: 1.1*
*Date: 2025-05-19* (Updated for workflow resilience and clarity)

## 1. Purpose

This document outlines the standard procedure and best practices for creating a new feature branch from the current working state, committing changes, and pushing the branch to the remote repository (`origin`). This ensures work is isolated and integrates smoothly.

## 2. Workflow Steps

1.  **Check Status (`git status | cat`)**
    *   **Action:** `git status | cat`
    *   **Purpose:** Understand the current state of the repository (modified, new, deleted files) before proceeding. Identify any unexpected changes. Use `| cat` for compatibility with non-interactive terminals.
    *   **Verification:** Review the output to confirm it reflects the expected changes.
    *   **Note:** If you see a warning about uncommitted changes (especially submodules or ignored files), explicitly review and decide whether to stage, commit, or ignore them before proceeding.

2.  **Stage Changes (`git add .` or `git add <file1> <file2>...`)**
    *   **Action:** `git add .` (to stage all changes) or specify files.
    *   **Purpose:** Prepare the desired changes for commit. Using `.` is convenient but ensure only intended changes are present (review `git status` first).
    *   **Verification:** Run `git status | cat` again to see staged changes.

3.  **Commit Changes (`git commit -m "..."`)**
    *   **Action:** `git commit -m "type: Short descriptive title"`
    *   **Purpose:** Record the staged changes to the local repository history.
    *   **Best Practice (Message):**
        *   Use Conventional Commits format (e.g., `feat:`, `fix:`, `refactor:`, `docs:`, `chore:`).
        *   Keep the message concise and descriptive of the change.
        *   **Tool Constraint:** When using `run_terminal_cmd`, the commit message *must* be a single line (no newlines). For multi-line messages, alternative methods or tools might be needed.
    *   **Verification:** Command should execute successfully. `git log -n 1` can show the latest commit.

4.  **Create & Switch to New Branch (`git checkout -b ...`)**
    *   **Action:** `git checkout -b <branch-name>`
    *   **Purpose:** Create a new branch based on the current commit and switch the working directory to it. Isolates new development.
    *   **Best Practice (Naming):** Use descriptive names, often prefixed (e.g., `feat/knowledge-mgmt`, `fix/auth-bug`, `refactor/api-error-handling`).
    *   **Verification:** Command output confirms switch to the new branch. `git branch` shows the new branch highlighted.
    *   **Proactive Branch Deletion Handling:** If you need to delete a branch, always check if it is the current branch. Switch to another branch (e.g., `master` or `main`) before deleting to avoid errors.

5.  **Push New Branch to Remote (`git push -u origin ...`)**
    *   **Action:** `git push -u origin <branch-name>`
    *   **Purpose:** Publish the new local branch to the remote repository (`origin`) and set up upstream tracking (`-u`). This allows future `git push` and `git pull` commands on this branch to work without specifying origin/branch.
    *   **Verification:** Command output should show the branch successfully pushed and tracking set up.

6.  **(Optional) Add PR Labels via CLI**
    *   **Action:** `gh pr edit <number> --add-label "label-name"`
    *   **Label Existence Check:** Before adding a label, check if it exists in the repository. If not, create it via the GitHub UI/CLI, or notify the reviewer to add it. If label addition fails, update the PR body to indicate readiness or status as a fallback.

7.  **(Optional) Review Uncommitted Changes Warning**
    *   **Action:** If you see a warning about uncommitted changes (especially submodules or ignored files) during PR creation, explicitly review these changes. Decide whether to stage, commit, or ignore them before proceeding to avoid confusion or missed content.

8.  **(Optional) Summarize Long Command Outputs**
    *   **Action:** For lengthy command outputs (e.g., `git pull`, `git log`), summarize the most relevant changes or actions for clarity in documentation or communication.

## 3. Key Considerations & Best Practices

*   **Directory Context:** Ensure all git commands are run from the correct directory (usually the workspace root). Use `cd /path/to/workspace_root && git ...` if unsure about the current shell's working directory.
*   **Tool Limitations:** Be aware of constraints like the single-line commit message for `run_terminal_cmd`.
*   **Error Handling:** If any step fails (e.g., commit message format error, push conflicts), diagnose the error message and take corrective action before proceeding.
*   **Conventional Commits:** Adhering to this standard improves history readability and enables automated changelog generation.
*   **Atomic Commits:** Aim for commits that represent a single logical change. Stage files selectively if needed.
*   **Uncommitted Changes Warning:** If you see a warning about uncommitted changes during PR creation, review and address them before proceeding to avoid confusion or missed content.
*   **Output Summarization:** For lengthy command outputs, summarize the most relevant changes or actions for clarity.

## 4. Example Scenario (This Session)

*   **Goal:** Create a new branch for knowledge management strategy work.
*   **Steps:**
    *   `git status | cat` (Verified changes: new strategy notepad, renamed notepads)
    *   `git add .` (Staged all changes)
    *   `git commit -m "feat: Implement Rule/Notepad strategy and align artifacts"` (Committed changes - initially failed due to newline, retried with single line)
    *   `git checkout -b feat/knowledge-mgmt-strategy` (Created and switched branch)
    *   `git push -u origin feat/knowledge-mgmt-strategy` (Published branch)
    *   (Optional) `gh pr edit <number> --add-label "ready-for-review"` (If label exists, otherwise update PR body)
