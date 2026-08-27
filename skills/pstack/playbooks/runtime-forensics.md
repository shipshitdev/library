### Runtime forensics

**You own the diagnosis.** Instrument the live process. Do not theorize
from source. The deliverable is a cited diagnosis, not a fix.

1. Capture the live signal on the matching surface: a CPU profile, a heap
   snapshot, or a trace. A real artifact, not a guess.
2. Reduce the artifact to the smoking gun. Parse large artifacts in a
   subagent. Keep the reduced finding in the main thread.
3. Prove the mechanism before believing it. Inject instrumentation or
   hotfix the live code without reloading.
4. Map the finding back to source: file, symbol, the line that allocates
   or schedules.
5. Throughput checkpoint stays one line: `throughput checkpoint: n/a,
   read-only forensics`.

**Reply:** the signal captured, the reduced finding, how you proved the
mechanism, the source location, artifact paths. No fix unless asked.
Hand back to Bug fix or Perf once the cause is known.
