# Workflow: Example Library Contribution Review

**Version**: 1.0
**Date**: 2025-05-10
**Steward**: Nexus

## 1. Purpose

This document outlines the standard procedure for reviewing and ensuring the quality of new examples and significant modifications to existing examples within the `knowledge_base/prompts/meta_prompting_system/example_library/by_task_type/` directory. The goal is to maintain a high-quality, consistent, and effective library for the Dynamic Example Injection Mechanism (DEIM).

## 2. Scope

This workflow applies to all new example submissions and substantial updates to examples in the DEIM library.

## 3. Trigger

*   A new example is proposed for inclusion in the library.
*   An existing example undergoes significant changes to its content, structure, or metadata.

## 4. Roles

*   **Contributor**: The individual creating or modifying an example.
*   **Reviewer(s)**: One or two peers assigned or volunteering to review the contribution.

## 5. Review Workflow Steps

### Step 1: Contributor Preparation

The Contributor is responsible for ensuring the example artifact (the collection of files within its unique directory) meets the following criteria *before* submitting for review:

1.  **Adherence to Design Principles**: The example content (`input.txt`, `output.txt`, `process_guidance.md`, `few_shot_examples.md`) aligns with the guidelines in `@knowledge_base/prompts/meta_prompting_system/dynamic_example_injection_mechanism/research_and_design_notes/few_shot_example_design_principles_v1.md`.
2.  **Structural Correctness**: The example's directory and file structure conform to `@knowledge_base/prompts/meta_prompting_system/example_library/by_task_type/README.md`.
    *   Unique example directory name using `snake_case_with_descriptive_name_and_sequential_id` under the appropriate task type category.
    *   Presence of `description.md`, `input.txt`, `output.txt`, and `metadata.json`.
    *   Correct use of optional files like `process_guidance.md` and `few_shot_examples.md`.
3.  **Metadata Integrity (`metadata.json`)**:
    *   The `metadata.json` file must be valid JSON.
    *   Its structure must mirror that of a single item within the `examples` array of the `@knowledge_base/prompts/meta_prompting_system/schemas/master_prompt_schema_v8.json`. This means it should have top-level keys like `id`, `type`, and a **nested `example_metadata` object**.
    *   The fields *within* the nested `example_metadata` object should align with those defined in `@knowledge_base/prompts/meta_prompting_system/example_library/schemas/example_metadata_schema_v1.json` (e.g., `difficulty`, `tests_concept`, `language`, `task_type_tags`, `domain_tags`, `complexity_level`, all descriptions, keywords, version, and dates).
    *   All required fields must be present and accurately populated.
4.  **Self-Review**: The Contributor performs a self-review for clarity, accuracy of content (input, output, guidance), correctness of metadata, and overall completeness.
5.  **(Recommended) Selector Test**: Optionally, the Contributor can test if the example is discoverable by the `@knowledge_base/prompts/meta_prompting_system/dynamic_example_injection_mechanism/selection_logic/v1_example_selector.py` script using plausible `required_example_characteristics` that should match the new example's metadata.

### Step 2: Submission for Review

*   The Contributor submits the example for review (e.g., via a Git Pull Request against the main branch containing the library, or by notifying the designated review channel/personnel).
*   The submission should include a brief description of the new example, its purpose, and the task type it addresses.

### Step 3: Reviewer(s) Assessment

Reviewer(s) will assess the submitted example against the following checklist:

**A. Structural Integrity & Naming Conventions:**
*   [ ] Example directory is correctly named and located under the appropriate task type (and domain/language subfolder if applicable).
*   [ ] All mandatory files (`metadata.json`, `input.txt`, `output.txt`) are present. `description.md` is highly recommended.
*   [ ] Optional files (`process_guidance.md`, `few_shot_examples.md`) are used appropriately and correctly.
*   [ ] File names are correct.

**B. Metadata Quality (`metadata.json`):**
*   [ ] File is valid JSON (verify with a linter if complex).
*   [ ] Structure matches an item from `master_prompt_schema_v8.json#examples`, including a **nested `example_metadata` object** (this is critical for V1 selector compatibility).
*   [ ] Fields within the nested `example_metadata` object align with `example_metadata_schema_v1.json`.
*   [ ] `id` (top-level) is unique, descriptive, and matches the directory name.
*   [ ] `type` (top-level, e.g., "positive", "edge_case") is appropriate.
*   [ ] `example_metadata.difficulty` is set.
*   [ ] `example_metadata.tests_concept` is descriptive.
*   [ ] `example_metadata.language` is accurate (if applicable).
*   [ ] `example_metadata.task_type_tags` are relevant, comprehensive, and correctly cased.
*   [ ] `example_metadata.domain_tags` are relevant, comprehensive, and correctly cased.
*   [ ] `example_metadata.complexity_level` (e.g., "simple", "moderate", "complex") is appropriate and correctly cased.
*   [ ] `example_metadata.example_description`, `input_description`, `output_description` are clear, accurate, and align with file contents.
*   [ ] `example_metadata.positive_keywords` and `negative_keywords` are well-chosen for discoverability.
*   [ ] `example_metadata.example_version` is set (e.g., "1.0" for new examples, increment for significant updates).
*   [ ] `example_metadata.creation_date` and `last_updated_date` are correctly formatted (YYYY-MM-DDTHH:MM:SSZ or YYYY-MM-DDTHH:MM:SS+/-HH:MM) and set.

**C. Content Quality:**
*   [ ] `description.md` (if present): Is it clear, concise, and accurately reflects the example's purpose and content?
*   [ ] `input.txt`: Does it represent a realistic, clear, and unambiguous input/query for an LLM? Is the content of high quality and representative of the intended use case? (Verify content is not just a placeholder if the example is mature).
*   [ ] `output.txt`: Is it a high-quality, correct, and ideal response to the `input.txt`? Does it effectively demonstrate the concept described? (Verify content is not just a placeholder if the example is mature).
*   [ ] `process_guidance.md` (if present): Is it clear, accurate, and genuinely helpful for understanding the transformation from input to output or the reasoning involved?
*   [ ] `few_shot_examples.md` (if present): Are the precursor examples clear, correct, and do they effectively set the context for the main example task? Is this file used appropriately for examples that are *about* few-shot learning itself?

**D. Alignment with Design Principles:**
*   [ ] Does the example adhere to the core tenets (Clarity, Relevance, Quality over Quantity, Consistency) from `@knowledge_base/prompts/meta_prompting_system/dynamic_example_injection_mechanism/research_and_design_notes/few_shot_example_design_principles_v1.md`?
*   [ ] Is the structure (e.g., conversational format, input/output delimitation) appropriate and clear?
*   [ ] If demonstrating Chain-of-Thought or complex reasoning, is it shown effectively?

**E. Uniqueness, Value, and Necessity:**
*   [ ] Does this example add distinct value to the library (e.g., covers a new task nuance, domain, technique, or addresses a known gap)?
*   [ ] Does it significantly overlap with existing examples? If so, is the overlap justified and clearly differentiated (e.g., a subtle but important variation)?

**F. Selector Compatibility (Conceptual Check):**
*   [ ] Based on its `metadata.json`, is it plausible that the `v1_example_selector.py` (or future versions) could effectively discover and select this example when appropriate characteristics are requested?

### Step 4: Feedback and Iteration

*   Reviewer(s) provide clear, constructive, and actionable feedback to the Contributor.
*   Feedback should reference specific checklist items or principles.
*   The Contributor addresses the feedback. This may involve discussion and multiple iterations.

### Step 5: Approval and Integration

*   Once all Reviewers approve the example, it is integrated into the main example library (e.g., by merging the Pull Request).

### Step 6: Post-Integration (Optional)

*   If a central registry or tracking sheet for examples exists, update it with the new example's details.
*   Announce the new example to the relevant team if appropriate.

## 6. Key Reference Documents for Review

*   **Overall Library Structure**: `@knowledge_base/prompts/meta_prompting_system/example_library/by_task_type/README.md`
*   **Example File Content Principles**: `@knowledge_base/prompts/meta_prompting_system/dynamic_example_injection_mechanism/research_and_design_notes/few_shot_example_design_principles_v1.md`
*   **Master Prompt Schema (for `examples` array item structure)**: `@knowledge_base/prompts/meta_prompting_system/schemas/master_prompt_schema_v8.json` (specifically the structure of an object within the `examples` array, which includes the nested `example_metadata` object).
*   **Detailed Metadata Fields (for the nested `example_metadata` object)**: `@knowledge_base/prompts/meta_prompting_system/example_library/schemas/example_metadata_schema_v1.json`.
*   **Selector Logic (for context on discoverability)**: `@knowledge_base/prompts/meta_prompting_system/dynamic_example_injection_mechanism/selection_logic/v1_example_selector.py`.

This workflow aims to be thorough yet practical, ensuring the continued growth of a high-quality example library.