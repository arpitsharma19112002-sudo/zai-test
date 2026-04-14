# BioPress Designer

Educational content generation tool for NEET/JEE exams.

## Features

- **CLI Interface** - Easy-to-use command-line tool
- **Multi-LLM Support** - Works with MiMo Claw, Kilo Claw, Grok, Claude, Ollama
- **Question Generation** - MCQ, Numerical, Case-based, Assertion-Reason
- **PDF Export** - NEET 2-column, NCERT, Bilingual, OMR-ready styles
- **Two-Stage Validation** - L1 (SymPy) + L2 (LLM)
- **Knowledge Base** - Comprehensive syllabus and rules
- **Visual Editor** - NiceGUI-based review and editing
- **REST API** - FastAPI endpoints for integration

## Installation

```bash
pip install biopress
```

Or install from source:

```bash
git clone <repo>
cd biopress
pip install -e .
```

## Quick Start

```bash
# Show help
biopress --help

# Generate questions
biopress generate --exam NEET --subject Physics --type mcq --count 10 --topic "Newton's Laws"

# Export to PDF
biopress export --input questions.json --output quiz.pdf --style neet

# Review and edit
biopress review launch --load questions.json

# Start API server
biopress api start
```

## Commands

- `generate` - Generate questions
- `validate` - Validate content
- `review` - Visual review tool
- `export` - Export to PDF
- `config` - Manage configuration
- `kb` - Knowledge base management
- `api` - Start API server

## Configuration

```bash
biopress config set provider ollama
biopress config set output_dir ./output
biopress config set language english
```

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Lint code
ruff check src/

# Type check
mypy src/
```

## License

MIT
