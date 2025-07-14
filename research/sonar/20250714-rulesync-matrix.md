---
title: "Rulesync Integration Matrix for AI Development Tools"
date: "2025-07-14T09:47:36+00:00"
tool: "perplexity-sonar"
model: "claude-opus-4"
---

# Summary

This report provides a comprehensive integration matrix for synchronizing a single `rulesync.md` file across five major AI development platforms as of July 2025. Each platform has distinct rule file formats, locations, and precedence behaviors that must be considered when implementing a unified rule management system. The report details exact file naming conventions, configuration commands for automated population, and critical edge cases that could disrupt rule synchronization. Key findings include Cursor IDE's complex multi-directory `.mdc` system, Zed Editor's compatibility-focused approach, and the varying precedence hierarchies across CLI tools from Gemini, OpenAI, and Anthropic.

# Findings

## 1. Gemini CLI (Public GA Release)

**Rule Files & Precedence:**
- **Primary file**: `GEMINI.md` in project root[9][57]
- **Global config**: `~/.gemini/GEMINI.md` for user-level defaults[9][57]
- **Override behavior**: Project-level `GEMINI.md` completely overrides global settings (no merge)[58]
- **Alternative**: `.idx/airules.md` for Firebase integration contexts only[9][57]

**CLI/Config Commands for rulesync:**
```bash
# Copy to project root
cp rulesync.md ./GEMINI.md

# Global installation
mkdir -p ~/.gemini && cp rulesync.md ~/.gemini/GEMINI.md

# No built-in reload command - requires CLI restart
```

**Edge Case Gotcha:**
The global `GEMINI.md` is completely ignored when a project-level file exists, breaking inheritance expectations. This is tracked as [issue #3479](https://github.com/google-gemini/gemini-cli/issues/3479)[58]. Workaround: Manually concatenate global and project rules.

## 2. OpenAI Codex CLI

**Rule Files & Precedence:**
- **Global instructions**: `~/.codex/instructions.md`[35][37]
- **Project-wide**: `./codex.md` at repository root[4][35][37]
- **Directory-specific**: `./codex.md` in current working directory[4][35]
- **Precedence cascade**: CWD > Project > Global (later overrides earlier)[35][37]

**CLI/Config Commands for rulesync:**
```bash
# Global setup
mkdir -p ~/.codex && cp rulesync.md ~/.codex/instructions.md

# Project setup
cp rulesync.md ./codex.md

# Disable project rules temporarily
export CODEX_DISABLE_PROJECT_DOC=1
# Or use flag: codex --no-project-doc
```

**Edge Case Gotcha:**
Multiple `codex.md` files in nested directories can create confusion. The CWD version always wins, potentially ignoring critical project-wide rules[35]. Solution: Use symlinks to maintain consistency across subdirectories.

## 3. Anthropic Claude Code CLI

**Rule Files & Precedence:**
- **Project rules**: `CLAUDE.md` in repository root[5][29][65]
- **Search path**: Any parent directory of execution location[29][65]
- **Global config**: `~/.claude.json` (for MCP servers, not rules)[62]
- **Override**: Only nearest `CLAUDE.md` in hierarchy is used[29][65]

**CLI/Config Commands for rulesync:**
```bash
# Project setup
cp rulesync.md ./CLAUDE.md

# Force reload during session
claude "read CLAUDE.md"

# Tool permission overrides (per-session)
claude --allowedTools bash,fs --disallowedTools network
```

**Edge Case Gotcha:**
Claude may cache rule content between commands. The explicit `read CLAUDE.md` command is sometimes required to ensure updates are recognized[5][65]. Additionally, the first line of `CLAUDE.md` should remind Claude to include the entire file in responses for better adherence[5].

## 4. Cursor IDE (Multi-.mdc Rules)

**Rule Files & Precedence:**
- **Directory**: `.cursor/rules/` at project root and nested subdirectories[1][2][7][12]
- **Extension**: `.mdc` (Markdown with YAML frontmatter)[8][12][13]
- **Activation types**: Always > Auto-attached > Agent-requested > Manual[12]
- **Nested precedence**: Deeper directories override parent rules[7][12]
- **Conflict resolution**: `priority` metadata (higher wins) > filename order > timestamp[4][12]

**CLI/Config Commands for rulesync:**
```bash
# Create rules directory
mkdir -p .cursor/rules

# Convert rulesync.md to .mdc format with metadata
cat << 'EOF' > .cursor/rules/000-core-rulesync.mdc
---
description: "Core rulesync standards"
globs: ["**/*"]
alwaysApply: true
priority: 999
version: 1.0.0
---
$(cat rulesync.md)
EOF

# Generate from conversation
# In Cursor chat: /Generate Cursor Rules
```

**Edge Case Gotcha:**
Overly broad glob patterns (e.g., `**/*`) can cause performance degradation as rules activate on every file reference[4][7]. Additionally, rules exceeding 500 tokens may be truncated during context window management[9]. Solution: Split large rules and use specific globs.

## 5. Zed Editor (.rules Variants)

**Rule Files & Precedence:**
- **Primary location**: Project root only (no subdirectory support)[10]
- **Compatible names** (first match wins)[10]:
  1. `.rules`
  2. `.cursorrules`
  3. `.windsurfrules`
  4. `.clinerules`
  5. `.github/copilot-instructions.md`
  6. `AGENT.md`
  7. `AGENTS.md`
  8. `CLAUDE.md`
  9. `GEMINI.md`
- **Library rules**: Stored separately in Zed's Rules Library[10]

**CLI/Config Commands for rulesync:**
```bash
# Primary setup
cp rulesync.md ./.rules

# Cross-tool compatibility
cp rulesync.md ./.cursorrules  # For Cursor compatibility
cp rulesync.md ./CLAUDE.md     # For Claude compatibility

# Library management (GUI only)
# Agent Panel > ... > Rules... > + New Rule
# Or: Command Palette > "agent: open rules library"
```

**Edge Case Gotcha:**
Zed reads only the **first matching file** from the compatibility list, ignoring all others[10]. Teams using multiple tools may inadvertently create conflicting rule files. Solution: Standardize on `.rules` and use symlinks for compatibility names.

# Implementation Strategy for rulesync

**Unified Command Structure:**
```bash
rulesync generate --platforms gemini,codex,claude,cursor,zed \
                 --source rulesync.md \
                 --format auto
```

**Platform-Specific Transformations:**
1. **Gemini/Claude**: Direct copy as markdown
2. **Codex**: Prepend with user preferences if merging global/local
3. **Cursor**: Add YAML frontmatter with appropriate metadata
4. **Zed**: Create primary `.rules` plus compatibility symlinks

**File System Layout After rulesync:**
```
project/
├── GEMINI.md              # Gemini CLI
├── codex.md               # OpenAI Codex
├── CLAUDE.md              # Claude Code
├── .cursor/
│   └── rules/
│       └── 000-rulesync.mdc  # Cursor IDE
├── .rules                 # Zed Editor (primary)
├── .cursorrules -> .rules # Zed compatibility symlink
└── rulesync.md            # Source of truth
```

# Sources

- [Firebase Gemini Documentation](https://firebase.google.com/docs/studio/set-up-gemini) - GEMINI.md configuration[9][57]
- [GitHub Issue #3479](https://github.com/google-gemini/gemini-cli/issues/3479) - Gemini precedence bug[58]
- [Apidog Codex CLI Guide](https://apidog.com/blog/openai-codex-cli/) - Codex file hierarchy[35]
- [Blott Studio Codex Tutorial](https://www.blott.studio/blog/post/openai-codex-cli-build-faster-code-right-from-your-terminal) - Codex configuration[37]
- [Grant Slatton Claude Code](https://grantslatton.com/claude-code) - CLAUDE.md best practices[5]
- [HTDocs Claude Guide](https://htdocs.dev/posts/claude-code-best-practices-and-pro-tips/) - Claude file locations[29]
- [Anthropic Engineering Blog](https://www.anthropic.com/engineering/claude-code-best-practices) - Claude reload mechanism[65]
- [Cursor Rules Documentation](https://docs.cursor.com/context/rules) - .mdc format specification[12]
- [Cursor Forum Best Practices](https://forum.cursor.com/t/optimal-structure-for-mdc-rules-files/52260) - Rule organization patterns[1]
- [Kirill Markin Cursor Guide](https://kirill-markin.com/articles/cursor-ide-rules-for-ai/) - Directory hierarchy[7]
- [Zed AI Rules Documentation](https://zed.dev/docs/ai/rules) - .rules implementation[10]
