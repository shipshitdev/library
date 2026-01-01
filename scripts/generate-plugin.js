#!/usr/bin/env bun
/**
 * Generate Claude Code plugin from library skill or command
 */

const fs = require('fs');
const path = require('path');
const { generateFromSkill, generateFromCommand } = require('./generate-manifest');

const LIBRARY_ROOT = path.resolve(__dirname, '..');
const PLUGINS_DIR = path.join(LIBRARY_ROOT, 'plugins', 'individual', '@agenticdev');

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
 * Generate plugin from skill
 */
function generateSkillPlugin(skillName, platform = 'cursor') {
  const skillPath = path.join(LIBRARY_ROOT, 'agents', `.${platform}`, 'skills', skillName);
  
  if (!fs.existsSync(skillPath)) {
    throw new Error(`Skill not found: ${skillPath}`);
  }
  
  const pluginName = `skill-${skillName}`;
  const pluginDir = path.join(PLUGINS_DIR, pluginName);
  const pluginManifestDir = path.join(pluginDir, '.claude-plugin');
  const pluginSkillsDir = path.join(pluginDir, 'skills', skillName);
  
  // Create directories
  fs.mkdirSync(pluginManifestDir, { recursive: true });
  fs.mkdirSync(pluginSkillsDir, { recursive: true });
  
  // Generate manifest
  const manifest = generateFromSkill(skillPath, platform, {
    homepage: `https://skillhub.com/plugins/${skillName}`
  });
  
  // Write manifest
  fs.writeFileSync(
    path.join(pluginManifestDir, 'plugin.json'),
    JSON.stringify(manifest, null, 2) + '\n'
  );
  
  // Copy skill directory contents
  copyDir(skillPath, pluginSkillsDir);
  
  console.log(`✅ Generated plugin: ${pluginName}`);
  console.log(`   Location: ${pluginDir}`);
  console.log(`   Manifest: ${path.join(pluginManifestDir, 'plugin.json')}`);
  
  return pluginDir;
}

/**
 * Generate plugin from command
 */
function generateCommandPlugin(commandName, platform = 'cursor') {
  const commandPath = path.join(LIBRARY_ROOT, 'agents', `.${platform}`, 'commands', `${commandName}.md`);
  
  if (!fs.existsSync(commandPath)) {
    throw new Error(`Command not found: ${commandPath}`);
  }
  
  const pluginName = `command-${commandName}`;
  const pluginDir = path.join(PLUGINS_DIR, pluginName);
  const pluginManifestDir = path.join(pluginDir, '.claude-plugin');
  const pluginCommandsDir = path.join(pluginDir, 'commands');
  
  // Create directories
  fs.mkdirSync(pluginManifestDir, { recursive: true });
  fs.mkdirSync(pluginCommandsDir, { recursive: true });
  
  // Generate manifest
  const manifest = generateFromCommand(commandPath, platform, {
    homepage: `https://skillhub.com/plugins/${commandName}`
  });
  
  // Write manifest
  fs.writeFileSync(
    path.join(pluginManifestDir, 'plugin.json'),
    JSON.stringify(manifest, null, 2) + '\n'
  );
  
  // Copy command file
  fs.copyFileSync(commandPath, path.join(pluginCommandsDir, `${commandName}.md`));
  
  console.log(`✅ Generated plugin: ${pluginName}`);
  console.log(`   Location: ${pluginDir}`);
  console.log(`   Manifest: ${path.join(pluginManifestDir, 'plugin.json')}`);
  
  return pluginDir;
}

/**
 * Generate all plugins for a platform
 */
function generateAllPlugins(platform = 'cursor') {
  const skillsDir = path.join(LIBRARY_ROOT, 'agents', `.${platform}`, 'skills');
  const commandsDir = path.join(LIBRARY_ROOT, 'agents', `.${platform}`, 'commands');
  
  const plugins = [];
  
  // Generate skill plugins
  if (fs.existsSync(skillsDir)) {
    const skills = fs.readdirSync(skillsDir, { withFileTypes: true })
      .filter(entry => entry.isDirectory())
      .map(entry => entry.name);
    
    for (const skill of skills) {
      try {
        generateSkillPlugin(skill, platform);
        plugins.push({ type: 'skill', name: skill, platform });
      } catch (error) {
        console.error(`❌ Failed to generate plugin for skill ${skill}:`, error.message);
      }
    }
  }
  
  // Generate command plugins
  if (fs.existsSync(commandsDir)) {
    const commands = fs.readdirSync(commandsDir)
      .filter(file => file.endsWith('.md'))
      .map(file => file.replace('.md', ''));
    
    for (const command of commands) {
      try {
        generateCommandPlugin(command, platform);
        plugins.push({ type: 'command', name: command, platform });
      } catch (error) {
        console.error(`❌ Failed to generate plugin for command ${command}:`, error.message);
      }
    }
  }
  
  console.log(`\n✅ Generated ${plugins.length} plugins for ${platform}`);
  return plugins;
}

// CLI usage
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Usage:');
    console.log('  generate-plugin.js skill <skill-name> [platform]');
    console.log('  generate-plugin.js command <command-name> [platform]');
    console.log('  generate-plugin.js all [platform]');
    console.log('');
    console.log('Examples:');
    console.log('  generate-plugin.js skill accessibility cursor');
    console.log('  generate-plugin.js command code-review cursor');
    console.log('  generate-plugin.js all cursor');
    process.exit(1);
  }
  
  const [action, name, platform = 'cursor'] = args;
  
  try {
    if (action === 'skill') {
      if (!name) {
        throw new Error('Skill name required');
      }
      generateSkillPlugin(name, platform);
    } else if (action === 'command') {
      if (!name) {
        throw new Error('Command name required');
      }
      generateCommandPlugin(name, platform);
    } else if (action === 'all') {
      generateAllPlugins(platform);
    } else {
      throw new Error(`Unknown action: ${action}`);
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

module.exports = {
  generateSkillPlugin,
  generateCommandPlugin,
  generateAllPlugins
};

