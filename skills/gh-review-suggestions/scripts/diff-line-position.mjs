#!/usr/bin/env node

import { readFileSync } from 'node:fs';

function parseArgs(argv) {
  const args = {
    diff: '',
    line: 0,
    path: '',
    side: 'RIGHT',
  };

  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--diff') {
      args.diff = readValue(argv, (index += 1), arg);
    } else if (arg === '--line') {
      args.line = Number.parseInt(readValue(argv, (index += 1), arg), 10);
    } else if (arg === '--path') {
      args.path = readValue(argv, (index += 1), arg);
    } else if (arg === '--side') {
      args.side = readValue(argv, (index += 1), arg).toUpperCase();
    } else if (arg === '--help' || arg === '-h') {
      printHelp();
      process.exit(0);
    } else {
      fail(`Unknown argument: ${arg}`);
    }
  }

  if (!args.path) {
    fail('Missing required --path <file>.');
  }
  if (!Number.isInteger(args.line) || args.line <= 0) {
    fail('Missing required --line <positive-number>.');
  }
  if (args.side !== 'RIGHT' && args.side !== 'LEFT') {
    fail('--side must be RIGHT or LEFT.');
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
  node diff-line-position.mjs --diff /tmp/pr.diff --path src/file.ts --line 42 [--side RIGHT]

If --diff is omitted, reads the diff from stdin.
Outputs JSON with path, line, side, and deprecated diff position.
`);
}

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function readDiff(path) {
  if (path) {
    return readFileSync(path, 'utf8');
  }
  return readFileSync(0, 'utf8');
}

function normalizePath(path) {
  return path.replace(/^["']|["']$/g, '').replace(/^[ab]\//, '');
}

function parseHunkHeader(line) {
  const match = line.match(/^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@/);
  if (!match) {
    return null;
  }
  return {
    oldLine: Number.parseInt(match[1], 10),
    newLine: Number.parseInt(match[2], 10),
  };
}

function findPosition(diff, targetPath, targetLine, targetSide) {
  let currentPath = '';
  let oldLine = 0;
  let newLine = 0;
  let position = 0;
  let inTargetFile = false;
  let inHunk = false;

  for (const rawLine of diff.split(/\r?\n/)) {
    if (rawLine.startsWith('diff --git ')) {
      currentPath = '';
      inTargetFile = false;
      inHunk = false;
      position = 0;
      continue;
    }

    if (rawLine.startsWith('+++ ')) {
      const filePath = normalizePath(rawLine.slice(4).trim());
      if (filePath !== '/dev/null') {
        currentPath = filePath;
        inTargetFile = currentPath === targetPath;
      }
      continue;
    }

    const hunk = parseHunkHeader(rawLine);
    if (hunk) {
      oldLine = hunk.oldLine;
      newLine = hunk.newLine;
      inHunk = inTargetFile;
      continue;
    }

    if (!inHunk) {
      continue;
    }

    const marker = rawLine[0] ?? '';
    if (marker !== '\\') {
      position += 1;
    }

    if (marker === '+') {
      if (targetSide === 'RIGHT' && newLine === targetLine) {
        return position;
      }
      newLine += 1;
    } else if (marker === '-') {
      if (targetSide === 'LEFT' && oldLine === targetLine) {
        return position;
      }
      oldLine += 1;
    } else {
      if (targetSide === 'RIGHT' && newLine === targetLine) {
        return position;
      }
      if (targetSide === 'LEFT' && oldLine === targetLine) {
        return position;
      }
      oldLine += 1;
      newLine += 1;
    }
  }

  return null;
}

const args = parseArgs(process.argv.slice(2));
const diff = readDiff(args.diff);
const normalizedPath = normalizePath(args.path);
const position = findPosition(diff, normalizedPath, args.line, args.side);

if (position === null) {
  fail(`Line ${args.line} on ${args.side} side of ${normalizedPath} was not found in the diff.`);
}

process.stdout.write(
  `${JSON.stringify({
    path: normalizedPath,
    line: args.line,
    side: args.side,
    position,
  })}\n`
);
