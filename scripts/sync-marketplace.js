#!/usr/bin/env bun
/**
 * Sync library plugins to marketplace
 * Generates all plugins and bundles, then updates marketplace data
 */

const { generateAllPlugins } = require('./generate-plugin');
const { generateAllBundles } = require('./generate-bundle');
const fs = require('fs');
const path = require('path');

const LIBRARY_ROOT = path.resolve(__dirname, '..');
const MARKETPLACE_ROOT = process.env.MARKETPLACE_ROOT || path.join(LIBRARY_ROOT, '..', 'tools', 'skillhubcom');

async function syncMarketplace() {
  console.log('🔄 Syncing library to marketplace...\n');

  // Step 1: Generate all plugins
  console.log('📦 Generating individual plugins...');
  try {
    await generateAllPlugins('cursor');
    console.log('✅ Individual plugins generated\n');
  } catch (error) {
    console.error('❌ Error generating plugins:', error.message);
    process.exit(1);
  }

  // Step 2: Generate all bundles
  console.log('📦 Generating bundle plugins...');
  try {
    await generateAllBundles('cursor');
    console.log('✅ Bundle plugins generated\n');
  } catch (error) {
    console.error('❌ Error generating bundles:', error.message);
    process.exit(1);
  }

  // Step 3: Clear marketplace cache (if it exists)
  console.log('🧹 Clearing marketplace cache...');
  try {
    const pluginServicePath = path.join(MARKETPLACE_ROOT, 'lib', 'plugin-service.ts');
    if (fs.existsSync(pluginServicePath)) {
      // The marketplace reads directly from library, so no cache to clear
      // But we could trigger a rebuild if needed
      console.log('✅ Marketplace will refresh on next request\n');
    }
  } catch (error) {
    console.warn('⚠️  Could not clear marketplace cache:', error.message);
  }

  console.log('✅ Sync complete!');
  console.log('\nNext steps:');
  console.log('1. Review generated plugins in library/plugins/');
  console.log('2. Marketplace will auto-discover plugins on next request');
  console.log('3. Test installation: claude --plugin-dir <plugin-path>');
}

// CLI usage
if (require.main === module) {
  syncMarketplace().catch((error) => {
    console.error('Fatal error:', error);
    process.exit(1);
  });
}

module.exports = { syncMarketplace };

