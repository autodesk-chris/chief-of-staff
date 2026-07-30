# MFM Prep: User Engagement - July 2026

Source: [July 26 MFM](https://autodesk.atlassian.net/wiki/spaces/fdo/pages/988122417/July+26+Monthly+Focus+Meeting) | Previous: MFM - User Engagement, 9 June 2026 (Granola)

Main focus this meeting: KR1 reversed from ~2.4% in June to 0.77% while Trig coverage kept expanding, so diagnose the reversal before committing more coverage.

## Pre-read summary

### Key points

- KR1 (SD first strike delta) fell every week in June, from 2.44% to 1.99% to 1.32% to 0.77%, back near the 0.75% priority baseline.
- KR2 (Board first strike) mirrored the pattern and now sits at 0.11%.
- Site-entered users active 2+ days/month reversed from 37.2% to 31.2%, now below the 35% baseline.
- Trig Stage 3 objectives live for all 3 company-size bands; Stage 4 build now prioritised ahead of Stage 3 emails.
- Two closed re-engagement experiments (post-click redirect, AUM re-engagement) both inconclusive; folded into an org-first restructure and the admin/user split was dropped for simplicity.
- Entry-point job email copy rewritten after user reports the previous version read as spam/phishing (likely contributor to the low-open bottleneck flagged in June).
- In-product learning nudge experiment is design-locked, blocked only on Intercom event whitelisting (Ammar, Anton).
- Autodesk Assistant / Fin integration now aligned with Chris and Amar; moving from planning into delivery.
- CX Score now reported as a Fin+Teammate blended read of 61% (Fin 69.6%, Teammate 59.3%), replacing the Fin-only 67% read used in June.
- Objective 4 on track on volume (12 interviews, 44 opt-ins), but the pre-read explicitly flags the product-side insight-to-action loop as broken.
- July is scoped as a 6-week cycle (to end of August) given summer holidays and reduced capacity.
- Intercom migration complete (go-live 3 July); permission bug found and fixed post-launch.

### Strong points of view

- "This looks like a volume problem, not a coverage one" (opens are the consistent bottleneck across every closed experiment and geo/control analysis, sample sizes too small to prove lift either way).
- The BD Fin content gap traced back to audience scoping, not a Fin capability gap, so similar invisible-content gaps across BD/Board are worth checking proactively.
- Access and timing were never the barrier to learning; the next lever is in-product learning at the moment of need (carried from June, still the operating hypothesis).

### Key data points

| Metric                                 | Value                                            | Context                                                           |
| -------------------------------------- | ------------------------------------------------ | ----------------------------------------------------------------- |
| KR1 SD first strike (days 2-7)         | 0.85% (0.77% peak-of-month)                      | 2.3% baseline, 5% target, was 2.4% in June                        |
| KR2 Board first strike                 | 0.11%                                            | 1.4% baseline, 5% target, was 0.4% in June                        |
| Obj 2 KR1 job coverage                 | 28% (10 of 35 jobs)                              | New metric definition; June reported no comparable value          |
| Obj 2 KR2 new users active 2+ days     | 36.4%                                            | 38% baseline, 60% target, was 37.4% in June                       |
| Obj 2 KR3 current users active 2+ days | 42.8%                                            | 50% baseline, 65% target, was 49.2% in June                       |
| Fin AI resolution rate                 | 86.9%                                            | 85% target, on track                                              |
| CX Score blended                       | 61%                                              | Fin 69.6% + Teammate 59.3%; new definition, June was 67% Fin-only |
| ICP interviews (last 4-6 weeks)        | 12                                               | Target 5+/month, on track                                         |
| Opted-in panel (cumulative)            | 44                                               | Target 50+, on track                                              |
| Experiment velocity (July pre-read)    | Live 3, In Dev 3, Backlog 2, Idea 2, Completed 2 | Down from Live 6 in June                                          |

### Decisions in the pre-read

- Trial users stay in the same Trig lifecycle stages, differentiated only by job/email content (settled after last month's decision to explore separate trial lifecycle).
- Admin/user split in the AUM re-engagement job dropped; single org-level target instead.
- Scenarios and FCC content deprioritised, scenarios launch pushed to Q3.
- July priorities carried forward from June rather than reopened against the latest squad strategy.

### Asks

- Instrumentation for Building Design FSM (unblocks Trig BD stages, previously flagged in May and June).
- Product-side ownership for Objective 4's insight-to-action loop (unblocks turning interview volume into product changes).

---

## Your 4Ps lens (week of June 15)

| Your priority | What it means for this MFM |
| --- | --- |
| Win the US | Trial Users research sprint and Kevin's US First Strike scan are the direct US inputs. Push Joseph to name the US decision this feeds, not just the report. |
| Trig | You agreed the June scope with Arne (stages 1-3 for Small/Medium). Stage 4 is now prioritised ahead of Stage 3 emails; check the trade-off is deliberate, not drift. |
| Accelerate agentic-first adoption across Growth | Squad has shipped a strong agent portfolio (Trig agent, /find_insights, /feedback-scan, /eod, /slides). Good signal, worth naming as the standard for other squads. |
| Operations (engineering FTE hiring) | Contractor start-of-August is on the plan; confirm it lands or the Autodesk Assistant delivery slips. |

---

## 1. Actions agreed 9 June - status check

| Agreed action | Status | Notes |
| --- | --- | --- |
| Redefine re-engagement metric as job coverage ratio (jobs live vs jobs needed) | Done | Reported this month as 28% (10 of 35 jobs). |
| Ana to share authoring system phasing plan within a week | Silently dropped | Not mentioned in the July pre-read. Worth checking. |
| Joe to assess seconding team members to hit end-of-June Trig coverage | Drifted | Stage 4 build now prioritised over Stage 3 emails; no mention of a resourcing shift. Coverage build continued but the delta reversed. |
| Each team member to define one focused June initiative with 2-3 deliverables | Partial | Visible for some (Malak content library, Kevin ticket tools, Clément research); patchy for others. |
| Get help button usage data across the user base (Malak) | Silently dropped | Not mentioned in the July pre-read. |
| Share Slack thread on Scenarios launch timeline for escalation to Hans | Overtaken by events | Scenarios launch postponed to Q3; escalation moot. |
| Set up Intercom MCP via Claude, check Dovetail MCP access | Not reported | No update. |
| June pre-read: build stages 1-4 for Small and Medium orgs | Partial | Stage 3 live for all bands, Stage 4 build now prioritised (ahead of Stage 3 emails). |
| June pre-read: "if time" jobs (Get people back, Promote champions, Stage 5, Shared Account Insights) | Not started | Explicitly deprioritised, called out in the pre-read. Clean carry, no hiding. |
| June pre-read: Modular learning content library (planning only) | Done | Roadmap and build list delivered; scripting starts mid-July, first 8 videos by 1 Aug. |
| June pre-read: Autodesk Assistant / Fin integration mapping | Done | Now aligned with Chris and Amar, moving into delivery. |
| June pre-read: US user insight expansion (AIA San Diego) | Done | Persona findings surfaced; US First Strike scan surfaced 2 validated blockers. |
| June pre-read: In-product learning delivery experiment (parked) | Reopened | Design-locked, blocked on Intercom whitelisting. |

---

## 2. Five topics for this meeting

### Topic 1. The KR1 reversal, and what actually explains it

- Coverage kept expanding, but KR1 slid every week from 2.44% to 0.77% and site-entered engagement fell below its own baseline. The pre-read frames this as "volume, not coverage", but there is no falsifiable diagnosis yet.
- Ask: what are the three most plausible causes, and how will Joseph rule them in or out by the August MFM?
- Push on: is the July priority set (build more stages + investigate the reversal) actually resourced for the investigation, or is investigation implicit?
- Reference: KR2 also fell (0.4% to 0.11%), so this is not just SD noise.

### Topic 2. Trial Users research sprint and the US bet

- 12-15 trial-user interviews feeding the end-July task force workshop and the 250 self-serve conversions KR is the closest thing in this pre-read to the "Win the US" priority you own.
- Ask: what is the specific decision this sprint is designed to make? "Feed a workshop" is not a decision.
- Push on: how does this connect to Kevin's US First Strike scan (2 validated blockers) and Clément's AIA San Diego findings? Is there a single US insight synthesis or three separate streams?

### Topic 3. Objective 4's broken loop

- The pre-read explicitly flags that the product-side insight-to-action loop is broken and asks for product-side ownership assigned. This is the second month in a row the squad has volume without impact on Objective 4.
- Ask: what does "ownership assigned" mean concretely - which squad, which person, what accountability?
- If this ask isn't landed at the meeting, it will drift into August. Do not accept "we'll follow up".

### Topic 4. CX Score composition change

- CX Score moved from "67% Fin-only" in June to "61% blended (Fin 69.6%, Teammate 59.3%)" in July. The Fin component improved. The blended read looks like a regression but is a new metric definition.
- Ask: was the target itself re-baselined against the new definition, or are we now measured against 80% on a metric composition that is materially different?
- If the target didn't move, the plan needs to address Teammate specifically, not just Fin.

### Topic 5. Autodesk Assistant delivery: from ask to ship

- Last month this was an open ask on resourcing. This month it is "aligned with Chris and Amar, moving into delivery" with a contractor targeted for start of August.
- Ask: what is the ship date, and what would slip it? If the contractor doesn't land in early August, does the plan hold?
- Also: what does "delivery" look like this cycle? Prototype, beta on a cohort, GA?

---

## 3. Metrics - light touch

- KR1 SD first strike: 0.85% vs 5% target. Reversed. The single most important metric conversation of the meeting; do not lose it to a metrics debate on other lines.
- KR2 Board first strike: 0.11% vs 5% target. Same pattern as KR1, weaker signal, worth one sentence.
- Obj 2 KR1 coverage: 28% vs 100% target, but this is now a new metric definition. Take the caveat, move on.
- Fin resolution 86.9% on track. Do not spend time here.
- Insights: 12 interviews, 44 panel. On track on volume. The interesting question is Topic 3, not this number.

Do not get drawn into a long metrics debate. Note the gap on KR1/KR2, accept the CX Score data caveat, move on to the reversal diagnosis.

---

## 4. What I want to walk out with

1. A named diagnosis plan for the KR1 reversal, with owner and a checkpoint before the August MFM.
2. A named product-side owner for Objective 4's insight-to-action loop, or an explicit decision that leadership picks the owner this week.
3. A one-line statement of the US decision the Trial Users research sprint is designed to make.
4. Autodesk Assistant contractor start date confirmed and a ship-shape target for this 6-week cycle.
5. Clarity on whether the CX Score target has been re-baselined against the new blended definition.

## Notes to self

- The lifecycle plan for June was your call with Arne (stages 1-3 for Small/Medium, larger orgs to July). Stage 4 now being built ahead of Stage 3 emails is a scope shift within that agreement, not a reversal of it. Worth naming, not worth relitigating.
- The squad has one of the strongest agentic-first portfolios in Growth (Trig agent, /find_insights, /feedback-scan, /eod, /slides). Consider using this MFM as the moment to name it as the standard other squads should reach.
- Joseph has been under pressure on Objective 1 for three months. Push hard on the diagnosis, but leave room to name that "volume, not coverage" is a real and testable hypothesis, not an excuse.
- Don't let the in-product learning nudge (Intercom whitelisting) become the whole learning-and-support conversation. It's a small unblock, not a strategy.
