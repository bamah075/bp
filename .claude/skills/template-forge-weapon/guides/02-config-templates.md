# Configuration File Templates

This guide covers generating standardized configuration files for your projects.

## Configuration file types

### Environment variables (.env)

Store sensitive data and environment-specific values:

```env
# Application
APP_NAME=my-app
APP_ENV=development
DEBUG=true

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
DB_POOL_SIZE=10
DB_TIMEOUT=30

# External services
SLACK_BOT_TOKEN=xoxb-xxxxx
SLACK_CHANNEL_ID=C0xxxxx

# Feature flags
ENABLE_ANALYTICS=true
ENABLE_NOTIFICATIONS=false
```

### YAML configuration (config.yaml)

For complex, hierarchical configurations:

```yaml
app:
  name: my-service
  version: 1.0.0
  environment: ${APP_ENV:development}
  debug: ${DEBUG:false}

server:
  host: ${SERVER_HOST:0.0.0.0}
  port: ${SERVER_PORT:8000}
  workers: ${WORKERS:4}

database:
  url: ${DATABASE_URL}
  pool_size: ${DB_POOL_SIZE:10}
  echo: false
  
integrations:
  slack:
    enabled: true
    token: ${SLACK_BOT_TOKEN}
    channel: ${SLACK_CHANNEL_ID}
  
  email:
    enabled: false
    provider: sendgrid
    api_key: ${SENDGRID_API_KEY}

logging:
  level: ${LOG_LEVEL:INFO}
  format: json
```

### JSON schema (config.schema.json)

Validate configuration structure:

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "app": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "environment": {"type": "string", "enum": ["development", "staging", "production"]},
        "debug": {"type": "boolean"}
      },
      "required": ["name", "environment"]
    },
    "database": {
      "type": "object",
      "properties": {
        "url": {"type": "string"},
        "pool_size": {"type": "integer", "minimum": 1}
      },
      "required": ["url"]
    }
  },
  "required": ["app", "database"]
}
```

## Generation workflow

When requesting configuration templates:

1. **Specify format** - .env, YAML, JSON, TOML, etc.
2. **List required settings** - What needs to be configured?
3. **Provide defaults** - What are sensible defaults?
4. **Describe validation** - Any constraints on values?
5. **Note secrets** - Which values are sensitive?

Example request:
```
Generate a YAML config for a notification service with:
- Service name, version, environment
- Database connection URL and pool size
- Slack integration (token, channel)
- Email integration (provider, API key)
- Logging configuration
- Feature flags for analytics and notifications
Include environment variable substitution and sensible defaults.
```

## Configuration management patterns

### Loading and validating

```python
import yaml
from pathlib import Path

class Config:
    """Load and validate configuration."""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.path = Path(config_file)
        self._data = None
        self.load()
    
    def load(self) -> None:
        """Load config from file, substitute env vars."""
        if not self.path.exists():
            raise FileNotFoundError(f"Config file not found: {self.path}")
        
        with open(self.path) as f:
            content = f.read()
        
        # Substitute environment variables
        import os
        import re
        content = re.sub(
            r'\$\{(\w+)(?::([^}]+))?\}',
            lambda m: os.getenv(m.group(1), m.group(2) or ''),
            content
        )
        
        self._data = yaml.safe_load(content)
        self.validate()
    
    def validate(self) -> None:
        """Validate config against schema."""
        # Use jsonschema for validation
        required_keys = ['app', 'database']
        for key in required_keys:
            if key not in self._data:
                raise ValueError(f"Missing required config key: {key}")
    
    def get(self, key: str, default=None):
        """Get config value using dot notation."""
        keys = key.split('.')
        value = self._data
        for k in keys:
            value = value.get(k, {})
        return value or default
```

### Environment-specific configs

```
config/
├── config.yaml           # Base configuration
├── config.development.yaml
├── config.staging.yaml
└── config.production.yaml
```

Load with environment priority:

```python
env = os.getenv('APP_ENV', 'development')
config_file = f"config/config.{env}.yaml"
config = Config(config_file)
```

## Validation checklist

- All required keys are present
- Default values are sensible
- Type constraints are enforced
- Sensitive values are marked as such
- Environment variable names are clear
- Documentation explains each setting

## Next steps

- See `examples/` for complete configuration examples
- Check `templates/` for blank configuration templates
- Review your project's existing configs for patterns to standardize
