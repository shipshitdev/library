#!/usr/bin/env node

import { execFileSync } from 'node:child_process';

const JSON_FIELDS = [
  'assignees',
  'author',
  'commentsCount',
  'createdAt',
  'isDraft',
  'labels',
  'number',
  'repository',
  'state',
  'title',
  'updatedAt',
  'url',
].join(',');

function parseArgs(argv) {
  const args = {
    limit: 20,
    owner: '',
    project: '',
    repo: '',
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--limit') {
      args.limit = Number.parseInt(readValue(argv, (index += 1), arg), 10);
    } else if (arg === '--owner') {
      args.owner = readValue(argv, (index += 1), arg);
    } else if (arg === '--project') {
      args.project = readValue(argv, (index += 1), arg);
    } else if (arg === '--repo') {
      args.repo = readValue(argv, (index += 1), arg);
    } else if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    } else {
      fail(`Unknown argument: ${arg}`);
    }
  }

  if (!Number.isInteger(args.limit) || args.limit <= 0) {
    fail('--limit must be a positive integer.');
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
  node github-inbox-report.mjs [--repo owner/name] [--owner owner] [--project owner/number] [--limit 20]

Report mode is read-only.
`);
}

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function gh(args, allowFailure = false) {
  try {
    return execFileSync('gh', args, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
    }).trim();
  } catch (error) {
    if (allowFailure) {
      return '';
    }
    const stderr = error.stderr ? String(error.stderr).trim() : '';
    fail(`gh ${args.join(' ')} failed:\n${stderr || error.message}`);
  }
}

function ghJson(args, allowFailure = false) {
  const output = gh(args, allowFailure);
  return output ? JSON.parse(output) : [];
}

function scopeArgs(args) {
  const scoped = [];
  if (args.repo) {
    scoped.push('--repo', args.repo);
  }
  if (args.owner) {
    scoped.push('--owner', args.owner);
  }
  if (args.project) {
    scoped.push('--project', args.project);
  }
  return scoped;
}

function searchIssues(args, bucket, extraArgs = []) {
  return ghJson(
    [
      'search',
      'issues',
      '--state',
      'open',
      '--json',
      JSON_FIELDS,
      '--limit',
      String(args.limit),
      ...scopeArgs(args),
      ...extraArgs,
    ],
    true
  ).map((item) => ({ ...item, bucket }));
}

function searchPrs(args, bucket, extraArgs = []) {
  return ghJson(
    [
      'search',
      'prs',
      '--state',
      'open',
      '--json',
      JSON_FIELDS,
      '--limit',
      String(args.limit),
      ...scopeArgs(args),
      ...extraArgs,
    ],
    true
  ).map((item) => ({ ...item, bucket }));
}

function repoName(item) {
  if (typeof item.repository === 'string') {
    return item.repository;
  }
  return item.repository?.fullName ?? item.repository?.nameWithOwner ?? item.repository?.name ?? '';
}

function labelNames(item) {
  return (item.labels ?? []).map((label) => label.name ?? label).filter(Boolean);
}

function priorityScore(item) {
  const labels = labelNames(item).join(' ').toLowerCase();
  if (item.bucket === 'Review requested') return 0;
  if (item.bucket === 'Failing authored PR') return 1;
  if (labels.includes('p0') || labels.includes('critical') || labels.includes('blocking')) return 2;
  if (labels.includes('p1') || labels.includes('high')) return 3;
  if (item.bucket === 'Assigned issue') return 4;
  if (item.bucket === 'Mention') return 5;
  if (item.bucket === 'Project item') return 6;
  return 10;
}

function mergeItems(items) {
  const byUrl = new Map();
  for (const item of items) {
    const existing = byUrl.get(item.url);
    if (!existing) {
      byUrl.set(item.url, { ...item, buckets: [item.bucket] });
    } else if (!existing.buckets.includes(item.bucket)) {
      existing.buckets.push(item.bucket);
    }
  }
  return [...byUrl.values()].sort((a, b) => {
    const scoreDelta = priorityScore(a) - priorityScore(b);
    if (scoreDelta !== 0) return scoreDelta;
    return String(b.updatedAt).localeCompare(String(a.updatedAt));
  });
}

function printItems(title, items) {
  process.stdout.write(`\n## ${title} (${items.length})\n`);
  if (items.length === 0) {
    process.stdout.write('No matching items.\n');
    return;
  }

  for (const item of items) {
    const labels = labelNames(item);
    const labelText = labels.length > 0 ? ` [${labels.join(', ')}]` : '';
    const repo = repoName(item);
    const buckets = item.buckets?.join(', ') ?? item.bucket;
    process.stdout.write(`- ${buckets}: ${repo}#${item.number} ${item.title}${labelText}\n`);
    process.stdout.write(`  ${item.url}\n`);
  }
}

const args = parseArgs(process.argv.slice(2));
const user = gh(['api', 'user', '--jq', '.login']);
const items = mergeItems([
  ...searchPrs(args, 'Review requested', ['--review-requested', '@me']),
  ...searchPrs(args, 'Failing authored PR', ['--author', '@me', '--checks', 'failure']),
  ...searchIssues(args, 'Assigned issue', ['--assignee', '@me']),
  ...searchIssues(args, 'Mention', ['--mentions', user, '--include-prs']),
  ...(args.project ? searchIssues(args, 'Project item', ['--include-prs']) : []),
]);

process.stdout.write(`# GitHub Inbox for ${user}\n`);
const scope = [args.repo && `repo ${args.repo}`, args.owner && `owner ${args.owner}`, args.project && `project ${args.project}`]
  .filter(Boolean)
  .join(', ');
process.stdout.write(`Scope: ${scope || 'all accessible repositories'}\n`);
printItems('Priority Queue', items.slice(0, args.limit));
