# Contributing to LLMTK

First off, thank you for considering contributing to LLMTK! It's people like you that make LLMTK such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include details about your configuration and environment

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain which behavior you expected to see instead
* Explain why this enhancement would be useful

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Include screenshots and animated GIFs in your pull request whenever possible
* Follow the Python style guide
* Include tests
* Document new code
* End all files with a newline

## Development Setup

```bash
# Clone repository
git clone git@github.com:arcifylabs/llmtk.git
cd llmtk

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"
```

## Development Workflow

1. Create feature branch from dev:
```bash
git checkout dev
git pull origin dev
git checkout -b feature/your-feature
```

2. Make changes and ensure tests pass:
```bash
# Run tests
pytest

# Type checking
mypy .

# Format code
black .
isort .
```

3. Commit and push:
```bash
git add .
git commit -m "feat: your feature description"
git push origin feature/your-feature
```

4. Create PR to dev branch

5. Once PR is approved and merged to dev:
```bash
git checkout main
git pull origin main
git merge dev
git push origin main  # This will run tests
```

## Release Process

1. Update version in `llmtk/__init__.py`:
```python
__version__ = "x.y.z"  # Following semver
```

2. Update CHANGELOG.md:
```markdown
## [x.y.z] - YYYY-MM-DD
### Added
- New features

### Changed
- Changes in existing functionality

### Fixed
- Bug fixes
```

3. Commit and push to main:
```bash
git add llmtk/__init__.py CHANGELOG.md
git commit -m "release: version x.y.z"
git push origin main
```

This will:
1. Run tests
2. Build package
3. Publish to PyPI

## CI/CD

- Push to `dev`: Runs tests
- Push to `main`: 
  1. Runs tests
  2. If tests pass, builds and publishes to PyPI

## Version Control

- Versions follow [SemVer](https://semver.org/)
- Version is managed manually in `llmtk/__init__.py`
- Version format: MAJOR.MINOR.PATCH
  - MAJOR: Breaking changes
  - MINOR: New features, backward compatible
  - PATCH: Bug fixes, backward compatible

## Style Guide

* Use [Black](https://github.com/psf/black) for code formatting
* Use [isort](https://pycqa.github.io/isort/) for import sorting
* Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
* Write docstrings for all public modules, functions, classes, and methods
* Use type hints for all function arguments and return values

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
