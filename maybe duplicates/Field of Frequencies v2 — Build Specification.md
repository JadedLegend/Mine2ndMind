# **Field of Frequencies v2 — Build Specification**

## **What This Document Is**

This is a complete build specification for a music lyric/concept generation web application. It is designed to be used as a seed document for AI-assisted development platforms (Lovable, Manus, Cursor, Claude, etc.).

Build this application incrementally. Start with Phase 1 and get it working before moving to Phase 2. Each phase adds a layer of intelligence.

## **The App in One Sentence**

A song lyric and concept generator that uses a philosophical framework called OPTE (Ontological Paradox Tolerance Expansion) as its operating logic, producing complete song packages ready for use with Suno AI music generation.

## **Tech Stack**

- **Frontend:** React + TypeScript + Vite + Tailwind CSS + shadcn/ui
- **Backend/DB:** Supabase (auth, storage, real-time)
- **AI:** Claude API (Anthropic) for generation — model: claude-sonnet-4-20250514
- **Design language:** Dark theme. Background: #0B0F14. Primary text: #E6EDF3. Secondary text: #9FB3C8. Accent colors defined below per Paradox Zone.

## **PHASE 1: CORE GENERATOR**

Build this first. Get it working end-to-end before adding anything else.

### **1.1 — The Generation Flow**

The user provides a **seed** — raw text, phrases, themes, fragments of writing. This can be messy, stream-of-consciousness, unpolished. The system takes the seed and generates a complete song: intro (optional prose block), verses, chorus, bridge, outro.

Every generated song also includes the **fixed style prompt** (defined below) which the user will copy alongside the lyrics into Suno.

### **1.2 — The Fixed Style Prompt**

This text is the identity constant. It appears with every generated song and is NEVER modified by the system. Display it in a copyable block alongside generated lyrics.

Ancient future cognitive drip liquid quantum trip-hop. Laid back, chilled, complex, trippy vibe. Labyrinth layers of fractalized melody rhyming with harmony. Living breathing media. Inspired by existence, both physical and metaphysical. Transducers tuning transcendent vibrational frequencies to trigger dormant & ancient wave functions. Auditory authenticity. Intention, inspiration, assistance. Light codes imbue this song personalizing sonic signatures. Vibrational equilibrium achieved. Psychic grip loosens while inside this creation. Embrace ambiguity. Wu wei. Action without striving. Effortless action. Rhythmic attunement. Leaning into coherence, resonance, harmony, melody, rhythm. Sonic served authenticity. Male dominant vocals. Novel & unique vocalist(s). Consonant-forward, precise diction, occasional double-time bursts, intentional micro-pauses, leave a few breaths for negative space. Uncertainty equals fully free permission. If you fall short, this is natural. You are supported.

### **1.3 — The System Prompt Architecture**

When generating a song, the system constructs a prompt to Claude that includes:

1. **Role definition:** "You are a lyric generation engine for an artist whose style is characterized by extreme multisyllabic density, internal rhyme cascades, paradox-inhabiting themes, and a blend of street-level grit with cosmic/metaphysical vision. Think MF DOOM meets Alan Watts meets Terence McKenna. The lyrics you produce will be performed through Suno AI."
2. **The user's seed text** (their raw input)
3. **Current slider/parameter values** (translated into generation instructions — see Section 2)
4. **Selected corpus segments** (thematic reference material — see Section 3)
5. **Anti-repetition context** (the last 5-10 song openings — see Section 4)
6. **Structural instructions:** "Generate a complete song with the following sections: \[Intro\] (optional — a prose/spoken-word block), \[Verse 1\], \[Chorus\], \[Verse 2\], \[Chorus\], \[Bridge\], \[Chorus\], \[Outro\]. Label each section with brackets. The song should follow the Paradox Loop structure: establish equilibrium, introduce tension/contradiction, break the structure open, discover something new, then reintegrate at a higher level of coherence."
7. **Style micro-directives** (dynamic additions based on current parameter settings — generated automatically)

### **1.4 — Song Display**

Each generated song shows:

- The lyrics with section labels (\[Intro\], \[Verse 1\], \[Chorus\], etc.)
- A "Copy Lyrics" button
- A "Copy Style Prompt" button (copies the fixed style prompt)
- A "Copy All" button (lyrics + style prompt together, ready to paste into Suno)
- A 1-5 star rating interface
- A "Save to Journal" button

### **1.5 — Song Pool & Lifecycle**

- The **active pool** holds up to 20 generated songs
- When the pool exceeds 20, the oldest unrated/unsaved songs are pruned first
- Songs saved to the Journal are permanent and not subject to pruning
- Songs with 4-5 star ratings are protected from pruning until the pool hits 50
- At 50 songs, everything except Journal entries is pruned

### **1.6 — Journal**

- Persistent storage of saved songs
- Each journal entry stores: lyrics, timestamp, all parameter settings at time of generation, rating (if given), the seed text used
- Searchable by theme/keyword
- Journal entries can be used as corpus segments in future generations (see Resonance Mode)

### **1.7 — Rating System**

- 1-5 stars on every generated song
- Ratings are stored with the song and its generation parameters
- Over time, the system uses rating history to inform generation (Phase 2+)

## **PHASE 2: THE CONTROL SURFACE**

These are the user-facing parameters. Each one is a slider or selector in the UI. Build them as a collapsible panel (default: collapsed, showing current values as compact chips/badges).

### **2.1 — Multisyllabic Density \[Slider: 1-10, default: 7\]**

This is the primary new control. It governs how dense and compressed the lyrical output is.

**How it translates to the generation prompt:**

At level 1-2, add to prompt: "Use spacious, breath-filled lines. Short phrases. Each word carries individual weight. Minimal internal rhyme. Spoken-word adjacent pacing."

At level 3-4, add: "Use natural conversational rhythms. Some internal rhyme patterns. Occasional multi-syllabic words but don't force them. Balance clarity with musicality."

At level 5-6, add: "Use consistent internal rhyme patterns. Multi-syllabic rhyme clusters should appear in every verse. Balance meaning and sonic texture equally. Lines should reward both listening and reading."

At level 7-8, add: "Prioritize dense multisyllabic internal rhyme cascades. Rhymes should connect across line boundaries, not just at line ends. Meaning becomes secondary to sonic architecture where necessary. Include occasional double-time bursts — compressed rapid-fire syllable sequences. Invented compound words and portmanteaus are encouraged. Think MF DOOM-level density."

At level 9-10, add: "Maximum compression. Every syllable is percussion. Internal rhymes cascade continuously. Meaning emerges from sound pattern, not literal semantics. Neologisms, portmanteaus, and invented language welcomed. Glossolalia edge — the lyrics should feel like they're vibrating at the boundary between language and pure sound. Atomic bombs in sentences."

**Sub-parameters** (shown when user expands an "Advanced" section under the main slider):

- **Semantic Drift** \[Slider: 1-10, default: auto-linked to density\] — How far from literal meaning the lyrics can drift. At 1: every line makes clear semantic sense. At 10: pure sonic association, meaning is emergent not explicit.
- **Negative Space** \[Slider: 1-10, default: 4\] — How many deliberate pauses, breath marks, and gaps to include. Inverse relationship with density but independently controllable. At 1: wall-to-wall syllables. At 10: sparse, each phrase surrounded by silence. Add to prompt: "Include \[X\] intentional micro-pauses or breath marks per verse, using ellipses (...) or line breaks."

### **2.2 — Creative Balance \[Slider: 0-100, default: 70\]**

How much the output draws from the user's seed vs. the system's own creative intelligence.

- 0 = Pure user material. System only structures/refines the seed.
- 50 = Equal blend. System uses seed as a jumping-off point.
- 100 = Pure system. Seed is just a thematic hint.

Add to prompt: "Creative balance is set to \[X\]%. At this level, \[describe behavior\]. The user's seed text is: \[seed\]. Honor the user's raw material at \[X\]% weight and bring your own creative contribution at \[100-X\]% weight."

### **2.3 — Creative Equilibrium \[Slider: 1-10, default: 10\]**

How much simultaneous tension the system holds between all its reference points.

- At 1: Commit to one clear direction. Minimal internal contradiction.
- At 5: Hold moderate tension between different themes/perspectives.
- At 10: Maximum paradox tolerance. The song should hold multiple contradictions simultaneously without resolving them. Embrace ambiguity fully.

Add to prompt: "Creative equilibrium is at \[X\]/10. \[At current level\]: \[describe behavior\]."

### **2.4 — Resonance Mode \[Toggle: ON/OFF, default: ON\]**

When ON, reveals:

- **Corpus Segment Selector** — The user picks 2-5 thematic segments to draw from (see Section 3 for the full list). These are reference themes, not copy sources.
- **Resonance Intensity** \[Slider: 1-10, default: 5\] — How tightly the output reflects the selected segments.
  - At 1: Segments are loose thematic suggestions. The connection may be subtle or subconscious.
  - At 5: Each segment should be recognizably present in the output.
  - At 10: Every segment must be explicitly woven into the song. The output is a tight synthesis of all selected segments.

Add to prompt: "Resonance Mode is active. Draw thematic inspiration from these corpus segments: \[list segments with their descriptions\]. Resonance intensity is \[X\]/10. At this level, \[describe expected integration depth\]."

### **2.5 — Tension Intensity \[Slider: 1-10, default: 5\]**

How much structural contradiction the system introduces into the song.

- At 1-3: "Introduce subtle thematic counterpoint. The song should have a unified mood with a gentle undertow of something unresolved beneath the surface."
- At 4-6: "Introduce active paradox. The song should hold two moods, perspectives, or truths in visible tension. The listener should feel the pull between them."
- At 7-10: "Introduce confrontational paradox. Opposites should collide within single lines. Include moments where the song contradicts itself deliberately. The tension should be structural, not just thematic."

### **2.6 — Paradox Zone Selector \[Multi-select icons, default: Auto\]**

Five clickable zone icons. The user can select one or more, or leave on Auto (system rotates).

| Zone | Glyph | Color | What it does to generation |
| --- | --- | --- | --- |
| Logic | 🜀 | #6FA8FF | Add to prompt: "Engage the Logic zone. Include self-referential structures, meta-commentary on the song itself, Gödelian self-awareness, pattern recognition as theme." |
| --- | --- | --- | --- |
| Matter | 🜁 | #8BC6A8 | Add to prompt: "Engage the Matter zone. Ground the song in physical/somatic reality. The body as instrument. Sensation, materiality, the weight of being embodied." |
| --- | --- | --- | --- |
| Water | 🜄 | #6FC3D4 | Add to prompt: "Engage the Water zone. Explore relational/emotional paradox. Connection that wounds, attachment that frees, the fluid space between people." |
| --- | --- | --- | --- |
| Fire | 🜂 | #E8A84C | Add to prompt: "Engage the Fire zone. Channel transformative energy. Creative destruction, the force that builds and burns simultaneously, will and drive and their cost." |
| --- | --- | --- | --- |
| Meta | 🜃 | #A88BFF | Add to prompt: "Engage the Meta zone. Go recursive. The song should be aware of itself as a song. Maps that change territories. Systems observing systems. The deepest layer of self-reference." |
| --- | --- | --- | --- |

In Auto mode: system picks 1-2 zones, weighted to avoid repeating the same zone as the last 3 songs.

### **2.7 — Break Intensity \[Slider: 1-10, default: 5\]**

How dramatic the structural rupture is (usually lands in the bridge section).

- At 1-3: "The bridge should shift tone or imagery subtly. A change in register, not a rupture."
- At 4-6: "The bridge should crack the song open. Shift perspective (first person to third, or introduce a new voice). Question the assumptions of the verses."
- At 7-10: "The bridge should be a structural dissolution. Fragment the lines. Break the rhyme scheme. Use raw, unprocessed language. Let the song enter temporary chaos before the final chorus pulls it back into coherence. This is the moment of ego dissolution in the song's arc."

## **PHASE 3: CORPUS SEGMENTS**

These are the thematic reference pools the user can select in Resonance Mode. They are drawn from a body of philosophical and autobiographical work.

### **3.1 — Thematic Segments (selectable in Resonance Mode)**

Present these as a visual grid of selectable cards. The user picks 2-5.

**Segment A: Systemic Critique** System prompt addition: "Draw from themes of systemic control, manufactured consent, institutional manipulation, spiritual suppression by societal structures, the illusion of choice. This is structural analysis of power, not conspiracy theory — it's about seeing the machinery."

**Segment B: Paradox as Operating System  
**System prompt addition: "Draw from themes of paradox as home, contradiction as engine, inhabiting rather than resolving opposing truths. 'Paradox is postal code.' The highest truths are found by holding contradictions, not resolving them."

**Segment C: Alchemy & Esoteric Transformation** System prompt addition: "Draw from themes of alchemical transformation, esoteric knowledge, sacred geometry, ancient keys, mythological frameworks for personal change. Fungi as teachers. Hidden layers of reality. The magical substrate beneath the mundane."

**Segment D: Psychedelic Phenomenology** System prompt addition: "Draw from themes of altered states, ego dissolution, dimensional shifts, the nature of perception itself. These are field reports from consciousness exploration — the terror and beauty of reality deconstruction and reconstruction."

**Segment E: The Artist's Struggle** System prompt addition: "Draw from themes of the creative process as alchemy — the pain, pressure, channeling, and sacrifice of making art. Starving for the art. The curse and blessing of being compelled to create. Meta-commentary on the act of writing these very lyrics."

**Segment F: Compression & Density (Meta-Penmanship)** System prompt addition: "Draw from themes of language itself as the subject. Atomic bombs in sentences. Lyrical glyphs. The compression of meaning into its densest possible form. Words as technology. The craft of density as a spiritual practice."

**Segment G: Nervous System & Regulation** System prompt addition: "Draw from themes of nervous system dysregulation, the search for a baseline that was never established, the body's memory of chaos, crisis as normalcy, the long road from survival mode to genuine regulation."

**Segment H: Institutional Betrayal** System prompt addition: "Draw from themes of systems designed to help becoming sources of harm. Therapy that was obedience training. Recovery models that didn't fit. Legal systems disconnected from justice. The deep learning that external demands are often threats to integrity."

**Segment I: Relational Paradox** System prompt addition: "Draw from themes of finding love in wreckage, connection through dysfunction, shame as bonding, the simultaneous truth that attachment enables connection AND produces suffering. Complex relationships that are not idealized but contain genuine resonance."

**Segment J: The Regulation Search** System prompt addition: "Draw from themes of actively working toward regulation for the first time. Mapping the brain's actual state. Using psychedelics, neurofeedback, writing as tools for rewiring. The conscious application of a philosophical framework to one's own healing."

### **3.2 — Journal Entries as Segments**

Any song saved to the Journal can also be selected as a corpus segment. When a journal entry is selected, its full lyrics are included in the system prompt as reference material with the instruction: "Draw thematic and stylistic inspiration from this previous work. Do not copy phrases or structures, but let it inform the emotional register, thematic territory, and density level of the new song."

## **PHASE 4: ANTI-REPETITION ENGINE**

This solves the primary problem: the system generating songs with similar openings.

### **4.1 — The Symmetry Log**

Every generated song's opening (first 2-4 lines) is stored in a rolling log of the last 20 songs.

When generating a new song, the system includes this in the prompt:

"CRITICAL INSTRUCTION — ANTI-REPETITION: The following are the opening lines of the last \[N\] songs generated. Your new song MUST begin differently from all of these. Do not use similar imagery, sentence structure, rhetorical stance, or emotional register as any of these openings. Find a genuinely novel entry point.

Recent openings:

1. \[first lines of song 1\]
2. \[first lines of song 2\] ...

Specifically AVOID:

- Starting with dense urban imagery (used in X of last Y songs)
- Starting with a first-person declarative statement (used in X of last Y songs)
- Starting with a sensory-overload description (used in X of last Y songs) \[These specific avoidance notes should be generated dynamically by analyzing common patterns in the log\]"

### **4.2 — Opening Variation Strategies**

If the system detects clustering in recent openings (3+ similar opening patterns in the last 10 songs), it adds one of these variation strategies to the prompt:

- "Start this song with dialogue or a direct address to someone"
- "Start this song from a third-person perspective before shifting to first person"
- "Start this song with a question"
- "Start this song with a single short line followed by silence, then build"
- "Start this song mid-thought, as if we're dropping into a conversation already happening"
- "Start this song with a concrete, specific, physical detail — not an abstraction"
- "Start this song with the chorus, then deconstruct it in the verses"
- "Start this song with the bridge energy — disoriented, fragmented — then assemble into coherence"

## **PHASE 5: EVOLUTIONARY FEEDBACK**

### **5.1 — Rating-Informed Generation**

After 20+ rated songs exist, the system begins learning from rating patterns.

Include in the system prompt: "Based on historical ratings, this user tends to rate songs highest when they have \[characteristics of 4-5 star songs\]. They tend to rate songs lowest when they have \[characteristics of 1-2 star songs\]. Optimize for the high-rated characteristics while maintaining creative variety."

The characteristics to track:

- Density level at time of generation
- Which corpus segments were active
- Which Paradox Zone was engaged
- Tension and Break intensity
- Creative balance and equilibrium settings
- Length of seed text provided

### **5.2 — Diagnostic Feedback (Shown to User)**

When patterns emerge in ratings, the system can surface gentle suggestions:

- If last 5 songs are all 1-2 stars: "Your recent generations haven't been landing. Consider reducing scope — try fewer corpus segments or lower tension intensity. Sometimes narrowing the aperture restores quality." (This is the Overmuch Syndrome protocol from OPTE.)
- If last 5 songs are all 3 stars (mediocre): "Output has been consistent but not exceptional. Consider introducing a change — try a Paradox Zone you haven't used recently, or increase Break Intensity to crack the pattern open." (This is the Over-Coherence protocol.)
- If ratings are volatile (5, 1, 5, 2, 4, 1): "Your ratings are swinging widely. Consider increasing Creative Balance toward your own voice, or reducing the number of corpus segments. More anchoring might help." (This is the Over-Chaos protocol.)

These suggestions appear as dismissible cards, never as interruptions.

## **UI LAYOUT**

### **Main View**

- Top: App title + navigation (Generator | Journal | Settings)
- Generator view:
  - Left/top: Seed input (large text area, placeholder: "Enter themes, phrases, fragments, raw writing...")
  - Below seed: Compact parameter bar showing current values as small badges/chips. Clicking any badge opens the full control panel.
  - Below parameters: "Generate" button (prominent)
  - Below generate: Generated song display with copy/rate/save controls
  - Below song: Song pool (scrollable list of recent generations, showing first line + rating)

### **Control Panel (Expandable)**

- Multisyllabic Density: large slider with current value displayed prominently
  - Expandable "Advanced" section for Semantic Drift and Negative Space
- Creative Balance: slider
- Creative Equilibrium: slider
- Resonance Mode: toggle, revealing corpus segment grid + intensity slider when ON
- Tension Intensity: slider
- Paradox Zone: 5 glyph icons (🜀 🜁 🜄 🜂 🜃) with their zone colors, plus an "Auto" option
- Break Intensity: slider

### **Journal View**

- List of saved songs with search
- Each entry shows: first line, date, rating, active parameters
- Click to expand full lyrics
- Option to select journal entry as a corpus segment for future generation

### **Visual Design Notes**

- Dark, dense, precise. The UI should feel like the music it generates — constricted and potent, not diffuse and decorative.
- Use the OPTE color system:
  - Background/Void: #0B0F14
  - Primary text/Signal: #E6EDF3
  - Secondary text/Noise: #9FB3C8
  - Logic zone: #6FA8FF
  - Meta zone: #A88BFF
  - Matter zone: #8BC6A8
  - Water zone: #6FC3D4
  - Fire zone: #E8A84C
  - Warning/collapse: #FF5E7E (use sparingly — only for diagnostic alerts)
- Minimal decoration. No gradients unless very subtle. The content is the interface.
- Typography should be clean and monospace-adjacent for lyrics display, sans-serif for UI.

## **DATABASE SCHEMA (Supabase)**

### **songs**

- id: uuid (primary key)
- created\_at: timestamp
- lyrics: text
- seed\_text: text
- rating: integer (1-5, nullable)
- saved\_to\_journal: boolean (default false)
- parameters: jsonb (stores all slider values at time of generation)
- paradox\_zones: text\[\] (which zones were active)
- corpus\_segments: text\[\] (which segments were selected)
- opening\_lines: text (first 2-4 lines, for symmetry log)

### **settings**

- id: uuid (primary key)
- user\_id: uuid (foreign key)
- default\_parameters: jsonb (user's preferred default slider values)

## **API INTEGRATION**

### **Claude API Call Structure**

POST https://api.anthropic.com/v1/messages

{

"model": "claude-sonnet-4-20250514",

"max\_tokens": 4000,

"system": "\[constructed system prompt with role + corpus segments + parameters\]",

"messages": \[

{

"role": "user",

"content": "\[seed text + parameter instructions + anti-repetition context + structural instructions\]"

}

\]

}

The system prompt and user message are constructed dynamically based on current parameter settings. See each parameter's description above for the exact prompt language to use at each setting level.

### **API Key**

Store the Anthropic API key in Supabase environment variables or a .env file. Never expose it client-side — route all API calls through a Supabase Edge Function or similar server-side proxy.

## **BUILD ORDER**

1. **First:** Basic generation flow — seed input, Claude API call with static system prompt, lyrics display, copy buttons. Get a song generating end-to-end.
2. **Second:** Multisyllabic Density slider — the primary new control. Wire it into the prompt.
3. **Third:** Remaining sliders (Creative Balance, Equilibrium, Tension, Break Intensity). Wire each into the prompt.
4. **Fourth:** Paradox Zone selector. Wire into prompt.
5. **Fifth:** Song pool, rating system, Journal. Supabase integration.
6. **Sixth:** Resonance Mode with corpus segments.
7. **Seventh:** Anti-repetition engine (Symmetry Log).
8. **Eighth:** Evolutionary feedback (rating-informed generation, diagnostic suggestions).

Each phase should be fully functional before moving to the next.