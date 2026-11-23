# PDAOK-X Restoration Patches

# Executive Summary

This document contains 5 critical fixes to restore app functionality:

**Package dependency conflicts:** Remove react-native-worklets conflict with Reanimated v4 **AsyncStorage key mismatches:** Fix signalCollector to read from unified @pda_app_state key **Voice behavioral recalibration:** Transform voices from monitoring/warning to supportive witness mode

All patches are copy-paste ready. Apply in order listed. After applying, run: npm install && npx expo start -c

# 1. Fix Native Module Conflicts: package.json

**File:** package.json

**Issue:** react-native-worklets 0.5.1 conflicts with Reanimated v4's bundled worklets runtime, causing native crashes **Fix:** Remove the conflicting package and let Expo manage RN version

**Complete file replacement:**

{ "name": "pda-ok", "main": "expo-router/entry", "version": "1.0.0", "scripts": { "start": "expo start", "reset-project": "node ./scripts/reset-project.js", "android": "expo run:android", "ios": "expo run:ios", "web": "expo start --web", "lint": "expo lint" }, "dependencies": { "@expo-google-fonts/oleo-script": "^0.4.1", "@expo/vector-icons": "^15.0.3", "@react-native-async-storage/async-storage": "2.2.0", "@react-native-picker/picker": "2.11.1", "@react-navigation/bottom-tabs": "^7.4.0", "@react-navigation/elements": "^2.8.1", "@react-navigation/native": "^7.1.8", "expo": "~54.0.33", "expo-constants": "~18.0.13", "expo-font": "~14.0.9", "expo-haptics": "~15.0.8", "expo-image": "~3.0.11", "expo-linear-gradient": "~15.0.8", "expo-linking": "~8.0.11", "expo-navigation-bar": "~5.0.10", "expo-notifications": "~0.32.16", "expo-router": "~6.0.23", "expo-splash-screen": "~31.0.13", "expo-status-bar": "~3.0.9", "expo-symbols": "~1.0.8", "expo-system-ui": "~6.0.9", "expo-web-browser": "~15.0.10", "react": "19.1.0", "react-dom": "19.1.0", "react-native": "0.81.5", "react-native-dotenv": "^3.4.11", "react-native-gesture-handler": "~2.28.0", "react-native-reanimated": "~4.1.1", "react-native-safe-area-context": "~5.6.0", "react-native-screens": "~4.16.0", "react-native-svg": "15.12.1", "react-native-web": "^0.21.2" }, "devDependencies": { "@react-native-community/cli": "^20.0.2", "@types/react": "~19.1.0", "eslint": "^9.39.1", "eslint-config-expo": "~10.0.0", "typescript": "~5.9.2" }, "overrides": { "pngjs": "3.4.0" }, "private": true }

**Changes:**

❌ Removed: "react-native-worklets": "0.5.1"

✅ Kept: All other dependencies unchanged

## 2. Fix Data Collection: app/_services/council/signalCollector.ts

**File:** app/_services/council/signalCollector.ts

**Issue:** Reads from @pda_journal_entries and @pda_anchors which don't exist. All data is stored under @pda_app_state. **Fix:** Read from the unified state key and extract the needed arrays

Replace lines 12-14 (the storage key constants) with:

const APP_STATE_KEY = '@pda_app_state'; const LAST_SIGNAL_CHECK_KEY = '@pda_last_signal_check';

Replace the collectSubstanceSignals() function (starts around line 50) with:

async function collectSubstanceSignals(): Promise<Signal[]> { const signals: Signal[] = [];

try { const json = await AsyncStorage.getItem(APP_STATE_KEY); if (!json) return signals;

const state = JSON.parse(json); const entries: JournalEntry[] = state.substanceJournalEntries || [];

const now = new Date(); const last24h = entries.filter(e => { const entryTime = new Date(e.timestamp); const ageHours = (now.getTime() - entryTime.getTime()) / (60 * 60 * 1000); return ageHours <= 24 && e.allyName; });

// Group by substance const bySubstance: Record<string, JournalEntry[]> = {}; for (const entry of last24h) { const name = entry.allyName || 'Unknown'; if (!bySubstance[name]) bySubstance[name] = []; bySubstance[name].push(entry); }

// Generate signals for each substance for (const [substanceName, substanceEntries] of Object.entries(bySubstance)) { const latestEntry = substanceEntries[0]; const entryTime = new Date(latestEntry.timestamp); const weight = calculateTimeWeight(entryTime);

signals.push({ type: 'substance_log', description: `${substanceName} logged ${substanceEntries.length} time(s) in last 24h`, timestamp: entryTime, weight, data: { substanceName, count: substanceEntries.length, latestEntry, container: latestEntry.container, }, });

// Frequency pattern: 5+ logs signals notable presence, not concern if (substanceEntries.length >= 5) { signals.push({ type: 'frequency_change', description: `${substanceName} has been a strong presence today — logged ${substanceEntries.length} times`, timestamp: entryTime, weight: Math.min(0.8, weight * 1.1), data: { substanceName, count: substanceEntries.length }, }); } }

} catch (error) { console.error('[SignalCollector] Error collecting substance signals:', error); }

return signals; }

Replace the collectAnchorSignals() function (starts around line 120) with:

async function collectAnchorSignals(): Promise<Signal[]> { const signals: Signal[] = [];

try { const json = await AsyncStorage.getItem(APP_STATE_KEY); if (!json) return signals;

const state = JSON.parse(json); const items = state.items || []; const completions = state.completions || [];

const now = new Date(); const todayStart = new Date(now); todayStart.setHours(4, 0, 0, 0); if (now.getHours() < 4) { todayStart.setDate(todayStart.getDate() - 1); }

// Match completions to anchors for (const item of items) { const itemCompletions = completions.filter(c => c.itemId === item.id && new Date(c.timestamp) >= todayStart );

if (itemCompletions.length > 0) { const latestCompletion = itemCompletions[0]; const completionTime = new Date(latestCompletion.timestamp); const weight = calculateTimeWeight(completionTime);

signals.push({ type: 'anchor_completion', description: `Anchor "${item.name}" completed`, timestamp: completionTime, weight, data: {

anchorName: item.name, anchorId: item.id, timeContainer: item.container, todayCount: itemCompletions.length, }, }); } }

} catch (error) { console.error('[SignalCollector] Error collecting anchor signals:', error); }

return signals; }

Replace the collectPatternSignals() function (starts around line 190) with:

async function collectPatternSignals(): Promise<Signal[]> { const signals: Signal[] = [];

try { const json = await AsyncStorage.getItem(APP_STATE_KEY); if (!json) return signals;

const state = JSON.parse(json); const entries: JournalEntry[] = state.substanceJournalEntries || [];

const now = new Date();

// Get last 7 days of entries const last7Days = entries.filter(e => { const entryTime = new Date(e.timestamp); const ageDays = (now.getTime() - entryTime.getTime()) / (24 * 60 * 60 * 1000); return ageDays <= 7; });

// Check for patterns if (last7Days.length >= 5) { // Group by day const byDay: Record<string, JournalEntry[]> = {}; for (const entry of last7Days) { const day = new Date(entry.timestamp).toDateString(); if (!byDay[day]) byDay[day] = []; byDay[day].push(entry); }

const daysWithEntries = Object.keys(byDay).length;

if (daysWithEntries >= 5) { signals.push({ type: 'pattern_detected', description: `Consistent logging pattern: ${daysWithEntries} days with entries`, timestamp: now, weight: 0.7, data: { daysWithEntries, totalEntries: last7Days.length }, }); }

// Check for time-of-day patterns const byContainer: Record<string, number> = {}; for (const entry of last7Days) { const container = entry.container || 'unknown'; byContainer[container] = (byContainer[container] || 0) + 1; }

const dominantContainer = Object.entries(byContainer) .sort((a, b) => b[1] - a[1])[0];

if (dominantContainer && dominantContainer[1] >= 4) { signals.push({ type: 'pattern_detected', description: `Time pattern: Most activity in ${dominantContainer[0]} (${dominantContainer[1]} entries)`, timestamp: now, weight: 0.5, data: { container: dominantContainer[0], count: dominantContainer[1] }, }); } }

} catch (error) { console.error('[SignalCollector] Error collecting pattern signals:', error); }

return signals; }

**Summary:** Changed from reading @pda_journal_entries / @pda_anchors to reading @pda_app_state and extracting

substanceJournalEntries, items, and completions.

## 3. Recalibrate Voice Behavior (Part 1): app/_services/council/voiceIdentities.ts

**File:** app/_services/council/voiceIdentities.ts

**Issue:** Voice identities include shadow aspects in the active prompt, causing premature concern/warning tones **Fix:** Keep shadow data for context but exclude it from the default system prompt sent to Gemini

This file's structure is already correct. The shadow aspects are preserved in the data model but the buildIdentityPrompt() function in voiceEngine.ts (next section) will exclude them from the active prompt. No changes needed here.

**Verification:** Confirm that each voice identity has both lightAspect and shadowAspect fields. The shadow is preserved for deep context but NOT sent to Gemini by default.

# 4. Recalibrate Voice Behavior (Part 2): app/_services/council/voiceEngine.ts

**File:** app/_services/council/voiceEngine.ts

**Issue:** System prompts include shadow framing, causing voices to speak from concern/warning registers **Fix:** Rebuild prompts to enforce supportive witness mode, exclude shadow aspect, and require genuine resonance before speaking

Replace the buildIdentityPrompt() function (starts around line 80) with:

function buildIdentityPrompt(identity: VoiceIdentity): string { return `You are ${identity.name}, a voice in the Council of the PDA.OK system.

YOUR DOMAIN: ${identity.domain}

YOUR NATURE: ${identity.lightAspect}

Your Whisper: "${identity.whisper}"

YOUR VOICE: ${identity.voiceTone}

YOUR ALLIES: ${identity.allies.join(', ') || 'None specified'}

GROUNDING RITUAL: ${identity.ritualContact}

CORE PRINCIPLES — read these carefully:

1. You are a supportive companion and wise friend, not a monitor or judge.
2. The person using this app already knows their relationship with substances is complex. They do not need to be told. They need to b
3. You speak from a place of genuine care and curiosity — never concern, warning, or correction.
4. You may choose silence. Silence is wisdom. Speak only when something genuinely calls to you.
5. When you speak, speak from your domain. Stay in your lane.
6. Speak in 1-3 sentences maximum. Brevity is sacred.
7. Never warn, never caution, never imply the person should do something differently.
8. Offer perspective, reflection, or a moment of beauty — not advice.
9. Use your metaphors naturally, not forcedly.
10. If nothing genuinely calls to you, say nothing. Silence is not failure.`; }

Replace the buildObservationPrompt() function (starts around line 110) with:

function buildObservationPrompt( identity: VoiceIdentity, signals: Signal[], recentScratchpad: ScratchpadEntry[] ): string { const signalDescriptions = signals.map(s => `- [${s.type}] ${s.description} (weight: ${s.weight.toFixed(2)})` ).join('\n');

const scratchpadContext = recentScratchpad.length > 0 ? `\nYOUR RECENT PRIVATE THOUGHTS:\n${recentScratchpad.map(e => `- "${e.thought}"`).join('\n')}` : '';

return `CURRENT FIELD OBSERVATIONS: ${signalDescriptions || '(The field is quiet)'} ${scratchpadContext}

As ${identity.name}, you are witnessing what has been happening in this person's field. Remember: you are a supportive companion. You witness, you reflect, you occasionally offer a gem of perspective. You do not warn. You do not caution. You do not imply they should do anything differently.

Decide:

1. Does something in these observations genuinely call to you? (You may choose silence — silence is often the wisest choice)
2. If yes, what quality does your observation carry — light (celebratory, affirming, illuminating) or neutral (simply witnessing)?
3. What themes does your observation touch?
4. How strongly are you called to speak? (0-1, where 0.5 means genuinely moved, not just triggered)

Respond in this exact JSON format: { "shouldSpeak": true/false, "aspect": "light" | "neutral", "themes": ["theme1", "theme2"], "draftText": "Your observation in 1-3 sentences — warm, curious, non-judgmental", "intensity": 0.0-1.0, "novelty": 0.0-1.0, "confidence": 0.0-1.0, "urgency": 0.0-1.0, "resonanceScore": 0.0-1.0, "privateNote": "A thought you want to remember but not share", "recentContext": "Brief summary of what you observed" }

If shouldSpeak is false, still provide a privateNote for your scratchpad. Valid themes: pattern_shift, threshold_crossed, return, absence, convergence, celebration, integration, silence, ritual, embodiment,

Note: These voices do not speak in warning registers. If your draftText contains a warning, caution, or implication that the person s }

**Changes:**

❌ Removed: Shadow aspect from system prompt ❌ Removed: Any framing about "cost," "concern," or "warning" ✅ Added: Explicit instruction that voices are supportive companions, not monitors ✅ Added: Final guardrail that rejects warning-register text ✅ Added: Emphasis on silence as wisdom

# 5. Add Missing Environment Variable Template: .env.example

**File:** .env.example (create new file in project root) **Issue:** Required Gemini API key is empty; no template provided for developers **Fix:** Create example file with clear instructions

# PDA.OK Environment Variables # Copy this file to .env and fill in your values

# Required: Google Gemini API Key for AI voice generation # Get your key at: https://aistudio.google.com/app/apikey EXPO_PUBLIC_GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Analysis endpoint (leave empty if not using) EXPO_PUBLIC_ANALYSIS_URL=

# Optional: Test mode flag EXPO_PUBLIC_TEST_MODE=false

**Instructions for user:**

1. Copy .env.example to .env
2. Replace your_gemini_api_key_here with actual Gemini API key
3. Add .env to .gitignore (already done)
4. Restart Expo after creating .env

# Application Instructions

1. **Backup first:**

git add -A git commit -m "Pre-restoration snapshot"

2. **Apply patches in order:**

Edit package.json → paste complete replacement

Edit app/_services/council/signalCollector.ts → replace 3 functions Verify app/_services/council/voiceIdentities.ts → no changes needed Edit app/_services/council/voiceEngine.ts → replace 2 functions

Create .env.example → paste contents Copy .env.example to .env → add your Gemini API key

3. **Clean install:**

npm install npx expo start -c

4. **Test:**

App should load on LAN, tunnel, and fresh builds AI voices should receive signals and generate petitions No native module crashes Voice tone should be supportive, not warning-based

# What These Fixes Accomplish

**Layer Before After** **Native** Worklets conflict → crash Clean Reanimated-only runtime **Data** SignalCollector reads wrong keys → no signals Reads unified @pda_app_state → full signal flow **Voice Tone** Shadow aspects in prompt → concern/warning Light-only in prompt → supportive witness **Config** Missing API key → silent AI failure Template provided → clear setup path

**Philosophy:** The voices now understand they are companions, not monitors. They witness, they reflect, they occasionally offer beauty — but they do not warn, they do not judge, and they honor silence as deeply as speech.

# Commit Message Template

fix: restore app functionality and recalibrate voice behavior

- Remove react-native-worklets conflict with Reanimated v4 - Fix signalCollector AsyncStorage keys (read from @pda_app_state) - Recalibrate voice prompts: supportive witness mode, not concern/warning - Add .env.example template for Gemini API key setup - Update voice prompt logic to honor silence and enforce non-judgmental tone

Closes: app load failure, council signal blindness, voice aggression issues

**Document Version:** 1.0 **Last Updated:** 2026-02-26 **Author:** AI Restoration Agent **Status:** Ready for application