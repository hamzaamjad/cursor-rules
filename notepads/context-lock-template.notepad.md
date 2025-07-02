# Context Lock Template

**Purpose**: This template defines a structure for agents to declare a lock on a specific operational context, preventing concurrent modifications or ensuring focused attention. This supports FlameLang symbolic runtime coordination.

---

**Lock ID**: `CL-{AgentID}-{TimestampYYYYMMDDHHMMSS}` (System Generated or Agent Generated)
**Agent ID**: `{RequestingAgentID}`
**Timestamp (Acquired)**: `{YYYY-MM-DDTHH:MM:SSZ}`
**Status**: `ACTIVE` | `REQUESTED` | `RELEASED` | `EXPIRED` 
**Expected Duration**: `{HH:MM:SS}` (e.g., 00:30:00 for 30 minutes)
**Actual Release Timestamp**: `{YYYY-MM-DDTHH:MM:SSZ}` (Filled upon release)

## Lock Scope & Focus:

**Primary Resource(s)**:
  - `@File:[path/to/primary/file.ext]` 
  - `@Symbol:[FullyQualifiedSymbolName]`
  - `@MemoryFragment:[MemorySystemUUID]`
  - `@KnowledgeGraphNode:[NodeID]`
  - *(Add other specific resource identifiers relevant to FlameLang)*

**Associated Resources (Informational)**:
  - `[List of related files, symbols, or concepts]`

**Lock Type**: 
  - `EXCLUSIVE_WRITE` (No other agent can write to primary resources)
  - `SHARED_READ` (Multiple agents can read, new writes may be blocked or queued)
  - `FOCUS_DIRECTIVE` (Agent declares its current focus; informational for other agents)

**Reason/Objective**: 
  - `[Brief description of why the lock is needed, e.g., "Refactoring core module X", "Executing critical data transformation Y", "Deep analysis of concept Z"]`

## Coordination Protocol:

**On Conflict**: 
  - `[Defined behavior if another agent attempts to access/modify locked resources, e.g., "Queue request", "Alert locking agent", "Deny with error"]`

**On Expiry**:
  - `[Behavior if lock expires before release, e.g., "Auto-release", "Alert locking agent", "Extend lock if agent active"]`

**Heartbeat/Keep-Alive (Optional)**:
  - `[Mechanism for agent to signal it's still actively using the context]`

---

**Usage**: Agents should create an instance of this notepad (e.g., `my-specific-task.context.lock.md`) and register its status/location with the central FlameLang coordination service or memory.
