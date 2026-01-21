/**
 * Standard webpack config for Sass with @shipshitdev/ui support
 * Use this in all Next.js apps to configure sass-loader properly
 */

const path = require('path');

/**
 * Configure webpack for Sass with proper deprecation handling
 */
function configureWebpackSass(config, projectRoot) {
  const rules = config.module.rules;
  const scssRule = rules.find(
    (rule) =>
      rule &&
      typeof rule === 'object' &&
      rule !== null &&
      'test' in rule &&
      rule.test &&
      typeof rule.test === 'object' &&
      'toString' in rule.test &&
      rule.test.toString().includes('scss')
  );

  if (
    scssRule &&
    typeof scssRule === 'object' &&
    scssRule !== null &&
    'oneOf' in scssRule &&
    Array.isArray(scssRule.oneOf)
  ) {
    scssRule.oneOf.forEach((oneOf) => {
      if (
        oneOf &&
        typeof oneOf === 'object' &&
        oneOf !== null &&
        'use' in oneOf &&
        Array.isArray(oneOf.use)
      ) {
        oneOf.use.forEach((loader) => {
          if (
            loader &&
            typeof loader === 'object' &&
            loader !== null &&
            'loader' in loader &&
            typeof loader.loader === 'string' &&
            loader.loader.includes('sass-loader')
          ) {
            const loaderWithOptions = loader;
            loaderWithOptions.options = {
              ...loaderWithOptions.options,
              api: 'modern-compiler',
              sassOptions: {
                ...loaderWithOptions.options?.sassOptions,
                includePaths: [path.join(projectRoot, 'node_modules')],
                silenceDeprecations: ['legacy-js-api'],
              },
            };
          }
        });
      }
    });
  }

  return config;
}

module.exports = { configureWebpackSass };
