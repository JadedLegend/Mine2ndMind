\# ParadoxTrader project review | November 19, 2026

\*\*Keep the build. Hold the spending ceiling. Fund one end-to-end paper experiment before another round of features.\*\* The project already preserves what an agent saw, what it chose, and what the model call cost. Starting over would mean rebuilding that evidence trail. The open financial question is whether an observation made here can become a timely, tradable options idea that survives its costs.

\## What has actually happened

I checked the private host read-only, queried the stored counts and provider-reported costs, traced the working code, and compared it with the earlier handoff. Graphify's index matched GitHub \`main\` at \`79d4bb1\`. The host was running \`fe18717\`. The separate Heartbeat page was under review in \[PR 48\](https://github.com/JadedLegend/ParadoxTrader/pull/48).

| Evidence at inspection | What it establishes |

| --- | --- |

| Two real-model runs, both started November 18, with all seven owners represented in each | The deployed system has actually taken model-powered turns. A restart would discard working integration effort. |

| 63 dispatched requests, 57 successful responses, four truncated and two with an unsupported finish reason | Real models can do the work. Failed replies also consume budget. All 63 requests had a reported cost in these ledgers. |

| $0.205826 in reported model charges across both runs, rounded to six decimals | A measured cost for this particular sample. Hosting, data subscriptions, provider billing fees and development time are additional. |

| 31 completed actions, consisting of 14 library visits, 11 rests, five explorations and one journal action | The agents used the choices they were given. Neither session recorded a market inquiry. The financial value of those early visits and rests is still an open question. |

| Zero inquiry, proposal, order, fill, position and review rows in both run databases | There is no trading return, drawdown or win rate to estimate from these sessions. |

| Dashboard answered an unauthenticated local request with HTTP 401. Dashboard, heartbeat timer and backup timer were active. The last backup service exit was successful. | The host is operational. A restore drill and a fresh authenticated browser session were outside this check. |

| 67 missed slots on November 19 at the time of the count. Repeated heartbeat worker exits with a manifest validation error. | An active timer can coexist with a whole day of missed work. I reproduced the current catalog failure independently using public prices and the selected model IDs. |

The cost is small today. The larger near-term expense is engineering time spent improving a system whose market decisions cannot yet be scored. The saved model limit was $3 per day. Thirty days at that ceiling would allow $90 in model reservations. Adding the original $15.60 monthly droplet-and-backup quote gives an illustrative $105.60 before taxes, data and other fees. The infrastructure quote comes from the original handoff. Actual current invoices and data-plan charges were unavailable for this review.

\## The path worth keeping

1\. \*\*Market to decision.\*\* The real heartbeat gives agents a shared watchlist, IEX stock snapshots and cached contextual feeds. The controller freezes the choice context and records the exact request. That makes it possible to ask later whether the evidence was available when the agent acted. Saved provider credentials alone establish neither entitlement nor coverage. \[Heartbeat entry point\](../scripts/heartbeat.py) · \[Market window\](../core/market/window.py) · \[Decision controller\](../core/runtime/rehearsal/controller.py)

2\. \*\*Decision to inquiry.\*\* An agent can open a private inquiry, distinguish an observation from an interpretation, revisit it, or abstain. The restricted action list ends at rest, journal, inquiry, library and exploration. The witness records what happened. Selecting a witness model in Settings does not make the current mechanical witness perform inference. \[Inquiry operations\](../core/runtime/inquiry.py) · \[Witness\](../core/runtime/rehearsal/witness.py) · \[Allowed actions\](../core/runtime/rehearsal/provider.py)

3\. \*\*Proposal to fill.\*\* The mock lifecycle has a durable order identity, recovery, partial fills, cancellations and position accounting. Its execution pilot is restricted to Alchemist and a fictional contract. There is a separate Alpaca wrapper with order methods. The restricted heartbeat has no path through a risk-reviewed proposal into an actual Alpaca paper fill and back. The wrapper's contracts-list call also does not supply a historical executable bid and ask. \[Mock lifecycle\](../core/trading/lifecycle.py) · \[Alpaca wrapper\](../core/trading/alpaca.py)

4\. \*\*Fill to economic result.\*\* The position code can calculate gross realized profit on mock fills. Fees and current marks can be unavailable. The cost records and position records are valuable building blocks. Evaluating a strategy still needs a timestamped entry and exit, realistic execution assumptions, attributable costs and a comparable reference decision. \[Position projections\](../core/trading/lineage/projections.py) · \[Position reads\](../core/trading/lineage/reads.py) · \[Existing evaluation protocol\](../docs/research/ParadoxEdgeTrader\_Evaluation\_Protocol.md)

\## Repairs in the review branch

| Problem | Repair and evidence |

| --- | --- |

| Two selected models advertised catalog prices the day planner rejected. One had premium cache writes and a long-prompt tier. The other had time-dependent prices. | The parser takes the highest advertised applicable text-unit rate across tiers for its reservation and routing ceiling. Unknown nonzero billing units and invalid prices still stop admission. The repaired validator accepted the current seven selections and the $3 limit using the public catalog alone. The worker now reports the validator's specific error code. |

| The router could receive a price ceiling just below an affordable advertised price. Lowering a positive daily budget could also leave the old, higher per-run limit in force. | Routing ceilings use the decimal that actually goes onto the wire. Settings identifies base prices. The next segment uses the revised allowance after earlier reservations, and the worker checks for budget changes between wakes and between turns. Previously dispatched requests keep their original accounting. |

| A price without a usable timestamp could inherit the time of the fetch or another source. A fresh symbol could also make a stale one look current. | Each trade carries its own timestamp into the decision and inquiry. A fallback daily bar is labeled with its interval start. The inquiry retains the check time separately. Future-dated data and unusable prices are omitted. \[Alpaca bar timestamps\](https://docs.alpaca.markets/us/docs/market-data-faq) |

| The Python CI run on main failed two comparisons with checked-in dashboard examples. | Reused the two updated examples already present in the Heartbeat page branch. Both are generated from the same offline session. \[Failing main run\](https://github.com/JadedLegend/ParadoxTrader/actions/runs/44589156424) |

| An ordinary Windows checkout converted the line endings of all fourteen original agent identity files. All fourteen stored Git blobs matched their expected hashes. | Pinned those files to their original line endings in Git attributes. The release builder already requests Unix line endings explicitly. |

These are local changes. Applying them to the live host would make scheduled, paid wakes eligible to resume. The audit used no paid inference and submitted no order.

\*\*Verification.\*\* The final source passed 788 Python tests and 1,694 subtests on Ubuntu with Python 3.12, and all five library and fixture reproducibility checks. The frontend passed all 580 tests, lint, TypeScript and the connected private-host production build. Vite still reports large chunks for the bundled corpus and rehearsal example. A fresh Windows checkout matched all fourteen original identity hashes. The Linux checks used a local WSL test environment with Poppler and Python venv support. The last read-only check on EdgeTrader still showed the old release and the catalog error.

\## What would earn the next dollar

\*\*First milestone, one auditable round trip.\*\* Keep the seven agents and the ability to abstain. Use one liquid underlying already on the watchlist. Record one observed contradiction, the proposed direction or volatility move, the time horizon and what would invalidate it. Freeze the source timestamps and the entry rule before the outcome. Use a declared scripted example to commission the machinery if no agent volunteers a proposal. Keep that example out of the strategy results.

Carry the existing proposal ID through one risk-limited, owner-authorized paper order. Record the exact contract, multiplier, limit, bid, ask, quote time and feed. After an interrupted connection, look up the same client order ID. Reconcile any fill and a closing fill or expiry into one report that another person can reconstruct from the stored records. A refusal, unfilled order or missing quote should stay visible as its actual outcome.

\*\*Second milestone, a bounded forward comparison.\*\* My suggested first operating trial is ten market sessions with the existing $3 daily ceiling, a maximum of $30 in model reservations if paid dispatch runs only on those days. Use the same opportunity timestamps and eligible contracts for the agents and one simple rule fixed in advance. Include abstentions and a cash reference. Record net dollars after spreads, slippage, fees and model costs, alongside drawdown, exposure, missed opportunities and data gaps. Treat seven agents looking at one event as one market opportunity. Ten sessions can expose an unusable process. Establishing an edge requires more independent opportunities and an untouched subsequent period.

| Decision | Evidence that would justify it |

| --- | --- |

| Continue the current build | A paper round trip survives restart and the result can be reconstructed. A forward trial then produces comparable decisions with known costs. |

| Increase the research budget | On a fresh period, any advantage survives conservative execution and operating costs, appears across independent events and justifies the drawdown. A targeted data purchase should answer an identified measurement gap. |

| Pause paid wakes | After the bounded trial, the system still cannot produce scorable opportunities or reliable costed outcomes, or the simpler rule delivers equivalent results at lower cost. Preserve the records for later investigation. |

| Rebuild a component | A concrete adapter or storage boundary prevents replay or reconciliation and a narrow replacement is cheaper to verify. The evidence reviewed here gives no reason to restart the whole project. |

\## What outside research adds

The TradingAgents authors report stronger results than their chosen baselines for a multi-agent stock-trading design. StockBench's multi-month evaluation found most tested models struggled to beat buy-and-hold, with some exceptions. Both are stock studies. My inference is that the architecture is plausible enough to test and the baseline matters enough to choose in advance. Neither study estimates the return of this options strategy. \[TradingAgents\](https://arxiv.org/abs/2412.20138) · \[StockBench\](https://arxiv.org/abs/2510.02209)

Alpaca documents two limitations that directly affect this experiment. Its free indicative options feed modifies quotes and delays trades. Its paper simulator omits several live frictions, including order queue position, latency slippage and regulatory fees. An indicative quote can support a pipeline rehearsal. A claim about the value of a short-lived discrepancy requires data with the timing and pricing precision to resolve it. \[Options chain and feed definitions\](https://docs.alpaca.markets/us/reference/optionchain) · \[Paper execution assumptions\](https://docs.alpaca.markets/us/docs/paper-trading)