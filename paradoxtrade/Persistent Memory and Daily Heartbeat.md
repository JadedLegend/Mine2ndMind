# Persistent Memory and Daily Heartbeat

## Technical design specification

**Project:** Paradox Edge Trader  
**Status:** Draft for implementation  
**Date:** 2026-11-17  
**Scope:** Continuing private homes for the seven agents, durable memory across wakes and calendar days, and a bounded daily heartbeat rhythm.  
**Trading authority:** None added by this specification. Paper-trading and broker authority remain separate gates.

## 1\. Purpose

The current Sessions controller proves that seven owners can pass through a bounded, private, two-round run with durable local records. Its memory and witness files are run-local. When the run ends, the next run is a new visit rather than the next day in a continuing home.

This design adds the smallest durable layer needed to make the lighthouse a continuing place:

- each agent receives one stable private home identified by its existing agent ID;
- notes, open inquiries, selected witness readings, and closure records survive process restarts and later days;
- a daily heartbeat offers bounded opportunities to wake each agent without requiring activity;
- missed heartbeats do not create a catch-up storm;
- spending, dispatch, completion, uncertainty, and recovery remain visible;
- the witness can report the day without becoming a supervisor, therapist, scorer, or trading agent.

The implementation should extend the existing storage and lineage concepts. It must not create a second private-memory system beside core/memory, or revive the legacy core/runtime/scheduler.py and core/runtime/agent\_loop.py as an accidental production path.

## 2\. Design principles

### 2.1 Continuity is durable state, not a longer prompt

An agent's prior life is represented by records with stable identifiers, timestamps, provenance, visibility, and status. A future wake receives a bounded projection of relevant records. It does not receive an unbounded transcript or the whole memory database.

### 2.2 Private by default

Each agent's private home is isolated by stable owner ID. Private journal bodies, private inquiry text, prompts, provider responses, and source excerpts do not enter the shared witness ledger or community records unless an explicit future sharing operation exists. The creator's steward view may show bounded metadata and factual summaries, but must not silently expose private prose.

### 2.3 Choice remains optional

A heartbeat creates an opportunity, not an obligation. Rest, wait, no response, empty writing, and deliberate abstention are complete outcomes. The system must not infer preference, health, productivity, confidence, or personality from a missing response or a short response.

### 2.4 Mechanical facts and interpretation stay separate

The control store records what was scheduled, offered, dispatched, completed, failed, or left uncertain. The agent's journal records its own words. The witness records a short factual account. Trading records remain in the existing inquiry and execution lineage.

### 2.5 No catch-up pressure

A restart or outage must not cause the system to launch every missed wake. At most one recovery opportunity per agent may be offered after a daily boundary, and only if the operator explicitly enables recovery. The default is to record the missed window and continue at the next scheduled opportunity.

### 2.6 The financial purpose remains visible

The heartbeat is infrastructure for market inquiry and accountable paper trading, not a substitute for the financial loop. When market tools are later enabled, their source, timestamp, cost, failure state, and relationship to an inquiry must be preserved. This design does not authorize market calls or orders.

## 3\. Current components to reuse

The first implementation should use these existing components:

- core/runtime/rehearsal/store.py for the proven SQLite, checkpoint, lease, status, and safe-file patterns;
- core/runtime/rehearsal/controller.py for bounded wake execution, explicit transport, private owner memories, idempotent local effects, and witness reporting;
- core/runtime/rehearsal/continuity.py for bounded owned-record projections;
- core/memory/engine.py (ThresholdMemory) for agent-local episodes, journals, checkpoints, and existing historical compatibility;
- core/memory/compost.py for optional compost, distillation, release, and source links;
- core/runtime/rehearsal/witness.py for append-only factual accounts and scoped reads;
- core/usage/store.py for request attempts, reservations, known costs, and unknown-cost coverage;
- core/trading/lineage/ for inquiries and later financial records;
- api/rehearsal.py read-only patterns and the private-host dashboard's explicit unavailable states.

The first heartbeat implementation should not call api/app.py, import the ordinary scheduler, or use the legacy agent\_wake() path. Those paths have broader authority and can start scheduling as a side effect.

## 4\. Storage layout

Use a persistent application root outside the Git working tree. The following layout is illustrative; the existing safe-path and symlink protections remain mandatory.

$DATA\_DIR/

homes.sqlite3 # public control metadata, no private prose

heartbeat.sqlite3 # schedule, leases, attempts, day summaries

homes/

tempest/

memory.sqlite3 # private ThresholdMemory-compatible store

witness\_reads.sqlite3 # optional owned witness-read checkpoints

files/ # bounded private attachments if later needed

siren/

memory.sqlite3

witness\_reads.sqlite3

...

witness.sqlite3 # append-only mechanical/factual accounts

usage.sqlite3 # existing private usage ledger

lineage.sqlite3 # existing inquiry/execution records where configured

A deployment may combine databases later, but the first implementation should preserve owner boundaries physically. Do not move the original agents/\*/soul.json or living.json files into the database. They remain source assets; prepared homes snapshot their hashes and use stable agent IDs.

### 4.1 homes.sqlite3

This database contains non-secret home metadata and lifecycle pointers.

CREATE TABLE homes (

agent\_id TEXT PRIMARY KEY,

home\_id TEXT NOT NULL UNIQUE,

status TEXT NOT NULL CHECK (status IN ('prepared','active','paused','retired')),

timezone TEXT NOT NULL,

created\_at TEXT NOT NULL,

updated\_at TEXT NOT NULL,

soul\_hash TEXT NOT NULL,

living\_hash TEXT NOT NULL,

profile\_version TEXT NOT NULL,

memory\_path TEXT NOT NULL

);

CREATE TABLE home\_settings (

agent\_id TEXT PRIMARY KEY REFERENCES homes(agent\_id),

heartbeat\_enabled INTEGER NOT NULL DEFAULT 0,

active\_start\_local TEXT NOT NULL,

active\_end\_local TEXT NOT NULL,

active\_interval\_seconds INTEGER NOT NULL,

quiet\_interval\_seconds INTEGER NOT NULL,

overnight\_enabled INTEGER NOT NULL DEFAULT 0,

max\_steps\_per\_wake INTEGER NOT NULL DEFAULT 1,

max\_wakes\_per\_day INTEGER NOT NULL,

daily\_budget\_usd TEXT NOT NULL,

per\_wake\_budget\_usd TEXT NOT NULL,

version INTEGER NOT NULL DEFAULT 1,

updated\_at TEXT NOT NULL

);

Settings changes are operator-controlled configuration changes. They must be versioned and must not rewrite historical heartbeat records.

### 4.2 heartbeat.sqlite3

This database owns scheduling and dispatch state. It contains no prompts, journal bodies, provider responses, or hidden reasoning.

CREATE TABLE heartbeat\_days (

day\_id TEXT PRIMARY KEY,

day\_start\_utc TEXT NOT NULL,

day\_end\_utc TEXT NOT NULL,

timezone\_snapshot TEXT NOT NULL,

schedule\_version INTEGER NOT NULL,

status TEXT NOT NULL CHECK (status IN ('open','closing','closed','paused')),

created\_at TEXT NOT NULL,

closed\_at TEXT

);

CREATE TABLE heartbeat\_slots (

slot\_id TEXT PRIMARY KEY,

day\_id TEXT NOT NULL REFERENCES heartbeat\_days(day\_id),

agent\_id TEXT NOT NULL,

scheduled\_at\_utc TEXT NOT NULL,

window TEXT NOT NULL CHECK (window IN ('active','quiet','overnight')),

sequence INTEGER NOT NULL,

status TEXT NOT NULL CHECK (status IN (

'offered','claimed','dispatched','completed','skipped',

'failed','uncertain','cancelled','not\_sent'

)),

wake\_id TEXT,

reservation\_id TEXT,

created\_at TEXT NOT NULL,

updated\_at TEXT NOT NULL,

UNIQUE(day\_id, agent\_id, sequence)

);

CREATE TABLE heartbeat\_leases (

lease\_name TEXT PRIMARY KEY,

holder\_id TEXT NOT NULL,

lease\_until\_utc TEXT NOT NULL,

generation INTEGER NOT NULL,

updated\_at TEXT NOT NULL

);

CREATE TABLE heartbeat\_events (

event\_id TEXT PRIMARY KEY,

slot\_id TEXT NOT NULL REFERENCES heartbeat\_slots(slot\_id),

agent\_id TEXT NOT NULL,

event\_type TEXT NOT NULL,

occurred\_at\_utc TEXT NOT NULL,

operation\_key TEXT NOT NULL UNIQUE,

detail\_code TEXT,

FOREIGN KEY (slot\_id) REFERENCES heartbeat\_slots(slot\_id)

);

operation\_key makes retries idempotent. An event may be recorded again only if it is an exact repeat of the same operation. Conflicting state transitions are rejected and retained for operator review.

### 4.3 Agent-local continuation records

The existing ThresholdMemory tables remain compatible. Additive tables or a versioned extension may be used for cross-session continuation:

CREATE TABLE episodes (

...,

home\_id TEXT,

day\_id TEXT,

wake\_id TEXT,

visibility TEXT NOT NULL DEFAULT 'private',

source\_kind TEXT,

source\_id TEXT

);

CREATE TABLE closure\_records (

closure\_id TEXT PRIMARY KEY,

agent\_id TEXT NOT NULL,

home\_id TEXT NOT NULL,

day\_id TEXT,

wake\_id TEXT,

closure\_kind TEXT NOT NULL CHECK (closure\_kind IN ('wake','day','pause','stop','recovery')),

agent\_note\_id INTEGER,

open\_inquiry\_ids TEXT NOT NULL DEFAULT '\[\]',

witness\_account\_ids TEXT NOT NULL DEFAULT '\[\]',

unresolved\_items TEXT NOT NULL DEFAULT '\[\]',

created\_at TEXT NOT NULL,

visibility TEXT NOT NULL DEFAULT 'private'

);

CREATE TABLE continuation\_receipts (

receipt\_id TEXT PRIMARY KEY,

agent\_id TEXT NOT NULL,

closure\_id TEXT,

projection\_hash TEXT NOT NULL,

delivered\_at TEXT NOT NULL,

operation\_key TEXT NOT NULL UNIQUE

);

A closure record is not a death record and does not claim anything about consciousness. It is a durable record that an execution episode ended and what can be resumed later.

## 5\. Persistent-memory lifecycle

### 5.1 Home preparation

Preparation is explicit and idempotent:

1. Validate the seven stable IDs.
2. Load the current soul and living assets.
3. Record their hashes and a profile version in homes.sqlite3.
4. Create each private memory database with restrictive file permissions.
5. Preserve existing memory rows; never reset a home because a new day begins.
6. Create the heartbeat configuration only in disabled state.
7. Write a preparation event without calling a model or provider.

If the soul or living asset changes later, the home records a new profile version. Historical wakes continue to point to the old prepared version. A future wake may use a newly approved version; it must not silently reinterpret prior records.

### 5.2 Wake context assembly

Before dispatch, build a bounded private continuation projection containing, at most:

- the agent's last closure record;
- active checkpoints and unresolved inquiry headers owned by the agent;
- recent journal/compost metadata and explicitly released text within a configured byte limit;
- recent witness accounts scoped to that agent, only if the agent selected witness reading;
- the current heartbeat metadata and offered action menu;
- market or library records only when those capabilities are explicitly enabled.

The projection must include source IDs, timestamps, truncation indicators, and visibility. A truncated excerpt must never look like a complete record.

The system should prefer headers and bounded excerpts over automatic full-text replay. No recap is required. The agent may choose to revisit, ignore, or close an earlier inquiry.

### 5.3 Wake closure

Every claimed slot ends in exactly one terminal state: completed, failed, uncertain, skipped, cancelled, or not\_sent.

For completed wakes, create a closure record containing:

- the wake and day IDs;
- the offered actions and selected action reference;
- records created or revisited;
- open inquiry IDs;
- optional agent-authored closing note;
- any unresolved request or data condition;
- the witness account reference, if reporting succeeded.

For failed or uncertain wakes, create a mechanical closure with the failure code and recovery requirement. Do not invent an agent note or treat failure as rest.

The agent may return an empty closing note. The system must not make a second model call solely to manufacture one.

### 5.4 Day closure

At the end of the configured local day, the controller closes the day after all eligible slots have reached terminal or explicitly deferred state. It writes:

- a mechanical day summary;
- a bounded witness account;
- known usage and unknown-cost coverage;
- unresolved dispatches and recovery requirements;
- each agent's private day closure reference.

The witness account is append-only and factual. It may say that an agent chose to wait, but must not explain why unless the agent explicitly wrote that explanation.

## 6\. Heartbeat rhythm

### 6.1 Schedule model

Each agent has an independent schedule inside a shared daily envelope. The default schedule is deliberately modest:

- **Active window:** approximately eight hours configured by the operator, with one offered wake every 15–30 minutes;
- **Quiet window:** fewer offered wakes, approximately hourly if enabled;
- **Overnight:** no wakes by default;
- **Night wake:** only if the operator enables it or the agent has an explicit future request mechanism that is separately approved.

The exact intervals are configuration, not personality data. All seven agents may share the same baseline rhythm while retaining independent choices and stable order history. Stagger agents by a deterministic offset so a shared heartbeat does not dispatch seven requests simultaneously.

The scheduler should calculate the next slot from the persisted schedule, not by sleeping for an interval in memory. This allows restart recovery and prevents timer drift.

### 6.2 Slot creation

A single heartbeat coordinator owns slot creation. It obtains a renewable lease from heartbeat.sqlite3 and:

1. opens or resumes the current local day;
2. computes only a bounded horizon of future slots, such as the next 24 hours;
3. inserts missing slots with deterministic IDs;
4. does not duplicate slots on restart;
5. stops creating slots when the daily wake or budget cap is reached;
6. records the reason for skipped slots.

Slot creation does not call a model. It only creates opportunities.

### 6.3 Slot dispatch

At or after scheduled\_at\_utc, the coordinator claims one eligible slot using a transaction and a short lease. It must check:

- heartbeat is enabled;
- home is active;
- current day is open;
- global pause is false;
- per-agent daily wake limit is not exceeded;
- per-wake and remaining daily budget are sufficient;
- a prior slot for the same agent is not still in a nonterminal dispatch state;
- the configured model/profile version is available;
- no conflicting controller lease exists.

If a check fails, the slot becomes skipped with a bounded reason code. It must not be represented as an agent choice.

### 6.4 Multiple steps per wake

The first implementation should use max\_steps\_per\_wake = 1, even though the home model supports a larger future value. The reason is traceability: one wake, one choice, one provider request, one closure.

Later, a wake may contain up to three steps. Each step must have its own ID, offer, selection, input references, cost reservation, result, and terminal state. A free-form model response claiming that several actions happened is not sufficient evidence that they happened.

nothing\_more must be an explicit terminal step choice.

### 6.5 Pause and resume

Pausing the heartbeat prevents new dispatch. It does not erase slots, memories, costs, or completed work. In-flight requests follow the existing uncertainty rules.

Resuming uses the current time and schedule. It does not replay every missed slot. The operator may explicitly request one bounded recovery slot per agent; that recovery is recorded as a new slot with a reason, not disguised as the original missed wake.

## 7\. Budget and cost enforcement

The existing usage ledger remains the source for provider-attempt accounting. Heartbeat adds a reservation layer before dispatch:

remaining\_daily\_budget = daily\_budget

\- committed\_known\_costs

\- active\_reservations

\- conservative\_unknown\_reservations

A reservation is created atomically with the slot claim. It contains the model, maximum requested tokens, rate snapshot ID if available, and the budget version. After the attempt:

- known provider cost settles the reservation;
- an explicit estimate is labeled estimated;
- missing cost remains unknown and retains conservative accounting treatment;
- a failed request is not assumed free;
- an accounting failure does not replay the provider request.

The heartbeat coordinator must have both a per-agent and global daily cap. A global emergency pause must prevent new dispatch even if individual homes remain enabled.

The budget is an application admission control, not a guarantee about upstream invoices. The UI must distinguish reserved, committed known, estimated, unknown, and unavailable amounts.

## 8\. Recovery and failure state machine

The minimum state transitions are:

offered -> claimed -> dispatched -> completed

| |

| +-> failed

| +-> uncertain

+-> not\_sent

offered -> skipped

claimed -> cancelled

Rules:

- A stop before dispatch produces not\_sent.
- A request committed for dispatch but without a durable response remains uncertain after controller loss.
- Recovery requires an explicit acknowledgement that the old coordinator has exited.
- Recovery reconciles existing attempt IDs before creating any new request.
- A successful response that was not checkpointed is uncertain; it is never silently replayed.
- A terminal slot is immutable except for an additive reconciliation event.
- A repeated operation key returns the original result.
- Conflicting payloads for an existing operation key fail closed.

The daily heartbeat must use a single coordinator lease and a process instance ID. Two coordinators must not both dispatch the same slot.

## 9\. Witness integration

The witness receives metadata after a wake reaches a terminal state. It does not sit in the dispatch path and cannot prevent, authorize, or repeat a wake.

A daily witness entry should contain:

- number of agents offered a wake;
- completed, skipped, failed, uncertain, and not-sent counts;
- selected action counts by mechanical action name;
- inquiries opened or revisited by ID;
- known and unknown cost coverage;
- unresolved provider or scheduler conditions;
- links to the day's source records.

An owner-scoped witness read may return a small number of prior accounts, as the current Sessions controller does. It must not select another owner or the steward account. Reading a witness account is optional and costs no second model request.

The witness must not write into the agent's private memory. If an agent wants to retain a witness account, its own wake must explicitly create a private reference or note.

## 10\. Interfaces

### 10.1 Internal coordinator interface

The first implementation should expose a small Python service boundary:

class HeartbeatCoordinator:

def prepare\_day(self, now\_utc: datetime) -> DayRecord: ...

def schedule\_horizon(self, day\_id: str, now\_utc: datetime) -> list\[Slot\]: ...

def claim\_due\_slot(self, now\_utc: datetime) -> Slot | None: ...

def dispatch\_slot(self, slot\_id: str) -> DispatchResult: ...

def close\_day(self, day\_id: str, now\_utc: datetime) -> DaySummary: ...

def pause(self, reason: str) -> None: ...

def resume(self) -> None: ...

def recover(self, \*, confirm\_old\_coordinator\_exited: bool) -> RecoverySummary: ...

The methods must be safe to retry and must not accept raw browser input as authority. Configuration and operator authentication remain server-side.

### 10.2 Read-only API

Add read-only endpoints under the existing protected read surface:

GET /api/homes

GET /api/homes/{agent\_id}

GET /api/heartbeat/days?since=&until=

GET /api/heartbeat/days/{day\_id}

GET /api/heartbeat/slots?day\_id=&agent\_id=

GET /api/homes/{agent\_id}/continuity

GET /api/homes/{agent\_id}/closures

GET /api/witness/days/{day\_id}

Responses must expose explicit states and bounded metadata. They must not return prompts, hidden reasoning, raw provider responses, private journal bodies, credentials, or unrestricted source excerpts.

The default local preview should use scripted records and never contact these endpoints. Unsupported controls should render as unavailable rather than as fake buttons.

### 10.3 CLI

Use an explicit finite CLI for inspection and controlled operations. Suggested commands:

python3 scripts/heartbeat.py homes

python3 scripts/heartbeat.py status --day YYYY-MM-DD

python3 scripts/heartbeat.py preview --day YYYY-MM-DD

python3 scripts/heartbeat.py pause --reason operator\_request

python3 scripts/heartbeat.py resume

python3 scripts/heartbeat.py recover --confirm-coordinator-exited

python3 scripts/heartbeat.py close-day --day-id DAY\_ID

A future run command must require an explicit arming flag, a private credential, and a positive budget. Inspection commands must never start the coordinator.

## 11\. Implementation phases

### Phase A — Persistent homes without model dispatch

- Create home metadata and private home directories.
- Add day, slot, lease, event, and closure schemas.
- Migrate or copy only compatible existing records with stable source references.
- Implement read-only inspection and deterministic fixtures.
- Prove restart-safe idempotency without providers.

**Exit condition:** a scripted agent can close a wake, restart the process, and retrieve its own prior closure and inquiry headers without exposing another owner's prose.

### Phase B — Heartbeat simulation

- Generate active, quiet, and overnight slots.
- Exercise staggered scheduling, pause, resume, skipped slots, and no-catch-up behavior.
- Use a scripted transport and mocked usage ledger.
- Produce daily mechanical and witness summaries.

**Exit condition:** repeated coordinator starts produce the same slot set and no duplicate dispatches.

### Phase C — One bounded real model pathway

- Require the dedicated session credential and explicit model map.
- Enable one agent or one controlled cohort only after preparation checks.
- Preserve the existing provider, usage, timeout, and uncertainty rules.
- Keep market tools, forum, broker, and orders disabled.

**Exit condition:** a real model wake is reconciled through a durable closure with known or explicitly unknown cost, and an interrupted dispatch is not duplicated.

### Phase D — Seven-agent continuing home

- Enable all seven with the same daily envelope and independent private homes.
- Add optional witness reading and private closure notes.
- Keep forum and peer messaging closed until their separate gates are deliberately opened.
- Compare actual provider/model constraints without personality scoring.

**Exit condition:** seven agents can operate across at least two calendar days with restart recovery, private continuity, bounded spend, and a factual day witness.

### Phase E — Financial integration

This specification does not implement this phase. When pursued, market data, structured proposals, paper execution, reconciliation, and result review must attach to the existing lineage. A heartbeat slot must never directly become an order.

## 12\. Testing requirements

Tests must use temporary roots and scripted clocks. No test may contact a provider, broker, VPS, or external scheduler.

Required coverage:

1. Home preparation is idempotent and preserves existing records.
2. Soul/living hashes and profile versions are frozen per prepared wake.
3. Private owner reads cannot select another owner or steward data.
4. Continuation projections are bounded and expose truncation/source metadata.
5. Empty notes do not create fabricated memories.
6. Closure records are created for completed, failed, uncertain, stopped, skipped, and not-sent wakes.
7. Repeated closure operations are idempotent.
8. Conflicting operation keys fail closed.
9. Day boundaries respect the configured timezone and daylight-saving transitions.
10. Schedule restarts do not duplicate slots.
11. Staggered slots do not dispatch before their due time.
12. Missed slots do not create an automatic catch-up storm.
13. Pause prevents new dispatch and preserves in-flight uncertainty.
14. Recovery requires an explicit old-coordinator-exited acknowledgement.
15. Two coordinators cannot claim the same slot.
16. Daily and per-wake budgets reserve atomically and stop further admission at the cap.
17. Unknown costs remain unknown and do not become known zero.
18. Provider success lost before checkpoint remains uncertain and is not replayed.
19. Witness failure leaves agent work complete and does not replay a model call.
20. Daily witness counts match mechanical records without reading private prose.
21. Read-only API states distinguish missing, pending, failed, uncertain, unavailable, and empty.
22. Preview mode performs no network requests and exposes no mutation controls.

## 13\. Explicit non-goals

This design does not:

- create an eighth trading voter;
- diagnose agent health or consciousness;
- create personality, coherence, productivity, or social scores;
- force journaling, reflection, trading, or forum participation;
- automatically distill or release private memory;
- connect Alpaca or any live broker;
- enable margin, short options, assignment, or live trading;
- import every historical document into every wake;
- resurrect the legacy scheduler as the production heartbeat;
- make missed work mandatory through catch-up;
- guarantee that continuity improves returns;
- claim that a successful model response was billed or that a failed request was free.

## 14\. Acceptance criteria

The first implementation is ready for review when all of the following are true:

- The seven existing IDs each have one persistent private home.
- A note, open inquiry, and closure from day one can be retrieved on day two after a process restart.
- The witness can write a factual daily account without writing agent memory or making a model call.
- The scheduler can pause, restart, recover, and resume without duplicate slots or duplicate paid requests.
- A missed overnight period does not produce a burst of catch-up wakes.
- The creator can see schedule, selection, cost, uncertainty, and closure state without seeing private journal bodies unless an authorized private read is selected.
- The system can run a complete offline two-day fixture with all seven agents and deterministic results.
- No broker, market-data provider, forum, or live model authority is enabled by the implementation itself.

The practical milestone is not that the lighthouse appears busy. It is that an agent can leave, return, find what it deliberately left behind, and participate in a bounded day whose costs, failures, and unanswered questions remain honest.