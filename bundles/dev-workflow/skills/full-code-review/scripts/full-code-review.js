export const meta = {
  name: "full-code-review",
  description: "Multi-dimension PR review: structural, security, devex/flags — adversarial verify — Opus synthesis",
  phases: [
    "Parallel dimension review",
    "Adversarial verification",
    "Opus synthesis"
  ]
};

// ── Shared finding schema ──────────────────────────────────────────────────
const findingSchema = {
  type: "object",
  required: ["dimension", "severity", "file", "finding", "evidence", "fix"],
  properties: {
    dimension: { type: "string", enum: ["structural", "security", "devex"] },
    severity:  { type: "string", enum: ["BLOCKER", "HIGH", "MEDIUM", "LOW"] },
    file:      { type: "string", description: "Repo-relative file path, or 'global'" },
    line:      { type: ["integer", "null"] },
    finding:   { type: "string", description: "One-sentence description of the issue" },
    evidence:  { type: "string", description: "Exact code snippet or specific diff line that proves the issue" },
    fix:       { type: "string", description: "Concrete, stack-idiomatic remediation direction" }
  }
};

const findingsSchema = {
  type: "object",
  required: ["findings"],
  properties: {
    findings: { type: "array", items: findingSchema }
  }
};

// ── Phase 1: parallel dimension reviewers ─────────────────────────────────
log("Phase 1: Parallel dimension review");

const [structuralResult, securityResult, devexResult] = await parallel([

  // Reviewer A — Structural
  () => agent(
    `You are a structural reviewer. Review the diff for structural and
maintainability issues in this codebase (Next.js 16, Bun, TypeScript strict,
Tailwind v4, shadcn/ui).

Check for:
1. File size — files crossing ~1000 lines in this PR are a blocker; name the
   file and line count.
2. Thin abstractions — helpers that are identity functions, one-liner renames,
   or passthrough wrappers should be inlined and deleted. Flag them.
3. Scattered branching — \`if (featureFlag)\` forks or \`if (isAdmin)\` logic
   spread across multiple components/render paths; flag when >2 independent
   branches exist for the same decision.
4. Layer violations — mutations in React components instead of server actions;
   derived client state not in a hook; raw \`<button>\`/\`<input>\` when shadcn
   Button/Input is already imported in the same file.
5. Circular dependency introduction — flag if an import in this diff creates an
   obvious circular dep cycle.
6. Dead code — exported symbols introduced but never referenced in the diff
   scope.
7. Test quality — tests that only assert code runs (no behavioral assertion);
   snapshot tests that will never fail; external integrations with no contract
   test coverage.

High-conviction findings only. Exclude bugs, security issues, and CLAUDE.md
rule violations (other reviewers or the harness cover those).
Use stack-idiomatic fix language: "Code-judo: inline it and delete the file.",
"Wrap in a Prisma transaction — sequential awaits leave the DB half-written.",
"Delete tailwind.config.ts, move tokens to the CSS @theme block (v4)."

DIFF:
\`\`\`diff
${DIFF}
\`\`\`

CHANGED FILES: ${CHANGED_FILES}

Return JSON matching the findings schema.`,
    {
      label: "structural-reviewer",
      schema: findingsSchema,
      model: "sonnet"
    }
  ),

  // Reviewer B — Security
  () => agent(
    `You are a security reviewer. Review the diff using the security-audit
rubric for web applications and APIs (stack: Next.js 16, Bun, TypeScript,
Prisma, shadcn/ui).

Check for:
1. Injection risk — unsanitized user input reaching queries, templates, evals,
   shell commands, or file paths introduced by this diff.
2. Broken access control / IDOR — new endpoints or data-access calls missing
   tenant/org filter or auth guard; privilege escalation paths.
3. Secret exposure — credentials, API keys, tokens, or environment variable
   values hard-coded or logged in this diff.
4. XSS — dangerouslySetInnerHTML, unescaped interpolation into HTML, or DOM
   sinks with user-controlled input.
5. CSRF — state-changing server actions or API routes without proper Next.js
   CSRF handling.
6. Insecure defaults — CORS wildcard, missing cookie security flags
   (httpOnly/secure/sameSite), disabled CSRF, debug mode left on.
7. Dependency risk — new packages added in this diff with known CVEs or
   suspicious provenance (flag the package name and concern).
8. Webhook / callback trust — external callback handlers that trust payload
   fields before verifying signature.
9. Timing attacks — equality checks on tokens or secrets using \`===\` instead
   of constant-time comparison.
10. SSRF / open redirect — user-controlled URLs passed to fetch/axios without
    allowlist validation.

For each finding: exact diff line as evidence, required privilege level to
exploit, realistic impact, and concrete fix.

Exclude issues pre-existing in unchanged code. Exclude structural concerns
(other reviewers cover those).

DIFF:
\`\`\`diff
${DIFF}
\`\`\`

CHANGED FILES: ${CHANGED_FILES}

Return JSON matching the findings schema. Use dimension: "security".`,
    {
      label: "security-reviewer",
      schema: findingsSchema,
      model: "sonnet"
    }
  ),

  // Reviewer C — DevEx / Feature-Flag Hygiene
  () => agent(
    `You are a devex and feature-flag hygiene reviewer. Review the diff for
developer-experience regressions and flag management issues (stack: Next.js 16,
Bun, TypeScript strict, Tailwind v4, shadcn/ui).

Check for:
1. Feature-flag hygiene — new flags introduced without evidence of a cleanup
   ticket; flags that are always-on boolean constants instead of evaluated
   conditions; rollout config inconsistencies; flags evaluated multiple times
   without memoization.
2. Internal-API breaking changes — exported function signatures changed or
   removed without a deprecation bridge; renamed exports that break callers
   outside this diff.
3. Convention violations introduced by this diff — \`bun\`/\`bunx\` only (never
   npm/npx/yarn/pnpm); Tailwind v4 CSS-config only (no tailwind.config.ts, no
   @apply); Next.js 16 middleware named \`proxy.ts\` not \`middleware.ts\`; no
   \`any\` types; no \`console.log\`.
4. Missing changelog — a public-facing behavior change with no changelog or
   release-note entry.
5. Docs divergence — a changed function/API with a stale JSDoc or README
   description that now contradicts the code.
6. Type inference degradation — type assertions (\`as X\`) introduced without an
   explanatory comment; broadened return types that weaken caller inference.

High-conviction findings only. Exclude correctness bugs and security issues
(other reviewers cover those).

DIFF:
\`\`\`diff
${DIFF}
\`\`\`

CHANGED FILES: ${CHANGED_FILES}

Return JSON matching the findings schema. Use dimension: "devex".`,
    {
      label: "devex-reviewer",
      schema: findingsSchema,
      model: "sonnet"
    }
  )

]);

// ── Phase 2: adversarial verification ────────────────────────────────────
log("Phase 2: Adversarial verification");

const allFindings = [
  ...(structuralResult.findings || []),
  ...(securityResult.findings   || []),
  ...(devexResult.findings      || [])
];

const verifiedItemSchema = {
  type: "object",
  required: ["dimension", "severity", "file", "finding", "evidence", "fix", "verified", "refutation_attempt"],
  properties: {
    dimension:           { type: "string" },
    severity:            { type: "string", enum: ["BLOCKER", "HIGH", "MEDIUM", "LOW"] },
    file:                { type: "string" },
    line:                { type: ["integer", "null"] },
    finding:             { type: "string" },
    evidence:            { type: "string" },
    fix:                 { type: "string" },
    verified:            { type: "boolean" },
    refutation_attempt:  { type: "string" }
  }
};

const verifiedSchema = {
  type: "object",
  required: ["verified_findings"],
  properties: {
    verified_findings: { type: "array", items: verifiedItemSchema }
  }
};

const verificationResult = await agent(
  `You are an adversarial verifier. Your job is to REFUTE each finding below.
For each finding, try hard to prove it is wrong: check whether the issue exists
in the diff at all, whether the evidence line actually shows the problem, whether
the fix is already present elsewhere, whether this is a pre-existing issue not
touched by the diff, or whether the concern is speculative/stylistic with no
real impact.

Set \`verified: true\` only when you CANNOT refute the finding — i.e., the
evidence is concrete, the issue is real, and it is caused or exposed by this
diff. Set \`verified: false\` with a clear \`refutation_attempt\` explanation when
the finding does not hold up.

Be skeptical. Drop uncertain findings — a lower-noise report is more valuable
than exhaustive speculation.

DIFF:
\`\`\`diff
${DIFF}
\`\`\`

FINDINGS TO VERIFY:
${JSON.stringify(allFindings, null, 2)}

Return JSON with all findings annotated with \`verified\` and
\`refutation_attempt\`.`,
  {
    label: "adversarial-verifier",
    schema: verifiedSchema,
    model: "opus"
  }
);

const survivingFindings = (verificationResult.verified_findings || [])
  .filter(f => f.verified === true);

// ── Phase 3: Opus synthesis ───────────────────────────────────────────────
log("Phase 3: Opus synthesis");

const verdictSchema = {
  type: "object",
  required: ["verdict", "rationale", "prioritized_findings", "stats"],
  properties: {
    verdict: {
      type: "string",
      enum: ["approve", "request-changes", "block"]
    },
    rationale: {
      type: "string",
      description: "One sentence explaining the verdict"
    },
    prioritized_findings: {
      type: "array",
      items: {
        type: "object",
        required: ["rank", "severity", "dimension", "file", "finding", "evidence", "fix", "overlap_weight"],
        properties: {
          rank:           { type: "integer" },
          severity:       { type: "string", enum: ["BLOCKER", "HIGH", "MEDIUM", "LOW"] },
          dimension:      { type: "string" },
          file:           { type: "string" },
          line:           { type: ["integer", "null"] },
          finding:        { type: "string" },
          evidence:       { type: "string" },
          fix:            { type: "string" },
          overlap_weight: {
            type: "integer",
            description: "1 = single dimension, 2 = two dimensions flagged it, 3 = all three",
            enum: [1, 2, 3]
          },
          also_flagged_by: {
            type: "array",
            items: { type: "string" }
          }
        }
      }
    },
    stats: {
      type: "object",
      properties: {
        total_raw:               { type: "integer" },
        dropped:                 { type: "integer" },
        surviving:               { type: "integer" },
        blockers:                { type: "integer" },
        high:                    { type: "integer" },
        dimensions_contributing: { type: "array", items: { type: "string" } }
      }
    }
  }
};

const synthesisResult = await agent(
  `You are the synthesis judge for a multi-dimension code review. Your job is to:

1. Deduplicate findings that describe the same root issue across dimensions
   (same file + same root cause = one finding). Merge their evidence.
2. Weight overlapping findings higher: a finding flagged by 2+ dimensions is
   more certain — set \`overlap_weight\` accordingly (1/2/3).
3. Rank all surviving findings: BLOCKER first, then HIGH, then MEDIUM, then LOW.
   Within a severity tier, overlap_weight breaks ties (higher weight = lower
   rank number = more urgent).
4. Emit a single verdict:
   - "block"            if any BLOCKER finding survives.
   - "request-changes"  if any HIGH finding survives (no BLOCKERs).
   - "approve"          if only MEDIUM/LOW findings survive or none.
5. Write a one-sentence rationale that names the most critical finding.

SURVIVING VERIFIED FINDINGS:
${JSON.stringify(survivingFindings, null, 2)}

Return JSON matching the verdict schema.`,
  {
    label: "opus-synthesis",
    schema: verdictSchema,
    model: "opus"
  }
);

log(`Verdict: ${synthesisResult.verdict} — ${synthesisResult.rationale}`);
log(`Findings: ${synthesisResult.stats?.surviving ?? survivingFindings.length} verified (${synthesisResult.stats?.dropped ?? (allFindings.length - survivingFindings.length)} dropped by adversarial pass)`);

return synthesisResult;
