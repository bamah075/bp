# Template Forge Weapon

The **Template Forge Weapon** is your comprehensive code generation and templating system. It standardizes the creation of production-ready code across all your projects.

## What it does

This weapon helps you generate:

- **Python modules & classes** - Ready-to-use code with error handling, logging, and configuration
- **Configuration files** - YAML, JSON, .env files with validation and environment substitution
- **API & integration handlers** - REST endpoints, webhooks, service clients
- **Feature scaffolding** - Complete features with logic, tests, and documentation
- **Test templates** - Unit tests, integration tests, fixtures, and mocks

## Quick start

### Generate a Python module

```
Request: "Generate a Python module called 'email_sender' that sends emails via SendGrid
- Main class: EmailSender with method send(to, subject, body)
- Configuration via environment variables
- Retry on failure with exponential backoff
- Comprehensive logging"
```

The weapon generates:
- `email_sender/__init__.py` - Package initialization
- `email_sender/core.py` - Main EmailSender class
- `email_sender/config.py` - Configuration management
- `email_sender/exceptions.py` - Custom exceptions
- `email_sender/tests/test_core.py` - Unit tests with fixtures

### Generate configuration

```
Request: "Create a YAML config for a notification service
- Database connection with pool settings
- Slack integration (token, channel)
- Email provider (API key, from address)
- Logging configuration
Include environment variable substitution and sensible defaults"
```

Generates: `config.yaml` with proper structure, validation, and documentation.

### Scaffold a complete feature

```
Request: "Scaffold a 'user_onboarding' feature that:
- Handles user signup events
- Sends welcome email using template
- Creates welcome tasks
- Logs all operations
Include full error handling, tests, and configuration"
```

Generates complete feature with handler, models, tests, and documentation.

## When to use this weapon

✅ **Use when:**
- You need to generate production-ready code
- You're creating new modules or features
- You need standardized templates for your projects
- You want to reduce boilerplate and repetition
- You're building reusable patterns

❌ **Don't use for:**
- Code review and refactoring (use code-review-pr-weapon)
- Architecture decisions (use adr-writing-weapon)
- General coding help (use python-weapon / react-weapon)

## Structure

```
template-forge-weapon/
├── SKILL.md                          # This skill definition
├── README.md                         # This file
├── guides/                           # How-to guides
│   ├── 01-python-modules.md
│   ├── 02-config-templates.md
│   ├── 04-feature-scaffolding.md
│   └── ...
├── examples/                         # Working examples
│   ├── notification_handler_example.py
│   └── ...
├── templates/                        # Blank templates to customize
│   ├── python_module_template.py
│   ├── config_template.yaml
│   └── test_template.py
└── research/                         # Background and references
    └── ...
```

## Key principles

### 1. Production-ready from the start

Generated code isn't a stub—it's usable immediately:
- Includes error handling and logging
- Has proper initialization and validation
- Tests are included from the start
- Configuration is built-in

### 2. Context-aware generation

Every template respects your project's style:
- Follows your team's patterns
- Uses your existing conventions
- Matches your language and framework choices
- Integrates with your infrastructure

### 3. Composition over repetition

Templates are reusable building blocks:
- Common patterns are extracted
- Utilities are shared
- Tests are parameterized
- Documentation is generated

## Examples and guides

- **Python modules**: `guides/01-python-modules.md`
- **Configuration**: `guides/02-config-templates.md`
- **API handlers**: `guides/03-api-integration-templates.md`
- **Features**: `guides/04-feature-scaffolding.md`
- **Testing**: `guides/05-test-generation.md`

See `examples/notification_handler_example.py` for a complete working example.

## Invoking the skill

When you say:
- "Generate a Python module for..."
- "Create a config template..."
- "Scaffold a complete feature..."
- "Build a test template for..."

The Template Forge Weapon activates and generates production-ready code.

---

**Part of the Legion AI Tools Factory pipeline.**

For more information on skills and the AI tooling system, see:
- `SKILL.md` - Full skill definition
- `../that-git-life/SKILLS.md` - Overview of all available skills
- `../that-git-life/README.md` - Project documentation
