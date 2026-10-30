# Sampling & Representativeness — Inference Limits

This reference is **scoped to inference**: what an instrument's sampling basis permits the user
to *conclude*. It is not a sampling-design manual — for frame construction, sample-size
determination, cluster and multistage design, and weighting mechanics, go to the source
manuals (*UN-HHS*, *UN-HB2026*, *STATCAN-SMP*). Here the goal is narrower and essential to the
skill: a questionnaire can be flawless in wording and structure and still support no valid
population claim. This file operationalizes **Doctrine #5** (be explicit about inference
limits).

It serves both modes: in **create**, fix the inferential goal up front and design and document
to it; in **review**, check that every claim the instrument or its report makes is licensed by
the sampling basis.

## Contents
- Part I — Population, frame, sample, inference
- Part II — Probability vs. non-probability: what each permits
- Part III — Self-selection and open web polls (the high-risk case)
- Part IV — Error: sampling vs. non-sampling, and total survey error
- Part V — Nonresponse, weighting, and their limits
- Part VI — Practical doctrine; defects vs. legitimate design choices

---

## Part I — Population, frame, sample, inference

Four things must be distinguished and kept aligned:

- **Target population** — who the study is about. Define it explicitly (*OMB-STD* Standard 1.2;
  *UN-HHS*).
- **Sampling frame** — the list or mechanism from which units are drawn. The frame must be
  *appropriate for the design and evaluated against the target population for quality*
  (*OMB-STD* Standard 2.1); *UN-HHS* devotes a chapter to frame properties and to coverage/frame
  error. A frame that under- or over-covers the target population introduces **coverage error**
  before a single question is asked.
- **Sample** — the units actually selected.
- **Inference** — the leap from the responding sample back to the target population. Whether
  that leap is valid depends entirely on how the sample was obtained.

---

## Part II — Probability vs. non-probability: what each permits

This is the decisive distinction for inference.

**Probability sampling.** Every unit has a known, non-zero chance of selection. Only under
probability sampling can sampling error be estimated, reliability gauged, and confidence
intervals constructed (*UN-HHS*; *OMB-STD* Standard 1.2, which ties "generally accepted
statistical methods" to "probabilistic methods that can provide estimates of sampling error").
*UN-HHS* recommends probability sampling always be used in household surveys, even when it costs
more than non-scientific alternatives.

**Non-probability sampling** (quota, cut-off, model-based, convenience, opt-in panels,
self-selection). *UN-HHS* is blunt: "there is no statistical theory to guide the use of
non-probability samples. They can only be assessed through subjective evaluation. Failure to
use probability techniques means … the survey estimates will be biased." *OMB-STD* permits
non-probability methods only when "justified statistically" and "able to measure estimation
error." *AAPOR-BP* adds that non-probability results require special statistical techniques and
great care about transparency. *UN-HB2026* treats the probability/non-probability divide
explicitly and situates newer non-probability and data-integration methods under "emerging
approaches" — useful, but not a license to claim probability-grade inference.

The practical upshot: **good questionnaire design does not buy representativeness.** Wording and
structure govern measurement quality; the sampling basis governs whether results generalize.
The two are independent.

---

## Part III — Self-selection and open web polls (the high-risk case)

The most common over-claim, and the one most relevant to open online polls. *ESOMAR/WAPOR-OP*
states that a scientific opinion poll selects respondents by explicit statistical sampling
criteria to ensure representativeness, and must **not** be confused with phone-in polls or other
self-selecting surveys — including those open to anyone who visits a website, which attract
people who feel strongly about the topic and **do not constitute a representative sample**.

For an instrument with a self-selected base (the typical open e-participation or website poll):
- Results describe **the people who chose to respond**, not the population.
- Subgroup breakdowns by sex, region, race, age, etc., describe *respondents in those cells*,
  not those segments of the population — even though the instrument collected the variables.
  Collecting sociodemographics does not retroactively create a probability sample.
- A **margin of error** should not be reported; sampling error is only estimable under
  probability sampling (*UN-HHS*, *OMB-STD*). Presenting one implies a representativeness the
  design lacks.
- Such instruments are still legitimate for **exploratory, illustrative, or engagement**
  purposes — provided the limits are stated and no population inference is drawn.

---

## Part IV — Error: sampling vs. non-sampling, and total survey error

Two broad error classes matter for inference:

- **Sampling error** — variability from observing a sample rather than the whole population.
  Estimable (and reducible by design and sample size) only under probability sampling
  (*UN-HHS*, *OMB-STD*).
- **Non-sampling error** — coverage error (frame ≠ population), nonresponse error, and
  measurement error (from wording, mode, interviewer, processing). These exist regardless of
  sampling basis and are often larger than sampling error.

The **total survey error (TSE)** perspective (*CCSG-QD*; reflected in *STATCAN-QG*'s accuracy
dimension) connects this file to the rest of the skill: a double-barreled item or a primed
question order is *measurement* error, just as a bad frame is *coverage* error. Quality is the
sum, not any single component. *STATCAN-QG* frames accuracy/reliability as one quality dimension
to be managed across the whole statistical process — not achieved by good wording alone.

---

## Part V — Nonresponse, weighting, and their limits

**Nonresponse.** *OMB-STD* requires designing for the highest practical response rate so results
are representative of the target population (Standard 1.3) and requires nonresponse-bias
analysis when response rates suggest potential bias; unit and item nonresponse must be measured,
adjusted for, and reported (Standard 3.2). *UN-HHS* tracks response and coverage rates across
selection stages. Low response is not just a volume problem — it is a *bias* risk if
non-respondents differ systematically from respondents.

**Weighting and calibration.** Weights can adjust a probability sample for unequal selection
probabilities, non-coverage, and nonresponse — e.g., calibrating weighted totals to known
population totals (*STATCAN-SMP*; *UN-HHS* on adjusting weights for non-coverage). But weighting
has limits that matter for honest reporting:
- It corrects imbalances on the **measured, known** dimensions used in the adjustment; it cannot
  fix imbalance on unmeasured dimensions.
- It does not convert a self-selected, non-probability base into a probability sample. Adjusting
  an opt-in poll to census margins makes it *look* balanced on those margins without restoring
  design-based inference.

State what was weighted and on which variables; do not let weighting imply more than it delivers.

---

## Part VI — Practical doctrine; defects vs. legitimate design choices

**In create mode:** state the inferential goal before choosing a design. If population inference
is required, a probability design is the path; if resources force non-probability, say so, and
scope the conclusions to exploratory/illustrative and document the limitation (Doctrine #5).

**In review mode**, this domain is mostly about **defect/misrepresentation**, not stylistic
divergence:

| Observation                                                        | Classify as |
|--------------------------------------------------------------------|-------------|
| Non-probability/self-selected results presented as population-level | Defect (misrepresentation) |
| Margin of error reported for a non-probability sample              | Defect      |
| Subgroup breakdowns from a self-selected base read as generalizable | Defect      |
| Frame not evaluated against the target population                  | Defect      |
| Low response with no nonresponse-bias consideration               | Defect      |
| Weighting implied to fix unmeasured self-selection bias           | Defect      |
| Using a non-probability design *with* explicit limits, for exploration | Legitimate design choice |

A correctly caveated non-probability study is not a flaw; an uncaveated inferential leap is.

---

## Sources drawn on in this reference
*UN-HHS*, *UN-HB2026*, *OMB-STD*, *AAPOR-BP*, *ESOMAR/WAPOR-OP*, *STATCAN-SMP*, *STATCAN-QG*,
*CCSG-QD* (total survey error). Full details in `source-map.md`. Full sampling-design mechanics
are in the UN and StatCan manuals; disclosure duties are in `ethics-and-standards.md`.
