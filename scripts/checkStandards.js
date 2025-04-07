const fs = require('fs');
const path = require('path');
const glob = require('glob');

/**
 * Configuration for project standards
 */
const standards = {
  // Directory structure standards
  directories: {
    required: [
      'frontend/src/components',
      'frontend/src/pages',
      'frontend/src/hooks',
      'frontend/src/utils',
      'frontend/src/services',
      'frontend/src/assets',
      'frontend/src/config',
      'frontend/src/constants',
      'backend/app', // Python app directory
      'backend/tests', // Python tests
      'backend/config', // Python config
      'backend/utils', // Python utilities
      'backend/models', // Python models
      'backend/routes', // Python routes
      'backend/services', // Python services
      'backend/ml/models',
      'backend/ml/training',
      'backend/ml/inference',
      'backend/ml/data',
      'backend/ml/utils',
      'backend/tests/ml',
      'backend/config/ml',
      'docs/frontend',
      'docs/backend',
      'docs/api',
      'docs/ml',
    ],
  },

  // Naming conventions
  naming: {
    components: {
      pattern: /^[A-Z][a-zA-Z0-9]*\.jsx$/,
      message: 'Component files should be PascalCase and end with .jsx',
    },
    hooks: {
      pattern: /^use[A-Z][a-zA-Z0-9]*\.js$/,
      message: 'Hook files should start with "use" and be camelCase',
    },
    utils: {
      pattern: /^[a-z][a-zA-Z0-9]*\.js$/,
      message: 'Utility files should be camelCase',
    },
    tests: {
      pattern: /^[A-Z][a-zA-Z0-9]*\.test\.jsx$/,
      message: 'Test files should match the source file name and end with .test.jsx',
    },
    pythonFiles: {
      pattern: /^[a-z][a-z0-9_]*\.py$/,
      message: 'Python files should be snake_case',
    },
    pythonTests: {
      pattern: /^test_[a-z][a-z0-9_]*\.py$/,
      message: 'Python test files should start with test_ and be snake_case',
    },
    mlModels: {
      pattern: /^[a-z][a-z0-9_]*\.py$/,
      message: 'ML model files should be snake_case',
    },
    mlTraining: {
      pattern: /^train_[a-z][a-z0-9_]*\.py$/,
      message: 'Training scripts should start with train_ and be snake_case',
    },
    mlInference: {
      pattern: /^predict_[a-z][a-z0-9_]*\.py$/,
      message: 'Inference scripts should start with predict_ and be snake_case',
    },
    mlData: {
      pattern: /^process_[a-z][a-z0-9_]*\.py$/,
      message: 'Data processing scripts should start with process_ and be snake_case',
    },
    mlConfig: {
      pattern: /^[a-z][a-z0-9_]*_config\.yaml$/,
      message: 'ML config files should be snake_case and end with _config.yaml',
    },
  },

  // Component structure standards
  componentStructure: {
    required: ['{name}.jsx', '{name}.css', '{name}.test.jsx', 'index.js'],
    optional: ['{name}.stories.jsx', 'use{name}Logic.js'],
  },
};

/**
 * Checks if required directories exist
 * @returns {Object} Results of directory checks
 */
function checkDirectoryStructure() {
  const results = {
    missing: [],
    exists: [],
  };

  standards.directories.required.forEach(dir => {
    if (!fs.existsSync(dir)) {
      results.missing.push(dir);
    } else {
      results.exists.push(dir);
    }
  });

  return results;
}

/**
 * Validates file naming conventions
 * @param {string} directory Directory to check
 * @returns {Object} Results of naming checks
 */
function checkNamingConventions(directory) {
  const results = {
    valid: [],
    invalid: [],
  };

  // Check components
  glob.sync(path.join(directory, '**/*.{jsx,tsx}')).forEach(file => {
    const basename = path.basename(file);
    if (!standards.naming.components.pattern.test(basename)) {
      results.invalid.push({
        file,
        message: standards.naming.components.message,
      });
    } else {
      results.valid.push(file);
    }
  });

  // Check hooks
  glob.sync(path.join(directory, '**/use*.{js,ts}')).forEach(file => {
    const basename = path.basename(file);
    if (!standards.naming.hooks.pattern.test(basename)) {
      results.invalid.push({
        file,
        message: standards.naming.hooks.message,
      });
    } else {
      results.valid.push(file);
    }
  });

  return results;
}

/**
 * Validates Python file naming conventions
 * @param {string} directory Directory to check
 * @returns {Object} Results of naming checks
 */
function checkPythonNamingConventions(directory) {
  const results = {
    valid: [],
    invalid: [],
  };

  // Check Python files
  glob.sync(path.join(directory, '**/*.py')).forEach(file => {
    const basename = path.basename(file);
    const isTest = basename.startsWith('test_');
    const pattern = isTest
      ? standards.naming.pythonTests.pattern
      : standards.naming.pythonFiles.pattern;
    const message = isTest
      ? standards.naming.pythonTests.message
      : standards.naming.pythonFiles.message;

    if (!pattern.test(basename)) {
      results.invalid.push({
        file,
        message,
      });
    } else {
      results.valid.push(file);
    }
  });

  return results;
}

/**
 * Checks component organization
 * @param {string} directory Directory to check
 * @returns {Object} Results of component checks
 */
function checkComponentOrganization(directory) {
  const results = {
    valid: [],
    incomplete: [],
  };

  glob.sync(path.join(directory, '**/[A-Z]*.{jsx,tsx}')).forEach(file => {
    const componentDir = path.dirname(file);
    const componentName = path.basename(file, path.extname(file));

    const requiredFiles = standards.componentStructure.required.map(template =>
      template.replace('{name}', componentName)
    );

    const missingFiles = requiredFiles.filter(
      requiredFile => !fs.existsSync(path.join(componentDir, requiredFile))
    );

    if (missingFiles.length > 0) {
      results.incomplete.push({
        component: componentName,
        directory: componentDir,
        missing: missingFiles,
      });
    } else {
      results.valid.push(componentName);
    }
  });

  return results;
}

/**
 * Generates a report of all checks
 * @returns {Object} Comprehensive check results
 */
function generateReport() {
  const report = {
    timestamp: new Date().toISOString(),
    directoryStructure: checkDirectoryStructure(),
    frontendNaming: checkNamingConventions('frontend/src'),
    backendNaming: checkPythonNamingConventions('backend'),
    componentOrganization: checkComponentOrganization('frontend/src/components'),
  };

  // Calculate statistics
  report.statistics = {
    directoriesPresent: report.directoryStructure.exists.length,
    directoriesMissing: report.directoryStructure.missing.length,
    validFrontendNames: report.frontendNaming.valid.length,
    invalidFrontendNames: report.frontendNaming.invalid.length,
    validBackendNames: report.backendNaming.valid.length,
    invalidBackendNames: report.backendNaming.invalid.length,
    validComponents: report.componentOrganization.valid.length,
    incompleteComponents: report.componentOrganization.incomplete.length,
  };

  return report;
}

/**
 * Creates missing directories
 */
function createMissingDirectories() {
  const { missing } = checkDirectoryStructure();
  missing.forEach(dir => {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`Created directory: ${dir}`);
  });
}

/**
 * Main function
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'check':
      const report = generateReport();
      console.log(JSON.stringify(report, null, 2));
      process.exit(
        report.statistics.directoriesMissing +
          report.statistics.invalidFrontendNames +
          report.statistics.invalidBackendNames +
          report.statistics.incompleteComponents >
          0
          ? 1
          : 0
      );
      break;

    case 'fix':
      createMissingDirectories();
      console.log('Fixed directory structure');
      break;

    case 'init':
      createMissingDirectories();
      // TODO: Add template generation
      console.log('Initialized project structure');
      break;

    default:
      console.log('Usage: node checkStandards.js [check|fix|init]');
      process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  checkDirectoryStructure,
  checkNamingConventions,
  checkPythonNamingConventions,
  checkComponentOrganization,
  generateReport,
  standards,
};
