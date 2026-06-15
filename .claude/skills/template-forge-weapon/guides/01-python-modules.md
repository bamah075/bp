# Generating Python Modules and Classes

This guide covers generating production-ready Python code: utility functions, classes, async handlers, and integration clients.

## Module structure

Every generated Python module includes:

```
my_module/
├── __init__.py          # Package initialization and exports
├── core.py              # Main logic and classes
├── handlers.py          # Request/event handlers (if applicable)
├── config.py            # Configuration management
├── exceptions.py        # Custom exceptions
├── utils.py             # Helper functions
└── tests/
    ├── __init__.py
    ├── test_core.py
    └── fixtures.py      # Test fixtures and mocks
```

## Generation checklist

When requesting a Python module, specify:

- **Module name** - What is the module called? (e.g., `email_scheduler`, `api_client`)
- **Purpose** - What does it do? One sentence that captures the WHY
- **Entry points** - What are the main functions/classes users will call?
- **Dependencies** - What external libraries does it need?
- **Error handling** - What can go wrong? How should it fail gracefully?
- **Configuration** - What settings does it need?

Example request:
```
Generate a Python module called "slack_notifier" that sends notifications to Slack.
- Main class: SlackNotifier with methods notify(), notify_thread()
- Needs python-slack-sdk, aiohttp
- Should retry on network failure with exponential backoff
- Configuration via environment variables: SLACK_BOT_TOKEN, SLACK_CHANNEL_ID
```

## Class generation patterns

### Basic class with configuration

```python
class MyHandler:
    """Handle X operations with Y configuration."""
    
    def __init__(self, config: dict):
        self.config = config
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Ensure all required config keys are present."""
        required = {'key1', 'key2'}
        if not required.issubset(self.config.keys()):
            raise ValueError(f"Missing config keys: {required - set(self.config.keys())}")
    
    def process(self, data: dict) -> dict:
        """Process input data according to config."""
        # Implementation
        pass
```

### Async handler pattern

```python
class AsyncAPIClient:
    """Client for async API communication."""
    
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make API request with error handling."""
        if not self.session:
            raise RuntimeError("Use async context manager: async with APIClient(...)")
        
        url = f"{self.base_url}{endpoint}"
        try:
            async with self.session.request(method, url, **kwargs) as resp:
                if resp.status >= 400:
                    raise APIError(f"API error: {resp.status}")
                return await resp.json()
        except asyncio.TimeoutError:
            raise APIError("Request timeout")
```

## Error handling patterns

Always include custom exceptions:

```python
class MyModuleError(Exception):
    """Base exception for this module."""
    pass

class ConfigError(MyModuleError):
    """Configuration is invalid."""
    pass

class NetworkError(MyModuleError):
    """Network operation failed."""
    pass
```

## Logging

Use standard library logging, never print():

```python
import logging

logger = logging.getLogger(__name__)

class MyClass:
    def process(self, data):
        logger.info(f"Processing {len(data)} items")
        try:
            result = self._do_work(data)
            logger.debug(f"Processing complete: {result}")
            return result
        except Exception as e:
            logger.error(f"Processing failed: {e}", exc_info=True)
            raise
```

## Testing your generated module

Generated modules include test templates. Example test structure:

```python
import pytest
from my_module import MyClass

@pytest.fixture
def config():
    return {'key1': 'value1', 'key2': 'value2'}

def test_initialization(config):
    obj = MyClass(config)
    assert obj.config == config

def test_missing_config():
    with pytest.raises(ValueError):
        MyClass({})

@pytest.mark.asyncio
async def test_async_operation():
    async with AsyncAPIClient("key", "http://api") as client:
        # Test implementation
        pass
```

## Next steps

- Review `guides/05-test-generation.md` for testing patterns
- See `examples/` for complete working modules
- Check `templates/` for blank module templates to customize
