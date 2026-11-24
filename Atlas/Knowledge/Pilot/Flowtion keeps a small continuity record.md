---
id: "flowtion-continuity"
kind: "design_decision"
status: "documented_design"
area: "Projects"
project: "Flowtion"
source_date: null
prepared_date: "2026-11-24"
review_status: "agent-reviewed; user review pending"
---

# Flowtion keeps a small continuity record

Flowtion proposes keeping a project's north star, current edge, next fifteen-minute step, and last change in a project heartbeat. A timestamped decision log, named tensions with status, and a one-paragraph story-so-far preserve continuity. The source says these update when the user accepts an offered action; automatic operation is a design claim, not verified here.

## Source

[[Projects/Flowtion/Core Idea|Core Idea]] · lines 50–60

> [!note] Status
> This is an assistant-authored distillation. Its status describes the source’s claim; documented implementation is not a fresh runtime verification.
