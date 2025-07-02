# Pantheon Knowledge Management: Rules vs. Notepads Strategy

*Version: 1.0*
*Date: 2025-05-07* (Note: Will insert current date dynamically if possible, otherwise placeholder)

## 1. Purpose

This document outlines the strategy for managing knowledge artifacts within the Pantheon project, specifically defining the roles and best practices for Cursor Rules (`.cursor/rules/*.mdc`) and Cursor Notepads (`.cursor/notepads/*.notepad.md`). The goal is to ensure clarity, maintainability, discoverability, and effective context provision for both human developers and AI agents like Nexus.

This strategy is based on Cursor documentation, external research on knowledge management, and internal experience (e.g., refactoring of `stepwise-autonomy.mdc`).

## 2. Core Principles

*   **Hybrid Approach:** Leverage the strengths of both structured directives (Rules) and rich contextual documents (Notepads).
*   **Clarity & Conciseness:** Rules should be focused and direct; Notepads can be detailed but must be well-structured.
*   **Discoverability:** Use clear naming conventions and referencing (`@RuleName`, `@NotepadName`) to link related artifacts.
*   **Maintainability:** Keep artifacts updated, version-controlled (via Git), and modular. Regularly review and prune obsolete content.
*   **Target Audience:** Consider both AI agent consumption (clear instructions, structured data where possible) and human readability (Markdown formatting, explanations).

## 3. Cursor Rules (`.cursor/rules/*.mdc`)

### 3.1. Purpose & Scope

*   **Primary Use:** Define concise, actionable directives, constraints, guidelines, or automated triggers for AI behavior (Agent, Cmd-K). Encode standard procedures or project-specific requirements that the AI must follow or consider.
*   **Ideal Content:**
    *   High-level principles (e.g., security requirements, coding standards).
    *   Specific constraints (e.g., "Always use PEP8 formatting", "Default to America/New_York timezone").
    *   Checklists for processes (e.g., TDD steps, deployment verification).
    *   Metadata for triggering context (e.g., `globs` for file types).
    *   Brief templates or code snippets directly illustrating a standard.
    *   References (`@`) to more detailed Notepads or specific files.
*   **Format:** MDC (`.mdc`). Utilize metadata (`description`, `globs`, `alwaysApply`) for activation control and discoverability.
*   **Size Guideline:** Aim for conciseness, generally under 500 lines. If a rule becomes excessively long or contains extensive procedures, consider refactoring details into a Notepad.

### 3.2. Activation Types

*   **`Always`:** For fundamental, project-wide constraints (use sparingly).
*   **`Auto Attached`:** For context relevant to specific file types/paths (e.g., Python-specific rules for `*.py` files). Use `globs`.
*   **`Agent Requested`:** For optional guidance the AI can choose to fetch based on task relevance. Requires a clear `description`. Good for specialized workflows or less common standards.
*   **`Manual`:** For specific invocation via `@RuleName` when needed for a particular task.

### 3.3. Best Practices

*   Use descriptive filenames (e.g., `python-clean-code.mdc`, `sql-performance.mdc`).
*   Provide a clear `description` in the metadata for `Agent Requested` rules.
*   Keep the core directive clear and prominent.
*   Use Markdown for readability within the rule content.
*   Reference Notepads (`@NotepadName`) for detailed procedures, long examples, or extensive documentation rather than embedding them directly in the rule.
*   Regularly review Rules for relevance and accuracy.

## 4. Cursor Notepads (`.cursor/notepads/*.notepad.md`)

### 4.1. Purpose & Scope

*   **Primary Use:** Serve as repositories for detailed information, procedures, templates, playbooks, or context that is too extensive for a Rule. Act as reference documents that can be explicitly brought into context using `@NotepadName`.
*   **Ideal Content:**
    *   Detailed step-by-step procedures or workflows (e.g., debugging guides, complex refactoring steps).
    *   Extensive documentation (e.g., architecture overviews, deep dives into specific modules).
    *   Large templates or boilerplate code.
    *   Collections of related best practices or design patterns with detailed explanations/examples.
    *   Meeting summaries or research findings relevant to ongoing work.
    *   Content previously refactored out of overly long Rules.
*   **Format:** Markdown (`.notepad.md`). Supports standard Markdown formatting, code blocks, lists, etc. Can include file attachments.
*   **Size Guideline:** No strict line limit, but prioritize clear structure (headings, sections) for readability and potential partial referencing (though full Notepad context is currently added when referenced).

### 4.2. Best Practices

*   Use descriptive filenames (e.g., `pantheon-workflow-playbook.notepad.md`, `api-design-deep-dive.notepad.md`).
*   Structure content logically using Markdown headings (`#`, `##`, etc.). This aids human readability and may potentially allow future AI features to reference specific sections.
*   Include code examples, diagrams (as attachments or ASCII), and clear explanations.
*   Clearly state the purpose and scope at the beginning of the Notepad.
*   Keep content focused on a specific domain or workflow.
*   Reference relevant Rules (`@RuleName`) or other Notepads (`@OtherNotepad`) where applicable.
*   Regularly review and update content, especially procedures and documentation.
*   Consider using templates within Notepads for recurring tasks (e.g., task retrospective format).

## 5. Decision Framework: Rule vs. Notepad

| Feature / Need                     | Choose Rule (`.mdc`)                      | Choose Notepad (`.notepad.md`)          | Rationale                                                                 |
| :--------------------------------- | :---------------------------------------- | :-------------------------------------- | :------------------------------------------------------------------------ |
| **Primary Goal**                   | Direct AI behavior / Enforce constraint | Provide detailed context / Reference info | Rules guide actions, Notepads inform understanding.                       |
| **Content Length**                 | Concise (< 500 lines target)            | Detailed / Long-form acceptable         | Rules need to be quickly processed; Notepads are for deeper dives.        |
| **Content Type**                   | Directives, checklists, short examples  | Procedures, extensive docs, templates  | Match format strength to content type.                                    |
| **Activation**                     | Automatic (Always, Globs) or Manual     | Manual (`@NotepadName` reference)       | Rules offer more control over implicit context; Notepads are explicit.    |
| **Metadata Needs**                 | High (Description, Globs, AlwaysApply)  | Low (Filename is primary identifier)    | Rules rely on metadata for triggering and AI discovery.                   |
| **File Attachments**               | No                                        | Yes                                     | Notepads can bundle related artifacts (diagrams, specs).                  |
| **Referencing Detailed Procedures**| Reference `@NotepadName`                  | Define procedures directly              | Keep Rules lean by linking to detailed steps in Notepads.                 |

## 6. Example: Refactoring `stepwise-autonomy`

The refactoring of `@.cursor/rules/stepwise-autonomy.mdc` serves as a prime example:
*   **Rule (`stepwise-autonomy.mdc`):** Retained the core principles, requirements (decomposition, verification, tool use), validation checks, and *references* to specific complex procedures. Kept concise.
*   **Notepad (`pantheon-workflow-playbook.notepad.md`):** Created to house the *detailed procedures* for handling structured data files, ensuring filesystem stability, and Python script execution, which were too verbose for the Rule itself. The Rule now references `@pantheon-workflow-playbook.notepad.md`.

## 7. Future Considerations

*   Explore potential for section-level referencing within Notepads if Cursor enables it.
*   Develop templates for common Notepad types (e.g., Playbook, Architecture Overview).
*   Periodically review the effectiveness of this strategy and refine as needed.
