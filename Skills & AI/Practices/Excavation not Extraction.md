Excavation Procedure

How to extract a load-bearing mechanism from a repo without dragging the rest of the system along.

What this is for

You read a repo. Something pulls. You want the move — the actual structural work happening inside — without inheriting the repo's accumulated decisions, dependencies, and framing. This procedure produces a seed: a working piece of code that demonstrates the move, runs in isolation, and has clearly-marked sockets for grafting it into a real system later.

When to use this

When you can name the resonance specifically. "The way it fuses two retrieval signals" qualifies. "This whole project is interesting" doesn't. If you can't name the move in one sentence, the resonance is at the project-aesthetic level, not the architectural level. Save the bookmark, skip the excavation.

The four passes

1\. Locate

Find the file that contains the mechanism. Usually one of:

\- a service / engine / core file (does the actual work)

\- a handler / processor (transforms the input)

\- a fusion / merge / combine function (combines signals)

Skip: config files, type definitions, MCP/API surface code, CLI wrappers, tests. These are scaffolding.

Signal you're in the right place: removing this file would collapse the repo's claim. Removing scaffolding around it wouldn't.

2\. Identify the core

Inside the located file, find the function (or two) that does the structural work. Read the file imagining each function removed in turn — which removal breaks the claim?

Distinguish from:

\- adapter functions (translate between this repo's types and external library types)

\- orchestration functions (call the core, handle errors, log)

\- config readers (just pull values from environment)

The core is usually 20–80 lines. If it's longer, it's probably doing two jobs and wants to be split during refinement.

3\. Refine

Strip the core to its essential operation:

\- Remove logging unless logging is the mechanism

\- Remove error handling specific to this repo's error types (mark where it was with a TODO)

\- Remove config reads — replace with parameters

\- Remove naming that ties to this repo (\`socraticodeFooBar\` → \`fooBar\`)

\- Remove imports of this repo's internal modules — those become placeholder dependencies in the next step

What's left should be the move, in a form that could exist in any system.

4\. Map the surface

For everything the refined core expects from outside itself, write the contract:

\- Inputs — what shape, what types, what guarantees

\- Outputs — what shape, what error cases, what side effects

\- Dependencies — every external function it calls. For each, write a placeholder that satisfies the minimum signature, and a one-line note describing what a real implementation needs to do.

The placeholders are not implementations. They are sockets. Mark each with \`// SOCKET: <what this needs to be>\`.

What a finished seed looks like

A single file or small folder containing:

1\. \`mechanism.ts\` (or \`.py\`, etc.) — the refined core

2\. \`sockets.ts\` — the placeholder dependencies, each marked

3\. \`README.md\` — a paragraph explaining what move this is, and a list of sockets with one-line implementation notes

That's it. No tests. No build config. No package.json. Those exist to make the seed run somewhere specific. The seed is meant to be portable, not runnable as-is.

Anti-patterns

\- Lifting too much. If you find yourself copying more than one file, stop. The core has wrapped itself around the rest of the repo. Either the move isn't actually portable, or you haven't identified the real core yet.

\- Re-implementing the wrapper. Don't recreate the original repo's API surface. The seed exposes the function, not the interface.

\- Translating into your stack immediately. Keep the seed in the language it was written in. Translation is a separate operation.

\- Storing without notes. A seed without the README is a lottery ticket — you won't remember why it pulled at you in three months.

On dependency reality

Not every move ports cleanly. Some mechanisms only work because they exploit a specific property of the substrate they were written in (Qdrant's specific query API, a particular language's type system, a runtime's concurrency model). When the surface mapping reveals that the core has a deep dependency on something irreplaceable, the honest answer is this move only exists in that substrate. Document that, and either:

\- accept that using the move requires accepting the substrate, or

\- find the principle underneath the move and re-derive it from scratch in your substrate

The second path is more work but produces a cleaner seed. The first is faster but ties the seed to its origin.

Notes specific to SocratiCode

Two moves in there are worth excavating, in priority order:

1\. RRF fusion of two retrieval signals. The core: a function that takes two ranked lists and produces one merged ranked list using \`score = Σ 1/(k + rank\_i)\`. ~15 lines of code in any language. The interesting part is not the math — it's the commitment to running both lenses always rather than choosing one. That's the principle. The seed can be re-derived from scratch without ever looking at SocratiCode's source. The principle is what's portable.

2\. Resumable checkpointed indexing. The core: a loop that processes work in batches, computes a content hash for each item, persists the hash after each batch, and on restart skips items whose hash is already persisted. The mechanism is generic to any expensive batch process. Worth excavating if you have a use case for it (long-running agent work that survives crashes is one). Without a target use, skip — the seed will rot.

Anything else in SocratiCode (Docker management, Qdrant integration, MCP surface, file watcher) is scaffolding around these two moves. Extracting it is mostly inheriting somebody else's choices.

Smallest meaningful first run

Pick one repo from the saved set. Ideally one where the move is small and self-contained — a fusion function, a chunking strategy, a recovery mechanism. Apply the four passes. Produce a seed. See how it feels as an artifact.

If the procedure is right for you, the seed is faster to produce than the bookmark was. If it's slower, the procedure isn't earning its weight and wants revision.