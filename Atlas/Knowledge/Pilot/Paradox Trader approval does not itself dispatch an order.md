---
id: "trader-approval-dispatch"
kind: "implementation_decision"
status: "documented_implementation"
area: "Projects"
project: "Paradox Trader"
source_date: null
prepared_date: "2026-11-24"
review_status: "agent-reviewed; user review pending"
---

# Paradox Trader approval does not itself dispatch an order

The documented mock lifecycle requires explicit queue approval, but approval itself sends nothing. It persists an intent and deterministic client-order ID before dispatch. A lost acknowledgement stays unknown; a lookup outage does not cause another submission. The described execution service is restricted to one agent and a fixed fictional contract, not a connected paper or live broker.

## Source

[[Projects/Paradox Trader/Traceable idea lineage — first implementation|Traceable idea lineage — first implementation]] · lines 24–28

> [!note] Status
> This is an assistant-authored distillation. Its status describes the source’s claim; documented implementation is not a fresh runtime verification.
