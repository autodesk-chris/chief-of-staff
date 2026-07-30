# MFM summary: Monetisation - June 2026

Date: June 16, 2026, 4:32 PM
Attendees: Maria, Ammar, Kevin, Tamira, Karoline (Karo), Caroline (Caro), Chris
Pre-read: [03_June Focus Meeting](https://autodesk.atlassian.net/wiki/spaces/fdo/pages/921166525)
Prep doc: [monetisation_mfm_review.md](./monetisation_mfm_review.md)

## Key takeaways

- Maria wants our focus not to be consulting on adjacent monetisation problems until self-serve conversion is demonstrated.
- Conversion rate may be materially wrong - new data suggests 10-13% vs prior assumption. Unclear whether 'conversions' counted include admin-assigned licences vs real paid purchases. Investigation needed before any monetisation target is re-set.
- Target is 250 conversions. This is designed to create focus, but we must remember that delivering value earns the right to charge users.
- Prioritisation. Important to prioritise - 2 or three things. Discussed AutoCAD to Forma (including DWG) and 'easy monetisation wins' opportunities
- AutoCAD focus. Don't limit to working with AutoCAD team, look at all options and choose best solution to get learning quickly. 
- Zoning. Discussed input based model. Opportunity to collect knowledge architects already have - opportunity to experiment. Don't worry about throwing away prototype code and rebuilding
- Ammar reframed Zoning into contextual data (Regrid API, US-wide) plus analysis (model compliance).
- SDK/payments experimentation. Karo picking up the investigation.
- Chris to investigate AI rendering monetisation with Samar.

## Decisions made

1. AutoCAD to Forma is #1 priority, specifically AutoCAD users in the US, not AutoCAD broadly. Includes DWG export/import
2. Zoning is #2; scope progresses by iterative experimentation. 
3. AI rendering / Board rendering monetisation is not a Monetisation squad workstream this cycle. Chris owns engagement with Samar at strategy level.
4. SDK/payments work transferred from Caroline to Karo
5. Trial conversion rate assumption is not safe to use; Lavinia and Maria to validate before any target reset.
6. Four current experiments stay at 100% treatment for now. Measure success using history baseline. Consider moving to proper AB test if traffic volume supports

## Actions

- [ ] Maria - map AutoCAD to Forma execution options (independent route vs AutoCAD PM partnership).
- [ ] Maria - run zoning user interviews this week; add questions on what zoning info architects receive and from whom, current workflow and blockers, parameter prioritisation (FAR, height, setbacks, parking).
- [ ] Maria - share interview script with Leslie or a researcher before next interview block.
- [ ] Kevin - investigate Regrid zoning data; resolve password access blocker.
- [ ] Karo - drive SDK/payments experiments, target two live next month.
- [ ] Ammar - notify Chris when SDK prototype exists so he can update Hans.
- [ ] Maria - investigate trial conversion rate discrepancy; separate licence allocation from paid conversion in the data.

## Task
- [ ] Chris - engage Samar on consumption-based monetisation strategy for Board rendering, at strategy level.

## Updates from pre-read

| From pre-read                                        | Landed at                                                                                       |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| AutoCAD to Forma as Pillar 1 (investigation framing) | Confirmed as #1 priority and narrowed to US-specific. Includes DWG                              |
| Zoning release end of June with prototype            | Confirmed as #2 priority                                                                        |
| AI rendering ownership ask of leadership             | Decision: not a squad workstream; lifted to Chris at strategy level                             |
| Trial sign-up still a blocker                        | Reframed as conversion-rate data integrity problem; backlog item being discussed with marketing |
| Payments / GET SDK 'in progress' under Caroline      | Reassigned to Karo; two experiments goal for next month                                         |
| 4 experiments live at 100% treatment                 | Confirmed; A/B at 50/50 only where top-of-funnel traffic supports it                            |

## Not covered from previous MFM

- September commitment to first consumption monetisation feature out. Not restated, not denied. Either it stands and Zoning analysis is the path, or it needs to be retired honestly.
- Free-forever plan (May 'in definition'). Compressed into SDK/payments stream under Karo without a named decision. Worth confirming it is properly deprioritised, not silently dropped.

## Follow-up required

- Maria - broader session on Zoning scope (input fields vs full data import, AI fallback, crowdsourcing horizon); not a 1-to-1.
- Chris - engage Samar on Board rendering monetisation; update Maria with the outcome.
- Maria - report back on conversion-rate investigation within 2 weeks.
- Maria - confirm status of Tido and Ivan threads at next MFM at the latest.
