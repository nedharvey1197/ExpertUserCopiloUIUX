#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const requiredEnvVars = {
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
};

function validateEnvFile(envPath, requiredVars) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  const envVars = {};
  const errors = [];

  // Parse .env file
  envContent.split('\n').forEach(line => {
    if (line && !line.startsWith('#')) {
      const [key, value] = line.split('=');
      if (key && value) {
        envVars[key.trim()] = value.trim();
      }
    }
  });

  // Validate required variables
  Object.entries(requiredVars).forEach(([key, type]) => {
    if (!envVars[key]) {
      errors.push(`Missing required environment variable: ${key}`);
    } else {
      // Type validation
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
  const frontendEnv = path.join(__dirname, '../frontend/.env');
  const backendEnv = path.join(__dirname, '../backend/.env');
  let hasErrors = false;

  // Check if .env files exist
  if (!fs.existsSync(frontendEnv)) {
    console.error('❌ Frontend .env file not found');
    hasErrors = true;
  }
  if (!fs.existsSync(backendEnv)) {
    console.error('❌ Backend .env file not found');
    hasErrors = true;
  }

  // Validate frontend environment
  if (fs.existsSync(frontendEnv)) {
    const frontendErrors = validateEnvFile(frontendEnv, requiredEnvVars.frontend);
    if (frontendErrors.length > 0) {
      console.error('❌ Frontend environment validation failed:');
      frontendErrors.forEach(error => console.error(`  - ${error}`));
      hasErrors = true;
    } else {
      console.log('✓ Frontend environment validated successfully');
    }
  }

  // Validate backend environment
  if (fs.existsSync(backendEnv)) {
    const backendErrors = validateEnvFile(backendEnv, requiredEnvVars.backend);
    if (backendErrors.length > 0) {
      console.error('❌ Backend environment validation failed:');
      backendErrors.forEach(error => console.error(`  - ${error}`));
      hasErrors = true;
    } else {
      console.log('✓ Backend environment validated successfully');
    }
  }

  if (hasErrors) {
    process.exit(1);
  }
}

main();
