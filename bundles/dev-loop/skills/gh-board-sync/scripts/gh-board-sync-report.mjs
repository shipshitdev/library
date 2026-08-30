#!/usr/bin/env node

// Read-only board-truth reconciliation report for a GitHub Projects v2 board.
// Collects the board, the repos it references, and recent merge activity, then
// buckets drift into the eight gh-board-sync checks. Never mutates anything —
// applying fixes is the skill's job, behind its own confirmation gates.

import { execFileSync } from 'node:child_process';

const DONE_STATUSES = new Set(['done']);
const IN_PROGRESS_STATUSES = new Set(['in progress']);
const HUMAN_REVIEW_STATUSES = new Set(['human review']);
const CLOSING_KEYWORD_PATTERN =
  /\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\b:?\s+(?:([\w.-]+\/[\w.-]+)#(\d+)|#(\d+))/gi;

const ITEMS_QUERY = `
query($id: ID!, $after: String) {
  node(id: $id) {
    ... on ProjectV2 {
      items(first: 100, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          fieldValues(first: 20) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue {
                name
                field { ... on ProjectV2SingleSelectField { name } }
              }
            }
          }
          content {
            __typename
            ... on DraftIssue { title }
            ... on Issue {
              number
              title
              state
              url
              updatedAt
              repository { nameWithOwner }
              milestone { title dueOn }
              subIssues(first: 50) { nodes { number state } }
              closedByPullRequestsReferences(first: 10, includeClosedPrs: true) {
                nodes { number state merged mergedAt url }
              }
            }
            ... on PullRequest {
              number
              title
              state
              url
              updatedAt
              merged
              mergedAt
              isDraft
              reviewDecision
              repository { nameWithOwner }
              commits(last: 1) {
                nodes { commit { statusCheckRollup { state } } }
              }
            }
          }
        }
      }
    }
  }
}`;

function parseArgs(argv) {
  const args = {
    horizon: 7,
    json: false,
    owner: '',
    project: '',
    repo: '',
    stale: 7,
    window: 14,
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--owner') {
      args.owner = readValue(argv, (index += 1), arg);
    } else if (arg === '--project') {
      args.project = readValue(argv, (index += 1), arg);
    } else if (arg === '--repo') {
      args.repo = readValue(argv, (index += 1), arg);
    } else if (arg === '--window') {
      args.window = Number.parseInt(readValue(argv, (index += 1), arg), 10);
    } else if (arg === '--stale') {
      args.stale = Number.parseInt(readValue(argv, (index += 1), arg), 10);
    } else if (arg === '--horizon') {
      args.horizon = Number.parseInt(readValue(argv, (index += 1), arg), 10);
    } else if (arg === '--json') {
      args.json = true;
    } else if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    } else {
      fail(`Unknown argument: ${arg}`);
    }
  }

  if (!args.owner || !args.project) {
    fail('Missing required --owner <login> and --project <number>.');
  }

  if (!Number.isInteger(args.window) || args.window <= 0) {
    fail('--window must be a positive integer (days).');
  }

  if (!Number.isInteger(args.stale) || args.stale <= 0) {
    fail('--stale must be a positive integer (days).');
  }

  if (!Number.isInteger(args.horizon) || args.horizon <= 0) {
    fail('--horizon must be a positive integer (days).');
  }

  return args;
}

function readValue(argv, index, flag) {
  const value = argv[index];
  if (!value || value.startsWith('--')) {
    fail(`Missing value for ${flag}.`);
  }
  return value;
}

function printHelp() {
  process.stdout.write(`Usage:
  node gh-board-sync-report.mjs --owner <owner> --project <number> [options]

Options:
  --repo owner/name   Limit repo-side checks to one repository (default: every
                      repository the board's items reference).
  --window 14         Days of merge/issue history for the untracked-work check.
  --stale 7           Days without movement before In Progress counts as stale.
  --horizon 7         Sprint horizon in days for milestone readiness — which
                      milestones come due, and what is still open in them.
  --json              Emit the raw finding buckets as JSON.

This report is read-only. It never writes to GitHub.
`);
}

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function gh(args) {
  try {
    return execFileSync('gh', args, {
      encoding: 'utf8',
      maxBuffer: 32 * 1024 * 1024,
      stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch (error) {
    const stderr = error.stderr ? String(error.stderr).trim() : '';
    fail(`gh ${args.join(' ')} failed:\n${stderr || error.message}`);
  }
}

function ghJson(args) {
  const output = gh(args);
  return output ? JSON.parse(output) : {};
}

function graphql(query, variables = {}) {
  const args = ['api', 'graphql', '-f', `query=${query}`];
  for (const [key, value] of Object.entries(variables)) {
    if (value !== null && value !== undefined) {
      args.push('-F', `${key}=${value}`);
    }
  }
  return ghJson(args);
}

function fetchBoardItems(projectId) {
  const items = [];
  let after = null;

  do {
    const response = graphql(ITEMS_QUERY, { id: projectId, after });
    const page = response.data?.node?.items;
    if (!page) {
      fail(`Could not load items for project node ${projectId}.`);
    }
    items.push(...page.nodes);
    after = page.pageInfo.hasNextPage ? page.pageInfo.endCursor : null;
  } while (after);

  return items;
}

function fieldValue(item, fieldName) {
  for (const value of item.fieldValues?.nodes ?? []) {
    if (value?.field?.name === fieldName) {
      return value.name ?? '';
    }
  }
  return '';
}

function normalizeStatus(status) {
  return status.trim().toLowerCase();
}

function classifyItems(rawItems) {
  const drafts = [];
  const items = [];

  for (const raw of rawItems) {
    const content = raw.content;
    if (!content || content.__typename === 'DraftIssue') {
      drafts.push({ title: content?.title ?? '(untitled draft)' });
      continue;
    }

    items.push({
      itemId: raw.id,
      type: content.__typename,
      number: content.number,
      title: content.title,
      state: content.state,
      url: content.url,
      updatedAt: content.updatedAt,
      repo: content.repository?.nameWithOwner ?? '',
      status: fieldValue(raw, 'Status'),
      priority: fieldValue(raw, 'Priority'),
      milestone: content.milestone ?? null,
      subIssues: content.subIssues?.nodes ?? [],
      closingPrs: content.closedByPullRequestsReferences?.nodes ?? [],
      merged: content.merged ?? false,
      mergedAt: content.mergedAt ?? null,
      isDraft: content.isDraft ?? false,
      reviewDecision: content.reviewDecision ?? '',
      checkState:
        content.commits?.nodes?.[0]?.commit?.statusCheckRollup?.state ?? '',
    });
  }

  return { drafts, items };
}

function issueIsShipped(item) {
  if (item.type === 'PullRequest') {
    return item.merged;
  }
  if (item.state === 'CLOSED') {
    return true;
  }
  return item.closingPrs.some((pr) => pr.merged);
}

function hasOpenPr(item) {
  return item.closingPrs.some((pr) => pr.state === 'OPEN');
}

function daysSince(isoDate, now) {
  if (!isoDate) {
    return Number.POSITIVE_INFINITY;
  }
  return (now - Date.parse(isoDate)) / (1000 * 60 * 60 * 24);
}

function extractClosedIssueRefs(body, repo) {
  const refs = new Set();
  if (!body) {
    return refs;
  }
  for (const match of body.matchAll(CLOSING_KEYWORD_PATTERN)) {
    const [, crossRepo, crossNumber, sameNumber] = match;
    if (crossRepo && crossNumber) {
      refs.add(`${crossRepo.toLowerCase()}#${crossNumber}`);
    } else if (sameNumber) {
      refs.add(`${repo.toLowerCase()}#${sameNumber}`);
    }
  }
  return refs;
}

function fetchRepoActivity(repo, windowDays) {
  const since = new Date(Date.now() - windowDays * 24 * 60 * 60 * 1000)
    .toISOString()
    .slice(0, 10);

  const mergedPrs = ghJson([
    'pr',
    'list',
    '--repo',
    repo,
    '--state',
    'merged',
    '--search',
    `merged:>=${since}`,
    '--limit',
    '100',
    '--json',
    'number,title,url,mergedAt,body',
  ]);

  const openIssues = ghJson([
    'issue',
    'list',
    '--repo',
    repo,
    '--state',
    'open',
    '--limit',
    '200',
    '--json',
    'number,title,url,createdAt',
  ]);

  const milestones = ghJson([
    'api',
    `repos/${repo}/milestones?state=open&per_page=100`,
  ]);

  return { repo, mergedPrs, openIssues, milestones };
}

function fetchMilestoneFocus(repo, milestoneTitle) {
  return ghJson([
    'issue',
    'list',
    '--repo',
    repo,
    '--milestone',
    milestoneTitle,
    '--state',
    'open',
    '--limit',
    '100',
    '--json',
    'number,title,url',
  ]);
}

function buildFindings(items, drafts, repoActivity, options) {
  const now = Date.now();
  const findings = {
    mergedNotDone: [],
    doneNotMerged: [],
    staleInProgress: [],
    reviewStarvation: [],
    untrackedWork: [],
    epicDrift: [],
    milestoneReadiness: [],
    priorityHygiene: [],
  };

  const boardIssueKeys = new Set();
  const boardPrKeys = new Set();
  for (const item of items) {
    const key = `${item.repo.toLowerCase()}#${item.number}`;
    if (item.type === 'Issue') {
      boardIssueKeys.add(key);
    } else {
      boardPrKeys.add(key);
    }
  }

  for (const item of items) {
    const status = normalizeStatus(item.status);
    const shipped = issueIsShipped(item);

    // Check 1 — merged/closed but the board still shows an unfinished lane.
    if (shipped && !DONE_STATUSES.has(status) && status !== 'deferred') {
      findings.mergedNotDone.push(item);
    }

    // Check 2 — Done on the board, but the work never actually landed.
    if (DONE_STATUSES.has(status) && !shipped) {
      findings.doneNotMerged.push(item);
    }

    // Check 3 — In Progress with no open PR and no movement in N days.
    if (
      IN_PROGRESS_STATUSES.has(status) &&
      !shipped &&
      !hasOpenPr(item) &&
      daysSince(item.updatedAt, now) >= options.stale
    ) {
      findings.staleInProgress.push({
        ...item,
        idleDays: Math.floor(daysSince(item.updatedAt, now)),
      });
    }

    // Check 4 — Human Review holding a PR that is already merged, or approved
    // with green checks (a human gate that has nothing left to gate).
    if (HUMAN_REVIEW_STATUSES.has(status)) {
      if (item.type === 'PullRequest' && item.merged) {
        findings.reviewStarvation.push({ ...item, reason: 'already merged' });
      } else if (
        item.type === 'PullRequest' &&
        item.reviewDecision === 'APPROVED' &&
        item.checkState === 'SUCCESS'
      ) {
        findings.reviewStarvation.push({
          ...item,
          reason: 'approved with green checks',
        });
      } else if (item.type === 'Issue' && shipped) {
        findings.reviewStarvation.push({
          ...item,
          reason: 'closing PR already merged',
        });
      }
    }

    // Check 6 — parent open while every child is closed.
    if (
      item.type === 'Issue' &&
      item.state === 'OPEN' &&
      item.subIssues.length > 0 &&
      item.subIssues.every((child) => child.state === 'CLOSED')
    ) {
      findings.epicDrift.push({ ...item, childCount: item.subIssues.length });
    }

    // Check 8 — active lanes with no Priority set.
    if (
      (IN_PROGRESS_STATUSES.has(status) || HUMAN_REVIEW_STATUSES.has(status)) &&
      !item.priority
    ) {
      findings.priorityHygiene.push(item);
    }
  }

  // Check 5 — merged PRs and open issues the board never tracked.
  for (const activity of repoActivity) {
    const repoKey = activity.repo.toLowerCase();

    for (const pr of activity.mergedPrs) {
      const prKey = `${repoKey}#${pr.number}`;
      if (boardPrKeys.has(prKey)) {
        continue;
      }
      const closedIssues = extractClosedIssueRefs(pr.body, activity.repo);
      const tracked = [...closedIssues].some((ref) => boardIssueKeys.has(ref));
      if (!tracked) {
        findings.untrackedWork.push({
          repo: activity.repo,
          kind: 'merged-pr',
          number: pr.number,
          title: pr.title,
          url: pr.url,
          mergedAt: pr.mergedAt,
        });
      }
    }

    for (const issue of activity.openIssues) {
      const issueKey = `${repoKey}#${issue.number}`;
      if (!boardIssueKeys.has(issueKey)) {
        findings.untrackedWork.push({
          repo: activity.repo,
          kind: 'open-issue',
          number: issue.number,
          title: issue.title,
          url: issue.url,
          createdAt: issue.createdAt,
        });
      }
    }

    // Check 7 — milestones due inside the sprint horizon, with readiness
    // counts and the open issues that make up the sprint's focus list.
    const horizonEnd = now + options.horizon * 24 * 60 * 60 * 1000;
    for (const milestone of activity.milestones) {
      if (!milestone.due_on) {
        continue;
      }
      const due = Date.parse(milestone.due_on);
      if (due <= horizonEnd) {
        findings.milestoneReadiness.push({
          repo: activity.repo,
          title: milestone.title,
          dueOn: milestone.due_on,
          openIssues: milestone.open_issues,
          closedIssues: milestone.closed_issues,
          overdue: due < now,
          focus: fetchMilestoneFocus(activity.repo, milestone.title),
        });
      }
    }
  }

  return { findings, draftCount: drafts.length };
}

function itemRef(item) {
  return `${item.repo}#${item.number}`;
}

function printSection(header, rows) {
  process.stdout.write(`\n${header}\n`);
  if (rows.length === 0) {
    process.stdout.write('  clean\n');
    return;
  }
  for (const row of rows) {
    process.stdout.write(`  ${row}\n`);
  }
}

function printReport(project, result, options) {
  const { findings, draftCount } = result;

  process.stdout.write(`Board sync report — ${project.title} (#${project.number})\n`);
  process.stdout.write(`${project.url}\n`);
  process.stdout.write(
    `window: ${options.window}d · stale threshold: ${options.stale}d · sprint horizon: ${options.horizon}d · drafts (not checked): ${draftCount}\n`
  );

  printSection(
    '1. Merged but not Done',
    findings.mergedNotDone.map(
      (item) => `${itemRef(item)} [${item.status || 'no status'}] ${item.title}`
    )
  );

  printSection(
    '2. Done but not merged (false green)',
    findings.doneNotMerged.map(
      (item) => `${itemRef(item)} [${item.state}] ${item.title}`
    )
  );

  printSection(
    `3. Stale In Progress (>= ${options.stale}d, no open PR)`,
    findings.staleInProgress.map(
      (item) => `${itemRef(item)} idle ${item.idleDays}d — ${item.title}`
    )
  );

  printSection(
    '4. Human Review starvation',
    findings.reviewStarvation.map(
      (item) => `${itemRef(item)} (${item.reason}) ${item.title}`
    )
  );

  printSection(
    `5. Untracked work (last ${options.window}d)`,
    findings.untrackedWork.map(
      (entry) =>
        `${entry.repo}#${entry.number} [${entry.kind}] ${entry.title}`
    )
  );

  printSection(
    '6. Epic/parent drift (parent open, all children closed)',
    findings.epicDrift.map(
      (item) => `${itemRef(item)} (${item.childCount} children) ${item.title}`
    )
  );

  printSection(
    `7. Sprint readiness — milestones due within ${options.horizon} days`,
    findings.milestoneReadiness.flatMap((m) => [
      `${m.repo} "${m.title}" due ${m.dueOn.slice(0, 10)}${m.overdue ? ' (OVERDUE)' : ''} — ${m.closedIssues}/${m.openIssues + m.closedIssues} closed`,
      ...m.focus.map((issue) => `  focus: #${issue.number} ${issue.title}`),
    ])
  );

  printSection(
    '8. Priority hygiene (active lanes without Priority)',
    findings.priorityHygiene.map(
      (item) => `${itemRef(item)} [${item.status}] ${item.title}`
    )
  );

  const driftCount =
    findings.mergedNotDone.length +
    findings.doneNotMerged.length +
    findings.staleInProgress.length +
    findings.reviewStarvation.length +
    findings.epicDrift.length +
    findings.priorityHygiene.length;

  process.stdout.write(
    `\nVerdict: ${
      driftCount === 0
        ? 'the board is trustworthy — no drift between board state and repo state.'
        : `${driftCount} drifted item(s) — the board does not currently reflect reality.`
    }\n`
  );
}

const args = parseArgs(process.argv.slice(2));

const summary = ghJson([
  'project',
  'view',
  String(args.project),
  '--owner',
  args.owner,
  '--format',
  'json',
]);

if (!summary.id) {
  fail(`Could not resolve project ${args.project} for owner ${args.owner}.`);
}

const rawItems = fetchBoardItems(summary.id);
const { drafts, items } = classifyItems(rawItems);

const repos = args.repo
  ? [args.repo]
  : [...new Set(items.map((item) => item.repo).filter(Boolean))];

const repoActivity = repos.map((repo) => fetchRepoActivity(repo, args.window));

const result = buildFindings(items, drafts, repoActivity, {
  horizon: args.horizon,
  stale: args.stale,
  window: args.window,
});

if (args.json) {
  process.stdout.write(
    `${JSON.stringify(
      {
        project: { title: summary.title, number: summary.number, url: summary.url },
        options: { window: args.window, stale: args.stale, horizon: args.horizon, repos },
        draftCount: result.draftCount,
        findings: result.findings,
      },
      null,
      2
    )}\n`
  );
} else {
  printReport(summary, result, args);
}
