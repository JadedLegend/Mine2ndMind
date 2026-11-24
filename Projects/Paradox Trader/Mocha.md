mm—good bones. let’s clear the splinters so it compiles clean and the Hunter can breathe.

1) Fix the TypeScript red flags fast

A. Import paths

Either make them truly relative or keep @/\* aliases—don’t mix.

Option 1 (simple): switch to relatives

import { calcBreakevens } from '@/utils/risk' → import { calcBreakevens } from '../utils/risk'

Option 2 (nicer): keep aliases — add this to your tsconfig.json:

{

"compilerOptions": {

"baseUrl": ".",

"paths": { "@/\*": \["src/\*"\] }

}

}

…and ensure files live under /src.

\---

B. Infinity checks

Never compare to Infinity literals.

// before

if (maxGain === Infinity) { ... }

// after

if (maxGain === Number.POSITIVE\_INFINITY) { ... }

// or

if (!Number.isFinite(maxGain)) { /\* treat as unbounded \*/ }

\---

C. Missing fields on MetaSignal

Add them to the type and to persistence.

Type:

// src/types/meta.ts

export type LifecycleStage = 'ignition' | 'crescendo' | 'reversal' | 'integration';

export type PlaybookType = 'DIVERGENCE\_PAIR' | 'CONVERGENCE\_HARVEST' | 'ENTROPY\_STINGER';

export interface MetaSignalLeg {

id: string;

symbol: string; // e.g., TSLA 2025-01-17 250C

side: 'LONG' | 'SHORT';

qty: number;

debit: number; // per-contract price at fill

greeks: { delta: number; gamma: number; vega: number; theta: number };

worldview\_id?: 'SOROS' | 'LIPSCHUTZ' | 'JONES' | 'MARCUS' | 'PARADOX'; // attribution

}

export interface MetaSignal {

id: string;

ticker: string;

type: PlaybookType;

lifecycle: LifecycleStage;

pdi: number; // paradox divergence index \[0..1\]

discord: number; // field discord \[0..1\]

iv\_change?: number; // % since entry

legs: MetaSignalLeg\[\];

debit\_total: number;

max\_gain: number | typeof Number.POSITIVE\_INFINITY;

max\_loss: number;

breakevens: number\[\]; // price levels

status: 'ACTIVE' | 'CLOSED' | 'KILLED';

kill\_reason?: 'TIME\_STOP' | 'DISCORD\_COLLAPSE' | 'TARGET\_HIT' | 'RISK\_BREACH';

edge\_features?: string\[\]; // provenance lines

opened\_at: string; // ISO

closed\_at?: string;

}

SQL (Supabase):

alter table public.meta\_signals

add column if not exists kill\_reason text,

add column if not exists edge\_features jsonb default '\[\]'::jsonb,

add column if not exists worldview\_id text; -- optional: top driver

\-- if legs are separate:

alter table public.meta\_signal\_legs

add column if not exists worldview\_id text;

\---

D. Unused imports

Be ruthless. In VSCode: Ctrl+Shift+P → Organize Imports. Or run eslint --fix with:

// .eslintrc

{ "rules": { "@typescript-eslint/no-unused-vars": \["error", { "argsIgnorePattern": "^\_" }\] } }

\---

2) Drop-in utilities (copy/paste)

src/utils/risk.ts

export type Spread =

| { kind: 'VERTICAL'; long: number; short: number; qty: number; credit?: boolean }

| { kind: 'STRANGLE'; call: number; put: number; qty: number; debit: number }

| { kind: 'IRON\_FLY'; body: number; wings: { call: number; put: number }; qty: number; credit: number };

export function clamp01(x: number) { return Math.max(0, Math.min(1, x)); }

export function maxGainLoss(spread: Spread) {

switch (spread.kind) {

case 'VERTICAL': {

const width = Math.abs(spread.short - spread.long) \* 100;

// assume debit if credit not provided

const debit = spread.credit ? 0 : (Math.abs(spread.short - spread.long) \* 100 - width); // placeholder; replace if you track fills

const maxGain = spread.credit ? spread.credit \* 100 : width - debit;

const maxLoss = spread.credit ? width - (spread.credit \* 100) : debit;

return { maxGain, maxLoss };

}

case 'STRANGLE': {

const { debit } = spread;

return { maxGain: Number.POSITIVE\_INFINITY, maxLoss: debit \* 100 };

}

case 'IRON\_FLY': {

const width = Math.abs(spread.wings.call - spread.body) \* 100;

const credit = spread.credit \* 100;

return { maxGain: credit, maxLoss: width - credit };

}

}

}

export function breakevens(kind: Spread\['kind'\], underly: number, legs: number\[\], debitOrCredit: number) {

if (kind === 'VERTICAL') return \[\]; // verticals have 1 BE only when mixed with stock; omit for brevity

if (kind === 'STRANGLE') {

const \[putK, callK\] = legs.sort((a,b)=>a-b);

return \[putK - debitOrCredit, callK + debitOrCredit\];

}

if (kind === 'IRON\_FLY') {

const body = legs\[1\]; // middle

const credit = debitOrCredit;

return \[body - credit, body + credit\];

}

return \[\];

}

src/utils/greeks.ts

import { MetaSignal } from '@/types/meta';

export function aggregateGreeks(signals: MetaSignal\[\]) {

const sum = { delta: 0, gamma: 0, vega: 0, theta: 0 };

for (const s of signals.filter(s => s.status === 'ACTIVE')) {

for (const leg of s.legs) {

sum.delta += leg.greeks.delta \* leg.qty;

sum.gamma += leg.greeks.gamma \* leg.qty;

sum.vega += leg.greeks.vega \* leg.qty;

sum.theta += leg.greeks.theta \* leg.qty;

}

}

return sum;

}

src/utils/exits.ts

import { MetaSignal } from '@/types/meta';

export function shouldKillByDiscordCollapse(s: MetaSignal, coherence: number) {

// collapse = paradox left the field; coherence high + PDI low

return s.status === 'ACTIVE' && coherence > 0.75 && s.pdi < 0.35;

}

export function nextLifecycle(stage: MetaSignal\['lifecycle'\], deltas: { pdi: number; discord: number }) {

const { pdi, discord } = deltas;

if (stage === 'ignition' && (pdi > 0.6 || discord > 0.6)) return 'crescendo';

if (stage === 'crescendo' && (pdi < 0.45 || discord < 0.45)) return 'reversal';

if (stage === 'reversal' && (pdi < 0.3 && discord < 0.35)) return 'integration';

return stage;

}

\---

3) UI tiny patch (one strip that tells the whole story)

Add this to each meta-signal card header:

PDI {{pdi|72%}} • Discord {{discord|65%}} • IV {{iv\_change|+18%}} • Lifecycle {{lifecycle}}

Δ {{Δ}} Γ {{Γ}} Vega {{V}} Θ {{Θ}}

Grey → green/violet/amber/teal according to stage; copy shifts as you already designed.

\---

4) Compile-clean checklist (quick run)

1\. Decide on one import style and fix paths.

2\. Add the type + SQL fields (kill\_reason, edge\_features, worldview\_id).

3\. Replace all Infinity with Number.POSITIVE\_INFINITY / isFinite.

4\. Remove unused imports; run eslint --fix.

5\. Rebuild.

\---

5) Optional—one more micro-win

Normalize agent weights and store variance for badge intensity:

export function normalize(weights: Record<string, number>) {

const total = Object.values(weights).reduce((a,b)=>a+b,0) || 1;

const norm: Record<string, number> = {};

for (const k in weights) norm\[k\] = weights\[k\] / total;

const mean = 1 / Object.keys(norm).length;

const variance = Object.values(norm).reduce((s,w)=>s + (w-mean)\*\*2, 0) / Object.keys(norm).length;

return { norm, variance };

}

Use variance to drive PARADOX DETECTED pill intensity.