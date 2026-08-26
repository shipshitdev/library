### Trace forensics

**You own the diagnosis from the artifact.** The capture already exists.
Read it. Do not re-run it.

1. Identify the format and load it with the right tool. Parse large
   artifacts in a subagent.
2. Transform the raw artifact into a form you can query. Dump into sqlite
   when that helps, one row per sample, frame, or node.
3. Narrow to the cause: hot path, retainer chain, or stuck thread.
4. Attribute to source. A frame with no source mapping is not yet a
   diagnosis. Resolve the symbols or say the artifact does not carry them.
5. Confirm against a paired capture when you have one. Without one, mark
   the finding as the strongest hypothesis, not a confirmed cause.
6. Hand back a cited diagnosis. Route to Bug fix or Perf issue once the
   cause is known.

**Reply:** the artifact and format, the reduced finding, the source
location, whether a paired capture confirmed it.
