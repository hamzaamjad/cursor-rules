# Agentic Project Initiation Playbook

**Purpose**: To provide a structured workflow for initiating and managing agentic development projects, ensuring clarity, efficient execution, and knowledge capture.

**When to Use**: When embarking on a new, non-trivial project that will involve multiple steps, potentially multiple agents (or a single agent over multiple sessions), and where systematic planning and knowledge integration are beneficial.

---

## Phase 1: Project Definition & Cartography

1.  **Define Project Scope & Goals Clearly**:
    *   Articulate the overall objective of the project.
    *   Define clear, measurable success criteria.
    *   Identify key deliverables.
    *   *Self-correction*: If goals are vague, use an agent (or self-reflection) to refine them into S.M.A.R.T (Specific, Measurable, Achievable, Relevant, Time-bound) objectives where possible.

2.  **Survey Existing Knowledge & Assets (Cartography)**:
    *   Identify relevant existing documents, schemas, code, rules (`.mdc`), and notepads within the workspace.
    *   Query internal knowledge bases (Knowledge Graph via `mcp_memory_search_nodes`, Vector DBs via `mcp_chroma_query_documents` with known collection names) for related concepts, prior art, or lessons learned.
    *   Perform targeted web research (e.g., using `mcp_perplexity-ask_perplexity_research`) if external context is needed.
    *   *Output*: A brief summary of relevant knowledge assets and any identified gaps.

3.  **Design Target Directory Structure & Perform Initial Reorganization**:
    *   Based on the project scope, envision an optimal directory structure for new artifacts (code, prompts, schemas, documentation, evaluations, etc.).
    *   Use `mcp_desktop_commander_create_directory` to create new folders.
    *   Use `mcp_desktop_commander_move_file` to reorganize existing relevant files into the new structure if needed.
    *   *Rationale*: A clean, logical structure significantly aids project clarity and future maintainability.

---

## Phase 2: Strategic Planning & Task Generation

4.  **Develop a Phased Implementation Roadmap**:
    *   Break down the overall project into logical phases and discrete, actionable tasks within each phase (similar to the `dynamic_example_injection_roadmap.md` we created).
    *   For each major task, consider inputs, outputs, and potential tools/agents to be used.
    *   Apply 80/20 prioritization: identify tasks that deliver the most value or unblock subsequent critical work.
    *   Save this roadmap as a Markdown file within the project's documentation or evaluation directory.

5.  **Generate Task-Specific Prompts (Leveraging Meta-Prompting)**:
    *   For the first (or next) actionable task identified in the roadmap, use the meta-prompting system (i.e., an LLM A instance guided by a meta-prompt generator template like `meta_prompt_generator_template_v1.json`) to generate a detailed, structured JSON prompt.
    *   This prompt will guide an LLM C instance (which could be another specialized agent or even the same agent switching roles) to execute the specific task.
    *   Store these generated task prompts in a designated project subdirectory (e.g., `PROJECT_NAME/generated_prompts_for_development/`).

---

## Phase 3: Iterative Execution & Knowledge Integration

6.  **Execute Roadmap Tasks Iteratively**:
    *   Process each task using the generated prompt with the designated LLM C / agent.
    *   Apply relevant `.cursor/rules/*.mdc` files (e.g., `stepwise-autonomy.mdc`, `python-clean-code.mdc`) during execution.
    *   Verify outputs against task success criteria.

7.  **Persistent Knowledge Integration (Crucial for Agentic Memory & Learning)**:
    *   **Purpose**: To ensure that key learnings, decisions, designs, and artifacts from the project are captured in a structured, retrievable way for future agentic or human use.
    *   **What to Capture**: 
        *   Key architectural decisions and their rationale.
        *   Finalized schemas, roadmaps, significant code modules (or summaries/pointers to them).
        *   Core principles extracted from research or analysis.
        *   Task Retrospective summaries if performed.
    *   **How to Capture (using Memory MCP Tools)**:
        *   **Create Entities**: Use `mcp_memory_create_entities(entities=[McpMemoryCreateEntitiesEntities(entityType="ProjectArtifact", name="UniqueNameForArtifact_YYYYMMDD", observations=["Description of artifact...", "Path: /path/to/artifact"])])` for major deliverables or concepts.
            *   *Example Entity Types*: `ProjectRoadmap`, `DesignDocument`, `SchemaDefinition`, `CorePrinciple`, `KeyDecision`, `TaskLearning`.
        *   **Add Observations**: Use `mcp_memory_add_observations(observations=[McpMemoryAddObservationsObservations(entityName="ExistingEntityName", contents=["New learning about this...", "Version 2.0 details..."])])` to add details or updates to existing entities.
        *   **Create Relations**: Use `mcp_memory_create_relations(relations=[McpMemoryCreateRelationsRelations(from="ArtifactA_Name", relationType="derivedFrom", to="SourceDocument_Name"), McpMemoryCreateRelationsRelations(from="KeyDecision_XYZ", relationType="impacts", to="SchemaDefinition_ABC")])` to link entities and show how they connect.
            *   *Example Relation Types*: `developedAsPartOf (ProjectName)`, `informedBy (PrincipleName)`, `versionOf (PreviousArtifactName)`, `dependsOn (AnotherArtifactName)`, `ledTo (DecisionOrLearningName)`.
    *   **When to Capture**: Ideally, at the end of each significant phase or task completion, or as key insights emerge.

8.  **Conduct Task/Phase Retrospectives**: Upon completion of significant phases or the overall project, use the `task-retrospective.mdc` framework to identify successes, challenges, and further systemic improvements.

---

This playbook provides a template. Adapt it based on project size and complexity.
