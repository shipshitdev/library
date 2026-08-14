#!/usr/bin/env node

import { execFileSync } from 'node:child_process';
import { existsSync, lstatSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const ROOT = join(SCRIPT_DIR, '..');
const CHECK = process.argv.includes('--check');
const PRINT = process.argv.includes('--print');

const ROLE_BY_DIRECTORY = {
  '.agents': 'Repository memory, standards, and maintenance skills',
  '.claude': 'Claude loader adapters for shared maintenance content',
  '.claude-plugin': 'Generated Claude marketplace catalog',
  '.codex': 'Codex loader adapters for shared maintenance content',
  '.github': 'Issue templates and GitHub Actions workflows',
  '.husky': 'Git hook configuration',
  assets: 'Static repository assets',
  bundles: 'Generated marketplace bundle snapshots',
  commands: 'Claude Code/plugin command adapters',
  docs: 'Human-facing orientation pages for flagship skills',
  prompts: 'Shared prompt resources',
  resources: 'Authoring references and supporting documentation',
  scripts: 'Validation, generation, migration, and audit tooling',
  skills: 'Canonical public Agent Skills sources',
};

const BLOCKS = {
  readmeSummary: ['README.md', 'catalog-summary'],
  readmeLayout: ['README.md', 'catalog-layout'],
  readmeSkillsHeading: ['README.md', 'catalog-skills-heading'],
  agentsSummary: ['AGENTS.md', 'catalog-summary'],
  memorySummary: ['.agents/memory/memory.md', 'catalog-summary'],
  memoryCounts: ['.agents/memory/memory.md', 'catalog-counts'],
  architectureLayout: ['.agents/memory/architecture.md', 'catalog-layout'],
  architectureBundles: ['.agents/memory/architecture.md', 'catalog-bundles'],
};

const staleFiles = [];

function readJson(path) {
  return JSON.parse(readFileSync(path, 'utf8'));
}

function countSkills() {
  const root = join(ROOT, 'skills');
  return readdirSync(root, { withFileTypes: true }).filter(
    (entry) => entry.isDirectory() && existsSync(join(root, entry.name, 'SKILL.md'))
  ).length;
}

function countCommands() {
  return readdirSync(join(ROOT, 'commands'), { withFileTypes: true }).filter(
    (entry) => entry.isFile() && entry.name.endsWith('.md')
  ).length;
}

function trackedTopLevelDirectories() {
  let paths = [];
  try {
    paths = execFileSync('git', ['ls-files', '-z'], {
      cwd: ROOT,
      encoding: 'utf8',
    })
      .split('\0')
      .filter(Boolean);
  } catch {
    paths = readdirSync(ROOT)
      .filter((name) => {
        const path = join(ROOT, name);
        return lstatSync(path).isDirectory() || lstatSync(path).isSymbolicLink();
      })
      .map((name) => `${name}/`);
  }

  return [...new Set(paths.filter((path) => path.includes('/')).map((path) => path.split('/')[0]))]
    .sort()
    .map((name) => ({
      path: `${name}/`,
      role: ROLE_BY_DIRECTORY[name] ?? 'Tracked repository content',
    }));
}

function buildCatalog() {
  const categories = readJson(join(SCRIPT_DIR, 'plugin-categories.json'));
  const bundles = Object.keys(categories.bundles).sort();
  const skills = countSkills();
  const commands = countCommands();
  return {
    generated: true,
    sources: {
      skills: 'skills/*/SKILL.md',
      commands: 'commands/*.md',
      bundles: 'scripts/plugin-categories.json',
      layout: 'git ls-files',
    },
    counts: {
      skills,
      commands,
      bundles: bundles.length,
      plugins: skills + bundles.length,
    },
    bundles,
    layout: trackedTopLevelDirectories(),
  };
}

function expectedBlock(text, marker, content) {
  const start = `<!-- ${marker}:start -->`;
  const end = `<!-- ${marker}:end -->`;
  const startIndex = text.indexOf(start);
  const endIndex = text.indexOf(end);
  if (startIndex === -1 || endIndex === -1 || endIndex < startIndex) {
    throw new Error(`Missing generated block ${marker}`);
  }
  const afterEnd = endIndex + end.length;
  return `${text.slice(0, startIndex)}${start}\n${content.trim()}\n${end}${text.slice(afterEnd)}`;
}

function updateBlock(relativePath, marker, content) {
  const path = join(ROOT, relativePath);
  const current = readFileSync(path, 'utf8');
  const expected = expectedBlock(current, marker, content);
  if (current === expected) return;
  if (CHECK) {
    staleFiles.push(`${relativePath} (${marker})`);
  } else {
    writeFileSync(path, expected);
  }
}

function writeGeneratedFile(relativePath, content) {
  const path = join(ROOT, relativePath);
  const current = existsSync(path) ? readFileSync(path, 'utf8') : '';
  if (current === content) return;
  if (CHECK) {
    staleFiles.push(relativePath);
  } else {
    writeFileSync(path, content);
  }
}

function layoutTable(catalog) {
  const countByPath = {
    '.claude-plugin/': `${catalog.counts.plugins} generated plugins`,
    'bundles/': `${catalog.counts.bundles} generated bundles`,
    'commands/': `${catalog.counts.commands} command adapters`,
    'skills/': `${catalog.counts.skills} canonical skills`,
  };
  const rows = catalog.layout.map(
    (entry) => `| \`${entry.path}\` | ${entry.role} | ${countByPath[entry.path] ?? 'Tracked'} |`
  );
  return ['| Path | Role | Generated fact |', '|---|---|---|', ...rows].join('\n');
}

function updatePackageDescription(catalog) {
  const path = join(ROOT, 'package.json');
  const packageJson = readJson(path);
  packageJson.description = `${catalog.counts.skills} AI agent skills for development workflows. Works with Claude Code, OpenAI Codex, and Cursor.`;
  const expected = `${JSON.stringify(packageJson, null, 2)}\n`;
  const current = readFileSync(path, 'utf8');
  if (current === expected) return;
  if (CHECK) {
    staleFiles.push('package.json (description)');
  } else {
    writeFileSync(path, expected);
  }
}

function updateDocuments(catalog) {
  const counts = catalog.counts;
  updateBlock(
    ...BLOCKS.readmeSummary,
    `${counts.skills} AI agent skills for development workflows. Works with Claude Code, OpenAI Codex, and Cursor.\n\nCatalog: **${counts.skills} skills · ${counts.commands} commands · ${counts.bundles} bundles · ${counts.plugins} plugins**.`
  );
  updateBlock(...BLOCKS.readmeLayout, layoutTable(catalog));
  updateBlock(...BLOCKS.readmeSkillsHeading, `## Skills (${counts.skills})`);
  updateBlock(
    ...BLOCKS.agentsSummary,
    `This is the shipshitdev/skills repo: ${counts.skills} AI agent skills for Claude Code, Codex, and Cursor. The generated catalog also contains ${counts.commands} command adapters, ${counts.bundles} bundles, and ${counts.plugins} marketplace plugins.`
  );
  updateBlock(
    ...BLOCKS.memorySummary,
    `Public skills library at \`shipshitdev/skills\`. Installable via \`npx skills add shipshitdev/skills --skill <name>\`. Works with Claude Code, Codex, Cursor, OpenClaw, and Gemini.\n\nGenerated catalog: **${counts.skills} skills · ${counts.commands} commands · ${counts.bundles} bundles · ${counts.plugins} plugins**.`
  );
  updateBlock(
    ...BLOCKS.memoryCounts,
    [
      '| Asset | Count | Canonical source |',
      '|---|---:|---|',
      `| Skills | ${counts.skills} | \`skills/*/SKILL.md\` |`,
      `| Commands | ${counts.commands} | \`commands/*.md\` |`,
      `| Bundles | ${counts.bundles} | \`scripts/plugin-categories.json\` |`,
      `| Plugins | ${counts.plugins} | skills + bundles |`,
    ].join('\n')
  );
  updateBlock(...BLOCKS.architectureLayout, layoutTable(catalog));
  updateBlock(
    ...BLOCKS.architectureBundles,
    `${counts.bundles} generated bundles: ${catalog.bundles.map((name) => `\`${name}\``).join(', ')}.`
  );
}

const catalog = buildCatalog();
const catalogJson = `${JSON.stringify(catalog, null, 2)}\n`;
writeGeneratedFile('catalog.json', catalogJson);
updateDocuments(catalog);
updatePackageDescription(catalog);

if (PRINT) {
  console.log(
    `Skills: ${catalog.counts.skills}\nCommands: ${catalog.counts.commands}\nBundles: ${catalog.counts.bundles}\nPlugins: ${catalog.counts.plugins}`
  );
}

if (CHECK && staleFiles.length > 0) {
  console.error('Generated catalog facts are stale:');
  for (const file of staleFiles) console.error(`  - ${file}`);
  process.exit(1);
}

if (!PRINT) {
  console.log(
    CHECK
      ? 'Generated catalog facts are current.'
      : `Generated catalog facts: ${catalog.counts.skills} skills, ${catalog.counts.commands} commands, ${catalog.counts.bundles} bundles, ${catalog.counts.plugins} plugins.`
  );
}
