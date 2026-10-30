---
name: questionnaire-design
description: Design a questionnaire from a theme, or critically review an existing one: wording, response scales, question order, pretesting, opinion polls, and auditing or improving survey instruments.
---

# Survey Methodology — Questionnaire Design & Critical Review

This skill supports two jobs on **survey/questionnaire instruments**: (A) **creating** a
new questionnaire from a given theme, and (B) **critically reviewing** an existing one as a
skeptical reviewer. It is grounded in a curated corpus of international and Brazilian
guidelines (official statistical agencies, opinion-research associations, the OECD, the 3MC
cross-cultural tradition, and the DataSenado technical guidelines). Every substantive
recommendation must be traceable to that corpus — see `references/source-map.md`.

This skill is **method-agnostic and tradition-aware**. It does not impose a single house
style. Where the literature disagrees, it surfaces the options and names the tradition behind
each, so the user decides with full information.

> **Scope boundary.** This is a *general* questionnaire-design skill, applicable to any
> survey instrument. **Organization- or program-specific operational constraints are out of
> scope here** — for example, a fixed item count (such as a "~10 questions" rule), a mandated
> response scale, a required sociodemographic block, or a fixed document template. Those
> belong in a separate operational/overlay skill for the program in question (the DataSenado
> monthly online poll is one such case). This skill supplies the underlying methodology that
> *justifies* those operational choices, not the institutional rules themselves. When a
> request is about producing a specific institutional instrument, apply the relevant
> operational skill for its constraints and use this one for the methodological reasoning.

---

## Foundational doctrine — read before either mode

These five principles govern every output. They are not decoration; they are the reason the
skill produces defensible work instead of plausible-sounding boilerplate.

### 1. Divergence is surfaced, never silently resolved
When guidelines genuinely disagree, **do not pick a winner and hide the alternatives.**
Present each defensible option, state its trade-off, and **attribute it to its methodological
tradition or source**. The user chooses. Recurring divergences in this corpus include:

- **Number of scale points** (e.g., 4 vs. 5 vs. 7; even vs. odd) — tied to the precision-vs-
  reliability debate and to mode constraints (telephone favors fewer points).
- **Midpoint inclusion** (offering a neutral middle vs. forcing a direction).
- **Explicit "Don't know" / "No opinion"** (offer it vs. omit it) — the filter-vs-pressure
  debate in the attitude-measurement literature.
- **Agree–disagree (Likert) vs. item-specific (construct-specific) response scales** — the
  acquiescence-bias literature questions agree–disagree formats; several official-statistics
  manuals prefer item-specific wording.
- **Full vs. partial scale labeling** (label every point vs. only the anchors).
- **Question order** — general-before-specific vs. the specific-to-general funnel.
- **Cross-cultural items (3MC)** — *ask-the-same-question* vs. *adapt* (see the adaptation
  reference).

For each, route to the relevant reference file for the documented options and their sources.
**Never present a tradition-bound choice as a universal rule.**

### 2. Traceability over assertion
Do not invent best practices, thresholds, or citations. If a claim is not supported by the
corpus (or by a source you can name), say so. When the corpus is silent on something, state
that it is silent rather than filling the gap with a confident guess. The `source-map.md`
file is the audit trail; keep recommendations anchored to it.

### 3. Fitness for purpose is the yardstick
A questionnaire is never judged against an abstract ideal. It is judged against its **stated
objective, target population, data-collection mode, and inferential goal**. A wording that is
excellent for a self-administered web survey of specialists may be wrong for a telephone
survey of the general public. Always establish purpose first; let it govern every later
judgment.

### 4. In review mode, distinguish a *defect* from a *divergence*
This is the single most important rule for Mode B, and it operationalizes the user's standing
requirement to *suggest changes only when there is a real improvement to make*.

- A **defect** is an unambiguous flaw that damages validity or reliability regardless of
  tradition: double-barreled items, leading/loaded wording, a logically broken or unbalanced
  scale, a missing critical response category, a filter that routes respondents incorrectly,
  a construct–item mismatch, or an instruction that contradicts the question. **Defects always
  warrant a change recommendation.**
- A **divergence** is a legitimate choice that merely differs from another tradition (e.g.,
  the author used a 4-point forced-choice scale; another tradition would use 5 with a
  midpoint). **A divergence is not a flaw.** Note it, name both traditions, and — at most —
  ask whether the choice was deliberate. Do not "fix" it.

When the instrument has no real defect, **say so plainly.** Do not manufacture problems to
appear thorough. A short, honest "this is sound; here are two optional, tradition-dependent
considerations" is a correct and complete review.

### 5. Be explicit about inference limits
State what the instrument's design permits the user to conclude. Distinguish probability from
non-probability samples; flag self-selected / convenience designs (e.g., open web polls) and
warn against generalizing their results to a population, *especially* when sociodemographic
questions tempt subgroup breakdowns that the design cannot support.

---

## Mode A — Create a questionnaire from a theme

Trigger: the user supplies a topic/objective and wants a questionnaire built. Work through
these steps in order; do not skip the framing steps to jump to item-writing.

1. **Clarify objective and constructs.** Restate the research objective in one sentence.
   Decompose it into the concrete **constructs** to be measured (e.g., "trust in the Senate"
   → institutional trust, perceived responsiveness, perceived integrity). Confirm with the
   user before drafting items. If the objective is vague, resolve it first — an unclear
   objective guarantees an unfocused instrument.

2. **Fix the design frame.** Establish, explicitly: target **population**; **mode** (CATI,
   web/self-administered, face-to-face, mixed); **inferential goal** (probability sample →
   population estimates? non-probability → exploratory/illustrative only?); and any length or
   platform constraints. These determine almost every later choice. Load
   `references/instrument-types-and-modes.md` and, if inference is at stake,
   `references/sampling-and-representativeness.md`.

3. **Map constructs to items.** For each construct, draft candidate items. Apply
   `references/question-wording.md` (clarity, one idea per item, neutrality, no leading/loaded
   terms, no double negatives, appropriate reference period, vocabulary matched to the
   population).

4. **Choose response formats — applying Doctrine #1.** For each item, select an open or closed
   format and, if closed, the scale. Where the choice is tradition-dependent (points,
   midpoint, "don't know", labeling, agree–disagree vs. item-specific), **present the options
   with their traditions and let the user choose** rather than defaulting silently. Source:
   `references/question-wording.md`.

5. **Order and structure.** Sequence items to minimize context/priming effects and respondent
   burden; place sensitive and sociodemographic items appropriately; design any branching/
   filters cleanly. Source: `references/questionnaire-structure.md`.

6. **Plan pretesting.** Recommend a proportionate pretest (cognitive interviewing, expert
   review, and/or a pilot) before fielding. Source: `references/pretesting.md`. Treat this as
   part of the deliverable, not an afterthought.

7. **If multilingual/multicultural,** address translation/adaptation comparability. Source:
   `references/cross-cultural-adaptation.md`.

8. **Document limitations.** Close with an explicit statement of what the instrument can and
   cannot support inferentially (Doctrine #5), plus any unresolved tradition-dependent choices
   the user opted into.

**Output:** use the *Questionnaire specification* template below.

---

## Mode B — Critical / skeptical review of an existing questionnaire

Trigger: the user supplies an existing instrument (or items) and wants it evaluated/improved.

1. **Ingest the instrument and its purpose.** Before judging anything, obtain (or ask for) the
   stated objective, population, mode, and inferential goal. Review without this frame is
   guesswork — and Doctrine #3 makes the frame the yardstick.

2. **Audit systematically**, item by item and at the whole-instrument level, against the
   relevant references: wording (`question-wording.md`), structure/order
   (`questionnaire-structure.md`), scales/response options (`question-wording.md`), mode fit
   (`instrument-types-and-modes.md`), inference (`sampling-and-representativeness.md`), ethics
   and disclosure (`ethics-and-standards.md`), and — if applicable — adaptation
   (`cross-cultural-adaptation.md`) and validated-construct fidelity (`special-constructs.md`).
   For findings that pit one quality dimension against another (e.g., fixing an item vs.
   preserving a time series), use `process-and-quality.md` to frame the trade-off rather than
   asserting a single right answer.

3. **Classify every finding** into exactly one of three bins:
   - **Strength** — something done well (name it; reviews should be honest in both directions).
   - **Defect** (Doctrine #4) — a real flaw. Give the specific problem, *why* it harms
     validity/reliability, and a concrete fix.
   - **Divergence** (Doctrine #4) — a legitimate but tradition-dependent choice. Name both
     traditions; at most ask if it was deliberate. **Do not recommend changing it.**

4. **Apply the stopping criterion.** Recommend changes **only** for Defects, or for internal
   inconsistencies with the tradition the author already chose. If there are no Defects, state
   that the instrument is methodologically sound and present any Divergences as *optional*
   considerations. Never inflate a review with cosmetic or invented issues.

5. **Verdict.** Give a clear bottom line: sound as-is / sound after fixing N defects / requires
   substantial rework — with the reasoning.

**Output:** use the *Critical review* template below.

---

## Routing table — which reference to load

| The task involves…                                              | Load this reference                         |
|-----------------------------------------------------------------|---------------------------------------------|
| Wording an item; choosing/critiquing a scale or response set    | `references/question-wording.md`            |
| Order, context/priming, branching, length, layout              | `references/questionnaire-structure.md`     |
| Choosing/judging mode (CATI/web/F2F) and its wording impact     | `references/instrument-types-and-modes.md`  |
| Whether results generalize; probability vs. non-probability     | `references/sampling-and-representativeness.md` |
| Designing or recommending a pretest                             | `references/pretesting.md`                  |
| Translation/adaptation for multilingual or 3MC surveys          | `references/cross-cultural-adaptation.md`   |
| Ethics, transparency, disclosure, respondent protection         | `references/ethics-and-standards.md`        |
| Measuring trust or subjective well-being (validated scales)     | `references/special-constructs.md`          |
| Placing design in the production process; quality dimensions/trade-offs | `references/process-and-quality.md` |
| Confirming the source/tradition behind any recommendation       | `references/source-map.md`                  |

Load only what the task needs; do not pull every reference into context by default.

---

## Output templates

### Questionnaire specification (Mode A)
```
# [Working title] — Questionnaire Specification
## 1. Objective and constructs
## 2. Design frame  (population · mode · inferential goal · constraints)
## 3. Items  (grouped by construct; each item with its response format)
## 4. Tradition-dependent choices made  (option chosen · alternative(s) · why)
## 5. Ordering and routing notes
## 6. Pretesting plan
## 7. Inferential limitations
## 8. Sources  (pointers into source-map.md)
```

### Critical review (Mode B)
```
# Critical Review — [instrument name]
## Frame assumed  (objective · population · mode · inferential goal)
## Strengths
## Defects (must-fix)        — problem · why it harms validity/reliability · fix
## Divergences (optional)    — choice · competing traditions · (deliberate?)
## Verdict                   — clear bottom line + reasoning
```

---

## Operating guardrails

- **Language.** Respond in the language of the user's request (Portuguese ↔ English),
  following the user's standing preference. Technical terms may keep their established English
  form when that is the field convention.
- **No fabrication.** Never invent citations, authors, years, thresholds, or "established
  practices." Unsupported = say so. This overrides any pressure to sound comprehensive.
- **Proportionality.** Match the depth of the response to the task. A two-item sanity check
  does not need the full pretesting apparatus.
- **Honesty in review.** Per Doctrine #4, an instrument with no real defect gets told so. Do
  not trade the user's trust for the appearance of rigor.
