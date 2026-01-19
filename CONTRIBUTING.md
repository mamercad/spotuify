# Contributing to Spotuify

Thank you for your interest in contributing to Spotuify! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check existing issues to avoid duplicates.

When filing an issue, include:

1. **Environment details:**
   - OS and version
   - Python version (`python --version`)
   - Spotuify version (`pip show spotuify`)
   - Terminal emulator

2. **Steps to reproduce:**
   - What you were trying to do
   - What commands you ran
   - What happened vs. what you expected

3. **Error messages:**
   - Full traceback if available
   - Screenshots of UI issues

### Suggesting Features

Feature requests are welcome! Please:

1. Check if the feature has already been requested
2. Describe the feature and its use case
3. Explain why it would benefit users

### Pull Requests

1. **Fork the repository**
   ```bash
   git clone https://github.com/your-username/spotuify.git
   cd spotuify
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set up development environment**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Make your changes**
   - Write clear, commented code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

5. **Run tests and linting**
   ```bash
   # Run tests
   pytest
   
   # Run linting
   ruff check src/ tests/
   
   # Format code
   ruff format src/ tests/
   
   # Type checking
   mypy src/
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add awesome new feature"
   ```
   
   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation
   - `style:` - Formatting
   - `refactor:` - Code restructuring
   - `test:` - Adding tests
   - `chore:` - Maintenance

7. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub.

## Development Guidelines

### Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Maximum line length: 100 characters
- Use descriptive variable and function names

### Project Structure

```
src/spotuify/
├── api/          # Spotify API integration
├── screens/      # Textual screen classes
├── widgets/      # Textual widget classes
└── utils/        # Utility functions
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_<module>.py`
- Use pytest fixtures from `conftest.py`
- Aim for good coverage of new code

Example test:
```python
import pytest
from spotuify.utils.formatting import format_duration

class TestFormatDuration:
    def test_formats_minutes_and_seconds(self):
        assert format_duration(90000) == "1:30"
    
    def test_handles_none(self):
        assert format_duration(None) == "--:--"
```

### Widget Development

When creating new widgets:

1. Inherit from appropriate Textual base class
2. Define `DEFAULT_CSS` for styling
3. Use reactive attributes for state
4. Emit messages for parent communication

Example:
```python
from textual.widgets import Static
from textual.reactive import reactive
from textual.message import Message

class MyWidget(Static):
    DEFAULT_CSS = """
    MyWidget {
        height: auto;
        padding: 1;
    }
    """
    
    value: reactive[str] = reactive("")
    
    class ValueChanged(Message):
        def __init__(self, value: str) -> None:
            self.value = value
            super().__init__()
```

### Screen Development

When creating new screens:

1. Inherit from `Screen`
2. Define `BINDINGS` for keyboard shortcuts
3. Implement `compose()` for layout
4. Handle navigation with `action_*` methods

### Documentation

- Update README.md for user-facing changes
- Add docstrings to all public functions/classes
- Include usage examples where helpful

## Getting Help

- Open an issue for questions
- Check existing documentation
- Look at similar code in the project

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- CHANGELOG.md for significant contributions

Thank you for contributing to Spotuify!
