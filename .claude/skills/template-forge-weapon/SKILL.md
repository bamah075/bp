---
name: template-forge-weapon
description: General-purpose code generation and templating specialist. Generates Python modules and classes, configuration files, API/integration templates, and feature scaffolding with tests across all project types. Use when the user says "generate a Python module", "scaffold a feature", "create a config template", "generate boilerplate", "create an integration handler", or "I need a template for X". Handles multi-language templates, configuration management, and complete feature generation from specifications.
license: MIT
---

# Template Forge Weapon

The Template Forge Weapon is your code generation and templating arsenal. It standardizes the creation of reusable components, modules, configurations, and complete features across all your projects. Whether you need a Python automation module, API integration handler, configuration file, or a complete feature scaffold with tests, this weapon generates production-ready code from specifications and best-practice templates.

---

## When to use this weapon

Activate when the user:

- Says "generate a Python module", "create a function", "scaffold a feature"
- Wants "boilerplate for X", "a template for Y", "configuration template"
- Asks "create a config file", "generate an integration handler", "API template"
- Needs "complete feature scaffolding", "test template", "module structure"
- Wants to "standardize code generation", "reuse patterns", "create templates"

Do NOT activate for:
- Code review and refactoring (code-review-pr-weapon)
- Architecture decisions (adr-writing-weapon)
- Project planning and PRDs (library-weapon)
- General coding help (python-weapon / react-weapon)

---

## Playbook

| Task | Guide |
|---|---|
| Generate Python modules and classes | `guides/01-python-modules.md` |
| Create configuration file templates | `guides/02-config-templates.md` |
| Build API and integration handlers | `guides/03-api-integration-templates.md` |
| Scaffold complete features | `guides/04-feature-scaffolding.md` |
| Generate test templates | `guides/05-test-generation.md` |
| Custom template creation | `guides/06-custom-templates.md` |
| Multi-project template management | `guides/07-template-organization.md` |

For working examples, see `examples/` directory with real-world patterns.

For blank templates, see `templates/` directory organized by type.

---

## Core principles

### 1. Template as specification

A template is not boilerplate you ignore—it is a specification for what *should* exist in your codebase. Every generated file should:
- Be immediately usable (not a stub)
- Follow your project's patterns and conventions
- Include necessary error handling and logging
- Have minimal docstrings (WHY over WHAT)
- Be testable and production-ready

### 2. Context-driven generation

Templates are generated with full context:
- Project type and structure
- Existing patterns in the codebase
- Language and framework conventions
- Team standards and rules
- Specific requirements from the user

### 3. Composition over copy-paste

Never generate the same pattern twice. Build reusable components:
- Utility functions extracted to shared modules
- Common configurations centralized
- Patterns documented and inherited by all new code
- Tests written once, configured many times

### 4. Test-first templates

Every generated feature includes tests from the start:
- Unit tests for functions and classes
- Integration tests for handlers and APIs
- Configuration validation tests
- Test fixtures and mocks included

### 5. Documentation is generation

Documentation is generated from the template:
- Docstrings describe the WHY, not the WHAT
- Examples are drawn from test cases
- Configuration options documented with their purpose
- API signatures and types are self-documenting

---

## Template types at a glance

### Python Modules & Classes

Generate production-ready Python code:
- Utility functions and helpers
- Classes with proper initialization
- Async/await handlers
- Configuration managers
- Integration clients

```python
# Example: Generated integration client
class APIIntegrationClient:
    """Handle API communication with retry logic and error handling."""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def fetch(self, endpoint: str) -> dict:
        """Fetch from endpoint with automatic retry."""
        # Implementation with exponential backoff
```

### Configuration Templates

Generate standardized config files:
- Environment configurations (.env, .env.local)
- Application settings (YAML, JSON, TOML)
- Database configurations
- Service credentials
- Feature flags

```yaml
# Example: Generated service config
app:
  name: my-service
  version: 1.0.0
  debug: ${DEBUG:false}
  
database:
  url: ${DATABASE_URL}
  pool_size: ${DB_POOL_SIZE:10}
  
integrations:
  api:
    enabled: true
    timeout: 30
```

### API & Integration Templates

Generate handlers and connectors:
- REST API endpoints with FastAPI
- Webhook handlers
- Event processors
- Third-party service clients
- Authentication and authorization

```python
# Example: Generated FastAPI endpoint
@router.post("/webhooks/github")
async def handle_github_webhook(payload: GitHubWebhook):
    """Process GitHub webhook with signature validation."""
    # Validation, processing, error handling
```

### Feature Scaffolding

Generate complete features with structure:
- Module entry points
- Feature handlers and logic
- Configuration for the feature
- Unit and integration tests
- Example usage

### Test Templates

Generate test infrastructure:
- Unit test fixtures
- Mock factories
- Integration test setup
- CI/CD test configurations
- Test data generators

---

## Generation workflow

1. **Gather requirements** - What are you building? (module name, purpose, dependencies, inputs/outputs)
2. **Select template type** - Which template category fits best?
3. **Apply context** - Adapt the template to your codebase style and patterns
4. **Generate code** - Create the actual files with proper structure
5. **Add tests** - Generate test files alongside the code
6. **Document** - Auto-generate docstrings and usage examples
7. **Review & integrate** - Review generated code, adjust as needed, commit

---

## References and resources

- Python module conventions: `research/python-conventions.md`
- Configuration management patterns: `research/config-patterns.md`
- API design best practices: `research/api-design.md`
- Test template patterns: `research/testing-patterns.md`

---

*Command Brief: [`ai-tools/command-briefs/template-forge-command-brief.md`](../../command-briefs/template-forge-command-brief.md)*
*Part of the Legion AI Tools Factory pipeline. Template system for standardized code generation across all projects.*
