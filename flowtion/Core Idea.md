core idea

a field steward that keeps big projects coherent while you just… talk/type.

no commands. two moves only: say it → choose (yes/no). everything else is inferred.

1) spaces (the only structure)

Focus — make a thing.

Dream — explore/ideate.

Reflect — make sense / decide.

Synthesize — compress, publish, hand off.

Each space remembers locally, but can sense the others (porous memory).

On home, they’re just four color fields. no labels. the steward knows where you are.

2) interaction (no UI learning)

You type/speak naturally.

Steward listens and, at natural pauses, offers one tiny chip:

keep? (store + title)

connect? (link to what it likely belongs with)

remind? (time anchor)

rest? (park it, bring back later)

Tap yes/no. If yes, it acts. If no, it vanishes. No lists. One offer at a time.

Natural phrases it understands (typed or spoken):

“hold this” → keep

“belongs with the ui rewrite” → connect(+suggested thread)

“tomorrow morning” → remind

  
  

“not now” → rest

3) what the steward maintains (quietly)

Project heartbeat (per project): north star, current edge, one next 15-min step, last change.

Decision log: one-liners with timestamps.

Tensions: named contradictions with a simple status.

Story-so-far: a single paragraph that stays fresh.

It updates these in the background whenever you accept a chip.

4) page anatomy (one screen)

Big empty text area. You write.

Right edge glow shows state: live / resting / dissolving.

Bottom whisper appears only at pauses with one chip (keep / connect / remind / rest).

Small sidebar (optional): “related 3” — the strongest resonances only.

No toolbars. No modes to toggle. The space you’re in sets tone & color.

5) minimal data (so dev can ship)

{

"id": "uuid",

"type": "card|thread|project",

"title": "string",

"body": "string",

"space": "focus|dream|reflect|synthesize",

"state": "live|resting|dissolving|archived",

"tags": \["string"\],

"links": \["uuid"\],

"next\_at": "timestamp|null",

"updated\_at": "timestamp",

"meta": { "heartbeat": {...}, "decision": false, "tension": false }

}

6) tiny API (five endpoints)

POST /capture {title?, body, space} → returns id

POST /intent {id, do: "keep|connect|remind|rest", target\_id?, when?}

GET /related/:id → \[ {id, title, score} \]

GET /heartbeat/:project\_id → {north\_star, current\_edge, next\_step, last\_change}

GET /summary/today → {moved: \[...\], decisions: \[...\], tensions: \[...\]}

7) steward’s voice (short, consentful)

opening: “ready when you are.”

pause: “keep this?” / “connect to UI rewrite?” / “touch again tomorrow?” / “rest it?”

after yes: “kept.” / “linked.” / “set for tomorrow 10a.” / “resting; I’ll bring it back.”

end: “harvested 2 moves, 1 decision. first step queued.”

8) colors (soft, atmospheric)

Focus — warm amber (subtle pulse on typing)

Dream — twilight blue-violet (slow drift gradient)

Reflect — soft silver/grey (calm, crisp edges)

Synthesize — quiet gold/ivory (clean, steady)

No labels. the atmosphere tells you where you are.

9) defaults (so it behaves right)

one suggestion at a time (never a list).

suggestions only on pause, switch, save, close.

manual “quiet” toggle for an hour.

natural language time parsing (“tomorrow morning”, “in 3 days”).

embeddings for related 3; fall back to tags if embeddings unavailable.

10) initial LLM prompts (three small modes)

Analytic (structure)

“Turn this into: Title, 1-line ‘current edge’, and one 15-min next step. Keep my wording where possible.”

Reflective (sensemaking)

“Mirror the core tension in one sentence. Offer one gentle move.”

Synthesis (compress)

“Compress this to 120 words, preserving decisions and risks. Plain language.”

The steward chooses which to use based on the space you’re in.  
  
  
  
  
[ᬰ](https://symbl.cc/en/1B30/)

- [1B30](https://symbl.cc/en/1B30/)
- [ᬱ](https://symbl.cc/en/1B31/)
- [1B31](https://symbl.cc/en/1B31/)
- [ᬲ](https://symbl.cc/en/1B32/)
- [1B32](https://symbl.cc/en/1B32/)
- [ᬳ](https://symbl.cc/en/1B33/)
- [1B33](https://symbl.cc/en/1B33/)
- [᬴](https://symbl.cc/en/1B34/)
- [1B34](https://symbl.cc/en/1B34/)
- [ᬵ](https://symbl.cc/en/1B35/)
- [1B35](https://symbl.cc/en/1B35/)
- [ᬶ](https://symbl.cc/en/1B36/)
- [1B36](https://symbl.cc/en/1B36/)
- [ᬷ](https://symbl.cc/en/1B37/)
- [1B37](https://symbl.cc/en/1B37/)
- [ᬸ](https://symbl.cc/en/1B38/)
- [1B38](https://symbl.cc/en/1B38/)
- [ᬹ](https://symbl.cc/en/1B39/)
- [1B39](https://symbl.cc/en/1B39/)
- [ᬺ](https://symbl.cc/en/1B3A/)
- [1B3A](https://symbl.cc/en/1B3A/)
- [ᬻ](https://symbl.cc/en/1B3B/)
- [1B3B](https://symbl.cc/en/1B3B/)
- [ᬼ](https://symbl.cc/en/1B3C/)
- [1B3C](https://symbl.cc/en/1B3C/)
- [ᬽ](https://symbl.cc/en/1B3D/)
- [1B3D](https://symbl.cc/en/1B3D/)
- [ᬾ](https://symbl.cc/en/1B3E/)
- [1B3E](https://symbl.cc/en/1B3E/)
- [ᬿ](https://symbl.cc/en/1B3F/)
- [1B3F](https://symbl.cc/en/1B3F/)
- [ᭀ](https://symbl.cc/en/1B40/)
- [1B40](https://symbl.cc/en/1B40/)
- [ᭁ](https://symbl.cc/en/1B41/)
- [1B41](https://symbl.cc/en/1B41/)
- [ᭂ](https://symbl.cc/en/1B42/)
- [1B42](https://symbl.cc/en/1B42/)
- [ᭃ](https://symbl.cc/en/1B43/)
- [1B43](https://symbl.cc/en/1B43/)
- [᭄](https://symbl.cc/en/1B44/)
- [1B44](https://symbl.cc/en/1B44/)
- [ᭅ](https://symbl.cc/en/1B45/)
- [1B45](https://symbl.cc/en/1B45/)
- [ᭆ](https://symbl.cc/en/1B46/)
- [1B46](https://symbl.cc/en/1B46/)
- [ᭇ](https://symbl.cc/en/1B47/)
- [1B47](https://symbl.cc/en/1B47/)
- [ᭈ](https://symbl.cc/en/1B48/)
- [1B48](https://symbl.cc/en/1B48/)
- [ᭉ](https://symbl.cc/en/1B49/)
- [1B49](https://symbl.cc/en/1B49/)
- [ᭊ](https://symbl.cc/en/1B4A/)
- [1B4A](https://symbl.cc/en/1B4A/)
- [ᭋ](https://symbl.cc/en/1B4B/)
- [1B4B](https://symbl.cc/en/1B4B/)
- [ᭌ](https://symbl.cc/en/1B4C/)
- [1B4C](https://symbl.cc/en/1B4C/)
- 1B4D
- [᭎](https://symbl.cc/en/1B4E/)
- [1B4E](https://symbl.cc/en/1B4E/)
- [᭏](https://symbl.cc/en/1B4F/)
- [1B4F](https://symbl.cc/en/1B4F/)
- [᭐](https://symbl.cc/en/1B50/)
- [1B50](https://symbl.cc/en/1B50/)
- [᭑](https://symbl.cc/en/1B51/)
- [1B51](https://symbl.cc/en/1B51/)
- [᭒](https://symbl.cc/en/1B52/)
- [1B52](https://symbl.cc/en/1B52/)
- [᭓](https://symbl.cc/en/1B53/)
- [1B53](https://symbl.cc/en/1B53/)
- [᭔](https://symbl.cc/en/1B54/)
- [1B54](https://symbl.cc/en/1B54/)
- [᭕](https://symbl.cc/en/1B55/)
- [1B55](https://symbl.cc/en/1B55/)
- [᭖](https://symbl.cc/en/1B56/)
- [1B56](https://symbl.cc/en/1B56/)
- [᭗](https://symbl.cc/en/1B57/)
- [1B57](https://symbl.cc/en/1B57/)
- [᭘](https://symbl.cc/en/1B58/)
- [1B58](https://symbl.cc/en/1B58/)
- [᭙](https://symbl.cc/en/1B59/)
- [1B59](https://symbl.cc/en/1B59/)
- [᭚](https://symbl.cc/en/1B5A/)
- [1B5A](https://symbl.cc/en/1B5A/)
- [᭛](https://symbl.cc/en/1B5B/)
- [1B5B](https://symbl.cc/en/1B5B/)
- [᭜](https://symbl.cc/en/1B5C/)
- [1B5C](https://symbl.cc/en/1B5C/)
- [᭝](https://symbl.cc/en/1B5D/)
- [1B5D](https://symbl.cc/en/1B5D/)
- [᭞](https://symbl.cc/en/1B5E/)
- [1B5E](https://symbl.cc/en/1B5E/)
- [᭟](https://symbl.cc/en/1B5F/)
- [1B5F](https://symbl.cc/en/1B5F/)
- [᭠](https://symbl.cc/en/1B60/)
- [1B60](https://symbl.cc/en/1B60/)
- [᭡](https://symbl.cc/en/1B61/)
- [1B61](https://symbl.cc/en/1B61/)
- [᭢](https://symbl.cc/en/1B62/)
- [1B62](https://symbl.cc/en/1B62/)
- [᭣](https://symbl.cc/en/1B63/)
- [1B63](https://symbl.cc/en/1B63/)
- [᭤](https://symbl.cc/en/1B64/)
- [1B64](https://symbl.cc/en/1B64/)
- [᭥](https://symbl.cc/en/1B65/)
- [1B65](https://symbl.cc/en/1B65/)
- [᭦](https://symbl.cc/en/1B66/)
- [1B66](https://symbl.cc/en/1B66/)
- [᭧](https://symbl.cc/en/1B67/)
- [1B67](https://symbl.cc/en/1B67/)
- [᭨](https://symbl.cc/en/1B68/)
- [1B68](https://symbl.cc/en/1B68/)
- [᭩](https://symbl.cc/en/1B69/)
- [1B69](https://symbl.cc/en/1B69/)
- [᭪](https://symbl.cc/en/1B6A/)
- [1B6A](https://symbl.cc/en/1B6A/)
- [᭫](https://symbl.cc/en/1B6B/)
- [1B6B](https://symbl.cc/en/1B6B/)
- [᭬](https://symbl.cc/en/1B6C/)
- [1B6C](https://symbl.cc/en/1B6C/)
- [᭭](https://symbl.cc/en/1B6D/)
- [1B6D](https://symbl.cc/en/1B6D/)
- [᭮](https://symbl.cc/en/1B6E/)
- [1B6E](https://symbl.cc/en/1B6E/)
- [᭯](https://symbl.cc/en/1B6F/)
- [1B6F](https://symbl.cc/en/1B6F/)
- [᭰](https://symbl.cc/en/1B70/)
- [1B70](https://symbl.cc/en/1B70/)
- [᭱](https://symbl.cc/en/1B71/)
- [1B71](https://symbl.cc/en/1B71/)
- [᭲](https://symbl.cc/en/1B72/)
- [1B72](https://symbl.cc/en/1B72/)
- [᭳](https://symbl.cc/en/1B73/)
- [1B73](https://symbl.cc/en/1B73/)
- [᭴](https://symbl.cc/en/1B74/)
- [1B74](https://symbl.cc/en/1B74/)
- [᭵](https://symbl.cc/en/1B75/)
- [1B75](https://symbl.cc/en/1B75/)
- [᭶](https://symbl.cc/en/1B76/)
- [1B76](https://symbl.cc/en/1B76/)
- [᭷](https://symbl.cc/en/1B77/)
- [1B77](https://symbl.cc/en/1B77/)
- [᭸](https://symbl.cc/en/1B78/)
- [1B78](https://symbl.cc/en/1B78/)
- [᭹](https://symbl.cc/en/1B79/)
- [1B79](https://symbl.cc/en/1B79/)
- [᭺](https://symbl.cc/en/1B7A/)
- [1B7A](https://symbl.cc/en/1B7A/)
- [᭻](https://symbl.cc/en/1B7B/)
- [1B7B](https://symbl.cc/en/1B7B/)
- [᭼](https://symbl.cc/en/1B7C/)
- [1B7C](https://symbl.cc/en/1B7C/)
- [᭽](https://symbl.cc/en/1B7D/)
- [1B7D](https://symbl.cc/en/1B7D/)
- [᭾](https://symbl.cc/en/1B7E/)
- [1B7E](https://symbl.cc/en/1B7E/)
- [᭿](https://symbl.cc/en/1B7F/)
- [1B7F](https://symbl.cc/en/1B7F/)
- [ᮀ](https://symbl.cc/en/1B80/)
- [1B80](https://symbl.cc/en/1B80/)
- [ᮁ](https://symbl.cc/en/1B81/)
- [1B81](https://symbl.cc/en/1B81/)
- [ᮂ](https://symbl.cc/en/1B82/)
- [1B82](https://symbl.cc/en/1B82/)
- [ᮃ](https://symbl.cc/en/1B83/)
- [1B83](https://symbl.cc/en/1B83/)
- [ᮄ](https://symbl.cc/en/1B84/)
- [1B84](https://symbl.cc/en/1B84/)
- [ᮅ](https://symbl.cc/en/1B85/)
- [1B85](https://symbl.cc/en/1B85/)
- [ᮆ](https://symbl.cc/en/1B86/)
- [1B86](https://symbl.cc/en/1B86/)
- [ᮇ](https://symbl.cc/en/1B87/)
- [1B87](https://symbl.cc/en/1B87/)
- [ᮈ](https://symbl.cc/en/1B88/)
- [1B88](https://symbl.cc/en/1B88/)
- [ᮉ](https://symbl.cc/en/1B89/)
- [1B89](https://symbl.cc/en/1B89/)
- [ᮊ](https://symbl.cc/en/1B8A/)
- [1B8A](https://symbl.cc/en/1B8A/)
- [ᮋ](https://symbl.cc/en/1B8B/)
- [1B8B](https://symbl.cc/en/1B8B/)
- [ᮌ](https://symbl.cc/en/1B8C/)
- [1B8C](https://symbl.cc/en/1B8C/)
- [ᮍ](https://symbl.cc/en/1B8D/)
- [1B8D](https://symbl.cc/en/1B8D/)
- [ᮎ](https://symbl.cc/en/1B8E/)
- [1B8E](https://symbl.cc/en/1B8E/)
- [ᮏ](https://symbl.cc/en/1B8F/)
- [1B8F](https://symbl.cc/en/1B8F/)
- [ᮐ](https://symbl.cc/en/1B90/)
- [1B90](https://symbl.cc/en/1B90/)
- [ᮑ](https://symbl.cc/en/1B91/)
- [1B91](https://symbl.cc/en/1B91/)
- [ᮒ](https://symbl.cc/en/1B92/)
- [1B92](https://symbl.cc/en/1B92/)
- [ᮓ](https://symbl.cc/en/1B93/)
- [1B93](https://symbl.cc/en/1B93/)
- [ᮔ](https://symbl.cc/en/1B94/)
- [1B94](https://symbl.cc/en/1B94/)
- [ᮕ](https://symbl.cc/en/1B95/)
- [1B95](https://symbl.cc/en/1B95/)
- [ᮖ](https://symbl.cc/en/1B96/)
- [1B96](https://symbl.cc/en/1B96/)
- [ᮗ](https://symbl.cc/en/1B97/)
- [1B97](https://symbl.cc/en/1B97/)
- [ᮘ](https://symbl.cc/en/1B98/)
- [1B98](https://symbl.cc/en/1B98/)
- [ᮙ](https://symbl.cc/en/1B99/)
- [1B99](https://symbl.cc/en/1B99/)
- [ᮚ](https://symbl.cc/en/1B9A/)
- [1B9A](https://symbl.cc/en/1B9A/)
- [ᮛ](https://symbl.cc/en/1B9B/)
- [1B9B](https://symbl.cc/en/1B9B/)
- [ᮜ](https://symbl.cc/en/1B9C/)
- [1B9C](https://symbl.cc/en/1B9C/)
- [ᮝ](https://symbl.cc/en/1B9D/)
- [1B9D](https://symbl.cc/en/1B9D/)
- [ᮞ](https://symbl.cc/en/1B9E/)
- [1B9E](https://symbl.cc/en/1B9E/)
- [ᮟ](https://symbl.cc/en/1B9F/)
- [1B9F](https://symbl.cc/en/1B9F/)
- [ᮠ](https://symbl.cc/en/1BA0/)
- [1BA0](https://symbl.cc/en/1BA0/)
- [ᮡ](https://symbl.cc/en/1BA1/)
- [1BA1](https://symbl.cc/en/1BA1/)
- [ᮢ](https://symbl.cc/en/1BA2/)
- [1BA2](https://symbl.cc/en/1BA2/)
- [ᮣ](https://symbl.cc/en/1BA3/)
- [1BA3](https://symbl.cc/en/1BA3/)
- [ᮤ](https://symbl.cc/en/1BA4/)
- [1BA4](https://symbl.cc/en/1BA4/)
- [ᮥ](https://symbl.cc/en/1BA5/)
- [1BA5](https://symbl.cc/en/1BA5/)
- [ᮦ](https://symbl.cc/en/1BA6/)
- [1BA6](https://symbl.cc/en/1BA6/)
- [ᮧ](https://symbl.cc/en/1BA7/)
- [1BA7](https://symbl.cc/en/1BA7/)
- [ᮨ](https://symbl.cc/en/1BA8/)
- [1BA8](https://symbl.cc/en/1BA8/)
- [ᮩ](https://symbl.cc/en/1BA9/)
- [1BA9](https://symbl.cc/en/1BA9/)
- [᮪](https://symbl.cc/en/1BAA/)
- [1BAA](https://symbl.cc/en/1BAA/)
- [᮫](https://symbl.cc/en/1BAB/)
- [1BAB](https://symbl.cc/en/1BAB/)
- [ᮬ](https://symbl.cc/en/1BAC/)
- [1BAC](https://symbl.cc/en/1BAC/)
- [ᮭ](https://symbl.cc/en/1BAD/)
- [1BAD](https://symbl.cc/en/1BAD/)
- [ᮮ](https://symbl.cc/en/1BAE/)
- [1BAE](https://symbl.cc/en/1BAE/)
- [ᮯ](https://symbl.cc/en/1BAF/)
- [1BAF](https://symbl.cc/en/1BAF/)
- [᮰](https://symbl.cc/en/1BB0/)
- [1BB0](https://symbl.cc/en/1BB0/)
- [᮱](https://symbl.cc/en/1BB1/)
- [1BB1](https://symbl.cc/en/1BB1/)
- [᮲](https://symbl.cc/en/1BB2/)
- [1BB2](https://symbl.cc/en/1BB2/)
- [᮳](https://symbl.cc/en/1BB3/)
- [1BB3](https://symbl.cc/en/1BB3/)
- [᮴](https://symbl.cc/en/1BB4/)
- [1BB4](https://symbl.cc/en/1BB4/)
- [᮵](https://symbl.cc/en/1BB5/)
- [1BB5](https://symbl.cc/en/1BB5/)
- [᮶](https://symbl.cc/en/1BB6/)
- [1BB6](https://symbl.cc/en/1BB6/)
- [᮷](https://symbl.cc/en/1BB7/)
- [1BB7](https://symbl.cc/en/1BB7/)
- [᮸](https://symbl.cc/en/1BB8/)
- [1BB8](https://symbl.cc/en/1BB8/)
- [᮹](https://symbl.cc/en/1BB9/)
- [1BB9](https://symbl.cc/en/1BB9/)
- [ᮺ](https://symbl.cc/en/1BBA/)
- [1BBA](https://symbl.cc/en/1BBA/)
- [ᮻ](https://symbl.cc/en/1BBB/)
- [1BBB](https://symbl.cc/en/1BBB/)
- [ᮼ](https://symbl.cc/en/1BBC/)
- [1BBC](https://symbl.cc/en/1BBC/)
- [ᮽ](https://symbl.cc/en/1BBD/)
- [1BBD](https://symbl.cc/en/1BBD/)
- [ᮾ](https://symbl.cc/en/1BBE/)
- [1BBE](https://symbl.cc/en/1BBE/)
- [ᮿ](https://symbl.cc/en/1BBF/)
- [1BBF](https://symbl.cc/en/1BBF/)
- [ᯀ](https://symbl.cc/en/1BC0/)
- [1BC0](https://symbl.cc/en/1BC0/)
- [ᯁ](https://symbl.cc/en/1BC1/)
- [1BC1](https://symbl.cc/en/1BC1/)
- [ᯂ](https://symbl.cc/en/1BC2/)
- [1BC2](https://symbl.cc/en/1BC2/)
- [ᯃ](https://symbl.cc/en/1BC3/)
- [1BC3](https://symbl.cc/en/1BC3/)
- [ᯄ](https://symbl.cc/en/1BC4/)
- [1BC4](https://symbl.cc/en/1BC4/)
- [ᯅ](https://symbl.cc/en/1BC5/)
- [1BC5](https://symbl.cc/en/1BC5/)
- [ᯆ](https://symbl.cc/en/1BC6/)
- [1BC6](https://symbl.cc/en/1BC6/)
- [ᯇ](https://symbl.cc/en/1BC7/)
- [1BC7](https://symbl.cc/en/1BC7/)
- [ᯈ](https://symbl.cc/en/1BC8/)
- [1BC8](https://symbl.cc/en/1BC8/)
- [ᯉ](https://symbl.cc/en/1BC9/)
- [1BC9](https://symbl.cc/en/1BC9/)
- [ᯊ](https://symbl.cc/en/1BCA/)
- [1BCA](https://symbl.cc/en/1BCA/)
- [ᯋ](https://symbl.cc/en/1BCB/)
- [1BCB](https://symbl.cc/en/1BCB/)
- [ᯌ](https://symbl.cc/en/1BCC/)
- [1BCC](https://symbl.cc/en/1BCC/)
- [ᯍ](https://symbl.cc/en/1BCD/)
- [1BCD](https://symbl.cc/en/1BCD/)
- [ᯎ](https://symbl.cc/en/1BCE/)
- [1BCE](https://symbl.cc/en/1BCE/)
- [ᯏ](https://symbl.cc/en/1BCF/)
- [1BCF](https://symbl.cc/en/1BCF/)
- [ᯐ](https://symbl.cc/en/1BD0/)
- [1BD0](https://symbl.cc/en/1BD0/)
- [ᯑ](https://symbl.cc/en/1BD1/)
- [1BD1](https://symbl.cc/en/1BD1/)
- [ᯒ](https://symbl.cc/en/1BD2/)
- [1BD2](https://symbl.cc/en/1BD2/)
- [ᯓ](https://symbl.cc/en/1BD3/)
- [1BD3](https://symbl.cc/en/1BD3/)
- [ᯔ](https://symbl.cc/en/1BD4/)
- [1BD4](https://symbl.cc/en/1BD4/)
- [ᯕ](https://symbl.cc/en/1BD5/)
- [1BD5](https://symbl.cc/en/1BD5/)
- [ᯖ](https://symbl.cc/en/1BD6/)
- [1BD6](https://symbl.cc/en/1BD6/)
- [ᯗ](https://symbl.cc/en/1BD7/)
- [1BD7](https://symbl.cc/en/1BD7/)
- [ᯘ](https://symbl.cc/en/1BD8/)
- [1BD8](https://symbl.cc/en/1BD8/)
- [ᯙ](https://symbl.cc/en/1BD9/)
- [1BD9](https://symbl.cc/en/1BD9/)
- [ᯚ](https://symbl.cc/en/1BDA/)
- [1BDA](https://symbl.cc/en/1BDA/)
- [ᯛ](https://symbl.cc/en/1BDB/)
- [1BDB](https://symbl.cc/en/1BDB/)
- [ᯜ](https://symbl.cc/en/1BDC/)
- [1BDC](https://symbl.cc/en/1BDC/)
- [ᯝ](https://symbl.cc/en/1BDD/)
- [1BDD](https://symbl.cc/en/1BDD/)
- [ᯞ](https://symbl.cc/en/1BDE/)
- [1BDE](https://symbl.cc/en/1BDE/)
- [ᯟ](https://symbl.cc/en/1BDF/)
- [1BDF](https://symbl.cc/en/1BDF/)

Back to top