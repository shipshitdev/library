#!/usr/bin/env node
/**
 * Generates marketplace.json with all bundles and individual skills
 */

import { existsSync, readdirSync, readFileSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const SKILLS_DIR = join(ROOT, 'skills');
const BUNDLES_DIR = join(ROOT, 'bundles');
const CATEGORIES = JSON.parse(readFileSync(join(__dirname, 'plugin-categories.json'), 'utf-8'));

// Get skill description from SKILL.md frontmatter
function getSkillDescription(skillName) {
  const skillPath = join(SKILLS_DIR, skillName, 'SKILL.md');
  if (!existsSync(skillPath)) return `${skillName} skill`;

  const content = readFileSync(skillPath, 'utf-8');
  const match = content.match(/^---\n[\s\S]*?description:\s*(.+?)\n[\s\S]*?---/);
  if (match) {
    return match[1].trim().replace(/^["']|["']$/g, '');
  }
  return `${skillName} skill`;
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

for (const skillName of skills) {
  const description = getSkillDescription(skillName);
  plugins.push({
    name: skillName,
    source: `./skills/${skillName}`,
    description: description.slice(0, 100), // Truncate long descriptions
  });
}

const marketplace = {
  name: 'shipshitdev',
  owner: {
    name: 'Ship Shit Dev',
  },
  description: '100+ AI agent skills for indie developers building startups',
  plugins,
};

const outputPath = join(ROOT, '.claude-plugin/marketplace.json');
writeFileSync(outputPath, JSON.stringify(marketplace, null, 2));

console.log(`Generated marketplace.json with ${plugins.length} plugins:`);
console.log(`  - ${Object.keys(CATEGORIES.bundles).length} category bundles`);
console.log(`  - ${skills.length} individual skills`);
