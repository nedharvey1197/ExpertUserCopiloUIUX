# Documentation and Code Standards Manual

## Table of Contents

1. [Documentation Automation](#documentation-automation)
2. [Repository Structure Standards](#repository-structure-standards)
3. [Naming Conventions](#naming-conventions)
4. [Component Organization](#component-organization)
5. [Setup Instructions](#setup-instructions)
6. [Usage Guide](#usage-guide)
7. [CI/CD Integration](#ci-cd-integration)
8. [Troubleshooting](#troubleshooting)
9. [ML/AI Standards](#ml-ai-standards)
10. [Environment Setup Standards](#environment-setup-standards)
11. [Environment Management Standards](#environment-management-standards)

## Documentation Automation

### Required Files to Copy

```
project-root/
├── scripts/
│   └── documentCode.js      # Main documentation script
├── .vscode/
│   ├── settings.json        # VSCode settings for documentation
│   └── extensions.json      # Required extensions
└── package.json            # Script commands
```

### Installation Steps

1. **Copy Files**:

   ```bash
   mkdir -p scripts .vscode
   cp source-repo/scripts/documentCode.js scripts/
   cp source-repo/.vscode/settings.json .vscode/
   cp source-repo/.vscode/extensions.json .vscode/
   ```

2. **Install Dependencies**:

   ```bash
   npm install --save-dev glob nodemon prettier typescript
   ```

3. **Add Script Commands** to `package.json`:
   ```json
   {
     "scripts": {
       "doc": "node scripts/documentCode.js frontend/src",
       "doc:watch": "nodemon --watch frontend/src --ext js,jsx,ts,tsx --exec 'npm run doc'",
       "doc:check": "node scripts/documentCode.js frontend/src --check",
       "doc:update": "node scripts/documentCode.js frontend/src --update"
     }
   }
   ```

## Repository Structure Standards

### Standard Project Structure

```
project-root/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/          # Shared components
│   │   │   ├── features/        # Feature-specific components
│   │   │   ├── layouts/         # Layout components
│   │   │   └── ui/             # Basic UI components
│   │   ├── pages/              # Page components
│   │   ├── hooks/              # Custom hooks
│   │   ├── utils/              # Utility functions
│   │   ├── services/           # API services
│   │   ├── assets/             # Static assets
│   │   ├── config/             # Configuration files
│   │   ├── constants/          # Constants
│   │   └── App.jsx            # Root component
│   ├── public/                 # Public assets
│   └── tests/                  # Test files
├── backend/
│   ├── app/                    # Main application package
│   │   ├── __init__.py
│   │   ├── models/            # Database models
│   │   ├── routes/            # API routes
│   │   ├── services/          # Business logic
│   │   └── utils/             # Utility functions
│   ├── tests/                 # Test files
│   ├── config/                # Configuration files
│   └── requirements.txt       # Python dependencies
├── scripts/                   # Build and utility scripts
├── docs/                     # Documentation
│   ├── frontend/
│   ├── backend/
│   └── api/
└── .vscode/                 # VSCode configuration
    ├── settings.json
    └── extensions.json
```

## Naming Conventions

### Frontend Files

1. **React Components**:

   - PascalCase with `.jsx` extension: `UserProfile.jsx`
   - Test files: `UserProfile.test.jsx`
   - CSS files: `UserProfile.css`

2. **Hooks**:

   - Start with 'use', camelCase: `useAuth.js`
   - Test files: `useAuth.test.js`

3. **Utilities**:
   - camelCase: `formatDate.js`
   - Test files: `formatDate.test.js`

### Backend Files

1. **Python Modules**:

   - snake_case: `user_service.py`
   - Test files: `test_user_service.py`

2. **Routes**:

   - snake_case: `auth_routes.py`
   - Test files: `test_auth_routes.py`

3. **Models**:
   - PascalCase for classes: `User.py`
   - Test files: `test_user.py`

### Component Structure

```
ComponentName/
├── ComponentName.jsx           # Main component
├── ComponentName.css          # Styles
├── ComponentName.test.jsx     # Tests
├── useComponentLogic.js       # Custom hook (optional)
└── index.js                  # Barrel export
```

## Component Organization

### React Component Structure

```jsx
// ComponentName.jsx
import React, { useState, useEffect } from 'react';
import './ComponentName.css';

/**
 * ComponentName - Component description
 *
 * @component
 * @param {Object} props - Component props
 * @param {string} props.name - Description of prop
 */
const ComponentName = ({ name }) => {
  // Implementation
};

export default ComponentName;
```

### Python Module Structure

```python
"""
Module description and purpose.
"""
from typing import Optional, List

class ClassName:
    """
    Class description and purpose.

    Attributes:
        attr1 (type): Description
        attr2 (type): Description
    """

    def method_name(self, param1: str) -> Optional[List[str]]:
        """
        Method description.

        Args:
            param1 (str): Parameter description

        Returns:
            Optional[List[str]]: Return value description
        """
        pass
```

## Usage Guide

### 1. Regular Documentation (`npm run doc`)

Use when adding documentation to new or undocumented files.

### 2. Watch Mode (`npm run doc:watch`)

Use during active development.

### 3. Documentation Check (`npm run doc:check`)

Use in CI/CD pipelines or before commits.

### 4. Update Documentation (`npm run doc:update`)

Use when refactoring or updating existing documentation.

## CI/CD Integration

```yaml
# .github/workflows/documentation.yml
name: Documentation Check

on:
  pull_request:
    branches: [main, develop]

jobs:
  check-documentation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
      - run: npm install
      - run: npm run doc:check
```

## Troubleshooting

### Common Issues

1. **Missing Documentation**:

   ```bash
   npm run doc:update -- --force
   ```

2. **Watch Mode Issues**:

   ```bash
   npm run doc:watch -- --clear-cache
   ```

3. **Component Detection Issues**:
   - Check naming conventions
   - Verify file structure
   - Ensure proper exports

### Maintenance Scripts

1. **Check Project Structure**:

   ```bash
   npm run check:structure
   ```

2. **Validate Naming Conventions**:

   ```bash
   npm run check:naming
   ```

3. **Audit Component Organization**:
   ```bash
   npm run check:components
   ```

---

**Note**: This manual should be treated as a living document. Update it as your project's needs evolve and new standards are established.

## ML/AI Standards

### Directory Structure

```
backend/
├── ml/
│   ├── models/              # ML model definitions
│   │   ├── __init__.py
│   │   └── model_name.py
│   ├── training/           # Training scripts
│   │   ├── __init__.py
│   │   └── train_model.py
│   ├── inference/          # Inference scripts
│   │   ├── __init__.py
│   │   └── predict.py
│   ├── data/              # Data processing
│   │   ├── __init__.py
│   │   └── preprocessing.py
│   └── utils/             # ML utilities
│       ├── __init__.py
│       └── ml_utils.py
├── tests/
│   └── ml/               # ML-specific tests
└── config/
    └── ml_config.yaml    # ML configuration
```

### Naming Conventions

1. **ML Models**:

   - Model files: `model_name.py`
   - Training scripts: `train_model_name.py`
   - Inference scripts: `predict_model_name.py`
   - Data processing: `process_model_name_data.py`

2. **Configuration**:
   - Model configs: `model_name_config.yaml`
   - Training configs: `train_model_name_config.yaml`

### Documentation Standards

```python
"""
ML Model Module

This module implements the {model_name} model for {task}.

Model Details:
- Architecture: {architecture}
- Input: {input_description}
- Output: {output_description}
- Performance: {performance_metrics}

Usage:
    from ml.models.model_name import ModelName

    model = ModelName(config)
    predictions = model.predict(input_data)
"""

class ModelName:
    """
    {model_name} model implementation.

    This model {model_description}.

    Attributes:
        config (Dict): Model configuration
        model (Any): The underlying ML model
    """

    def train(self, data: Dict[str, Any]) -> Dict[str, float]:
        """
        Train the model on the provided data.

        Args:
            data (Dict[str, Any]): Training data

        Returns:
            Dict[str, float]: Training metrics
        """
        pass

    def predict(self, input_data: Any) -> Any:
        """
        Generate predictions for the input data.

        Args:
            input_data (Any): Input data for prediction

        Returns:
            Any: Model predictions
        """
        pass
```

### Best Practices

1. **Model Versioning**:

   - Use semantic versioning for models
   - Store model artifacts with version tags
   - Document model dependencies

2. **Data Management**:

   - Document data preprocessing steps
   - Include data validation checks
   - Version control for data processing scripts

3. **Performance Monitoring**:

   - Log model metrics
   - Track prediction latency
   - Monitor model drift

4. **Testing**:
   - Unit tests for model components
   - Integration tests for inference
   - Performance benchmarks

## Replication Files

To replicate this setup in a new repository, you need the following files:

1. **Core Files**:

   ```
   ├── scripts/
   │   ├── documentCode.js      # Frontend documentation
   │   ├── documentPython.py    # Backend documentation
   │   └── checkStandards.js    # Standards checking
   ├── docs/
   │   └── DOCUMENTATION_STANDARDS.md
   ├── .vscode/
   │   ├── settings.json
   │   └── extensions.json
   └── package.json
   ```

2. **Environment Setup**:

   - Frontend: `npm install`
   - Backend: `poetry install` or `pip install -r requirements.txt`

3. **Git Setup**:

   - `.gitignore` for both frontend and backend
   - GitHub Actions workflows (if needed)

4. **Documentation Commands**:

   ```bash
   # Frontend
   npm run doc
   npm run doc:watch
   npm run doc:check

   # Backend
   npm run doc:python
   npm run doc:python:watch
   npm run doc:python:check

   # Full Stack
   npm run doc:all
   npm run doc:all:watch
   npm run doc:all:check
   ```

## Project Initialization

For new projects, use:

1. **Frontend**:

   ```bash
   npx create-react-app frontend
   ```

2. **Backend**:

   ```bash
   # Using Poetry
   poetry new backend
   cd backend
   poetry add flask python-dotenv

   # Or using venv
   python -m venv backend/venv
   source backend/venv/bin/activate
   pip install flask python-dotenv
   ```

3. **Copy Standards**:

   ```bash
   # Copy all files from the replication files section
   # Update package.json with your project name
   # Install dependencies
   npm install
   ```

4. **Initialize Git**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit with standards"
   ```

The existing tools (Poetry, venv) handle most of the environment setup, so we don't need additional scripts for that. The standards checking and documentation scripts provide the rest of the automation needed.

## Environment Setup Standards

### Environment Files

1. **Frontend Environment**:

   - Location: `frontend/.env`
   - Prefix: `VITE_` for Vite.js
   - Required Variables:
     ```env
     VITE_API_URL=http://localhost:5000
     VITE_API_VERSION=v1
     VITE_ENABLE_ML_FEATURES=true
     VITE_ENABLE_ANALYTICS=true
     VITE_AUTH_ENABLED=true
     VITE_AUTH_DOMAIN=your-auth-domain
     VITE_AUTH_CLIENT_ID=your-client-id
     VITE_APP_NAME=ExpertUserCopiloUIUX
     VITE_APP_ENV=development
     VITE_ML_ENDPOINT=http://localhost:5000/ml
     VITE_ML_MODEL_VERSION=v1
     ```

2. **Backend Environment**:

   - Location: `backend/.env`
   - Required Variables:

     ```env
     # Database
     DB_NAME=your_db_name
     DB_USER=your_db_user
     DB_PASSWORD=your_db_password
     DB_HOST=localhost
     DB_PORT=5432

     # Neo4j
     NEO4J_URI=bolt://localhost:7687
     NEO4J_USER=neo4j
     NEO4J_PASSWORD=your_neo4j_password

     # Server
     PORT=5000
     HOST=0.0.0.0
     ENV=development
     DEBUG=true

     # ML/AI
     ML_MODEL_PATH=./ml/models
     ML_DATA_PATH=./ml/data
     ML_TRAINING_PATH=./ml/training
     ML_INFERENCE_PATH=./ml/inference

     # Security
     JWT_SECRET=your-jwt-secret-key
     JWT_EXPIRATION=24h
     CORS_ORIGIN=http://localhost:5173

     # File Upload
     UPLOAD_FOLDER=./uploads
     MAX_CONTENT_LENGTH=16777216

     # Logging
     LOG_LEVEL=INFO
     LOG_FILE=app.log
     ```

### Environment Validation

1. **Validation Script**:

   - Location: `scripts/validateEnv.js`
   - Usage: `npm run validate:env`
   - Checks:
     - Required variables presence
     - Variable types (string, number, boolean)
     - File existence

2. **Example Files**:
   - Frontend: `frontend/.env.example`
   - Backend: `backend/.env.example`
   - Purpose: Template for new developers

### Best Practices

1. **Security**:

   - Never commit `.env` files
   - Use strong passwords
   - Rotate secrets regularly
   - Use different values for development/production

2. **Development**:

   - Use `.env.example` as template
   - Document all variables
   - Validate environment on startup
   - Use type-safe environment variables

3. **Deployment**:
   - Use environment-specific files
   - Secure secret management
   - Regular environment audits
   - Backup environment configurations

### Commands

```bash
# Validate environment
npm run validate:env

# Validate all (env, code, docs)
npm run validate:all

# Check environment without modifying
npm run validate:env --check

# Update environment files
npm run validate:env --update
```

## Environment Management Standards

### Environment Types

1. **Local Environment Variables** (Project-specific):

   - Location: `.env` files in project directories
   - Purpose: Project configurations, secrets, endpoints
   - Examples:

     ```env
     # frontend/.env
     VITE_API_URL=http://localhost:5000
     VITE_APP_NAME=ExpertUserCopiloUIUX

     # backend/.env
     DB_NAME=AACTFEB
     DB_USER=nedharvey
     ```

2. **MAC Environment Variables** (System-wide):
   - Location: `~/.zshrc` or `~/.bash_profile`
   - Purpose: Development tools, global paths
   - Examples:
     ```bash
     # ~/.zshrc
     export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home
     export PATH=$PATH:$JAVA_HOME/bin
     export PYTHONPATH=/usr/local/lib/python3.9/site-packages
     ```

### Required Environment Variables

1. **Local Variables**:

   - Frontend: API URLs, feature flags, auth settings
   - Backend: Database configs, ML paths, security settings
   - See `.env.example` files for complete list

2. **MAC Variables**:
   - Required:
     - `PYTHONPATH`: Python package path
     - `JAVA_HOME`: Java installation path
     - `PATH`: System executable path
     - `NODE_PATH`: Node.js package path
   - Optional:
     - `PYTHON_VERSION`: Python version
     - `NODE_VERSION`: Node.js version
     - `JAVA_VERSION`: Java version

### Environment Validation

1. **Commands**:

   ```bash
   # Check all environments
   npm run check:env

   # Check local environment only
   npm run validate:env

   # Full validation
   npm run check:all
   ```

2. **Validation Rules**:
   - Required variables present
   - Correct variable types
   - Valid file paths
   - Security compliance

### Best Practices

1. **Local Environment**:

   - Never commit `.env` files
   - Use `.env.example` as template
   - Document all variables
   - Validate on startup

2. **MAC Environment**:

   - Keep minimal and focused
   - Document in setup guide
   - Regular validation
   - Version control for `.zshrc`

3. **Security**:

   - Use strong passwords
   - Rotate secrets regularly
   - Different values per environment
   - Secure secret management

4. **Development**:
   - Use type-safe variables
   - Regular environment audits
   - Automated validation
   - Clear documentation

### Setup Guide

1. **New Developer Setup**:

   ```bash
   # Clone repository
   git clone <repository-url>
   cd <project-directory>

   # Copy environment files
   cp frontend/.env.example frontend/.env
   cp backend/.env.example backend/.env

   # Set up MAC environment
   echo 'export PYTHONPATH=/usr/local/lib/python3.9/site-packages' >> ~/.zshrc
   echo 'export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home' >> ~/.zshrc
   echo 'export PATH=$PATH:$JAVA_HOME/bin' >> ~/.zshrc

   # Reload shell
   source ~/.zshrc

   # Validate setup
   npm run check:all
   ```

2. **Regular Maintenance**:

   ```bash
   # Check environment
   npm run check:env

   # Update dependencies
   npm install
   pip install -r requirements.txt

   # Validate all
   npm run check:all
   ```
