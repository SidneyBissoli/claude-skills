# Pretesting

Pretesting is the set of activities that evaluate an instrument and its field procedures
**before** data collection begins. It is not optional polish: *OMB-STD* Standard 1.4 *requires*
agencies to ensure all survey components function as intended and that measurement error is
controlled by pretesting (or by having successfully fielded the components previously);
*CCSG-PT* calls it essential for identifying and reducing measurement error and protecting
comparability. *ASA-WIS*, *NG-2006*, *STATCAN-SMP*, and *ESS-HB* all treat testing before
fielding as a standard step.

This reference serves both modes: in **create**, deliver a *proportionate* pretest plan as part
of the design; in **review**, check whether the instrument was (or should have been) pretested,
and whether the plan fits the study's goals, mode, and population.

Source tags resolve in `source-map.md`.

## Contents
- Part I — Why pretest, and what counts
- Part II — The toolkit: techniques, purposes, limits
- Part III — Sequencing and combining techniques
- Part IV — Two non-negotiables: same mode, same population
- Part V — Staff, 3MC, and documentation
- Part VI — Proportionality; create vs. review

---

## Part I — Why pretest, and what counts

The purpose is to surface problems while they are still cheap to fix — ambiguous wording,
misread response options, broken routing, length/timing issues, comprehension gaps, and
mode-specific failures (*CCSG-PT*, *ASA-WIS*). *OMB-STD* allows prior successful fielding of the
same components to substitute for a fresh pretest — but *new or substantially changed* items,
and any new population or mode, require testing. The output of pretesting is not just a verdict
but a documented list of problems and decisions about changes (Part V).

---

## Part II — The toolkit: techniques, purposes, limits

*CCSG-PT* (Table 1) catalogues the common techniques. No single method is sufficient, and
studies comparing methods have found they can yield **different or even contradictory** results
about the same item — so choose deliberately by strengths and weaknesses, not habit.

- **Expert review.** Specialists scrutinize draft items. Low-cost first pass, good before
  recruiting respondents (*CCSG-PT*). *HARVARD-PSR* notes review services (and the QUAID tool)
  that flag common wording problems.
- **Focus groups / in-depth interviews.** Used *early*, often before item drafting, to develop
  constructs and surface vocabulary (*CCSG-PT*). Limit: some topics are too sensitive to discuss
  in a group; *CCSG-PT* reports a Malawi case where in-depth interviews had to precede focus
  groups for menstruation. Don't over-rely on focus groups (a caution *CCSG-PT* raises for
  health research).
- **Cognitive interviewing.** Respondents think aloud (concurrently or retrospectively) so the
  researcher sees comprehension, recall, judgment, and response-mapping (*CCSG-PT*).
  *HARVARD-PSR* gives the practitioner version: have people think aloud and probe "What does
  that mean to you?" Requires a discursive style *different from* standardized interviewing and
  therefore special training (Part V).
- **Behavior coding.** Systematic coding of interviewer–respondent interaction to detect items
  that routinely cause trouble (*CCSG-PT*).
- **Pilot study / field test ("dress rehearsal").** Runs all procedures and materials at small
  scale before launch (*CCSG-PT*). Checks instrument length/timing, response rates under a
  protocol, layout familiarity, the answering process, and item-difficulty statistics; a
  robust-sample pilot with adequate power is often the best overall test. *ASA-WIS* and
  *NG-2006* both make a pilot a standard final step; *STATCAN-SMP* lists cognitive testing,
  focus groups, and informal testing among methods.
- **Observational interviews** (*ESS-HB*) — one-on-one sessions to identify wording, question
  order, response-category, and visual-design problems under near-real conditions.
- **3MC/cultural techniques** (*CCSG-PT*): vignettes, consensus panels, questerviews, and
  ethnographic pretest interviews, which probe whether a question makes sense within a culture.

---

## Part III — Sequencing and combining techniques

*CCSG-PT* guideline 2: combine methods to exploit strengths and cover weaknesses, moving from
**specific** to **comprehensive**:

1. Focus groups / in-depth interviews → develop constructs and wording.
2. Cognitive interviews → develop and refine items.
3. Field pilot → test the whole instrument and field procedures together.

Expect **multiple iterations**, not one large pretest: test, revise, test again, documenting
each round (*CCSG-PT*). The *GSS* runs a "full pretest" of all new items under realistic field
conditions between cognitive testing and a pilot; *CCSG-PT*'s SAMHSA A-CASI example shows
lab cognitive testing → pilot → experimental pilot → split-sample comparison when a mode change
could shift trend lines.

---

## Part IV — Two non-negotiables: same mode, same population

*CCSG-PT* guidelines 4 and 5 are firm, and they are the most common pretesting **defects** when
violated:

- **Same mode.** Early construct testing can use face-to-face lab methods, but once a draft
  exists it must be tested *in the mode the main survey will use*. Interviewer- and
  self-administered surveys differ in who reads the questions, who handles routing, social
  interaction, context effects (primacy/recency), and social-desirability pressure — so a
  pretest in the wrong mode misses mode-specific failures (*CCSG-PT*).
- **Same target population.** Pretest with the population the survey will actually sample. Even
  questions reused from other studies need local pretesting, because performance depends on the
  current mode, question order, population, and (in 3MC) the translation (*CCSG-PT*).

---

## Part V — Staff, 3MC, and documentation

**Staff and training.** Some techniques need skills standard interviewers lack — cognitive
interviewing's discursive probing is "a new concept" even for experienced standardized
interviewers and needs dedicated training (*CCSG-PT* recounts adding a training day in a Nepali
WHO study because interviewers kept pushing for a codable answer instead of probing thinking).

**3MC pretesting.** Pretest every language version; it is essential for measurement and
cross-cultural equivalence (*CCSG-PT*). Cognitive interviewing does not transfer unchanged
across cultures — response patterns to probes differ by language group, and culture- or
language-specific probes and rapport-building may be needed. Decide whether to develop cognitive
protocols directly in each target language or translate a source protocol. For translation and
adaptation specifics, see `cross-cultural-adaptation.md`.

**Evaluate, document, decide.** *CCSG-PT* guidelines 6–7: evaluate the results, fully document
the protocol and findings, and make explicit decisions about instrument changes — then feed
revisions back into another testing round. Document enough that another analyst can understand
what was tested and why a change was made.

---

## Part VI — Proportionality; create vs. review

**Proportionality.** Match pretest depth to stakes (the skill's proportionality guardrail). A
short, low-stakes instrument of well-worn items may need only expert review and a small pilot;
a high-stakes population survey, a new construct, or a multilingual study warrants the full
sequence. The question is never "did they do everything?" but "was the testing adequate to the
risk?"

**In review mode**, classify with Doctrine #4:

| Observation                                                       | Classify as |
|-------------------------------------------------------------------|-------------|
| New/changed items fielded with no pretest and no prior validation | Defect      |
| Pretested in a different mode than the main survey                | Defect      |
| Pretested on a different population than will be sampled          | Defect      |
| Cognitive interviewing run by untrained standardized interviewers | Defect      |
| A proportionate plan; reuse of previously-fielded components      | Legitimate  |
| Choice among adequate techniques (expert review vs. cognitive…)   | Divergence  |

If the instrument was adequately tested for its risk level, say so; do not demand more testing
for its own sake.

---

## Sources drawn on in this reference
*CCSG-PT*, *OMB-STD*, *ASA-WIS*, *NG-2006*, *STATCAN-SMP*, *ESS-HB*, *HARVARD-PSR*. Full details
in `source-map.md`. Cross-cultural pretesting connects to `cross-cultural-adaptation.md`.
