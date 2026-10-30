# Process & Quality Framing

This is a **framing** reference, not a how-to: it situates questionnaire design within the
end-to-end statistical production process and within a formal quality framework, so the other
references are understood as parts of a whole rather than a checklist. It is deliberately light.
Two sources anchor it: the **GSBPM** (where in the process design happens) and the **Statistics
Canada Quality Guidelines** (what "quality" means and which dimensions a questionnaire affects).

Use it in **create** mode to place the design task in sequence (what must precede and follow
it) and in **review** mode to ask whether the instrument was built within a quality-managed
process, not in isolation. Source tags resolve in `source-map.md`.

## Contents
- Part I — Where questionnaire design sits in the process (GSBPM)
- Part II — The quality dimensions (Statistics Canada)
- Part III — How the skill's references map to process and quality
- Part IV — Framing notes for review

---

## Part I — Where questionnaire design sits in the process (GSBPM)

*UNECE-GSBPM* (v5.2, 2025) models a statistical business process as structured activities
converting inputs into outputs, organized in phases. Questionnaire design is **not a
free-standing act**; it lives inside the **Design** and **Build** phases and depends on
upstream decisions and downstream consequences:

- **Phase 2 — Design.** Sub-process **2.3 Design collection** "prepares a collection strategy …
  and determines the most appropriate collection instruments and methods," which depend on the
  type of data collection and the collection unit type (enterprise, person, etc.). It runs
  partly **in parallel with 2.2 (Design variable descriptions)**, because the variables to be
  collected and the choice of instrument are interdependent — i.e., *what* you measure and *how
  you ask it* are decided together, not sequentially.
- **Phase 3 — Build.** Sub-process **3.1 Reuse or build collection instruments** turns the
  design into the actual instrument, and the GSBPM explicitly notes development that **iterates
  between Design and Build** — consistent with the multi-round pretest-and-revise cycle in
  `pretesting.md`. The model also flags **multi-mode collection** and security as design
  concerns at this stage.
- **Overarching activities** (e.g., quality management, metadata management) run *across* all
  phases — quality is not a final gate but a continuous activity.

The practical lesson for this skill: an instrument is only as sound as the objective and
variable definitions that precede it (Design) and the testing and fielding that follow it
(Build/Collect). A questionnaire judged in isolation from its objective and its process is
judged incompletely — the methodological echo of Doctrine #3 (fitness for purpose).

---

## Part II — The quality dimensions (Statistics Canada)

*STATCAN-QG* (6th ed., 2019) frames statistical quality as **fitness for use** across **six
dimensions**. A questionnaire influences several of them directly:

1. **Relevance** — whether the information meets users' needs. Set by the objective and the
   construct-to-item mapping (`questionnaire-structure.md` Part I).
2. **Timeliness and punctuality** — delay between reference period and availability, and
   adherence to schedule. Instrument length and mode affect field duration
   (`instrument-types-and-modes.md`).
3. **Accuracy and reliability** — how well the estimates reflect reality. Driven by *both*
   measurement error (wording, scales, order — `question-wording.md`,
   `questionnaire-structure.md`) *and* sampling/coverage/nonresponse error
   (`sampling-and-representativeness.md`). This is the total-survey-error link: accuracy is the
   sum of components, not wording alone.
4. **Accessibility and clarity** — how readily users can obtain and understand the data and its
   documentation. Connects to the disclosure duties in `ethics-and-standards.md`.
5. **Interpretability** — availability of the metadata needed to make sense of the data:
   concepts, variables, classifications, and methods. Documentation of design decisions,
   adaptations, and question wording (`cross-cultural-adaptation.md`, `ethics-and-standards.md`)
   feeds this dimension.
6. **Coherence and comparability** — the degree to which the data can be reliably combined or
   compared across time, space, and sources. This is exactly what verbatim repetition
   (`questionnaire-structure.md` Part IV), harmonization (`cross-cultural-adaptation.md`), and
   validated standard measures (`special-constructs.md`) protect.

These dimensions can **trade off** against each other (e.g., improving a flawed item raises
accuracy but can break coherence with a historical series — the dilemma named in
`questionnaire-structure.md` Part IV). Quality is managed by balancing them against the survey's
purpose, not by maximizing one.

---

## Part III — How the skill's references map to process and quality

| Skill reference                        | GSBPM locus                    | Quality dimension(s) most affected            |
|----------------------------------------|--------------------------------|-----------------------------------------------|
| `questionnaire-structure.md` (objective→items) | 2.1–2.3 Design          | Relevance                                     |
| `question-wording.md`                  | 2.3 Design / 3.1 Build         | Accuracy & reliability                        |
| `questionnaire-structure.md` (order, layout) | 2.3 / 3.1                 | Accuracy & reliability                        |
| `instrument-types-and-modes.md`        | 2.3 Design collection          | Timeliness; accuracy                          |
| `sampling-and-representativeness.md`   | 2.4 Design frame & sample      | Accuracy & reliability                        |
| `pretesting.md`                        | Design↔Build iteration; 4 Collect (pilot) | Accuracy & reliability             |
| `cross-cultural-adaptation.md`         | 2.2–2.3; 3.1                   | Coherence & comparability; interpretability   |
| `special-constructs.md`                | 2.2–2.3; 3.1                   | Coherence & comparability                     |
| `ethics-and-standards.md`              | Overarching; dissemination     | Accessibility & clarity; interpretability     |

This table is a map, not a workflow — it shows that the references are facets of one
quality-managed process, each touching a different point of GSBPM and a different quality
dimension.

---

## Part IV — Framing notes for review

In review mode this reference rarely produces stand-alone "defects"; it supplies *context* for
the findings of the other references:

- Ask whether design decisions were made **with the objective and variable definitions**, not
  after the fact (GSBPM 2.2–2.3 interdependence). A questionnaire whose items don't trace to a
  defined objective is a relevance failure (already a defect under
  `questionnaire-structure.md`).
- Ask whether quality was **managed across the process** (documentation, testing, metadata) or
  treated as a final formatting step. Missing metadata/documentation is an interpretability
  weakness.
- When findings conflict (a fix improves accuracy but harms coherence), present the **trade-off
  across quality dimensions** explicitly rather than asserting one right answer — the
  process/quality framing is what lets the user decide against purpose.

This reference does not turn questionnaire review into a process audit. It ensures the review
remembers that a questionnaire is one component of a larger system whose quality is the sum of
its parts.

---

## Sources drawn on in this reference
*UNECE-GSBPM* (v5.2, 2025), *STATCAN-QG* (6th ed., 2019). Full details in `source-map.md`.
Total-survey-error connections appear in `sampling-and-representativeness.md`; the
fitness-for-purpose doctrine is in `SKILL.md`.
