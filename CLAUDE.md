# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

mtexts is a newly created Python repository. As the project develops, this section will be updated with information about its purpose and architecture.

## Python Code Style (PEP 8)

When writing Python code for this repository, strictly adhere to PEP 8 conventions:

### Indentation and Line Length
- Use 4 spaces for indentation (no tabs)
- Limit lines to 79 characters for code, 72 for docstrings/comments
- Use parentheses for line continuation in expressions
- Break lines before binary operators

### Whitespace
- No trailing whitespace
- Surround operators with single space on either side
- No space around = in keyword arguments or defaults
- Use blank lines to separate logical sections
- Two blank lines around top-level functions and classes
- One blank line around method definitions in classes

### Naming Conventions
- snake_case for functions, variables, modules
- PascalCase for classes
- UPPER_CASE for constants
- _leading_underscore for internal use
- __double_leading_underscore for name mangling

### Imports
- Separate standard library, third-party, and local imports
- Absolute imports are preferred over relative imports
- One import per line
- Imports at top of file

### Comments and Documentation
- Use docstrings for all public modules, functions, classes, methods
- Comments should be complete sentences
- Update comments when code changes
- Comments should explain why, not what

### Programming Recommendations
- Use is/is not for None comparisons
- Use if not x instead of if len(x) == 0
- Explicit exception classes in except clauses
- Return statements consistent in functions
- Use context managers (with) for resource handling

## Development Setup

As the project is in its initial stages, specific build, run, and test commands will be added here as they are established.