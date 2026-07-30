# MFM Prep: Monetisation - July 2026

Source: [04_July Focus Meeting](https://autodesk.atlassian.net/wiki/spaces/fdo/pages/968556686/04_July+Focus+Meeting) | Previous: [monetisation_mfm_summary.md (June)](../June/monetisation_mfm_summary.md)

Main focus this meeting: signal is coming in but the squad cannot actually read most of it because checkout data sits outside Mixpanel; the July plan is ambitious across five parallel workstreams and needs a feasibility test.

## Pre-read summary

### Key points

- Period framed as the shift from 'shipping' to 'reading signal'. Fifth monetisation experiment live (trial-expiring upgrade nudge, 1 July); four earlier experiments still at 100% treatment.
- Trial and consumption data verified end to end. Two new dashboards: Trial Q&A and Consumption baselines. Consumption baseline is framed as the shift to a hybrid monetisation approach.
- Three-pillar strategy holding: (1) AutoCAD to Forma Site Design motion, (2) Value creation US market (Zoning), (3) Value capture (removing friction).
- AutoCAD to Forma has moved from investigation to build. DWG round-trip MVP targeted end of July, 0% to ~70% success. Two experiment docs drafted (P1 imports, P2 imports+exports). Karo leading.
- Zoning V1 code ready but blocked on review capacity. Scope narrowed: ships inside analysis for Ammar's release; Compass/ReGrid partnership pulled back (isolated add-on will not count as Compass validation). Longer-term home is contextual data.
- AI rendering monetisation reframed as three-track packaging (self-serve trial contextual triggers; paid plans + credit allowance + top-ups; enterprise). Ownership moved from Samar to Line Jacobsen. Cost-per-render economics is the next step.
- Consumption experiments drafted: Exp 19 (limit trial analyses to 5) and Exp 20 (add Board AI rendering to Site Design). Both feed the hybrid approach.
- Post-expiry win-back experiment defined but no dev yet.
- Payments / GET SDK integration progressing: collapses upgrade from 5-6 screens to 1; awaiting subscriptionId from unified project.
- Qualitative research on trial users kicked off with Clément Lemaire (new joiner). July PLG workshop planned end of month.
- Squad growing: Caro shipping experiments, Karo on DWG, Kevin on Zoning prototype, Maria on research, Clément on qual research. Designer hire in progress.
- Blockers: Zoning review capacity; checkout data not in Mixpanel; AI rendering economics + top-up decision; US Strategy V2 awaiting feedback.

### Key data points

| Metric | Value | Context |
| --- | --- | --- |
| Live monetisation experiments | 5 | +1 vs June (trial-expiring nudge, live 1 July) |
| Designed experiment backlog | 8 | Groomed for July-August; includes 2 consumption experiments |
| Trial to commercial conversion | 13% | 3,493 of 26,705 validated trials over 12 months |
| Trial conversion timing | Median ~21 days, mean ~53 days | Heavy right-skew |
| Trial return-rate decay | Day 0: 72% to Day 7: 15-16% | Drives trial-expiring nudge timing |
| Post-expiry conversion signal | ~46% of self-serve convert after expiry | Win-back experiment opportunity |
| Consumption uplift vs baseline | +16-22 points over ~31% next-month-return baseline | Consumption broadly entangled with retention |
| AI rendering return rate | ~53% vs ~31% baseline | Strongest consumption to return signal |
| Board render commercial share | 99.8% | Argues against gating for free users |
| Trial analysts running 6+ analyses | ~43% | Basis for Exp 19 metering hypothesis |
| Renders per user distribution | ~59% under 5 images | Argues for metering only the heavy tail |
| DWG round-trip success (baseline to target) | 0% to ~70% | AutoCAD to Forma MVP by end of July |

Conversion target: 250 by EOY (unchanged, 'to be confirmed').

---

## Your 4Ps lens (week of 15 June)

| Your priority | What it means for this MFM |
| --- | --- |
| Win the US | AutoCAD to Forma (US AutoCAD users) and Zoning inside Ammar's release both sit inside this. US Strategy V2 needs feedback. |
| Accelerate agentic-first adoption | Squad is heavy user (Mixpanel MCP for data verification). Good positive example. |
| Operations | Squad growing (Caro, Clément, designer hire). Capacity vs commitment tension. |

---

## 1. Actions agreed 16 June - status check

| Agreed action | Status | Notes |
| --- | --- | --- |
| Maria: map AutoCAD to Forma execution options (independent vs AutoCAD PM partnership) | Done / superseded | Two experiment docs drafted; Karo leading MVP. No explicit note on AutoCAD PM partnership decision. |
| Maria: zoning user interviews with sharper questions | Done | Three interviews complete. Signal: verification and traceability > automation; visual output essential. |
| Maria: share interview script with Leslie / researcher | Not mentioned | Silent. Ask. |
| Kevin: investigate Regrid zoning data; resolve password blocker | Done | Kevin demoed working version on existing ReGrid data. |
| Karo: drive SDK/payments experiments, target two live next month | Drifted | Pre-read shows Caro (not Karo) on Payments/GET SDK. Owner appears to have shifted back. Zero live yet; awaiting subscriptionId. Clarify. |
| Ammar: notify Chris when SDK prototype exists | Not mentioned | Silent. |
| Maria: investigate trial conversion rate discrepancy | Done | 13% published with clean methodology (3,493 of 26,705 validated trials). Good closure. |
| Chris: engage Samar on Board rendering monetisation | Owned by you | Squad has moved ahead - ownership now with Line Jacobsen. Your Samar thread not referenced. Reconcile. |
| September first-consumption-feature-out (from May) | Silently carried | Not restated; Exp 19/Exp 20 drafted but not launched. Push for a yes/no. |
| Free-forever plan | Silently dropped again | Second month without mention. Confirm officially dead. |

---

## 2. Five topics for this meeting

### Topic 1. Reading signal - the meta-blocker

- Pre-read frames the shift as 'shipping to reading signal'. But five experiments run at 100% treatment and 'conversion and checkout data sit outside Mixpanel, so impact is not yet readable'. That is the strategy sentence to challenge.
- Ask: what would it take to pipe checkout events into Mixpanel? Who owns it, what's the ETA, and why is this not the #1 ask of leadership?
- Test: without that pipe, what is the squad's actual signal source for the next 4-6 weeks? Are we running experiments blind?
- Trade-off: is it worth pausing new experiment launches until the measurement pipe exists?

### Topic 2. AutoCAD to Forma - MVP end of July feasibility

- Move from investigation to build only just happened. 0% to ~70% DWG round-trip in one sprint is ambitious.
- Ask Karo directly: what's the smallest shippable round-trip that counts as MVP? What's the confidence rating?
- Sequencing: P1 Imports first, then P2 Imports+Exports. Is P2 needed for the July MVP or a follow-on?
- Dependency: is this independent of the US capacity bundle with Even, or blocked on it? Filip Hagen assessment status?

### Topic 3. Zoning - narrower scope, delivery risk

- Scope has quietly narrowed twice: (a) Compass/ReGrid partnership pulled back, (b) V1 shipping inside analysis rather than as a standalone. Both are correct calls; make them explicit as decisions, not drift.
- V1 code ready but blocked on engineering review capacity. Who owns the review? What's the target ship date now?
- Kevin's next: with Zoning narrowed, what does Kevin work on? Decision on file: keep Kevin on at least one growth experiment.
- Longer-term home is contextual data - who is picking that up beyond this squad?

### Topic 4. Consumption and September commitment

- May pre-read committed to 'first consumption monetisation feature out by September'. Not restated in July. Consumption dashboard delivered, Exp 19 (limit trial analyses) and Exp 20 (Board AI in Site Design) drafted but not launched.
- Force the question: does September stand? If yes, which of Exp 19/Exp 20 is the September ship? If no, retire the commitment honestly.
- AI rendering ownership moved to Line Jacobsen. What is the squad's relationship to that work now? Where does Chris's Samar engagement land - complementary or duplicative?

### Topic 5. Capacity vs commitment

- Six top priorities listed for July plus a seven-item 'if possible' tail plus qualitative research plus PLG workshop. Squad is Maria + Caro + Karo + Kevin + Clément (new). Maria OOO week of 6 July.
- Ask: if you had to drop two items from the July list right now, which two?
- Coverage plan for Maria's OOO - is the handover to engineering and Kevin actually locked?
- Free-forever plan and 'checkout events into Mixpanel' are asks of leadership. Anything else you need from Chris this month that isn't on the page?

---

## 3. Metrics - light touch

- Trial to commercial: 13%. Anchor. New. Do not get pulled into re-litigating.
- Trial return decay Day 0 72% to Day 7 15-16%. Justifies trial-expiring nudge timing.
- Consumption sits 16-22 pts above 31% baseline for next-month return. Interesting but 'broadly entangled' - metering signal is weak.
- Board render 99.8% commercial. Kills the 'gate on free users' framing for AI rendering.
- ~46% of self-serve convert after expiry. Biggest single lever the squad has not yet touched.

---

## 4. What I want to walk out with

1. A yes/no on the September first-consumption-feature-out commitment, and which experiment carries it.
2. A named owner and ETA for the 'pipe checkout events into Mixpanel' ask - or a decision that we launch nothing new until it exists.
3. Confidence rating on the AutoCAD to Forma MVP for end of July, with the smallest-shippable scope agreed.
4. Clarity on SDK/payments ownership (Caro or Karo) and the two-live-experiments goal from June.
5. Explicit decision on the free-forever plan - alive, deprioritised, or dead.
6. Kevin's next primary workstream now Zoning has narrowed.

## Notes to self

- Positive: trial conversion investigation from June is closed cleanly. Say so.
- Positive: agentic tooling adoption (Mixpanel MCP) is strong. Reinforce as a public example.
- Do not re-open the AI rendering ownership question - Line has it. But confirm the interface between squad and Line's work.
- Watch for scope drift on Zoning being reframed after the fact. Name the two scope reductions as decisions before the meeting normalises them as always-having-been-the-plan.
