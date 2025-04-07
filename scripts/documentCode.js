const fs = require('fs');
const path = require('path');
const glob = require('glob');

/**
 * Configuration for the documentation process
 * @type {Object}
 */
const config = {
  // File patterns to process
  patterns: {
    react: ['**/*.jsx', '**/*.tsx'],
    ignore: ['**/node_modules/**', '**/dist/**', '**/build/**'],
  },

  // Comment templates
  templates: {
    component: (name, description = '') =>
      `/**
 * ${name} - ${description}
 *
 * @component
 * @version 1.0.0
 * @author Generated by Documentation Script
 * @lastModified ${new Date().toISOString().split('T')[0]}
 */`,

    props: props =>
      `/**
 * @typedef {Object} Props
 * ${props.map(p => ` * @property {${p.type}} ${p.name} - ${p.description}`).join('\n')}
 */`,

    function: (name, params = [], returns = '') =>
      `/**
 * ${name}
 *
 * @function
 * ${params.map(p => ` * @param {${p.type}} ${p.name} - ${p.description}`).join('\n')}
 * ${returns ? ` * @returns {${returns.type}} ${returns.description}` : ''}
 */`,

    hook: (name, deps = []) =>
      `/**
 * ${name} effect hook
 *
 * @hook
 * @dependencies [${deps.join(', ')}]
 */`,

    'module': '''"""
{module_name}

{description}

This module is part of the backend API and provides {purpose}.
"""
''',

    'class': '''class {class_name}:
    """
    {class_name} - {description}

    This class {purpose}.

    Attributes:
        {attributes}
    """
''',

    'method': '''    def {method_name}(self, {params}) -> {return_type}:
        """
        {description}

        Args:
            {args_doc}

        Returns:
            {return_doc}

        Raises:
            {raises_doc}
        """
'''
  },
};

/**
 * Analyzes a React component file and extracts key information
 * @param {string} content - File content to analyze
 * @returns {Object} Component information
 */
function analyzeComponent(content) {
  const info = {
    name: '',
    props: [],
    functions: [],
    hooks: [],
    description: '',
  };

  // Extract component name
  const componentMatch = content.match(/function\s+(\w+)|const\s+(\w+)\s*=/);
  if (componentMatch) {
    info.name = componentMatch[1] || componentMatch[2];
  }

  // Extract props
  const propsMatch = content.match(/{\s*([^}]+)\s*}\s*=\s*props/);
  if (propsMatch) {
    info.props = propsMatch[1].split(',').map(prop => ({
      name: prop.trim(),
      type: 'any', // Default type, would need TypeScript or prop-types for better inference
      description: 'Description needed',
    }));
  }

  // Extract hooks
  const hookMatches = content.matchAll(/use\w+\(/g);
  for (const match of hookMatches) {
    info.hooks.push({
      name: match[0].slice(0, -1),
      deps: [],
    });
  }

  // Extract functions
  const functionMatches = content.matchAll(/function\s+(\w+)|const\s+(\w+)\s*=\s*\([^)]*\)\s*=>/g);
  for (const match of functionMatches) {
    const name = match[1] || match[2];
    if (name && name !== info.name) {
      info.functions.push({
        name,
        params: [],
        returns: { type: 'void', description: 'Description needed' },
      });
    }
  }

  return info;
}

/**
 * Generates documentation comments for a component
 * @param {Object} info - Component information
 * @returns {string} Documentation comments
 */
function generateDocs(info) {
  let docs = [];

  // Component documentation
  docs.push(config.templates.component(info.name, info.description));

  // Props documentation if any
  if (info.props.length > 0) {
    docs.push(config.templates.props(info.props));
  }

  // Function documentation
  info.functions.forEach(func => {
    docs.push(config.templates.function(func.name, func.params, func.returns));
  });

  // Hook documentation
  info.hooks.forEach(hook => {
    docs.push(config.templates.hook(hook.name, hook.deps));
  });

  return docs.join('\n\n');
}

/**
 * Processes a single file and adds documentation
 * @param {string} filePath - Path to the file
 */
function processFile(filePath) {
  console.log(`Processing ${filePath}...`);

  const content = fs.readFileSync(filePath, 'utf8');
  const info = analyzeComponent(content);
  const docs = generateDocs(info);

  // Check if file already has documentation
  if (!content.startsWith('/**')) {
    const newContent = `${docs}\n\n${content}`;
    fs.writeFileSync(filePath, newContent, 'utf8');
    console.log(`✓ Added documentation to ${filePath}`);
  } else {
    console.log(`! Skipped ${filePath} - already has documentation`);
  }
}

/**
 * Main function to process all files
 * @param {string} baseDir - Base directory to start from
 */
function main(baseDir = 'src') {
  const patterns = config.patterns.react.map(pattern => path.join(baseDir, pattern));

  const files = glob.sync(patterns, { ignore: config.patterns.ignore });

  console.log(`Found ${files.length} files to process...`);

  files.forEach(processFile);

  console.log('Documentation process complete!');
}

// Run the script if called directly
if (require.main === module) {
  const baseDir = process.argv[2] || 'src';
  main(baseDir);
}

module.exports = {
  processFile,
  analyzeComponent,
  generateDocs,
  config,
};
