# Vault Organization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Implement the user's approved consolidation, duplicate cleanup, and linked summaries in an Obsidian-compatible Markdown vault.

**Architecture:** Six content areas hold source notes, with named projects and ordered corpora retained inside them. Atlas holds navigation, summaries, and migration records. Inbox holds new material. Duplicates confirmed by the user resolve to a preferred source, with old paths recorded for recovery through Git.

**Tech Stack:** Markdown, Obsidian wikilinks, CSV migration records, Python standard-library migration and validation utilities outside the vault.

**Spec:** [[Atlas/Organization Review|Organization Review]], approved by the user on November 23, 2026, with the subsequent confirmation that the listed duplicates are duplicates and all proposed suggestions should be implemented.

## Global constraints

- Preserve source wording; organization and link repairs do not imply rewriting original material.
- Preserve named projects, creative worlds, OPTE's sequence, and recoverability of removed versions through Git.
- Respect the user's removal of numbered discussion exports; use the retained distillation.
- Keep interpretation distinct from source material and documented design distinct from verified implementation.
- Use no new dependencies or automatic chat-capture service.

## Review focus

- Emoji, punctuation, spaces, and case differences in paths must survive a Windows filesystem migration.
- A duplicate graph may join more than two notes; every old path must resolve to one recorded survivor without cycles.
- Embedded notes, wikilinks, relative Markdown links, and Obsidian configuration paths must follow moves.
- A link to a deliberately removed discussion must not silently become a broken navigation entry.
- Summaries must cite actual retained sources and state the extent of their reading.

## Tasks

### Task 1: Inventory and migration map

- [x] Snapshot the updated Git baseline and preserve the earlier review note.
- [x] Select a preferred source for each user-confirmed duplicate group and record reasons.
- [x] Assign every surviving source a destination within the six approved areas; inspect mixed folders by note.
- [x] Check that destination paths are unique without regard to case and remain inside the vault.

### Task 2: Move, deduplicate, and reconnect

- [x] Apply the map; remove the leftover numbered discussion export if present.
- [x] Repair resolvable internal links and Obsidian path settings, preserving prose and code fences.
- [x] Replace obsolete browse pages with live indexes, and save a CSV mapping of original paths and duplicate survivors.
- [x] Verify every source is retained, user-confirmed redundant, or intentionally removed; compare source bodies after accounting for link rewrites.

### Task 3: Orientations, syntheses, and retrieval indexes

- [x] Read retained entry sources for each area before writing source-linked summaries.
- [x] Give each area a brief orientation, a fuller synthesis, and a complete linked index.
- [x] Update Home, Decisions, Review, Import Log, and the organization review to reflect the implemented structure.
- [x] Explain manual capture and maintenance in the vault, with automatic capture left as future work.

### Task 4: Validate and review

- [x] Check generated links, duplicate redirects, collision safety, inventories, JSON configuration, and whitespace.
- [x] Compare pre-existing unresolved source links separately from migration-caused breaks.
- [ ] Obtain a fresh review of the completed migration and address material findings.
- [ ] Record verification results and commit the completed local change.

## Progress and implementation decisions

- Baseline: `2664a86`; implementation branch: `main-vault-organization`.
- The branch uses `main-` because Git cannot create a `main/` namespace while the existing `main` branch occupies that name.
- This is a document migration: verification checks preservation, paths, links, and inventories rather than adding application unit tests.
- Local backup and migration utilities live outside the vault under the Codex temporary directory. Git and the committed migration record provide durable recovery.

- Migration verification: 946 source notes and four Word originals retained; 59 redundant versions removed across 55 confirmed groups; one discussion remnant removed. All 950 sources are indexed exactly once.
- Preservation verification: source wording compared with Git after masking link markup and removing newly added aliases; four Word originals byte-compared; 27 code blocks compared unchanged.
- Link verification: 1,389 generated internal links resolve; zero new unresolved source references. The 104 pre-existing unresolved references are recorded separately.
- Filename normalization: removed one stray backtick, retaining its original title as an alias and its old path in the migration record.
