#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const buildDir = './build';
const basePath = '/nyc-lots';

function fixPaths(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  
  // Fix relative paths to use base path
  content = content.replace(/href="\.\/([^"]*)/g, `href="${basePath}/$1`);
  content = content.replace(/src="\.\/([^"]*)/g, `src="${basePath}/$1`);
  content = content.replace(/import\("\.\/([^"]*)"/g, `import("${basePath}/$1"`);
  
  // Fix the base path calculation in the script
  content = content.replace(
    /base: new URL\("\."\, location\)\.pathname\.slice\(0\, -1\)/g,
    `base: "${basePath}"`
  );
  
  fs.writeFileSync(filePath, content);
  console.log(`Fixed paths in: ${filePath}`);
}

// Fix index.html
const indexPath = path.join(buildDir, 'index.html');
if (fs.existsSync(indexPath)) {
  fixPaths(indexPath);
} else {
  console.error('index.html not found in build directory');
}

console.log('Path fixing complete!');
