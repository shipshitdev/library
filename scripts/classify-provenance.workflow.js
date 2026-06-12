export const meta = {
  name: 'classify-provenance',
  description: 'Classify each unclassified skill as external/internal-port/in-house, verifying any external upstream by fetching the real file before claiming it',
  phases: [
    { title: 'Classify', detail: 'one verifier agent per skill — fingerprint, search, fetch-verify' },
  ],
}

const SKILLS = ["accessibility","advanced-evaluation","agent-architecture-audit","agent-browser","agent-config-audit","agent-folder-init","ai-agent-cost-optimizer","ai-loading-ux","ai-regression-testing","analyze-codebase","api-design-expert","aws-infrastructure","biome-validator","brand-architect","bun-validator","business-model-auditor","business-operator","changelog-generator","channel-validator","clerk-validator","cofounder-evaluator","comment-mode","commit-summary","competitive-intelligence-analyst","component-library","constraint-eliminator","content-creator","content-script-developer","context-degradation","context-fundamentals","context-optimization","copy-validator","copywriter","cto-advisor","de-slop","debug","deploy","deployment-composer","design-consistency-auditor","devcontainer-setup","docker-expert","docs","early-hiring-advisor","ec2-backend-deployer","email-finder","error-handling-expert","evaluation","execution-accelerator","execution-validator","expert-architect","expert-validator","expo-architect","financial-operations-expert","fullstack-workspace-init","fundraise-advisor","funnel-architect","funnel-validator","gh-address-comments","gh-fix-ci","gh-inbox","gh-pr-publish","gh-project-board","gh-review-suggestions","git-safety","github-actions-author","graphql-architect","html-style","humanizer","husky-test-coverage","idea-validator","incremental-fetch","landing-page-vercel","lead-channel-optimizer","leads-researcher","linter-formatter-init","llm-structured-output","market-sizer","memory-systems","micro-landing-builder","mongodb-atlas-checker","mongodb-migration-expert","monitoring-setup","multi-agent-patterns","mvp-architect","nestjs-expert","nestjs-queue-architect","nextjs-validator","nextra-writer","offer-architect","offer-validator","open-source-checker","outbound-optimizer","package-architect","partnership-builder","performance-expert","playwright-e2e-init","positioning-angles","pricing-strategist","production-audit","project-init-orchestrator","prompt-engineering","qa-reviewer","quick-view","react-hook-form","react-native-components","react-refactor","react-testing-library","redis-caching","refactor-code","release-pr-gates","retention-engine","roadmap-analyzer","rules-capture","scaffold","search-domain-validator","security-audit","security-expert","session-documenter","session-end","session-start","shadcn-setup","shadcn","skill-capture","skill-comply","skill-scout","spec-first","startup-icp-definer","strategy-expert","stripe-implementer","support-systems-architect","table-filters","tailwind-validator","tailwind","task-prd-creator","testing-cicd-init","testing-expert","tool-design","traffic-architect","traffic-validator","turborepo","typescript-refactor","workspace-performance-audit","x-algorithm-optimizer","youtube-video-analyst"]

const BASE = '/Users/decod3rs/www/shipshitdev/public/skills/skills'

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  properties: {
    skill: { type: 'string' },
    classification: { enum: ['external', 'internal-port', 'in-house', 'uncertain'] },
    upstream_repo: { type: 'string', description: 'owner/repo, or empty string if none' },
    upstream_path: { type: 'string', description: 'path to the upstream file within the repo, or empty' },
    upstream_url: { type: 'string', description: 'full https blob URL you actually fetched and verified, or empty' },
    license: { type: 'string', description: 'SPDX id of the upstream repo if known, else empty' },
    confidence: { enum: ['high', 'medium', 'low'] },
    verified: { type: 'boolean', description: 'true only if you fetched the upstream_url and its content clearly matches this skill' },
    evidence: { type: 'string', description: 'one or two sentences: what specifically matched or why in-house' },
  },
  required: ['skill', 'classification', 'upstream_repo', 'upstream_url', 'license', 'confidence', 'verified', 'evidence'],
}

const KNOWN = `Known upstream families in this marketplace (for reference — do NOT force-fit):
- pbakaus/impeccable (Apache-2.0): design-quality skills (audit, critique, polish, layout, quieter, shape, clarify) — ALREADY classified, not in your set.
- obra/superpowers (MIT): agent workflow skills (writing-plans, systematic-debugging, etc.) — ALREADY classified. NOTE: 'executing-plans' shares a name with superpowers but is NOT in your set.
- anthropics/skills (Apache-2.0): artifacts, mcp-builder, skill-creator, theme-factory, internal-comms — ALREADY classified.
- Dimillian/Skills (MIT): react-component-performance, plus swift/ios skills — ALREADY classified.
- snarktank/ai-dev-tasks: the classic create-prd / generate-tasks / process-task-list pattern — CHECK if 'task-prd-creator' or 'spec-first' derive from it.
- Vincent's own private 'vitae' spec-pipeline (internal, no public repo): writing-prds, prd-quality-gate, context-engineering, execution-debugging were ported from it. Other spec/PRD/context skills MIGHT be internal-port too (classification: internal-port, upstream_repo empty).`

phase('Classify')

const results = await parallel(SKILLS.map((skill) => () =>
  agent(
    `You are classifying the provenance of ONE Agent Skill in a vendored marketplace, so the owner can later check whether the original author shipped improvements worth porting back.

Skill: "${skill}"
Local file to read FIRST: ${BASE}/${skill}/SKILL.md  (also glance at ${BASE}/${skill}/README.md and ${BASE}/${skill}/references/ if present)

Your job: decide if this skill was IMPORTED from a public open-source upstream, ported from the owner's own private repo, or written in-house — and if external, VERIFY the upstream by actually fetching it.

Method:
1. Read the local SKILL.md. Note the exact skill name, the description, distinctive section headings, signature phrases, any embedded URLs/credits/license lines, and any tell-tale wording.
2. Decide whether this looks like a generic/original skill or a port. Most skills in this marketplace are the owner's OWN work (solo founder's GTM + engineering toolkit). DEFAULT to in-house.
3. If — and only if — the content smells imported, web-search for the origin: try the skill name + a distinctive verbatim phrase + "SKILL.md github", and the known families below.
4. If you find a candidate public file, you MUST fetch it (WebFetch the raw/blob URL) and confirm its content genuinely matches this skill (same name/structure, substantial verbatim or near-verbatim overlap). Only then set classification="external" and verified=true with the EXACT url you fetched.
5. If a skill is clearly part of the owner's private spec-pipeline ('vitae') with no public repo, use classification="internal-port", upstream_repo="", verified=false.
6. If you cannot verify a real matching upstream, DO NOT invent one. Use "in-house" (original) or "uncertain" (smells imported but unconfirmed), upstream_url="", verified=false.

${KNOWN}

HARD RULES:
- NEVER output an upstream_url you did not actually fetch and see matching content for. A fabricated or guessed URL is the worst possible outcome.
- "external" REQUIRES verified=true. If verified=false, classification must be in-house, internal-port, or uncertain.
- Be conservative. A same-name skill is NOT proof; the content must match.
- confidence: "high" only when verified=true OR you are certain it is original in-house work. Otherwise "medium"/"low".

Return the structured object for skill="${skill}".`,
    { label: skill, phase: 'Classify', model: 'sonnet', schema: SCHEMA }
  )
))

return { results: results.filter(Boolean) }
