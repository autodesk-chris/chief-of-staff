# The dishes framework

A cooking metaphor for how Forma delivers user outcomes. Used to frame how we think about creating value for users and enabling fast experimentation to understand better. Three concepts: dishes, recipes, ingredients.

## The three concepts

**Dish** = the use case the user is trying to complete. Outcome-based, not feature-based. The thing the user actually pays for and remembers. Example: "a capacity study for a US residential project."

**Recipe** = the specific combination of capabilities needed to deliver the dish end-to-end. The workflow.

**Ingredient** = an individual capability that goes into a recipe. Ingredients can come from three layers:
- Native Forma (core platform features our product teams build)
- First-party extensions (tools we build on the SDK, filling gaps quickly)
- Third-party extensions (tools built by partners and the ecosystem)

## How they work together

- Strategy starts from the dish (the outcome the user wants), then works backwards to the recipe, then to the ingredients required.
- Forma doesn't have to own every ingredient natively. Speed matters more than ownership: if first-party or third-party extensions complete the recipe faster, that is the right call.
- Forma's job isn't just creating ingredients. It's writing the recipe and teaching people how to cook the dish (onboarding, profiling, guided flows, learning content).
- The dishes framework is the antidote to feature-list thinking. A user who has all the ingredients but no recipe doesn't get the outcome.

## Dishes are nested, not fixed

Whether something is a dish or an ingredient depends on the user's intent and the scope of value they're trying to get.

- **Parking analysis** is an ingredient inside the capacity-study dish for a developer running residential feasibility.
- **Parking analysis** is also a dish in its own right for an architect whose job is to optimise a parking strategy.
- Both are valid. The framing follows the user, not the org chart.

This matters because it changes how teams should scope. A monolithic "capacity study" dish takes a long time to validate end-to-end. But individual ingredient-dishes (parking analysis, floorplate analysis, cost feasibility) can each be tested as standalone dishes with the user segment that wants them most. When each sub-dish proves value, they compose into the larger recipe.

**Scoping rule of thumb:** scope the smallest dish you can put in front of real users in the shortest time. Prove the value moment exists. Then expand into the larger recipe. If a team can't describe a dish small enough to test live with users, typically in a sprint (not months), the scope is wrong.

## Dishes and First Strike

The dish concept is the strategic / scope language. First Strike is the measurement language. They map together.

| Concept | Definition | Where it sits in the dish |
|---|---|---|
| **First Strike (FSM)** | A user gets their first data-driven answer to a design question - the first taste of outcome-based decision-making. | The first bite of the dish. The earliest point in the recipe where the user experiences real value. |
| **Key Usage Indicator (KUI)** | The user completes the full loop at least once: intent → proposal → analysis → decision → iterate. | One complete serving of the dish. |
| **Upgrade trigger** | The loop is completed more than once. | Repeat consumption - the user is coming back for the dish. |

Implications:

- **One First Strike, many dishes.** First Strike is a single shared definition of value across Forma (a data-driven answer that reframes a design decision). Different dishes are different routes to that same FSM. Teams don't define their own FSM - they define how their dish gets a user there.
- **One shared value moment, many on-ramps.** Following the Canva pattern: different entry points (Site Design, Board, Building Design) can lead to one shared definition of value (outcome evaluation), even though the specific dish differs by user context. Profiling routes users to the right dish; the FSM concept is shared.
- **Tiebreaker test.** A useful test for whether a user has experienced the value moment: would they tell a colleague about what just happened? If yes, it's a value moment. If no, it's a usage event.

## Worked example: the US capacity study recipe

One example of the framework applied. The capacity study is a dish for US residential developers; the recipe is the workflow of ingredients needed to deliver it.

1. Set up the site with US parcel data (ReGrid integration - currently a gap)
2. Generate building massing options (native)
3. Run floorplate analysis for apartment layouts and unit mix (first-party extension - in alpha)
4. Analyse parking requirements (first-party extension, rebuilt from third-party)
5. Calculate cost/revenue feasibility (first-party extension - in alpha)
6. Run environmental analyses - sun, shadow, wind (native)
7. Compare proposals and present to client (native + Board)

Each numbered ingredient is potentially a dish on its own for a different user segment. That's how teams can test value fast: ship parking analysis as a dish for the user who wants parking optimisation today, while it's also being built into the bigger capacity-study recipe.

## Strategic implications

- **Success definition.** Usage of feature dishes that deliver real outcomes + proven willingness to pay (WF4 / export as proxy, currently ~2%).
- **H1 target.** At least 4 US recipes defined and scoped by end of H1. Capacity study is recipe #1. Site plan delivery (3-6 months) and facade / sections deliveries (6-12 months) follow.
- **First Strike evolves per market.** The first-value moment is the same shape (a data-driven answer that reframes a design decision), but the right dish differs. Norway = environmental analysis. US = capacity study. UK recipes overlap with US ingredients.
- **Product bets connect to recipes.** Each of the five FY27 bets expands what "analysis" means in Forma and brings more users within reach of a meaningful first strike.
- **Friction principle.** Remove friction that blocks value, keep friction that enables it. Profiling around the user's outcome (not internal categories) is valuable friction because it routes users to the right dish.

## Related concepts

- **Bowling alley.** The first-session experience is the lane. The recipe defines what staying on the lane looks like. User Engagement bumpers (AI support, 1:1 engagement at scale, learning content) catch users who veer off.
- **Consumption flywheel.** Complete workflows → users explore more proposals → more analyses run → more data → better AI models → more value per user.
- **Default operating mode.** Working on the assumption most experiments fail, we minimise alignment time. If first-party or third-party tools deliver the outcome faster than native, we should use them.

## How teams should use this

1. **Start from the user's intent**, not the feature backlog. What outcome are they trying to get?
2. **Name the dish.** One sentence.
3. **Define the usage metric that shows users are getting value from the dish.** What can you observe in the data that tells you a user has experienced the outcome the dish promises? This is how you'll know the dish is working - it's the dish-specific signal that the user has hit First Strike via this route.
4. **Scope the smallest testable version.** Can you put this in front of real users in a sprint, not months? If not, decompose further - find the sub-dish.
5. **Write the recipe.** What ingredients are needed? Which are native, which can come from extensions, which are gaps?
6. **Test live.** Measure the usage metric. Iterate. Compose sub-dishes into larger recipes once value is proven.

## Source

Primary articulation: `Work/Notes/Strategy/Overall/How we win/General/Growth_strategy_framing_v4.md` (sections "The recipe model", "First strike must evolve per market", "Operating model: continuous shipping").

FSM / KUI / Upgrade-trigger definitions: Slack thread in #priv-forma-design-leadership-fy27, 2026-06-10, Chris's post after alignment with Carl and Product Area leaders.

Originally clarified for the US strategy group (Maria, Zach, Even). Task closed 2026-06-02.
