# Heartbeat Clock on the DigitalOcean Droplet

## Implementation plan

**Project:** Paradox Edge Trader  
**Host:** DigitalOcean EdgeTrader, Ubuntu 24.04, NYC3  
**Status:** Deployment plan only; no remote changes performed  
**Related design:** [Persistent Memory and Daily Heartbeat](PERSISTENT_MEMORY_AND_HEARTBEAT.md)  
**Trading authority:** None. This plan does not connect Alpaca, enable orders, or start model-powered agents.

## 1\. Objective

Install a small, restart-safe clock on the prepared DigitalOcean host that can eventually create and dispatch due heartbeat slots for the seven private homes.

The first installed version must be **clock-only and paused**. It may:

- inspect the persistent heartbeat database;
- create or reconcile a bounded schedule;
- record due, skipped, paused, and recovery states;
- expose local status for the read-only dashboard or operator CLI;
- run deterministic offline fixtures.

It must not initially:

- call an LLM provider;
- read or use an ambient Manus credential;
- connect to market-data services;
- connect to Alpaca;
- submit a trade or proposal;
- open the forum or peer messaging;
- start the legacy application scheduler;
- expose a public HTTP port.

The first remote milestone is therefore **a durable, inspectable clock**, not autonomous activity.

## 2\. Why use a systemd timer plus finite tick

Use a systemd timer to invoke a short heartbeat tick command approximately once per minute. Do not begin with a resident Python loop and do not reuse core/runtime/scheduler.py.

A finite tick is preferable on this one-vCPU host because:

- systemd owns process restart and logging;
- a process crash cannot leave an in-memory scheduler believing it owns time;
- the database lease prevents duplicate ticks if a second invocation overlaps;
- a restart does not require reconstructing a sleep interval;
- the tick can calculate due slots from persisted UTC timestamps;
- Persistent=false prevents systemd from replaying every missed timer event after downtime;
- the application itself can record that a time window was missed without launching catch-up wakes.

The timer is only a clock signal. The application remains responsible for schedule calculation, leases, budgets, pause state, and slot transitions.

## 3\. Host layout

Use the locations already prepared in the VPS handoff, with one explicit addition for the continuing-home data:

/opt/paradoxtrader/

releases/<release-id>/ # immutable extracted releases

current -> releases/<release-id>

/etc/paradoxtrader/

heartbeat.env # root-owned, mode 0600, initially disabled

heartbeat-policy.json # non-secret policy, root-owned

/var/lib/paradoxtrader/

homes.sqlite3

heartbeat.sqlite3

witness.sqlite3

usage.sqlite3

lineage.sqlite3 # when the financial lineage is enabled

homes/<agent-id>/memory.sqlite3

heartbeat/ # optional local runtime markers

migrations/ # applied migration receipts

/var/log/paradoxtrader/

heartbeat-status.json # bounded latest status, no private prose

/var/backups/paradoxtrader/

... # local SQLite backups, separate from provider backups

/run/paradoxtrader/

heartbeat.tick # optional transient marker, not source of truth

The application release and data directory must be separate. A release replacement must not replace or delete /var/lib/paradoxtrader.

The application user paradoxtrader owns the data and release runtime files. Root owns service definitions and the secret environment file. SSH remains key-only and UFW remains closed to all inbound ports other than the already-approved OpenSSH path.

## 4\. Required application entry point

Add a finite command with no import-time side effects:

python3 -m scripts.heartbeat tick

The command must:

1. load the root path and policy from explicit arguments or the service environment;
2. acquire the database-backed coordinator lease;
3. open or reconcile the current local day;
4. create only the configured schedule horizon;
5. mark stale offered slots as skipped according to policy;
6. identify due slots;
7. stop at the first implementation's clock\_only dispatch boundary;
8. write bounded status and event records;
9. release the lease;
10. exit with a useful systemd status code.

Suggested command modes:

python3 -m scripts.heartbeat tick --mode clock-only

python3 -m scripts.heartbeat status --json

python3 -m scripts.heartbeat pause --reason operator\_request

python3 -m scripts.heartbeat resume

python3 -m scripts.heartbeat recover --confirm-old-coordinator-exited

python3 -m scripts.heartbeat close-day --day-id DAY\_ID

status, pause, resume, and recover must be separate explicit operations. The timer must never infer that it is authorized to resume a paused system.

The command must not import api/app.py. The broader backend can start the legacy scheduler as a side effect and is not the heartbeat entry point.

## 5\. Service account and filesystem permissions

Create or reuse the locked-password paradoxtrader user. Apply these permissions:

/etc/paradoxtrader/heartbeat.env root:paradoxtrader 0640

/etc/paradoxtrader/heartbeat-policy.json root:paradoxtrader 0640

/opt/paradoxtrader paradoxtrader:paradoxtrader 0750

/var/lib/paradoxtrader paradoxtrader:paradoxtrader 0700

/var/backups/paradoxtrader root:paradoxtrader 0750

/var/log/paradoxtrader paradoxtrader:paradoxtrader 0750

Private home databases should be mode 0600. Parent directories must reject unsafe pre-existing symlinks using the same protections already used by the Sessions store.

The service must never write prompts, provider responses, journal bodies, or API keys to journald. Python exceptions should be converted to bounded error codes in the application status record; systemd logs may contain a unit failure and timestamp, not private payloads.

## 6\. Environment and policy

Initial /etc/paradoxtrader/heartbeat.env should contain only non-secret runtime settings and an explicit disabled state:

PARADOXTRADER\_ROOT=/opt/paradoxtrader/current

PARADOXTRADER\_DATA\_DIR=/var/lib/paradoxtrader

PARADOXTRADER\_HEARTBEAT\_MODE=clock-only

PARADOXTRADER\_HEARTBEAT\_ENABLED=false

PARADOXTRADER\_ALLOW\_REAL\_MODELS=false

PARADOXTRADER\_ALLOW\_MARKET\_DATA=false

PARADOXTRADER\_ALLOW\_BROKER=false

PARADOXTRADER\_LOG\_LEVEL=INFO

Do not put OPENROUTER\_API\_KEY, Alpaca credentials, Graphify credentials, or any other provider secret in this file during clock-only installation. The first implementation should fail closed if a provider credential is present but the corresponding authority flag is false.

The policy file should define:

{

"timezone": "America/New\_York",

"active\_start\_local": "09:00",

"active\_end\_local": "17:00",

"active\_interval\_seconds": 1800,

"quiet\_interval\_seconds": 3600,

"overnight\_enabled": false,

"max\_steps\_per\_wake": 1,

"max\_wakes\_per\_day": 16,

"per\_wake\_budget\_usd": "0.00",

"daily\_budget\_usd": "0.00",

"catch\_up": "never",

"dispatch\_mode": "clock-only"

}

These are implementation defaults for a disabled clock, not a financial allocation or a promise about the creator's intended future schedule. A real model budget must be selected deliberately later.

## 7\. systemd units

Install a dedicated oneshot service:

\# /etc/systemd/system/paradoxtrader-heartbeat.service

\[Unit\]

Description=Paradox Edge Trader heartbeat tick

Wants=paradoxtrader-heartbeat.timer

After=local-fs.target

ConditionPathIsDirectory=/var/lib/paradoxtrader

\[Service\]

Type=oneshot

User=paradoxtrader

Group=paradoxtrader

EnvironmentFile=/etc/paradoxtrader/heartbeat.env

WorkingDirectory=/opt/paradoxtrader/current

ExecStart=/opt/paradoxtrader/venv/bin/python -m scripts.heartbeat tick --mode clock-only

NoNewPrivileges=true

PrivateTmp=true

ProtectSystem=strict

ProtectHome=true

ReadWritePaths=/var/lib/paradoxtrader /var/log/paradoxtrader /run/paradoxtrader

UMask=0077

TimeoutStartSec=45s

Install a timer that does not replay missed invocations:

\# /etc/systemd/system/paradoxtrader-heartbeat.timer

\[Unit\]

Description=Paradox Edge Trader heartbeat clock

\[Timer\]

OnBootSec=2min

OnUnitActiveSec=60s

AccuracySec=5s

RandomizedDelaySec=5s

Persistent=false

Unit=paradoxtrader-heartbeat.service

\[Install\]

WantedBy=timers.target

The timer may be enabled for clock-only operation after offline verification. It must not be enabled by the release installer while PARADOXTRADER\_HEARTBEAT\_ENABLED=false unless the tick explicitly supports a harmless paused status. A paused clock may be useful for status and migration checks, but its behavior must be documented.

The installer must run systemctl daemon-reload and systemctl enable --now paradoxtrader-heartbeat.timer only after a preflight check. It must not enable the old application service or api/app.py.

## 8\. Preflight checks before enabling the timer

The installation script should fail closed unless all checks pass:

1. Ubuntu version and architecture are supported.
2. The release archive checksum matches the expected release manifest.
3. The release directory is not the Git working tree.
4. Python virtual environment exists and imports the heartbeat module.
5. SQLite databases can be created and reopened by paradoxtrader.
6. Data directories have expected owner and mode.
7. Existing path components are not unsafe symlinks.
8. The policy parses and uses a valid IANA timezone.
9. heartbeat\_enabled is false for the first installation.
10. Real-model, market-data, and broker flags are all false.
11. No provider credentials are required by clock-only mode.
12. The heartbeat database migration is idempotent.
13. The status command returns paused or clock\_only without external network access.
14. The systemd unit has the expected User, WorkingDirectory, ExecStart, and write paths.
15. The old scheduler is not enabled or running.

The preflight must not contact a model provider, data provider, broker, Graphify, or any external service.

## 9\. Deployment sequence

### Stage 0 — Local implementation and fixture verification

Implement the heartbeat command and schemas in a review branch. Run unit tests with a temporary data root and a fake clock. Verify that two ticks at the same timestamp create one slot set and one lease transition.

### Stage 1 — Release preparation

Build the normal release archive from a clean commit. Include migrations, the heartbeat command, systemd templates, an operator runbook, and tests. Do not include local databases, .env files, keys, journal bodies, or provider responses.

### Stage 2 — Host inspection only

Connect through the owner-controlled SSH key. Inspect Ubuntu, disk, memory, existing users, UFW, service state, and the staged archive. Confirm the droplet still has no application service or prepared session. Do not start the application.

### Stage 3 — Install clock-only files

Install the release, venv, directories, user permissions, migration, policy, and units. Run migrations and offline preflight. Run one manual:

sudo -u paradoxtrader /opt/paradoxtrader/venv/bin/python \\

\-m scripts.heartbeat tick --mode clock-only

Inspect the resulting status and SQLite rows. This should create no provider attempt and no agent wake.

### Stage 4 — Enable the timer while paused

Enable only paradoxtrader-heartbeat.timer. Allow several ticks to run. Confirm:

- no external network connection is attempted;
- no model call occurs;
- no broker call occurs;
- no duplicate slots or events appear;
- the service exits successfully;
- journald output contains no private text;
- paused status remains visible;
- a reboot does not create a catch-up burst.

### Stage 5 — Read-only inspection

Install or separately enable the already planned loopback-only dashboard gateway only after its pending 404 and backup-staging fixes are complete. Keep any operator authentication server-side. The dashboard should show heartbeat state as paused/clock-only and should not render a wake or resume mutation button until that control is explicitly implemented and protected.

### Stage 6 — Future clock arming

Only after offline and host verification should the creator decide whether to enable schedule creation for the seven homes. This still does not grant model, market, or broker authority. The first armed clock should use zero-dollar budget and clock-only dispatch until the durable home implementation is proven across two calendar days.

### Stage 7 — Future model commissioning

Model commissioning is a separate change with a separate review. It requires a dedicated provider credential, exact model map, positive operator-selected budget, explicit arming, and a dry-run/one-agent plan. The clock service must remain capable of running in paused or clock-only mode without those credentials.

## 10\. Operations and safety controls

### Pause

The normal emergency action is an application pause recorded in heartbeat.sqlite3, followed by stopping the timer if necessary:

sudo -u paradoxtrader /opt/paradoxtrader/venv/bin/python \\

\-m scripts.heartbeat pause --reason operator\_request

sudo systemctl stop paradoxtrader-heartbeat.timer

Stopping systemd is a second barrier. The database pause is the durable source of truth and should be performed first when the CLI is healthy.

### Resume

Resume must be deliberate and must not create missed-slot catch-up:

sudo -u paradoxtrader /opt/paradoxtrader/venv/bin/python \\

\-m scripts.heartbeat resume

sudo systemctl start paradoxtrader-heartbeat.timer

The command should report how many slots remain due, skipped, uncertain, or deferred before the timer is started.

### Status

Useful inspection commands:

systemctl status paradoxtrader-heartbeat.timer

systemctl list-timers paradoxtrader-heartbeat.timer

journalctl -u paradoxtrader-heartbeat.service --since today --no-pager

sudo -u paradoxtrader /opt/paradoxtrader/venv/bin/python \\

\-m scripts.heartbeat status --json

Status output should include the current day, mode, pause state, last successful tick, lease state, due slot count, skipped count, uncertain count, and budget coverage. It must not include prompts, journal contents, provider responses, or secrets.

### Failure response

- If the tick fails before acquiring a lease, systemd records the failed unit and the next tick retries.
- If the lease is held by a live coordinator, the tick exits without dispatch.
- If a lease is expired, recovery requires the application’s explicit stale-lease rules; systemd must not force-delete it.
- If SQLite is unavailable, no slot is treated as dispatched.
- If a migration is incomplete, the service remains paused and reports a bounded migration error.
- If the host clock is invalid or time jumps backward, the coordinator records the anomaly and refuses unsafe slot dispatch.
- If the host reboots, the nonpersistent timer does not replay all missed ticks.
- If disk space is low, the service pauses new writes before databases become corrupted.

## 11\. Backups and persistence

Use the existing local SQLite backup helper only after its pending staging-cleanup and explicit-handle fixes are completed. Back up the control, heartbeat, witness, usage, lineage, and home databases with SQLite's backup API, not by copying live database files blindly.

A local backup is not an atomic snapshot across all databases. The backup manifest must include:

- database path;
- backup timestamp;
- SQLite integrity-check result;
- source file size and hash;
- backup file size and hash;
- schema/migration version;
- whether any database was unavailable.

Provider disk backups and local SQLite backups serve different purposes. The local backup should be retained outside the active data directory and should not contain secrets in filenames or logs. An offsite copy remains a separate future decision.

Do not back up the repository working tree as a substitute for the private data directory. Do not put private home databases, witness databases, or usage ledgers in Git.

## 12\. Verification matrix

The first host verification should prove the following without any provider credential:

| Check | Expected result |
| --- | --- |
| Import heartbeat module | Succeeds in the release venv |
| Manual clock-only tick | Exits 0 and writes bounded status |
| Repeated same-time tick | No duplicate slots or events |
| Timer status | Enabled only for the heartbeat timer |
| Legacy scheduler | Not running or enabled |
| Network inspection | No provider or broker connection |
| Agent home state | Prepared/paused; no model wake |
| Journal state | No synthetic notes created by the clock |
| Witness state | Only mechanical clock/status facts, if configured |
| Reboot | No catch-up burst |
| Pause | New slots are not dispatched |
| Resume | Continues from current time without replay |
| Lease contention | Second tick exits safely |
| Database integrity | All SQLite databases pass integrity checks |
| Dashboard | Read-only and explicit about paused/clock-only state |

A later two-day offline fixture should run against the same code and schema as the droplet release. It should exercise all seven homes, active and quiet windows, process interruption, stale lease recovery, day closure, witness reporting, and cost-free clock operation.

## 13\. Rollback

Rollback must be a release change, not a data deletion:

1. pause the heartbeat in the database;
2. stop and disable only the heartbeat timer;
3. preserve /var/lib/paradoxtrader unchanged;
4. point /opt/paradoxtrader/current to the prior immutable release;
5. run read-only migration compatibility checks;
6. restart no service until the status command succeeds;
7. keep the failed release, logs, and migration receipt for review.

Never roll back by deleting heartbeat rows, homes, witness accounts, usage records, or inquiry lineage. If a schema rollback is unsafe, keep the data and deploy a forward-compatible reader or restore into a disposable copy for investigation.

## 14\. Acceptance criteria for the droplet clock

The clock service is ready for its first paused installation when:

- it is packaged in a clean release and has offline tests;
- it uses a finite systemd-timer tick rather than the legacy scheduler;
- it runs as paradoxtrader, with root-owned unit and environment files;
- it has no provider, market-data, broker, or Graphify dependency;
- the heartbeat database and home migrations are idempotent;
- duplicate ticks and lease contention are safe;
- the timer is nonpersistent and does not replay downtime;
- pause is durable in the database and independently enforceable by systemd;
- status is readable without exposing private prose;
- the host has no public heartbeat port;
- backup and recovery procedures are tested before any real model credential is installed;
- the first remote verification confirms zero agent dispatches and zero external provider calls.

The next meaningful milestone after this plan is not “the agents are running.” It is: **the droplet can keep accurate time, preserve private state, remain paused on demand, survive restart, and honestly show why nothing has happened yet.**