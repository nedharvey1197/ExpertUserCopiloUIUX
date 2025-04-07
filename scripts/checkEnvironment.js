#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const requiredEnvVars = {
  local: {
    frontend: {
      VITE_API_URL: 'string',
      VITE_API_VERSION: 'string',
      VITE_ENABLE_ML_FEATURES: 'boolean',
      VITE_ENABLE_ANALYTICS: 'boolean',
      VITE_AUTH_ENABLED: 'boolean',
      VITE_AUTH_DOMAIN: 'string',
      VITE_AUTH_CLIENT_ID: 'string',
      VITE_APP_NAME: 'string',
      VITE_APP_ENV: 'string',
      VITE_ML_ENDPOINT: 'string',
      VITE_ML_MODEL_VERSION: 'string',
    },
    backend: {
      DB_NAME: 'string',
      DB_USER: 'string',
      DB_PASSWORD: 'string',
      DB_HOST: 'string',
      DB_PORT: 'number',
      NEO4J_URI: 'string',
      NEO4J_USER: 'string',
      NEO4J_PASSWORD: 'string',
      PORT: 'number',
      HOST: 'string',
      ENV: 'string',
      DEBUG: 'boolean',
      ML_MODEL_PATH: 'string',
      ML_DATA_PATH: 'string',
      ML_TRAINING_PATH: 'string',
      ML_INFERENCE_PATH: 'string',
      JWT_SECRET: 'string',
      JWT_EXPIRATION: 'string',
      CORS_ORIGIN: 'string',
      UPLOAD_FOLDER: 'string',
      MAX_CONTENT_LENGTH: 'number',
      LOG_LEVEL: 'string',
      LOG_FILE: 'string',
    },
  },
  mac: {
    required: ['PYTHONPATH', 'JAVA_HOME', 'PATH', 'NODE_PATH'],
    optional: ['PYTHON_VERSION', 'NODE_VERSION', 'JAVA_VERSION'],
  },
};

function checkLocalEnv() {
  const results = {
    frontend: { exists: false, valid: false, errors: [] },
    backend: { exists: false, valid: false, errors: [] },
  };

  // Check frontend .env
  const frontendEnv = path.join(__dirname, '../frontend/.env');
  if (fs.existsSync(frontendEnv)) {
    results.frontend.exists = true;
    const content = fs.readFileSync(frontendEnv, 'utf8');
    const envVars = parseEnvFile(content);
    const errors = validateEnvVars(envVars, requiredEnvVars.local.frontend);
    results.frontend.valid = errors.length === 0;
    results.frontend.errors = errors;
  }

  // Check backend .env
  const backendEnv = path.join(__dirname, '../backend/.env');
  if (fs.existsSync(backendEnv)) {
    results.backend.exists = true;
    const content = fs.readFileSync(backendEnv, 'utf8');
    const envVars = parseEnvFile(content);
    const errors = validateEnvVars(envVars, requiredEnvVars.local.backend);
    results.backend.valid = errors.length === 0;
    results.backend.errors = errors;
  }

  return results;
}

function checkMacEnv() {
  const results = {
    required: { valid: false, missing: [] },
    optional: { valid: false, missing: [] },
  };

  // Get current environment variables
  const env = process.env;

  // Check required variables
  requiredEnvVars.mac.required.forEach(varName => {
    if (!env[varName]) {
      results.required.missing.push(varName);
    }
  });
  results.required.valid = results.required.missing.length === 0;

  // Check optional variables
  requiredEnvVars.mac.optional.forEach(varName => {
    if (!env[varName]) {
      results.optional.missing.push(varName);
    }
  });
  results.optional.valid = results.optional.missing.length === 0;

  return results;
}

function parseEnvFile(content) {
  const envVars = {};
  content.split('\n').forEach(line => {
    if (line && !line.startsWith('#')) {
      const [key, value] = line.split('=');
      if (key && value) {
        envVars[key.trim()] = value.trim();
      }
    }
  });
  return envVars;
}

function validateEnvVars(envVars, requiredVars) {
  const errors = [];
  Object.entries(requiredVars).forEach(([key, type]) => {
    if (!envVars[key]) {
      errors.push(`Missing required environment variable: ${key}`);
    } else {
      switch (type) {
        case 'number':
          if (isNaN(Number(envVars[key]))) {
            errors.push(`${key} must be a number`);
          }
          break;
        case 'boolean':
          if (envVars[key] !== 'true' && envVars[key] !== 'false') {
            errors.push(`${key} must be a boolean (true/false)`);
          }
          break;
      }
    }
  });
  return errors;
}

function main() {
  console.log('🔍 Checking Environment Setup...\n');

  // Check local environment
  console.log('📁 Local Environment:');
  const localResults = checkLocalEnv();

  if (localResults.frontend.exists) {
    console.log('  Frontend:');
    console.log(`    Status: ${localResults.frontend.valid ? '✓ Valid' : '✗ Invalid'}`);
    if (!localResults.frontend.valid) {
      console.log('    Errors:');
      localResults.frontend.errors.forEach(error => console.log(`      - ${error}`));
    }
  } else {
    console.log('  Frontend: ✗ .env file not found');
  }

  if (localResults.backend.exists) {
    console.log('  Backend:');
    console.log(`    Status: ${localResults.backend.valid ? '✓ Valid' : '✗ Invalid'}`);
    if (!localResults.backend.valid) {
      console.log('    Errors:');
      localResults.backend.errors.forEach(error => console.log(`      - ${error}`));
    }
  } else {
    console.log('  Backend: ✗ .env file not found');
  }

  // Check MAC environment
  console.log('\n💻 MAC Environment:');
  const macResults = checkMacEnv();

  console.log('  Required Variables:');
  console.log(`    Status: ${macResults.required.valid ? '✓ Valid' : '✗ Invalid'}`);
  if (!macResults.required.valid) {
    console.log('    Missing:');
    macResults.required.missing.forEach(varName => console.log(`      - ${varName}`));
  }

  console.log('  Optional Variables:');
  console.log(`    Status: ${macResults.optional.valid ? '✓ Valid' : '⚠️ Some Missing'}`);
  if (!macResults.optional.valid) {
    console.log('    Missing:');
    macResults.optional.missing.forEach(varName => console.log(`      - ${varName}`));
  }

  // Exit with error if any required checks fail
  if (!localResults.frontend.valid || !localResults.backend.valid || !macResults.required.valid) {
    process.exit(1);
  }
}

main();
