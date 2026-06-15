# Feature Scaffolding

This guide covers generating complete, production-ready features with structure, logic, configuration, tests, and documentation.

## Feature anatomy

A complete feature includes:

```
features/
└── my_feature/
    ├── __init__.py              # Feature exports and initialization
    ├── handler.py               # Main feature logic
    ├── config.py                # Feature configuration
    ├── models.py                # Data models and schemas
    ├── exceptions.py            # Feature-specific exceptions
    ├── README.md                # Feature documentation
    └── tests/
        ├── __init__.py
        ├── test_handler.py      # Handler tests
        ├── test_models.py       # Model validation tests
        └── fixtures.py          # Shared test data
```

## Generation checklist

When requesting complete feature scaffolding, specify:

- **Feature name** - What is it called? (e.g., `email_notifications`, `user_analytics`)
- **Purpose** - What problem does it solve? (one paragraph)
- **Inputs** - What data does it receive?
- **Outputs** - What does it produce?
- **External dependencies** - Does it integrate with APIs, databases, etc.?
- **Configuration** - What settings does it need?
- **Error cases** - What can go wrong?
- **Success criteria** - How do you know it worked?

Example request:
```
Scaffold a complete "email_notifications" feature that:
- Listens for notification events (user signup, password reset, etc.)
- Composes email using Jinja2 templates
- Sends via SendGrid API
- Tracks delivery status (sent, bounced, opened)
- Retries failed deliveries with exponential backoff
Configuration: SendGrid API key, email templates directory, retry settings
Error handling: Failed sends logged and queued for retry, network timeouts
Success criteria: Email sent within 30 seconds, 99% delivery rate
```

## Feature handler structure

```python
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class EmailNotificationRequest:
    """Request to send an email notification."""
    recipient: str
    template: str
    context: dict
    priority: str = "normal"

class EmailNotificationHandler:
    """Handle email notification requests."""
    
    def __init__(self, config: dict, sendgrid_client):
        self.config = config
        self.client = sendgrid_client
        self._validate_config()
    
    def _validate_config(self) -> None:
        """Ensure all required config is present."""
        required = {'api_key', 'from_email', 'templates_dir'}
        if not required.issubset(self.config.keys()):
            raise ValueError(f"Missing config: {required - set(self.config.keys())}")
    
    async def handle(self, request: EmailNotificationRequest) -> dict:
        """Process a notification request."""
        try:
            logger.info(f"Processing email for {request.recipient}")
            
            # Compose email
            email_content = self._compose_email(request)
            
            # Send via SendGrid
            result = await self.client.send(email_content)
            
            logger.info(f"Email sent to {request.recipient}")
            return {'status': 'sent', 'message_id': result['id']}
        
        except Exception as e:
            logger.error(f"Email delivery failed: {e}", exc_info=True)
            raise
    
    def _compose_email(self, request: EmailNotificationRequest) -> dict:
        """Compose email from template and context."""
        # Load template
        template_path = Path(self.config['templates_dir']) / f"{request.template}.html"
        
        # Render with context
        from jinja2 import Environment, FileSystemLoader
        env = Environment(loader=FileSystemLoader(self.config['templates_dir']))
        template = env.get_template(f"{request.template}.html")
        html = template.render(request.context)
        
        return {
            'to': request.recipient,
            'from': self.config['from_email'],
            'subject': f"{request.template.title()} Notification",
            'html': html
        }
```

## Feature models and schemas

```python
from pydantic import BaseModel, EmailStr
from typing import Dict, Optional

class NotificationEvent(BaseModel):
    """Event that triggers a notification."""
    event_type: str  # 'signup', 'password_reset', etc.
    user_email: EmailStr
    data: Dict
    created_at: datetime

class DeliveryStatus(BaseModel):
    """Status of a sent notification."""
    message_id: str
    recipient: EmailStr
    status: str  # 'sent', 'bounced', 'opened'
    timestamp: datetime
    retry_count: int = 0
```

## Testing your feature

Generated test structure:

```python
import pytest
from features.my_feature import MyFeatureHandler

@pytest.fixture
def config():
    return {
        'api_key': 'test-key',
        'from_email': 'test@example.com',
        'templates_dir': './templates'
    }

@pytest.fixture
def mock_client():
    """Mock external service client."""
    class MockClient:
        async def send(self, data):
            return {'id': 'msg-123'}
    return MockClient()

def test_handler_initialization(config):
    handler = MyFeatureHandler(config, mock_client)
    assert handler.config == config

@pytest.mark.asyncio
async def test_request_handling(config, mock_client):
    handler = MyFeatureHandler(config, mock_client)
    request = create_test_request()
    result = await handler.handle(request)
    assert result['status'] == 'sent'

def test_missing_config_raises_error():
    with pytest.raises(ValueError):
        MyFeatureHandler({}, mock_client)
```

## Feature integration checklist

- [ ] Handler correctly processes all input types
- [ ] Configuration validates on startup
- [ ] Error cases are logged and handled gracefully
- [ ] External service failures don't crash the feature
- [ ] Tests cover success and failure paths
- [ ] Documentation explains how to use the feature
- [ ] Example usage is provided
- [ ] Feature is importable from package

## Next steps

- See `examples/` for complete feature implementations
- Check `templates/` for feature scaffold templates
- Review `guides/05-test-generation.md` for comprehensive testing
- Look at `guides/06-custom-templates.md` to customize scaffolds
