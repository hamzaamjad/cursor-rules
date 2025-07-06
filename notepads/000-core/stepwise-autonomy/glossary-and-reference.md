# Stepwise Autonomy Glossary and Reference

This notepad contains extended glossary terms, abstract tool interface mappings, and reference materials extracted from the main stepwise-autonomy rule to optimize token efficiency.

## Glossary of Terms

**MCP (Model Context Protocol)**: A term describing the mechanism (often a defined API or function-calling framework) through which language models interact with tools and external services. MCP services are specific instances of such services (e.g., Context7, Perplexity, Puppeteer) that provide capabilities like documentation lookup, research, or browser automation.

**@Refs**: A reference system for linking to files, documentation, or other resources using the format `@Type:path/to/resource`. For example, `@File:src/main.py` or `@Docs:security.mdc#Authentication`.

**Cursor Agent Mode**: An execution environment where the model can directly manipulate files and run commands through specialized tools rather than only generating code snippets.

**Holistic Check**: The process of examining components related to the modified code to identify potential impacts or required corresponding changes.

**Verification**: The systematic confirmation that each step has succeeded before proceeding to the next step.

**Tree of Thoughts (ToT)**: An advanced reasoning technique that explores multiple solution paths before committing to one, achieving 15-30% accuracy improvement on complex tasks.

**Constraint Resonance Network**: A pattern where constraints at different system levels reinforce each other, creating emergent optimization opportunities.

## Abstract Tool Interface and Mapping

The tool names used in the stepwise-autonomy protocol are example implementations. In different agent runtimes, these may be mapped to different function names. The underlying principle of using available tools rather than generating raw output remains constant regardless of specific tool naming conventions.

### Example Tool Alias Block for Agent Implementation

To ensure clarity for agents that do not support dynamic aliasing, developers can map abstract tool names to concrete implementations:

- `abstract: edit_file` -> `concrete: functions.writeFile(path, content)`
- `abstract: run_terminal_cmd` -> `concrete: functions.executeShellCommand(command)`
- `abstract: read_file` -> `concrete: functions.readFile(path)`
- `abstract: list_files` -> `concrete: functions.listFiles(directory)`
- `abstract: search_files` -> `concrete: functions.searchFiles(pattern, path)`

The specific concrete invocations will depend on the agent's toolkit and runtime environment.