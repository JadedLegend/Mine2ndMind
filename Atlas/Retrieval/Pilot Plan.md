---
title: Semantic Retrieval Pilot Plan
date: 2026-11-24
tags: [atlas/retrieval]
---

# Semantic Retrieval Pilot Plan

Xerj is set aside while the knowledge material is prepared and tested. The existing organized source vault remains the source collection.

The user’s direction is meaning-aware chunking, distillation, embeddings, and metadata. The user selected Projects and their decisions. The first working sample covers Flowtion, Privthee, Paradox Trader, and PDAOK, preserving the distinction between design commitments, documented implementation decisions, and planned work. This bounded sample makes the quality inspectable before a bulk pass.

1. Keep exact source passages, locators, and normalized-text hashes with each distilled note. Unknown source dates stay unknown. A claim retains its status as a proposal, interpretation, hypothesis, or creative work.
2. Make Markdown notes and portable JSONL records from ten reviewed semantic units. Preserve qualifications and source attribution. These are assistant-authored distillations of the sources, not new user decisions.
3. Provide an embedding-based boundary experiment over whole text blocks. Topic changes suggest boundaries; size limits operate between blocks and never silently truncate them. Reviewed semantic units and automatically suggested boundaries remain distinguishable.
4. Embed the distilled notes with a pinned local neural model. Store vectors and metadata in a local SQLite file and apply metadata filters before exact cosine ranking. This small vector store needs no server. Indexing raw transcripts is not the default.
5. Test paraphrased queries, source changes, source citation fidelity, rebuild behavior, vector compatibility, and metadata filters. Report measured pilot results without treating a small authored test set as a corpus-wide benchmark.

Implementation choices: ONNX Runtime, the official all-MiniLM-L6-v2 model, its tokenizer, and Python’s SQLite module. Dependencies are isolated outside the vault; generated database files are ignored by Git. Notes are never sent to an embedding API.

Semantic chunking is a strategy to evaluate rather than a universal guarantee. Late chunking is a different technique: it embeds the longer context before pooling smaller spans. This pilot uses ordinary local sentence embeddings and does not claim to implement late chunking.

References: [late chunking paper](https://arxiv.org/abs/2409.04701), [evaluation of semantic chunking](https://arxiv.org/abs/2410.13070), [embedding model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2).
