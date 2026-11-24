---
aliases: ["1"]
---

## PHASE 1: Memory & Continuity (DO THIS FIRST)
**What this solves:** Claude forgetting you between sessions. The upstream problem.

| Repo | What to extract | Already researched? |
|------|----------------|-------------------|
| [claude-mem](https://github.com/thedotmack/claude-mem) | How it persists context across Code sessions. What format it uses. | NEW |
| [Iron-mem](https://github.com/BMC-INC/Iron-mem) | Rust-based persistent session memory. Records tool calls, compresses via API, injects as IRONMEM.md. 10 MCP tools. | Yes — RESEARCHED, not installed |
| [claude-code-memory-bank](https://github.com/hudrazine/claude-code-memory-bank) | Memory bank patterns for Code specifically. | NEW |
| [claude_code_journaling](https://github.com/vystrcild/claude_code_journaling) | Session journaling — what gets recorded and how. | NEW |
| [ReMe](https://github.com/agentscope-ai/ReMe) | Already BUILT in your ecology. 99.5% compression, hybrid search, daily journals. Study it to understand what you already have. | Yes — BUILT |
| [context-hub](https://github.com/Andrewyng/context-hub) | Annotation loop — persistent notes on knowledge entries that compound over time. | Yes — RESEARCHED |

**Instruction to Code:** "These repos all solve memory and continuity. I need you to understand how each one persists context across sessions. Don't install any of them yet. Read the actual source code — how they store, compress, retrieve, and inject memory. Then tell me: which approach would work best given that I already have RECALL (ChromaDB) and ReMe patterns in my ecology? I want ONE coherent memory system, not six competing ones."