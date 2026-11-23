What we’re adding (plain English)

1\. Modes (Patternseer, Momentum Mode, Groundkeeper, Synth) live in a tiny registry.

2\. Tasks and journal entries can carry an optional modeId.

3\. A quick Mode Switcher chip shows on task cards and the journal screen.

4\. Starting a task opens an optional Mode Session (start/stop, adds XP + notes).

5\. Insights: “Tasks finished by mode”, “Time in mode”, “Which mode helps which task type”.

\---

Minimal data model

// models/mode.ts

export type ModeId = 'patternseer' | 'momentum' | 'groundkeeper' | 'synth';

export interface Mode {

id: ModeId;

name: string;

emoji: string;

color: string; // for badges

activation: string; // short phrase

deactivation: string; // short phrase

}

export const MODES: Record<ModeId, Mode> = {

patternseer: { id:'patternseer', name:'Patternseer', emoji:'🧠', color:'#6C7A89',

activation:"Let me watch until it makes sense.",

deactivation:"The pattern is seen; the watcher can rest." },

momentum: { id:'momentum', name:'Momentum Mode', emoji:'⚡', color:'#D97706',

activation:"Small start — forward anyway.",

deactivation:"Momentum complete; stillness earned." },

groundkeeper: { id:'groundkeeper', name:'Groundkeeper', emoji:'🌊', color:'#0EA5E9',

activation:"Return to the ground that holds me.",

deactivation:"Roots drawn in; balance restored." },

synth: { id:'synth', name:'Synth', emoji:'🪶', color:'#8B5CF6',

activation:"Let’s play with the pieces.",

deactivation:"The current slows; creation rests." },

};

// models/task.ts

import type { ModeId } from './mode';

export interface Task {

id: string;

title: string;

notes?: string;

// ...

modeId?: ModeId; // <— NEW

}

// models/modeSession.ts

import type { ModeId } from './mode';

export interface ModeSession {

id: string;

modeId: ModeId;

taskId?: string; // optional link

startedAt: number;

endedAt?: number;

xpEarned?: number;

notes?: string;

}

\---

Tiny UI pieces

1) ModeChip (shows on TaskCard & Journal header)

// components/ModeChip.tsx

import { MODES, ModeId } from '../models/mode';

export function ModeChip({ modeId, onPress }: { modeId?: ModeId; onPress: ()=>void }) {

const m = modeId ? MODES\[modeId\] : undefined;

return (

<Pressable onPress={onPress} className="px-2 py-1 rounded-full border border-gray-300 flex-row items-center">

<Text>{m ? \`${m.emoji} ${m.name}\` : 'Set mode'}</Text>

</Pressable>

);

}

2) ModePicker (bottom sheet with activation line)

// components/ModePicker.tsx

import { MODES, ModeId } from '../models/mode';

export function ModePicker({ initial, onSelect }: { initial?: ModeId; onSelect:(m:ModeId)=>void }) {

return (

<View className="p-4">

{Object.values(MODES).map(m => (

<Pressable key={m.id} onPress={()=>onSelect(m.id)} className="p-3 my-1 rounded-xl"

style={{backgroundColor:'#fff', borderWidth:1, borderColor:'#eee'}}>

<Text className="text-lg">{m.emoji} {m.name}</Text>

<Text className="text-xs opacity-70 mt-1">“{m.activation}”</Text>

</Pressable>

))}

</View>

);

}

3) Quick session modal (when you press “Start” on a task)

// components/StartModeSession.tsx

import { MODES, ModeId } from '../models/mode';

export function StartModeSession({ task, defaultMode, onBegin }:{

task?: Task; defaultMode?: ModeId; onBegin:(mode:ModeId)=>void

}) {

// shows current mode with activation phrase + “Begin session” button

}

\---

Light analytics (no charts required to start)

Reducer/selectors

selectCompletedTasksByMode(modeId)

selectMinutesInModeLast7Days(modeId)

selectBestModeForTaskTag(tag) (simple winner by completion rate)

Insight cards

“This week: ⚡ Momentum helped finish 6 tasks (avg 13 min/session).”

“When writing, 🧠 Patternseer → 2× completion vs no mode.”

\---

String set (ready to paste)

Patternseer: “Let me watch until it makes sense.” / “The pattern is seen; the watcher can rest.”

Momentum Mode: “Small start — forward anyway.” / “Momentum complete; stillness earned.”

Groundkeeper: “Return to the ground that holds me.” / “Roots drawn in; balance restored.”

Synth: “Let’s play with the pieces.” / “The current slows; creation rests.”

\---

Where to put things (your repo)

models/mode.ts, models/modeSession.ts

components/ModeChip.tsx, components/ModePicker.tsx, components/StartModeSession.tsx

Add modeId to TaskCard and Journal entry screen header

Add an “Insights → Modes” section (simple list first; chart later)

\---

Aider-ready prompts (copy/paste)

Add mode system

Create models/mode.ts with a Mode registry for 4 modes (patternseer, momentum, groundkeeper, synth) including emoji, color, activation, deactivation.

Add optional modeId to Task interface.

Add a new models/modeSession.ts with ModeSession {id, modeId, taskId?, startedAt, endedAt?, xpEarned?, notes?}.

UI hooks

In components/TaskCard (or equivalent), render a ModeChip on the right side of the card.

On press, open ModePicker in a bottom sheet and persist the chosen modeId on the task.

Start session

When the user taps "Start" on a task, show StartModeSession modal:

\- Display emoji, name, activation line for the current mode (or let them pick one).

\- Button "Begin session" sets startedAt=Date.now, creates a ModeSession linked to the task.

\- On "Complete", close session, set endedAt=Date.now, award xpEarned=5 by default, and show the deactivation phrase in a toast.

Insights

Add a new screen "ModesInsights" under /app/analytics/modes.tsx.

Show: tasks completed per mode last 7 days, total minutes per mode, and best mode by task tag.

Use simple Text rows first; charts later.

\---

Gentle workflow you can follow

1\. Pick a task → tap Set mode → read the activation line.

2\. Start → do 5–10 min → complete → read deactivation line.

3\. Check Insights weekly to see which mode actually helps which task types.