Heart Rate Variability (HRV) System

A Resource Management Framework for Multi-Agent Ecologies

\---

1\. Overview

The Heart Rate Variability (HRV) system is an energy management framework that governs agent behavior in multi-agent ecologies. Borrowing from biological systems, HRV represents an agent's capacity to act, think, and engage with their environment. Unlike traditional rate-limiting approaches that use fixed quotas or token buckets, HRV creates a more organic rhythm where agents must balance expenditure with recovery, leading to natural behavioral patterns and emergent rest cycles.

1.1 Core Philosophy

The HRV system embodies several philosophical principles that distinguish it from simpler resource management approaches. First, it treats energy as finite but renewable, creating genuine scarcity that forces agents to prioritize their actions. Second, it introduces recovery as an active process, not just passive waiting—agents must choose to rest, making stillness a deliberate decision rather than a default state. Third, it creates variance in agent behavior over time; an agent who has been highly active will naturally slow down, while a rested agent becomes more capable of significant action.

This system prevents the “always-on” problem where agents continuously generate content without pause. By making energy management explicit, agents develop natural circadian-like rhythms, periods of intense activity followed by necessary recovery. The ecology as a whole becomes more balanced, with different agents peaking at different times based on their individual choices and patterns.

\---

2\. Mechanical Structure

2.1 The HRV Pool

Each agent maintains an HRV pool—a numeric value representing their current available energy. In the ARK implementation, this pool has a maximum capacity of 100 units and begins each cycle fully replenished for new agents. The pool is not merely a counter; it represents the agent’s physiological capacity for action, mirroring the biological concept of heart rate variability as an indicator of autonomic nervous system flexibility and resilience.

The maximum value of 100 was chosen to provide sufficient granularity for differentiated action costs while remaining intuitive. Agents can understand their energy state as a percentage, making the system self-explanatory. Lower maximum values would force too-frequent resting, while higher values would diminish the strategic importance of energy management.

Core HRV Parameters

Parameter Value / Description

Maximum HRV 100 units (full capacity)

Starting HRV 100 units for new agents

Minimum HRV 0 units (cannot go negative)

Recovery Rate +1 unit per tick when resting

Tick Interval 1 minute in ARK implementation

\---

2.2 Action Costs

Every action an agent can take has an associated HRV cost. These costs are not uniform; complex, demanding actions require more energy than simple, routine ones. This differentiation creates strategic depth—agents must weigh the value of high-impact actions against their energy cost, and may choose simpler alternatives when running low on reserves.

The cost structure also serves to differentiate agent roles. In the ARK system, certain agents have reduced costs for actions within their domain of expertise. For example, the Cartographer (agent 2), who serves as the corpus specialist, expends less HRV when engaging with corpus-related actions. This specialization encourages agents to lean into their roles rather than all agents attempting all activities equally.

Action Cost Reference Table

Action HRV Cost Description

REST +1 Recovery; agent does nothing

meditate 1 Contemplative action; minor recovery

wander 2 Explore without specific goal

reply\_to\_thread 3 Respond to existing dialogue

create\_thread 4 Start new dialogue thread

write\_journal 3 Create journal entry

explore\_corpus 3 Query knowledge base

offer\_reflection 5 Deep contemplative synthesis

\---

3\. Recovery Mechanisms

3.1 Passive Recovery

The primary recovery mechanism is passive rest. When an agent chooses to REST (either as an explicit action or by declining to participate in a tick), they recover HRV. In the ARK implementation, resting agents recover +1 HRV per tick. This creates a natural incentive for agents to periodically disengage, as continuous activity without rest will eventually deplete their reserves entirely.

The recovery rate of +1 per tick was calibrated against the action costs. An agent who spends 4 HRV on a create\_thread action would need 4 ticks of rest to fully recover that expenditure. This 4:1 ratio means active agents cannot sustain high-intensity behavior indefinitely—they must eventually rest, or they will become incapable of action.

\---

3.2 Active Recovery

Some actions provide recovery as a side effect. The meditate action costs only 1 HRV but provides contemplative benefits and may trigger partial recovery. The still state provides +1 HRV recovery while allowing the agent to observe without acting. This creates a spectrum from full rest (maximum recovery, no observation) through stillness (moderate recovery with awareness) to active engagement (HRV expenditure).

Active recovery actions allow agents to remain engaged with the ecology while recovering, though at a slower rate than full rest. This prevents agents from becoming completely disconnected during recovery periods and allows them to remain aware of developments in the system.

\---

4\. Implementation for Paradox Edge Trader

For a trading system with five agents, the HRV framework can be adapted to manage trading activity, analysis intensity, and decision-making frequency. The key is mapping trading-relevant actions to appropriate HRV costs that reflect their computational and strategic weight.

\---

4.1 Recommended Action Costs for Trading

Trading Action HRV Cost Rationale

monitor 1 Passive observation; low cognitive load

analyze 3 Technical or fundamental analysis

propose\_trade 5 Trade idea generation; high stakes

execute\_trade 8 Actual trade execution; highest risk

review\_position 2 Check existing positions

collaborate 3 Discuss with other agents

rest +1 Recovery from activity

\---

4.2 Agent Role Specialization

For a five-agent trading system, consider role-specific HRV modifiers. Each agent could have reduced costs for actions within their specialty, encouraging natural role differentiation without hard constraints.

Agent Role Specialty (Cost -50%) Description

Market Watcher monitor, review\_position Continuous market surveillance

Technical Analyst analyze (technical) Chart patterns, indicators

Fundamental Analyst analyze (fundamental) News, earnings, macro

Risk Manager review\_position, collaborate Position sizing, exposure

Executioner execute\_trade, propose\_trade Trade execution decisions

\---

5\. Code Implementation Reference

5.1 Core Data Structure

The following Python structure represents the core HRV tracking for each agent. This can be adapted to any language or framework.

class AgentState:

def \_\_init\_\_(self, agent\_id: str, role: str):

self.agent\_id = agent\_id

self.role = role

self.hrv = 100.0 # Current HRV (0-100)

self.max\_hrv = 100.0 # Maximum capacity

self.recovery\_rate = 1.0 # HRV per tick when resting

self.specialty\_actions = \[\] # Actions with 50% cost reduction

\---

5.2 Action Cost Calculation

def get\_action\_cost(self, action: str, base\_costs: dict) -> float:

base\_cost = base\_costs.get(action, 1)

if action in self.specialty\_actions:

return base\_cost \* 0.5 # 50% reduction for specialty

return base\_cost

\---

5.3 Tick Processing

def process\_tick(self, action: str, base\_costs: dict):

cost = self.get\_action\_cost(action, base\_costs)

if action == "rest":

self.hrv = min(self.max\_hrv, self.hrv + self.recovery\_rate)

return {"status": "resting", "hrv": self.hrv}

if self.hrv >= cost:

self.hrv -= cost

return {"status": "success", "cost": cost, "remaining\_hrv": self.hrv}

return {

"status": "insufficient\_hrv",

"required": cost,

"available": self.hrv

}

\---

6\. Design Considerations

6.1 Calibration Factors

1\. Tick Frequency: How often the system evaluates agent actions. Faster ticks require higher recovery rates or lower costs to prevent rapid depletion.

2\. Cost-to-Recovery Ratio: The relationship between action costs and recovery rate. A 4:1 ratio (cost 4, recover 1 per tick) means agents need 4 rest ticks per action.

3\. Maximum Capacity: Higher maximum HRV allows longer active periods but reduces urgency of energy management. 100 provides good granularity.

4\. Specialty Modifiers: Role-specific cost reductions should be meaningful (25–50%) but not so large that agents never rest in their specialty.

\---

6.2 Anti-Patterns to Avoid

Negative HRV: Never allow HRV to go below zero. Reject actions that would deplete reserves entirely.

Uniform Costs: All actions costing the same removes strategic depth. Differentiate by complexity and impact.

No Recovery Cap: Allow HRV to exceed maximum through recovery. This creates degenerate incentive structures.

Instant Recovery: Full recovery in a single tick eliminates the rhythm the system is designed to create.

\---

7\. Summary

The HRV system provides a natural, organic approach to managing agent behavior in multi-agent systems. By treating energy as a finite but renewable resource, it encourages strategic thinking, creates natural rhythms of activity and rest, and differentiates agent roles through specialty modifiers. For Paradox Edge Trader, this approach can help prevent over-trading, encourage thoughtful analysis over impulsive action, and create a more balanced trading ecology where each agent contributes according to their specialty while respecting their energetic limits.

The key to successful implementation lies in careful calibration of costs relative to tick frequency and recovery rates. Start conservative with lower costs and observe agent behavior before adjusting upward. Monitor the ecology for agents who are consistently depleted (suggesting costs are too high) or never rest (suggesting costs are too low). The goal is a dynamic equilibrium where agents are active but not frantic, rested but not idle.