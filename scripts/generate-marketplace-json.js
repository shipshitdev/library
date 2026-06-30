#!/usr/bin/env node
/**
 * Generates marketplace.json with all bundles and individual skills
 */

import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const SKILLS_DIR = join(ROOT, 'skills');
const CATEGORIES = JSON.parse(readFileSync(join(__dirname, 'plugin-categories.json'), 'utf-8'));

// Get skill description from SKILL.md frontmatter.
// Handles plain/quoted single-line values AND YAML block scalars
// (folded `>`/`>-` and literal `|`/`|-`), which the previous single-line
// regex captured as the literal indicator (e.g. ">-") instead of the text.
function getSkillDescription(skillName) {
  const skillPath = join(SKILLS_DIR, skillName, 'SKILL.md');
  if (!existsSync(skillPath)) return null;

  const content = readFileSync(skillPath, 'utf-8');
  const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
  if (!fmMatch) return null;

  const lines = fmMatch[1].split('\n');
  const idx = lines.findIndex((l) => /^description:\s*/.test(l));
  if (idx === -1) return null;

  const keyIndent = lines[idx].match(/^(\s*)/)[1].length;
  let value = lines[idx].replace(/^description:\s*/, '');
  const blockMatch = value.match(/^([>|])[+-]?\s*$/);

  if (blockMatch) {
    const folded = blockMatch[1] === '>';
    const parts = [];
    for (let i = idx + 1; i < lines.length; i += 1) {
      const line = lines[i];
      if (line.trim() === '') {
        parts.push('');
        continue;
      }
      const indent = line.match(/^(\s*)/)[1].length;
      if (indent <= keyIndent) break; // dedent → next frontmatter key
      parts.push(line.trim());
    }
    while (parts.length && parts[parts.length - 1] === '') parts.pop();
    value = folded ? parts.join(' ') : parts.join('\n');
  } else {
    value = value.replace(/^["']|["']$/g, '');
  }

  return value.trim() || null;
}

const plugins = [];

// 1. Add category bundles
for (const [category, config] of Object.entries(CATEGORIES.bundles)) {
  plugins.push({
    name: `shipshitdev-${category}`,
    source: `./bundles/${category}`,
    description: config.description,
  });
}

// 3. Add individual skills
const skills = readdirSync(SKILLS_DIR, { withFileTypes: true })
  .filter((d) => d.isDirectory())
  .map((d) => d.name)
  .sort();

let includedSkillCount = 0;

for (const skillName of skills) {
  const description = getSkillDescription(skillName);
  if (!description) {
    console.warn(`Skipping invalid skill directory without SKILL.md: ${skillName}`);
    continue;
  }
  plugins.push({
    name: skillName,
    source: `./skills/${skillName}`,
    // Mirror the full SKILL.md description so the "Use when …" trigger clause
    // is discoverable in the catalog. The source frontmatter is already length-
    // capped (1024/1536); the previous slice(0, 100) cut clauses off mid-word.
    // Collapse whitespace so literal (`|`) block scalars render as a single-line
    // blurb instead of leaking embedded newlines into the catalog card.
    description: description.replace(/\s+/g, ' ').trim(),
  });
  includedSkillCount += 1;
}

const marketplace = {
  name: 'shipshitdev',
  owner: {
    name: 'Ship Shit Dev',
  },
  description: `${includedSkillCount} AI agent skills for development workflows`,
  plugins,
};

const outputDir = join(ROOT, '.claude-plugin');
if (!existsSync(outputDir)) {
  mkdirSync(outputDir, { recursive: true });
}
const outputPath = join(outputDir, 'marketplace.json');
writeFileSync(outputPath, `${JSON.stringify(marketplace, null, 2)}\n`);

console.log(`Generated marketplace.json with ${plugins.length} plugins:`);
console.log(`  - ${Object.keys(CATEGORIES.bundles).length} category bundles`);
console.log(`  - ${includedSkillCount} individual skills`);
