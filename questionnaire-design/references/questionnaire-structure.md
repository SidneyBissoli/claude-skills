# Questionnaire Structure, Order & Layout

This reference governs the instrument *as a whole* — how items are sequenced, grouped, routed,
and laid out — as distinct from the wording of any single item (`question-wording.md`). It
serves both modes:

- **Create (Mode A):** use these to assemble and sequence the instrument after items exist.
- **Review (Mode B):** audit the architecture, then classify with Doctrine #4 — structural
  flaws that bias or break the instrument are **defects**; legitimate sequencing choices that
  merely follow a different tradition are **divergences**, not flaws.

Source tags resolve in `source-map.md`.

## Contents
- Part I — Architecture requirements (defect-grade)
- Part II — Placement & sequencing choices (divergence-grade)
- Part III — Layout, length, and mode interaction
- Part IV — Consistency for comparison over time
- Review-mode quick map: defect vs. divergence

---

## Part I — Architecture requirements (defect-grade)

**1. Anchor every item to the analysis plan.** Before sequencing, confirm that each item exists
to answer a stated objective and that every objective is covered. *ASA-WIS* recommends drafting
an outline of the final report / a "data analysis plan" that links each objective to specific
items — the easiest way to ensure the instrument "contains everything that is needed and
nothing extraneous." *NG-2006* makes the same point via a conceptual framework and the
*succinct* criterion: questions beyond the research objectives should be cut. An item tied to
no objective, or an objective with no item, is a structural **defect**.

**2. Sequence logically and self-evidently.** The order must make sense to the respondent.
*STATCAN-SMP*: questions "must be sequenced logically for the respondent"; an illogical or
overlong flow discourages respondents and causes break-offs or wrong routing. *ESS-HB*: the
sequence should be "self-evident," so the questionnaire follows a natural order.

**3. Open well.** *ESS-HB* and *HARVARD-PSR*: opening questions should apply to all
respondents and be easy and interesting; *HARVARD-PSR* adds that an introduction and (for
self-administered forms) a section title or (for interviewer modes) smooth verbal transitions
orient the respondent. A difficult, narrow, or off-putting first question is a **defect**.

**4. Manage context and order effects.** Earlier items can prime later answers. *AAPOR-BP*
gives the canonical case: asking about specific policy positions of a leader before a general
favorability item primes respondents to weight those positions more heavily — so general
items often belong *before* specific ones on the same concept. *HARVARD-PSR* and *CCSG-QD*
note the same priming risk, and *CCSG-QD* shows order effects persist cross-culturally.
Because order effects can run in either direction, the safeguard is twofold: sequence
deliberately (general → specific by default) **and** test for order-induced bias (*ESS-HB*
recommends addressing sequence bias during questionnaire testing — see `pretesting.md`).
Leaving a plausible priming path unexamined is a **defect**; the specific order chosen, when
defensible and tested, is a design decision.

**5. Route correctly; keep filters proportionate.** Respondents should see only applicable
items (*HARVARD-PSR*). But filtering has a cost: *NG-2006* warns against over-filtering, which
confuses respondents, and *STATCAN-SMP* ties skip complexity to mode — self-administered/paper
instruments "should not have complicated skip patterns," whereas interviewer- or
computer-assisted modes can carry complex branching. A filter that routes respondents to the
wrong place, or complex skips in a self-administered form, is a **defect**.

**6. Group related content; signal the structure.** Organize items into coherent thematic
blocks and make the structure visible — sections with headings, transitions between blocks
(*NG-2006*, *HARVARD-PSR*). *ESS-HB* favors a **modular** structure (self-contained, reusable
across waves or studies), with thematic sections sequenced according to the data-collection
method.

---

## Part II — Placement & sequencing choices (divergence-grade)

Apply Doctrine #1: present options with their tradition; do not impose one.

**A. Placement of sensitive and sociodemographic items.**
- *Options & traditions.* One tradition places sensitive items and demographics (especially
  income) **near the end**, after rapport is built and so an early refusal does not lose the
  whole interview (*HARVARD-PSR*). *ESS-HB* converges on reaching sensitive topics
  **gradually** and not placing them at the beginning. A second tradition treats demographic
  placement as **population-dependent**: *NG-2006* notes some designers put demographics first,
  others last, "depending on how forthcoming the target population is," and that explaining or
  normalizing a sensitive item can help (echoed by *DATASENADO-DIR*).
- *Decision drivers:* population's willingness, mode, and whether early demographics are needed
  for routing. Record the choice; in review, this is a **divergence**, not a defect — unless a
  genuinely threatening item sits cold at the very start, which the ESS/Harvard consensus
  treats as harmful.

**B. Randomizing the order of items within a battery.**
- *Options & traditions.* For a series of similar items, *HARVARD-PSR* notes that randomizing
  the order respondents encounter them can improve data (by spreading order effects). This is a
  technique to adopt or not depending on mode capability and the analysis plan; *DATASENADO-DIR*
  applies the analogous logic to rotating *response options* (Part II of `question-wording.md`).

**C. Funnel direction (general→specific vs. specific→general).**
- *Options & traditions.* The common default is general-before-specific to avoid priming
  (*AAPOR-BP*, *HARVARD-PSR*). A specific-to-general ("funnel") ordering is sometimes used
  deliberately to walk respondents from concrete instances toward a summary judgment. Neither
  is universally correct; the priming consequence differs, so the decision should be made
  against the construct and verified in testing (*ESS-HB*).

---

## Part III — Layout, length, and mode interaction

**Length and burden.** Keep the instrument as short as the objectives allow; long, monotonous
questionnaires depress attention and completion (*HARVARD-PSR*, *STATCAN-SMP*). Length also
constrains mode — long instruments work poorly on the telephone (*ASA-WIS*).

**Visual and screen layout.** Layout is not cosmetic: *STATCAN-SMP* notes that poor physical
layout causes data-capture errors, and *ESS-HB* stresses that non-verbal stimuli (graphical
symbols, layout) and, in computer-assisted modes, screen design are vital to how respondents
and interviewers proceed. *NG-2006* adds practical layout advice for self-administered forms:
clear title reflecting the objective, sections with bold headings, smooth section-to-section
flow with appropriate filtering, larger fonts for older respondents, and a cover letter
stating purpose, affiliation, confidentiality, and data use.

**Mode determines layout choices.** Visual modes (paper/web) carry primacy effects and allow
richer layout; aural modes (telephone) carry recency effects and require short, simple
structures. Decide mode before finalizing structure. See `instrument-types-and-modes.md`.

---

## Part IV — Consistency for comparison over time

When data must be compared with earlier waves or other studies, repeating an item *verbatim*
protects comparability (*ASA-WIS*, *CCSG-QD*). This creates a real dilemma, named by *ASA-WIS*:
if the existing item is flawed, the designer must weigh fixing it (improving validity but
breaking the trend) against retaining it (preserving the trend but carrying the flaw). Treat
this as an explicit, documented trade-off — not a silent choice. Social change can also shift
the meaning of terms or the realistic range of response categories over time (*ASA-WIS*), so
"verbatim" repetition still warrants a check that the item still means the same thing.

---

## Review-mode quick map: defect vs. divergence

| Observation about the instrument                              | Classify as |
|---------------------------------------------------------------|-------------|
| Item tied to no objective; objective with no item             | Defect      |
| Illogical / confusing overall flow                            | Defect      |
| Hard, narrow, or off-putting opening question                 | Defect      |
| Plausible priming path left unexamined/untested               | Defect      |
| Incorrect routing; complex skips in a self-administered form  | Defect      |
| Threatening item placed cold at the very start                | Defect      |
| Demographics/sensitive items at end vs. (population-based) start | Divergence |
| Battery items randomized vs. fixed order                      | Divergence  |
| General→specific vs. specific→general funnel (tested)         | Divergence  |

As in `question-wording.md`: a divergence is named and attributed, not rewritten; a clean
instrument is reported as clean.

---

## Sources drawn on in this reference
*ASA-WIS*, *NG-2006*, *STATCAN-SMP*, *ESS-HB*, *HARVARD-PSR*, *AAPOR-BP*, *CCSG-QD*,
*DATASENADO-DIR*. Full details in `source-map.md`. This file does not import structural claims
from sources that do not address instrument structure.
