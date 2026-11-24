---
id: "trader-choice-evidence"
kind: "implementation_decision"
status: "documented_implementation"
area: "Projects"
project: "Paradox Trader"
source_date: null
prepared_date: "2026-11-24"
review_status: "agent-reviewed; user review pending"
---

# Paradox Trader records the conditions around a choice

The Sessions update documents separate records for offered actions, costs and constraints, the committed choice, execution, and private admitted input. A malformed response is a processing failure, not an inferred decision to rest. Offered actions are not guaranteed resource allocations. A choice can therefore be described with its conditions and outcome without treating it as proof of an agent's personality or preference.

## Source

[[Projects/Paradox Trader/Offered choices and owner-local continuity|Offered choices and owner-local continuity]] · lines 5–17

> [!note] Status
> This is an assistant-authored distillation. Its status describes the source’s claim; documented implementation is not a fresh runtime verification.
