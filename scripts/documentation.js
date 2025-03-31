const fs = require('fs');
const path = require('path');
const glob = require('glob');

/**
 * @function addFileDocumentation
 * @description Adds file-level documentation to a file
 * @param {string} filePath - Path to the file
 * @param {string} content - File content
 * @returns {string} Updated content with documentation
 */
function addFileDocumentation(filePath, content) {
    const fileName = path.basename(filePath);
    const fileExt = path.extname(filePath);
    const fileDir = path.dirname(filePath);
    const relativePath = path.relative(process.cwd(), filePath);

    let doc = '';

    if (fileExt === '.js' || fileExt === '.jsx' || fileExt === '.ts' || fileExt === '.tsx') {
        doc = `/**
 * @fileoverview ${fileName}
 * @module ${relativePath}
 * @author [Author Name]
 * @created ${new Date().toISOString().split('T')[0]}
 * @last-modified ${new Date().toISOString().split('T')[0]}
 * @version 1.0.0
 */\n\n`;
    } else if (fileExt === '.py') {
        doc = `"""
File: ${fileName}
Description: [Add description]
Author: [Author Name]
Created: ${new Date().toISOString().split('T')[0]}
Last Modified: ${new Date().toISOString().split('T')[0]}
Version: 1.0.0

This module handles [specific functionality].
"""

`;
    }

    return doc + content;
}

/**
 * @function processFile
 * @description Processes a single file for documentation
 * @param {string} filePath - Path to the file
 */
function processFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const updatedContent = addFileDocumentation(filePath, content);
    fs.writeFileSync(filePath, updatedContent);
    console.log(`Documented: ${filePath}`);
}

/**
 * @function processDirectory
 * @description Processes all files in a directory
 * @param {string} dir - Directory to process
 */
function processDirectory(dir) {
    const patterns = [
        '**/*.js',
        '**/*.jsx',
        '**/*.ts',
        '**/*.tsx',
        '**/*.py'
    ];

    patterns.forEach(pattern => {
        glob.sync(pattern, { cwd: dir }).forEach(file => {
            const filePath = path.join(dir, file);
            processFile(filePath);
        });
    });
}

// Process frontend and backend directories
processDirectory('frontend/src');
processDirectory('backend');

console.log('Documentation update complete!'); 