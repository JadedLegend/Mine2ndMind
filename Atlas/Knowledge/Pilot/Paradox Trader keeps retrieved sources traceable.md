---
id: "trader-source-provenance"
kind: "implementation_decision"
status: "documented_implementation"
area: "Projects"
project: "Paradox Trader"
source_date: null
prepared_date: "2026-11-24"
review_status: "agent-reviewed; user review pending"
---

# Paradox Trader keeps retrieved sources traceable

The shared-library document requires retrieved passages to carry an original filename, original hash, section ID, and extraction locator. Search offsets refer to Unicode characters in an extracted section, not original page coordinates. Agent interpretations can be stored separately with those references; source documents do not become agent-authored journal history. Original files are retained for fuller checking. This is the library document's implementation account.

## Source

[[Projects/Paradox Trader/Shared original-document library|Shared original-document library]] · lines 28–34

> [!note] Status
> This is an assistant-authored distillation. Its status describes the source’s claim; documented implementation is not a fresh runtime verification.
