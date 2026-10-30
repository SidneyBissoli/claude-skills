# Instrument Types & Data-Collection Modes

This reference covers the **mode** of data collection and the **type** of instrument, and how
each constrains design and inference. Mode is decided *early*, before wording and structure are
finalized, because it determines what those can be (*ASA-WIS*, *CCSG-QD*). It serves both modes
of the skill: in **create**, choose mode and instrument type up front; in **review**, check
that wording, structure, and inferential claims are consistent with the mode actually used.

Source tags resolve in `source-map.md`.

## Contents
- Part I — The mode taxonomy and its defining dimensions
- Part II — Comparative properties of the main modes
- Part III — How mode constrains wording and structure
- Part IV — Instrument type and inference (probability vs. self-selected)
- Part V — Choosing a mode; defects vs. legitimate choices

---

## Part I — The mode taxonomy and its defining dimensions

The main modes are **self-administered** (paper/mail; web/electronic) and
**interviewer-administered** (telephone, including CATI; face-to-face/CAPI), plus
**mixed-mode** combinations (*AAPOR-BP*, *NG-2006*, *STATCAN-SMP*). *CCSG-QD* frames mode along
three dimensions that explain most of its design consequences:

1. **Who enters the data** — an interviewer (telephone, face-to-face) or the respondent (web,
   paper).
2. **Channel of communication** — visual, oral, aural, or tactile.
3. **Sense of privacy** — self-administered modes usually create more privacy than
   interviewer-administered ones.

These dimensions, not the technology label, drive the trade-offs below.

---

## Part II — Comparative properties of the main modes

Drawn from *AAPOR-BP*, *STATCAN-SMP*, *NG-2006*, and *HARVARD-PSR*. No mode is best in the
abstract; each trades cost against control, reach, and data quality.

**Web / online (self-administered).** Fast and low-cost; good when contact is by email. Reduces
social-desirability pressure on sensitive items (no interviewer to disclose to). But coverage
is uneven — older, lower-income, and rural respondents are less likely to have reliable access
or comfort (*AAPOR-BP*). Visual channel → **primacy** effects; radio buttons outperform
drop-downs (*HARVARD-PSR*).

**Telephone / CATI (interviewer-administered).** Costlier than web (requires interviewers); a
trained interviewer can clarify and sustain engagement, reducing break-offs (*AAPOR-BP*). Aural
channel → **recency** effects and a practical ceiling on the number of scale points and on
question length. *HARVARD-PSR* recommends allowing "Don't know" as a *volunteered* response on
the phone rather than reading it.

**Face-to-face / CAPI (interviewer-administered).** Highest cost and time, but the interviewer
builds rapport and supports long or complex instruments; can carry complex branching
(*AAPOR-BP*, *STATCAN-SMP*). Often used when the frame is a list of addresses.

**Mail / paper (self-administered).** Works when mailing addresses are known; respondents
answer at their convenience without a computer, and it suits sensitive topics. But it cannot be
automated, so it works best with a **straightforward flow** — complex skips confuse respondents
(*AAPOR-BP*, *STATCAN-SMP*).

**Self-administered vs. interviewer-administered, summarized (*STATCAN-SMP*).**
- Self-enumeration: better for sensitive questions (private, no interviewer), but quality can
  suffer because respondents may miss skips or misread; must avoid complicated skip patterns.
- Interviewer-assisted: better response rates and engagement, can handle complex branching, but
  the interviewer's presence can introduce response error and social-desirability/"appropriate
  answer" pressure on sensitive topics (*STATCAN-SMP*, *NG-2006*).

---

## Part III — How mode constrains wording and structure

Mode is not cosmetic; it changes what the instrument can contain. Decide it first, then design
accordingly (cross-references in brackets):

- **Length and complexity** — telephone favors short stems and simple structures; face-to-face
  tolerates the most complexity [`questionnaire-structure.md`].
- **Scale points** — aural modes cap the number of points respondents can hold in mind
  [`question-wording.md` Part III-A].
- **Skip/branching** — complex skips are fine in interviewer/computer-assisted modes, a defect
  in self-administered paper [`questionnaire-structure.md`].
- **Option-order effects** — visual modes → primacy; aural → recency; rotate/randomize to
  mitigate [`question-wording.md` Part II-15].
- **"Don't know"/neutral handling** — mode shifts whether these are read or only volunteered
  [`question-wording.md` Part III-B/C].
- **Sensitive items** — self-administration reduces social-desirability bias; reserve the most
  sensitive content for private modes [`question-wording.md` Part I-9].

---

## Part IV — Instrument type and inference (probability vs. self-selected)

Mode (how data are collected) is distinct from **instrument type and sampling basis** (who
answers and what the results can support). This distinction is where most over-claiming
happens, and it underpins the inference caution carried in `sampling-and-representativeness.md`.

*ESOMAR/WAPOR-OP* is explicit: a scientific opinion poll selects respondents by explicit
statistical sampling criteria to ensure representativeness and words questions in a balanced
way. It must **not** be confused with phone-in polls or other self-selecting surveys — including
those open to anyone visiting a website, which attract people who feel strongly about the topic
and **do not constitute a representative sample**. *AAPOR-BP* draws the same probability vs.
non-probability line and notes that non-probability results require special statistical
techniques and great care about transparency.

Practical consequences for design and reporting:
- A self-selected web instrument (the typical open online poll) can be perfectly well-*designed*
  yet still **not support population inference**. Good wording does not buy representativeness.
- If the instrument collects sociodemographics, resist the temptation to present subgroup
  breakdowns as if they generalized; a non-probability base cannot license that (Doctrine #5).
- Disclose the mode and the sampling method (probability vs. quota/non-probability) — an
  ethics/transparency requirement (*ESOMAR/WAPOR-OP*; see `ethics-and-standards.md`).

For the full treatment of coverage, self-selection, and what each design permits you to
conclude, go to `sampling-and-representativeness.md`.

---

## Part V — Choosing a mode; defects vs. legitimate choices

**Decision drivers** (*AAPOR-BP*, *ASA-WIS*, *NG-2006*): the sampling frame and quality of
contact information (addresses → mail/face-to-face; phone numbers → telephone; email/panel →
web); budget and time; the population's access and comfort; topic sensitivity; and instrument
length/complexity.

Most mode choices are **legitimate design decisions**, driven by these constraints — not
defects, and not "divergences" in the Part III sense of `question-wording.md`. What *is* a
defect is a **mismatch**: complex skips in a self-administered paper form; a long, fine-grained
scale battery on the telephone; or — most seriously — presenting self-selected, non-probability
results as representative of a population. The first two are design errors; the last is a
misrepresentation that the ethics and sampling references treat as unacceptable.

---

## Sources drawn on in this reference
*AAPOR-BP*, *STATCAN-SMP*, *NG-2006*, *HARVARD-PSR*, *CCSG-QD*, *ESOMAR/WAPOR-OP*. Full details
in `source-map.md`. Inference and sampling specifics are developed in
`sampling-and-representativeness.md`; disclosure requirements in `ethics-and-standards.md`.
