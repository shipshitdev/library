#!/usr/bin/env bun
/**
 * Generate bundled Claude Code plugin from bundle definition
 */

const fs = require('fs');
const path = require('path');
const { generateManifest } = require('./generate-manifest');

const LIBRARY_ROOT = path.resolve(__dirname, '..');
const BUNDLES_FILE = path.join(LIBRARY_ROOT, 'bundles.json');
const PLUGINS_DIR = path.join(LIBRARY_ROOT, 'plugins', 'bundles', '@agenticdev');

/**
 * Copy directory recursively
 */
function copyDir(src, dest) {
  if (!fs.existsSync(src)) {
    return;
  }
  
  fs.mkdirSync(dest, { recursive: true });
  
  const entries = fs.readdirSync(src, { withFileTypes: true });
  
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      // Skip certain directories
      if (entry.name === 'node_modules' || entry.name === '.git') {
        continue;
      }
      copyDir(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

/**
 * Load bundles configuration
 */
function loadBundles() {
  if (!fs.existsSync(BUNDLES_FILE)) {
    throw new Error(`Bundles file not found: ${BUNDLES_FILE}`);
  }
  
  const content = fs.readFileSync(BUNDLES_FILE, 'utf8');
  return JSON.parse(content);
}

/**
 * Generate bundle plugin
 */
function generateBundlePlugin(bundleId, platform = 'cursor') {
  const bundles = loadBundles();
  const bundle = bundles.bundles.find(b => b.id === bundleId);
  
  if (!bundle) {
    throw new Error(`Bundle not found: ${bundleId}`);
  }
  
  const pluginName = `bundle-${bundleId}`;
  const pluginDir = path.join(PLUGINS_DIR, pluginName);
  const pluginManifestDir = path.join(pluginDir, '.claude-plugin');
  const pluginSkillsDir = path.join(pluginDir, 'skills');
  const pluginCommandsDir = path.join(pluginDir, 'commands');
  
  // Create directories
  fs.mkdirSync(pluginManifestDir, { recursive: true });
  fs.mkdirSync(pluginSkillsDir, { recursive: true });
  fs.mkdirSync(pluginCommandsDir, { recursive: true });
  
  // Copy skills
  const skillsDir = path.join(LIBRARY_ROOT, 'skills');
  const includedSkills = [];
  
  if (bundle.skills && bundle.skills.length > 0) {
    for (const skillName of bundle.skills) {
      const skillPath = path.join(skillsDir, skillName);
      
      if (!fs.existsSync(skillPath)) {
        console.warn(`⚠️  Skill not found: ${skillName} (skipping)`);
        continue;
      }
      
      const destSkillDir = path.join(pluginSkillsDir, skillName);
      copyDir(skillPath, destSkillDir);
      includedSkills.push(skillName);
    }
  }
  
  // Copy commands
  const commandsDir = path.join(LIBRARY_ROOT, 'commands');
  const includedCommands = [];
  
  if (bundle.commands && bundle.commands.length > 0) {
    for (const commandName of bundle.commands) {
      const commandPath = path.join(commandsDir, `${commandName}.md`);
      
      if (!fs.existsSync(commandPath)) {
        console.warn(`⚠️  Command not found: ${commandName} (skipping)`);
        continue;
      }
      
      fs.copyFileSync(commandPath, path.join(pluginCommandsDir, `${commandName}.md`));
      includedCommands.push(commandName);
    }
  }
  
  // Generate manifest
  const manifest = generateManifest({
    name: `@agenticdev/bundle-${bundleId}`,
    description: bundle.description || bundle.name,
    version: bundle.version || '1.0.0',
    tags: bundle.tags || [],
    homepage: `https://skillhub.com/bundles/${bundleId}`,
    author: {
      name: 'Ship Shit Dev'
    }
  });
  
  // Add bundle metadata
  manifest.bundle = {
    id: bundle.id,
    name: bundle.name,
    category: bundle.category,
    includedSkills: includedSkills,
    includedCommands: includedCommands,
    icon: bundle.icon
  };
  
  // Write manifest
  fs.writeFileSync(
    path.join(pluginManifestDir, 'plugin.json'),
    JSON.stringify(manifest, null, 2) + '\n'
  );
  
  // Create README for bundle
  const readme = `# ${bundle.name}

${bundle.description}

## Included Items

### Skills (${includedSkills.length})
${includedSkills.map(skill => `- ${skill}`).join('\n')}

### Commands (${includedCommands.length})
${includedCommands.map(cmd => `- ${cmd}`).join('\n')}

## Installation

\`\`\`bash
claude --plugin-dir ./${pluginName}
\`\`\`

Or install via marketplace:
\`\`\`bash
/plugin install @agenticdev/bundle-${bundleId}
\`\`\`
`;
  
  fs.writeFileSync(path.join(pluginDir, 'README.md'), readme);
  
  console.log(`✅ Generated bundle plugin: ${pluginName}`);
  console.log(`   Location: ${pluginDir}`);
  console.log(`   Skills: ${includedSkills.length}`);
  console.log(`   Commands: ${includedCommands.length}`);
  
  return pluginDir;
}

/**
 * Generate all bundles
 */
function generateAllBundles(platform = 'cursor') {
  const bundles = loadBundles();
  
  console.log(`Generating ${bundles.bundles.length} bundles for ${platform}...\n`);
  
  const results = [];
  
  for (const bundle of bundles.bundles) {
    try {
      generateBundlePlugin(bundle.id, platform);
      results.push({ bundle: bundle.id, status: 'success' });
    } catch (error) {
      console.error(`❌ Failed to generate bundle ${bundle.id}:`, error.message);
      results.push({ bundle: bundle.id, status: 'error', error: error.message });
    }
  }
  
  console.log(`\n✅ Generated ${results.filter(r => r.status === 'success').length}/${bundles.bundles.length} bundles`);
  
  return results;
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Usage:');
    console.log('  generate-bundle.js <bundle-id> [platform]');
    console.log('  generate-bundle.js all [platform]');
    console.log('');
    console.log('Examples:');
    console.log('  generate-bundle.js testing-suite cursor');
    console.log('  generate-bundle.js all cursor');
    console.log('');
    console.log('Available bundles:');
    const bundles = loadBundles();
    bundles.bundles.forEach(b => {
      console.log(`  - ${b.id}: ${b.name}`);
    });
    process.exit(1);
  }
  
  const [bundleId, platform = 'cursor'] = args;
  
  try {
    if (bundleId === 'all') {
      generateAllBundles(platform);
    } else {
      generateBundlePlugin(bundleId, platform);
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

module.exports = {
  generateBundlePlugin,
  generateAllBundles,
  loadBundles
};

