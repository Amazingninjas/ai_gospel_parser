# Contributing to AI Gospel Parser

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment

## How to Contribute

### Reporting Bugs

1. Check if the bug is already reported in [Issues](https://github.com/yourusername/ai_gospel_parser/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python/Node versions, Docker)

### Suggesting Features

1. Check [Discussions](https://github.com/yourusername/ai_gospel_parser/discussions) for similar ideas
2. Create a new discussion or issue with:
   - Clear use case
   - Expected behavior
   - Why it would be valuable

### Contributing Code

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/ai_gospel_parser.git
   cd ai_gospel_parser
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests for new features
   - Update documentation

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest -v

   # Frontend build
   cd frontend
   npm run build
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub.

## Development Setup

### Backend

```bash
cd backend
python3 -m venv venv_backend
source venv_backend/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Write docstrings for functions
- Keep functions focused and small

### TypeScript (Frontend)
- Use TypeScript strict mode
- Prefer functional components
- Use custom hooks for reusable logic
- Follow React best practices

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Maintain or improve test coverage

## Documentation

- Update README.md if adding features
- Update USER_GUIDE.md for user-facing changes
- Add code comments for complex logic
- Update API documentation if adding endpoints

## Questions?

Open a discussion or issue if you have questions!
