
# Contributing to CMU-Africa Information Assistant

Thank you for your interest in contributing to the CMU-Africa Information Assistant! This document provides guidelines for contributing to the project.

## 🤝 How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the [Issues](https://github.com/your-repo/issues) section
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for new features or improvements:

1. Open an issue with the tag `enhancement`
2. Describe the feature and its benefits
3. Provide use cases and examples
4. Discuss implementation approach if you have ideas

### Code Contributions

#### Getting Started

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/cmu-africa-assistant.git
   ```
3. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Run the application:
   ```bash
   streamlit run src/app.py
   ```

#### Making Changes

1. **Write clean code**:
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Use type hints where applicable
   - Keep functions small and focused

2. **Test your changes**:
   - Test all affected features manually
   - Ensure no existing functionality breaks
   - Test with different inputs and edge cases

3. **Document your changes**:
   - Update README.md if needed
   - Add comments for complex logic
   - Update docstrings

#### Submitting Pull Requests

1. Commit your changes:
   ```bash
   git add .
   git commit -m "Add: brief description of changes"
   ```

2. Push to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request:
   - Provide a clear title and description
   - Reference any related issues
   - List all changes made
   - Add screenshots for UI changes

#### Pull Request Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged
4. Your contribution will be credited

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Maximum line length: 100 characters
- Use meaningful variable names
- Add type hints for function parameters and return values

Example:
```python
def get_answer(self, query: str, language: str = "en") -> Dict:
    """
    Get answer for a query
    
    Args:
        query: User query
        language: Response language
        
    Returns:
        Dictionary with answer and metadata
    """
    # Implementation
    pass
```

### File Organization

- Keep related functionality together
- One class per file (with exceptions)
- Use `__init__.py` for package initialization
- Organize imports: standard library, third-party, local

### Commit Messages

Follow the conventional commits format:

```
Type: Brief description

Longer description if needed

Fixes #123
```

Types:
- `Add`: New feature or functionality
- `Fix`: Bug fix
- `Update`: Changes to existing features
- `Docs`: Documentation changes
- `Refactor`: Code refactoring
- `Test`: Adding or updating tests
- `Style`: Code style changes (formatting, etc.)

## 🧪 Testing Guidelines

### Manual Testing

Before submitting a PR, test:

1. **Chat Interface**:
   - Send various queries
   - Check response accuracy
   - Verify sources are displayed
   - Test feedback buttons

2. **Admin Panel**:
   - Add a document
   - Upload bulk documents
   - View index statistics
   - Delete a document

3. **Settings Page**:
   - Check configuration status
   - View feedback stats
   - Test language switching

### Edge Cases

Test with:
- Empty inputs
- Very long inputs
- Special characters
- Multiple languages
- Invalid API keys
- Network errors

## 📚 Adding New Features

### Adding New Languages

1. Add translations to `src/utils/translations.py`:
   ```python
   "es": {
       "app_title": "Asistente de Información CMU-Africa",
       # ... more translations
   }
   ```

2. Update `src/config.py`:
   ```python
   SUPPORTED_LANGUAGES = {
       "en": "English",
       "fr": "Français",
       "es": "Español"
   }
   ```

3. Test all UI elements in the new language

### Adding New Document Categories

1. Update sample data in `src/data/sample_knowledge_base.json`
2. Add category-specific logic if needed
3. Update documentation

### Adding New Features to Admin Panel

1. Create a new tab or section in `src/pages/admin.py`
2. Implement the feature logic
3. Add appropriate error handling
4. Update documentation

## 🔍 Code Review Checklist

Before submitting, ensure:

- [ ] Code follows style guidelines
- [ ] All functions have docstrings
- [ ] Changes are tested manually
- [ ] No hardcoded secrets or API keys
- [ ] Error handling is implemented
- [ ] Documentation is updated
- [ ] Commit messages are clear
- [ ] No unnecessary files are included

## 🌟 Areas for Contribution

We especially welcome contributions in these areas:

### High Priority
- Additional language support
- Improved error handling
- Performance optimizations
- Comprehensive logging
- User authentication

### Medium Priority
- Advanced analytics dashboard
- Export chat history feature
- Email notifications
- Mobile responsiveness improvements
- Dark mode support

### Nice to Have
- Voice input support
- Integration with other services
- Custom theming options
- Advanced search filters
- API documentation

## 📞 Getting Help

If you need help with contributions:

- Check the [README.md](README.md) for setup instructions
- Review existing code for examples
- Ask questions in the issue comments
- Contact maintainers via email

## 🎉 Recognition

All contributors will be:
- Listed in the CONTRIBUTORS.md file
- Credited in release notes
- Acknowledged in the project README

Thank you for contributing to CMU-Africa Information Assistant!
