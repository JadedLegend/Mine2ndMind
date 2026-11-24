# Local semantic retrieval pilot

The user selected **Projects and their decisions** for the first pilot. Xerj remains set aside. This sample prepares ten distilled units from six documents across Flowtion, Privthee, Paradox Trader, and PDAOK.

Start at [[Atlas/Knowledge/Pilot|Projects and Decisions Pilot]] to read the notes. They are assistant-authored drafts for inspection. Their classifications distinguish a documented design, an ethical commitment, documented implementation, and planned work; none is silently upgraded to a verified current runtime fact.

## What runs

1. `pilot.json` holds the ten editorial distillations, exact source locators, classifications, and pinned source hashes.
2. `build` checks those citations, renders reviewable Markdown notes, exports JSONL, and embeds the short distillations with a local neural model.
3. SQLite stores the vectors and metadata in `.local/index.sqlite3`. Search filters metadata first, then uses exact cosine similarity. This is a small local vector store, with no database server or approximate vector index.
4. Search returns the distilled text, status, and source locator. Exact source passages are optional with `--include-evidence`.

`source_chunks.jsonl` preserves the reviewed semantic passages for checking. `records.jsonl` contains the derived notes and evidence. The vector index embeds **title + distilled text**, rather than the long source passages. The metadata remains available for filtering and citations.

## Meaning-aware boundaries

Two methods are deliberately distinguished:

- **Reviewed semantic units:** the ten pilot sources were selected at coherent changes in thought. A decision keeps the rationale or qualification needed to interpret it. This selection is editorial, not the output of an automatic boundary detector.
- **Embedding-based candidates:** `segment` compares adjacent whole-block neural embeddings, proposing a new group when cosine similarity falls below 0.5. It also limits groups to 150 words at block boundaries. Heading context is attached to following text, frontmatter is omitted, and fenced code stays whole. Candidate boundaries require reading and review; they are not automatically promoted into distilled facts.

The model has a 256-token window. An oversized unit is rejected rather than silently truncated. The boundary experiment in [[Atlas/Retrieval/Boundary Candidates.json|Boundary Candidates]] produced six candidate groups from the PDAOK phase document. It is an experiment, not an exhaustive chunking pass over the vault.

This is ordinary embedding-based retrieval. It does **not** implement late chunking. The [late-chunking paper](https://arxiv.org/abs/2409.04701) embeds longer context before pooling smaller spans. [Comparative research](https://arxiv.org/abs/2410.13070) also cautions against assuming semantic chunking universally outperforms simpler methods.

## Search now

The local environment and index have already been created on this machine. From the vault folder, in PowerShell:

```powershell
$pilotPython = Join-Path $env:LOCALAPPDATA 'Mine2ndMind\semantic-pilot-env\Scripts\python.exe'
& $pilotPython Atlas/Retrieval/pilot.py search 'Does approving an order send it immediately?' --project 'Paradox Trader' --k 3
& $pilotPython Atlas/Retrieval/pilot.py search 'What carries a project across a restart?' --project Flowtion
& $pilotPython Atlas/Retrieval/pilot.py search 'What is still future work?' --status planned
```

Supported filters are `--project`, `--kind`, and `--status`. The Python search function also accepts area and source-date equality filters. A cosine score expresses similarity, not truth or confidence.

## Source fidelity and dates

Every record keeps an exact source quote, line range, character offsets, normalized source SHA-256, and quote SHA-256. Offsets count Unicode characters after decoding UTF-8, removing a BOM, and normalizing newlines to LF. These are not byte offsets or rendered page numbers.

Unknown source dates remain `null`. `prepared_date` records when the distillation was curated; it is not the source date or an implementation date. No source date is inferred from download timestamps.

Build refuses a changed pinned source until the distillation is reviewed. Search excludes records whose source has changed and reports the excluded count. Rebuilding replaces the generated index atomically and removes records no longer in the pilot. A different model profile requires rebuilding rather than mixing vector spaces.

## Editing and scope

The pilot Markdown notes are review artifacts generated from `pilot.json`. The build refuses to overwrite an edited note. Keep any edits or personal interpretations before rebuilding, then reconcile them with the curation record. This small pilot does not yet provide an automatic bulk distillation agent or a Markdown-to-curation editor.

Original source notes are unchanged. This branch has not processed all Projects material or the entire vault. Source-document claims about tests, deployment, and implementation have not been independently rerun for this retrieval pilot.

## Model and setup on another machine

The pinned model is [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2), revision `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, producing 384-dimensional vectors. `model.json` pins the model and tokenizer checksums. Inference uses ONNX Runtime on the CPU, with attention-mask mean pooling and L2 normalization.

Dependencies and model downloads need network access during setup. No note text is sent to an embedding API. Subsequent inference uses the pinned local files. The environment and model cache are outside the vault; the rebuildable database is ignored by Git.

For a new machine with `uv` available:

```powershell
$pilotEnv = Join-Path $env:LOCALAPPDATA 'Mine2ndMind\semantic-pilot-env'
uv venv --python 3.12 $pilotEnv
$pilotPython = Join-Path $pilotEnv 'Scripts\python.exe'
uv pip install --python $pilotPython -r Atlas/Retrieval/requirements.lock
& $pilotPython Atlas/Retrieval/pilot.py prepare-model
& $pilotPython Atlas/Retrieval/pilot.py build
```

## Checks

```powershell
python -m unittest discover -s Atlas/Retrieval -p 'test_*.py'
& $pilotPython Atlas/Retrieval/pilot.py evaluate
& $pilotPython Atlas/Retrieval/pilot.py segment 'Projects/PDAOK/PDAOK Phases.md'
```

The first ten authored query checks retrieved the expected note first in **8/10** cases and within the top three in **10/10**. One query uses a metadata filter. This is a small, self-authored sanity check against ten curated notes, not independent validation or a comparison with other chunking strategies. Full results are in [[Atlas/Retrieval/Evaluation.json|Evaluation]].
