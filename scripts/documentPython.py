#!/usr/bin/env python3
"""
Python Documentation Generator
Automatically generates and updates documentation for Python files.
"""

import ast
import glob
import os
import re
import sys
from typing import List, Dict, Optional, Tuple
from pathlib import Path

class PythonDocGenerator:
    def __init__(self):
        self.templates = {
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
''',
            'function': '''def {function_name}({params}) -> {return_type}:
    """
    {description}

    Args:
        {args_doc}

    Returns:
        {return_doc}

    Raises:
        {raises_doc}
    """
''',
            'route': '''@app.route("{route_path}", methods={methods})
def {route_name}({params}) -> {return_type}:
    """
    {description}

    Endpoint: {route_path}
    Methods: {methods}

    Args:
        {args_doc}

    Returns:
        {return_doc}

    Raises:
        {raises_doc}
    """
'''
        }

    def analyze_file(self, file_path: str) -> Dict:
        """Analyze a Python file and extract its structure."""
        with open(file_path, 'r') as f:
            content = f.read()

        tree = ast.parse(content)
        analysis = {
            'module_name': os.path.basename(file_path).replace('.py', ''),
            'classes': [],
            'functions': [],
            'routes': [],
            'imports': []
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                analysis['classes'].append({
                    'name': node.name,
                    'methods': [method.name for method in node.body if isinstance(method, ast.FunctionDef)],
                    'docstring': ast.get_docstring(node) or ''
                })
            elif isinstance(node, ast.FunctionDef):
                if any(isinstance(decorator, ast.Call) and
                      isinstance(decorator.func, ast.Name) and
                      decorator.func.id == 'route'
                      for decorator in node.decorator_list):
                    analysis['routes'].append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node) or ''
                    })
                else:
                    analysis['functions'].append({
                        'name': node.name,
                        'docstring': ast.get_docstring(node) or ''
                    })
            elif isinstance(node, ast.Import):
                analysis['imports'].extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                analysis['imports'].extend(f"{node.module}.{alias.name}" for alias in node.names)

        return analysis

    def generate_docs(self, file_path: str, analysis: Dict) -> str:
        """Generate documentation for a Python file."""
        content = []

        # Module docstring
        module_name = analysis['module_name']
        content.append(self.templates['module'].format(
            module_name=module_name,
            description=f"Module for {module_name} functionality",
            purpose=f"handles {module_name} related operations"
        ))

        # Imports
        for imp in analysis['imports']:
            content.append(f"from {imp} import {imp.split('.')[-1]}\n")

        # Classes
        for cls in analysis['classes']:
            content.append(self.templates['class'].format(
                class_name=cls['name'],
                description=f"Class for {cls['name']} operations",
                purpose=f"manages {cls['name'].lower()} related functionality",
                attributes="\n        ".join(f"{method} (method): {method} method" for method in cls['methods'])
            ))

        # Functions and Routes
        for func in analysis['functions'] + analysis['routes']:
            template = self.templates['route'] if func in analysis['routes'] else self.templates['function']
            content.append(template.format(
                function_name=func['name'],
                route_name=func['name'],
                route_path=f"/api/{func['name']}",
                methods="['GET', 'POST']",
                params="self" if func in analysis['classes'] else "",
                return_type="Dict[str, Any]",
                description=f"Function for {func['name']} operations",
                args_doc="\n            ".join(f"{param} ({type}): Description" for param, type in [("param1", "str")]),
                return_doc="Dict containing the operation result",
                raises_doc="\n            ".join(f"{exc}: Description" for exc in ["ValueError"])
            ))

        return "\n".join(content)

    def process_file(self, file_path: str, check_only: bool = False) -> bool:
        """Process a single Python file."""
        try:
            analysis = self.analyze_file(file_path)
            new_content = self.generate_docs(file_path, analysis)

            if check_only:
                with open(file_path, 'r') as f:
                    current_content = f.read()
                return current_content == new_content

            with open(file_path, 'w') as f:
                f.write(new_content)
            return True
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
            return False

def main():
    """Main entry point for the documentation generator."""
    generator = PythonDocGenerator()
    check_only = '--check' in sys.argv
    update_only = '--update' in sys.argv
    target_dir = sys.argv[1] if len(sys.argv) > 1 else 'backend'

    files = glob.glob(os.path.join(target_dir, '**/*.py'), recursive=True)
    success_count = 0
    total_count = len(files)

    for file_path in files:
        if generator.process_file(file_path, check_only):
            success_count += 1
            print(f"✓ Processed {file_path}")
        else:
            print(f"✗ Failed to process {file_path}")

    print(f"\nProcessed {success_count}/{total_count} files successfully")
    return success_count == total_count

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
