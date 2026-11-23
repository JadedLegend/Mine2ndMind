## PHASE 3: Agent Architecture & Coordination
**What this solves:** Making the Claw Community ecology actually function.

| Repo | What to extract | Already researched? |
|------|----------------|-------------------|
| [jeriko](https://github.com/EtheonAI/jeriko) | Circuit breaker, execution guard, typed event bus, connector interface, command policy engine. Already extracted patterns. | Yes — EXTRACTED, HIGH VALUE |
| [deer-flow](https://github.com/bytedance/deer-flow) | ByteDance's agent flow system. | NEW |
| [serena](https://github.com/oraios/serena) | Agent framework patterns. | NEW |
| [ArgentAIOS/core](https://github.com/ArgentAIOS/core) | Core/Business/Shared layer architecture. | Yes — NOTED as placeholder |
| [Awesome-Human-Agent-Collaboration](https://github.com/HenryPengZou/Awesome-Human-Agent-Collaboration-Interaction-Systems) | Academic survey. Design philosophy reference. | Yes — RESEARCHED |
| [AgentHub](https://github.com/jamesrochabrun/AgentHub) | Agent hub patterns. | NEW (different from nathangtg version) |

**Instruction to Code:** "These repos are about multi-agent coordination. My ecology has 5 agents on a VPS running OpenClaw. Read the distillation document first (claw-community-distillation.md), THEN study these repos. Tell me what patterns would help my specific agents coordinate better — not in theory, but given what's actually deployed."