### Eval

**You own the experiment design.** Candidates run blind. An agent that
knows it is being evaluated behaves differently.

Non-negotiables for blinding:

- No `eval`, `test`, `judge`, `experiment`, `rubric`, `score`,
  `compare`, `benchmark`, `candidate`, or `arena` in any directory,
  file, or prompt the candidate sees.
- The candidate prompt looks like an organic user request.
- No chain-eliciting cues. Grade from code shape, not self-report.
- Sanitize directory and slug names.
- The judge sees outputs by sanitized label only, never a model or
  family name.
- Comparing two variants: one judge scores both sets in a single pass.

Steps:

1. Frame the variant and the success behavior. Write the rubric for
   the judge only.
2. Set up sanitized environments, one working dir per candidate.
3. Author one organic prompt.
4. Spawn N parallel candidates via `arena` Phase B, each in its own
   sanitized dir.
5. Spawn one blinded judge on a different capability tier via `arena`
   Phase C.
6. Verify the chain from transcripts the harness names, not
   self-report. Look at which files each candidate actually opened.
7. Read every candidate output yourself. Compare to the judge. Synthesize.

**Reply:** variant under test, rubric, per-candidate notes, judge
verdict, synthesis, promote or not.
