# Site Design analytics - verified events and query patterns

**Created:** 2026-05-26
**Source:** Designmode repo (`spacemakerai/designmode`), Mixpanel project 1938089, D&A team corrections
**Full research log:** `Work/Notes/Data/data_understanding_site_design_analytics.md`

---

## Critical corrections

- **Page name "DesignMode" is deprecated** (11 users). Use `"Site Design"` (23,817 users)
- **Do not use `product` property** for MAU counting - gives wrong numbers (~double). Use `Loaded a Page` with `name` filter
- **`Activation: Triggered Analysis` is dead** - returns 0. Use `site_design_analysis_run` instead
- **`Any Forma Analysis` is a black box** - can't break down by type. Use `site_design_analysis_run` instead
- **`Activation: Added design element` is a black box** - not in designmode repo, all properties return undefined
- **`terrain` category auto-fires** from contextual data ordering - not real design work
- **Mixpanel Business Context is not configured** for project 1938089 - must be explicit about events and filters

---

## Mixpanel project

- **Project ID:** 1938089 (In-market Forma)
- **Filters:** `formaUser` (user, boolean) = `true`, `licenseType` (user, string) = `commercial`

---

## Page names for Loaded a Page event

| Page name | Product/Module | Notes |
|---|---|---|
| `app-home` | App Home | Entry point |
| `Project overview` | Project Overview | |
| `Site Design` | Site Design | **Current name** |
| `forma_board` | Board | |
| `Forma project setup` | Site Setup | |
| `Board landing` | Board Landing | |
| `Hub selector` | Hub | |
| `Building Design` | Building Design | |
| `Compare` | Compare mode | |
| `SunAnalysis` | Sun Analysis | |
| `SiteDaylightAnalysis` | Daylight Analysis | |
| `WindAnalysis` | Wind Analysis | |
| `MicroclimateAnalysis` | Microclimate | |
| `SolarEnergyAnalysis` | Solar Energy | |
| `NoiseAnalysis` | Noise Analysis | |
| `DesignMode` | **DEPRECATED** | Do not use |

---

## Site Design funnel definition (source-verified)

| Step | Event name | Filter | Rationale |
|---|---|---|---|
| 1. App Home | `Loaded a Page` | `name = "app-home"` | Entry point, validated MAU method |
| 2. Enter Site Design | `Loaded a Page` | `name = "Site Design"` | Current page name |
| 3. Order contextual data | `Order Data` | `spec_id = "contextual_data_order_submitted"` | Tier 1, final order step |
| 4. Add design element | `Add` | `spec_id = "site_design_tool_element_added"` | Tier 1, all tool additions |
| 5. Run analysis | `Run` | `spec_id = "site_design_analysis_run"` | Tier 1, discovered from source code |

**Conversion window:** 30 days
**Global filters:** formaUser (boolean) = true, licenseType (string) = commercial

### Stricter step 4: "real design work"

Filter `site_design_tool_element_added` to building categories + file imports:
- `category` in: `building`, `basic_building`, `line_building`, `row_house`
- OR `forma_file_import_files_imported` (separate event, needs Mixpanel custom event to combine)

---

## Key spec_ids

### Site Design module (`designmode`)

| spec_id | Action | What | Key properties |
|---|---|---|---|
| `site_design_loaded` | PageEvent | SD app loaded | mode (main, compare, viewAnalysis, lightMode) |
| `site_design_tool_selected` | Select | Tool selected | tool_name, sub_tool_name, method, category |
| `site_design_tool_element_added` | Add | Element added | tool_name, sub_tool_name, category, shape_type |
| `site_design_tool_element_edited` | Edit | Element edited | tool_name, sub_tool_name, category, shape_type |
| `site_design_analysis_run` | Run | Analysis triggered | analysis_type, has_3d_geometry, uses_custom_circle, circle_radius |
| `site_design_analysis_viewed` | View | Analysis result viewed | view_duration, view_type, analysis_type |

### Other relevant modules

| spec_id | Module | Action | What |
|---|---|---|---|
| `contextual_data_order_submitted` | order-sidebar | Order Data | Contextual data order completed |
| `contextual_data_order_selected_provider` | order-sidebar | Order Data | Provider selected |
| `contextual_data_order_preview_clicked` | order-sidebar | Order Data | 3D preview clicked |
| `forma_file_import_files_imported` | forma-file-import | Import | File imported (has fileExtensions) |
| `site_members_invite_sent` | forma-site-members | Invite | Email invite sent |
| `site_members_invite_link_copied` | forma-site-members | Invite | Invite link copied |
| `app_home_opened` | forma-home-ui | Open | App Home entered |
| `forma_setup_site_created` | forma-setup | Create | New site created |

---

## Element add categories (from source code)

Source: all call sites for `Events.Tool.elementAdded` in the designmode repo.

| Category | Tool name | What the user did | Design work? |
|---|---|---|---|
| `building` | `place_mode` | Placed building from library | Yes |
| `basic_building` | `basic_building` | Drew basic building footprint | Yes |
| `line_building` | `line_building` | Drew linear building | Yes |
| `row_house` | `row_house` | Placed row houses | Yes |
| `terrain` | `place_mode` | Auto-placed from data order | No - auto/setup |
| `referenceImage` | `place_mode` | Placed reference image | No - reference |
| `site_limit` | `draw` | Drew site limit boundary | No - setup |
| `generic` | `draw` | Drew generic shape | Ambiguous |
| `vegetation` | `draw` | Drew trees/vegetation | Landscaping |
| `property_boundary` | `draw` | Drew property boundary | Planning |
| `site_area` | `iterative_explore` | Defined site area | Planning |
| `parking` | `surface_parking` | Added surface parking | Infrastructure |
| `road` | `transportation` | Drew roads | Infrastructure |
| `zone` | `draw` | Drew zone boundary | Planning |
| `constraint` | `draw` | Drew constraint volume | Planning |
| `annotation_label` | `add_label` | Added text label | Annotation |

---

## Analysis types (from source code)

Analysis types for `site_design_analysis_run` breakdown:

| analysis_type value | What |
|---|---|
| `sun` | Sun/shadow analysis |
| `sky-component` | Daylight potential |
| `wind` | Wind analysis |
| `microclimate` | Microclimate analysis |
| `solar-panel` | Solar energy analysis |
| `noise` | Noise analysis |
| `area-metrics` | Area metrics |
| `embodied-carbon` | Embodied carbon |

Note: `site_design_analysis_viewed` only fires for `area-metrics` and `embodied-carbon`. Other analysis types use module-specific PageEvents (e.g. `SunAnalysis`, `WindAnalysis`).

---

## Saved Mixpanel reports

### Framework reports

| Bookmark ID | Report name | Skill |
|---|---|---|
| 81305099 | DT: Expanded MAU model - MAUs | `pull-framework-report` |
| 81306575 | Expanded MAU model - rates 1 | `pull-framework-report` |
| 87987919 | Expanded MAU model - rates part_2 | `pull-framework-report` |
| 48215435 | DT: User Engagement [Commercial] % | `pull-framework-report` |

### First Strike reports (Lavinia Dieac)

| Report ID | Name |
|---|---|
| 86601289 | MAUs First Strike Rate for Site [any time] |
| 86601195 | New MAUs First Strike Rate for Site [first 7 days] |
| 86614572 | First Strike Completion, first day (Site/Board Entered) |
| 87041563 | Actuals First Strike Completion, first day vs first 7 days |

---

## Event tier system

| Tier | Signal | How to query |
|---|---|---|
| **Tier 1** | Has snake_case `spec_id`, `module` set | Action name (Add, Run) + spec_id filter |
| **Tier 2** | `product` property set, no real spec_id | Filter by `product`, breakdown by `feature` |
| **Tier 3** | Event name is the identifier | Use event name directly (e.g. `DesignMode: Draw site limit`) |

Prefer tier 1 over tier 2 over tier 3.

---

## Source code reference

**Repo:** `spacemakerai/designmode` (internal)
- `src/core/analytics/internal/new_analytics.ts` - All tier 1 events
- `src/core/analytics/internal/legacy.ts` - Legacy events (prefixed "DesignMode: ")
- `src/core/analytics/internal/utils.ts` - Type definitions (Tool, AnalysisType, Method enums)
