### Authoring or modifying a skill

**You own the skill's voice.** Name `skill-creator` for the authoring
workflow. Capture a finished session with `skill-capture` only when the
human asks.

1. Follow `skill-creator` for structure, frontmatter, and progressive
   disclosure.
2. Validate: `name` matches the directory, referenced files exist,
   cross-skill links resolve, no concrete model names.
3. Test cases if structural. Skip if subjective.
4. Run Opening a PR.

When in doubt, delete. Prose earns its keep by changing a decision.
Point at structural sources. Hardcoded details go stale. Delegate to
other skills by name. Do not restate them.

**Reply:** summary of the skill, key design decisions, validation notes.
