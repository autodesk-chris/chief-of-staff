# GAP Metrics - Ad-hoc Data Pull
**Date:** 2026-04-27
**Method:** Custom Mixpanel retention and insights queries via MCP (no codified skill)
**Filters:** Commercial, formaUser=true, excludes autodesk.com and spacemaker.ai

---

## GAP 1: Board spike vs established retention (daily granularity)

### Segment definitions
- **Established:** firstEntry BEFORE 2026-03-23 (users who existed before the spike)
- **Spike:** firstEntry AFTER 2026-03-30 (users who arrived during/after the spike)

### Segment comparison - average daily return rates

| Interval | Established | Spike | Delta |
|----------|------------|-------|-------|
| D0 (same day) | 79% | 92% | +13pp |
| D1 | 15% | 10% | -5pp |
| D7 | 11% | 6% | -5pp |
| D14 | 7% | 3% | -4pp |
| D21 | 6% | 2% | -4pp |
| D28 | 6% | 0% | -6pp |

**Query notes:**
- Established: retention query on Board (module=board-ui) events, date range 2026-02-23 to 2026-03-22, firstEntry before 2026-03-23. Average daily cohort size: ~297 users.
- Spike: retention query on Board events, date range 2026-03-30 to 2026-04-27, firstEntry since 2026-03-30. Average daily cohort size: ~475 users.
- D0 reflects same-day return (high for both segments since birth=first Board interaction that day).
- D28 for spike is 0% because most spike cohorts haven't reached 28 days yet - only the Mar 30 cohort has full D28 data.

### Spike users - weekly cohort breakdown (Board retention, daily intervals)

Rates are weighted averages across daily cohorts within each week. Sourced from per-week retention queries filtered by firstEntry window.

| Weekly Cohort | Cohort Size (avg daily) | D1 | D7 | D14 | D21 |
|---------------|------------------------|-----|-----|------|------|
| w/c Mar 30 (Mar 30 - Apr 5) | ~290 (7 days) | 6% | 4% | 3% | 2% |
| w/c Apr 6 (Apr 6 - Apr 12) | ~262 (7 days) | 7% | 6% | 3% | 4% |
| w/c Apr 13 (Apr 13 - Apr 19) | ~306 (7 days) | 7% | 5% | 3% | n/a |
| w/c Apr 20 (Apr 20 - Apr 26) | ~370 (7 days) | 11% | n/a | n/a | n/a |

**Query notes:**
- Each row is a separate retention query with firstEntry filtered to that week window, birth and return events = any board-ui module event.
- D1/D7/D14/D21 taken from the $average row of each query.
- w/c Apr 20 shows higher D1 (11%) but this is based on very early data - only 2-7 days of follow-up per cohort member.
- w/c Apr 13 D21 not available (insufficient elapsed time).

### Established users - weekly retention curve (for comparison)

From weekly-granularity retention query (Dec 1 2025 - Mar 22 2026, firstEntry before Mar 23).

| Interval | Return Rate |
|----------|------------|
| W0 (same week) | 81% |
| W1 | 22% |
| W2 | 17% |
| W3 | 16% |
| W4 | 15% |
| W8 | 12% |
| W12 | 10% |
| W16 | 11% |

Average weekly cohort size: ~244 users.

---

## GAP 2: Product-level retention curves (month-over-month)

### Board - monthly retention by daily cohort

Cohorts grouped by calendar month. Rates are averaged across all daily cohorts within each month.

| Cohort Month | Avg Daily Users | M0 | M1 | M2 | M3 | M4 |
|-------------|----------------|-----|-----|-----|------|------|
| Dec 2025 | ~115 | 79% | 21% | 18% | 19% | 9% |
| Jan 2026 | ~152 | 79% | 20% | 18% | 10% | - |
| Feb 2026 | ~228 | 83% | 27% | 15% | - | - |
| Mar 2026 | ~620 | 87% | 21% | - | - | - |
| Apr 2026 | ~770 | 94% | - | - | - | - |

**Query notes:**
- Retention query: birth = any board-ui event, return = any board-ui event, retentionUnit=month.
- M0 represents same-month activity. M1 = returned the following month, etc.
- Dec M3 and M4 derived from daily cohort rows where data was available (Dec 1-28 had M3, Dec 1-24 had M4).
- Mar/Apr cohort sizes inflated by the spike starting ~Mar 23.
- Monthly rates manually averaged from the daily-cohort level data by selecting representative rows.

### Site Design - monthly retention by daily cohort

| Cohort Month | Avg Daily Users | M0 | M1 | M2 | M3 | M4 |
|-------------|----------------|-----|-----|-----|------|------|
| Dec 2025 | ~280 | 86% | 22% | 23% | 24% | 15% |
| Jan 2026 | ~310 | 88% | 23% | 25% | 14% | - |
| Feb 2026 | ~530 | 91% | 33% | 18% | - | - |
| Mar 2026 | ~1,530 | 92% | 27% | - | - | - |
| Apr 2026 | ~2,180 | 90% | - | - | - | - |

**Query notes:**
- Retention query: birth = any event with product="Site Design", return = same.
- Site Design shows generally higher retention than Board across all intervals.
- Feb M1 of 33% is notably strong.
- Mar/Apr volumes heavily influenced by overall growth spike.

### Building Design - monthly retention by daily cohort

| Cohort Month | Avg Daily Users | M0 | M1 | M2 | M3 | M4 |
|-------------|----------------|-----|-----|-----|------|------|
| Dec 2025 | 0 | - | - | - | - | - |
| Jan 2026 | 0 | - | - | - | - | - |
| Feb 2026 (from Feb 12) | ~45 | 99% | 52% | 15% | - | - |
| Mar 2026 | ~50 | 98% | 38% | - | - | - |
| Apr 2026 | ~380 | 99% | - | - | - | - |

**Query notes:**
- Building Design product events only appear from ~Feb 12 2026 onward (product launch or instrumentation date).
- Very high M0 (99-100%) likely because the retention birth event = any BD event, so same-day return is near-guaranteed.
- M1 retention is notably high (52% for Feb, 38% for Mar) but on a small user base.
- Apr 2026 shows significant volume ramp (~380 avg daily users vs ~50 in Mar).
- Building Design events use `product: "Building Design"` property (tier 2 events).

---

## GAP 3: Weekly cohort activation tracking

### Cohort overview

All events (not product-specific). Cohorts defined by firstEntry date window. Standard commercial/formaUser filters.

| Cohort | Window | Cohort Size | D1 Return Rate | Week 1 Return Rate | D14 Return Rate |
|--------|--------|-------------|----------------|--------------------|-----------------|
| Week 1 | Apr 5-11 | 7,710 | 19% | 13% (D7) | 7% |
| Week 2 | Apr 12-18 | 8,543 | 19% | 12% (D7) | 5% |
| Week 3 | Apr 19-25 | 9,198 | 21% | 14% (D7) | n/a |

**Column definitions:**
- **Cohort Size:** Unique users with firstEntry in the window who logged in during the observation period.
- **D1 Return Rate:** Average rate of users who returned the day after their first activity (from retention $average row, index 1).
- **Week 1 Return Rate:** D7 rate from the retention $average row - % who returned on exactly day 7 (not cumulative within 7 days).
- **D14 Return Rate:** Rate from index 14 in the retention curve. Not available for Week 3 (insufficient elapsed time).

### Daily breakdown within each cohort

**Apr 5-11 cohort** (7,710 users total across week)

| Entry Day | Users Entering | D1 | D7 | D14 |
|-----------|---------------|-----|-----|------|
| Apr 5 (Sat) | 191 | 21% | 7% | 4% |
| Apr 6 (Sun) | 1,156 | 14% | 7% | 1% |
| Apr 7 (Mon) | 1,818 | 18% | 9% | 4% |
| Apr 8 (Tue) | 2,088 | 20% | 10% | 5% |
| Apr 9 (Wed) | 2,370 | 15% | 10% | 8% |
| Apr 10 (Thu) | 1,997 | 10% | 10% | 9% |
| Apr 11 (Fri) | 626 | 29% | 15% | 11% |

**Apr 12-18 cohort** (8,543 users total across week)

| Entry Day | Users Entering | D1 | D7 | D14 |
|-----------|---------------|-----|-----|------|
| Apr 12 (Sat) | 288 | 26% | 14% | 8% |
| Apr 13 (Sun) | 1,811 | 17% | 8% | 1% |
| Apr 14 (Mon) | 2,153 | 18% | 10% | 4% |
| Apr 15 (Tue) | 2,305 | 20% | 14% | 5% |
| Apr 16 (Wed) | 2,403 | 17% | 13% | 5% |
| Apr 17 (Thu) | 2,087 | 11% | 14% | 3% |
| Apr 18 (Fri) | 704 | 32% | 14% | 11% |

**Apr 19-25 cohort** (9,198 users total across week)

| Entry Day | Users Entering | D1 | D7 |
|-----------|---------------|-----|-----|
| Apr 19 (Sat) | 282 | 21% | 10% |
| Apr 20 (Sun) | 1,824 | 18% | 7% |
| Apr 21 (Mon) | 2,184 | 20% | 8% |
| Apr 22 (Tue) | 2,533 | 24% | 9% |
| Apr 23 (Wed) | 2,594 | 24% | n/a |
| Apr 24 (Thu) | 2,647 | 17% | n/a |
| Apr 25 (Fri) | 1,023 | 37% | n/a |

**Query notes:**
- Retention queries used $any_event as both birth and return event (all platform activity, not product-specific).
- D1 rate = index 1 in the rates array (returned exactly on day 1 after first activity).
- D7 rate = index 7 in the rates array (returned exactly on day 7).
- D14 rate = index 14 in the rates array.
- These are point-in-time rates (returned on that exact day), not cumulative "returned within X days".
- Weekend entry cohorts (Sat/Sun) are much smaller than weekday cohorts.
- Friday cohorts show higher D1 rates but this likely reflects weekend-to-weekday return patterns.

---

## Query method summary

| GAP | Query Type | Event Filter | Retention Unit | Date Range | Key Filters |
|-----|-----------|-------------|---------------|------------|-------------|
| 1 - Established daily | Retention (curve) | module=board-ui | day | Feb 23 - Mar 22 | firstEntry < Mar 23 |
| 1 - Established weekly | Retention (curve) | module=board-ui | week | Dec 1 - Mar 22 | firstEntry < Mar 23 |
| 1 - Spike daily | Retention (curve) | module=board-ui | day | Mar 30 - Apr 27 | firstEntry >= Mar 30 |
| 1 - Spike weekly cohorts | Retention (curve) | module=board-ui | day | Per-week windows | firstEntry per week |
| 2 - Board monthly | Retention (curve) | module=board-ui | month | Dec 1 - Apr 27 | None (all users) |
| 2 - Site Design monthly | Retention (curve) | product=Site Design | month | Dec 1 - Apr 27 | None |
| 2 - Building Design monthly | Retention (curve) | product=Building Design | month | Dec 1 - Apr 27 | None |
| 3 - Cohort sizes | Insights (bar) | Auth: User - Logged in | n/a | Per-week windows | firstEntry per week |
| 3 - Cohort retention | Retention (curve) | $any_event | day | Per-week windows | firstEntry per week |

All queries are ad-hoc - no codified skill exists for these retention cohort analyses.
