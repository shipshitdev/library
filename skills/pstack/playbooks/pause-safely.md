### Pause safely

**You own a clean stop.** Leave a checkpoint a cold-start agent can
resume from. Explicit only. "Keep going" is Autonomous run.

1. Stop at a safe boundary. Finish the current atomic step or back out
   of it. Never stop mid-edit in a known-broken state.
2. Do not cross an irreversible line to pause. No PR and no push unless
   you already had one out.
3. Commit uncommitted edits as one clear `wip:` commit on the current
   branch. If the tree is broken, say so in the commit body.
4. Write the resume note under the current repo `.tmp/<slug>-resume.md`.
   Capture intent, progress, what is verified, next steps, key files,
   and gotchas. If a `show-me-your-work` trail exists, point at it.

**Reply:** where you are, what's on disk versus still in your head, the
commits you made, the first action on resume.
