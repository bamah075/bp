"""
Example: Simple notification handler

This example demonstrates a complete, production-ready notification handler
that follows all the patterns and conventions from the template-forge-weapon.

The handler:
- Validates incoming notification requests
- Composes messages from templates
- Sends notifications via multiple channels
- Handles failures gracefully with retry logic
- Logs all operations
- Includes comprehensive error handling
"""

import asyncio
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)


class NotificationChannel(str, Enum):
    """Supported notification channels."""
    EMAIL = "email"
    SLACK = "slack"
    SMS = "sms"


class NotificationError(Exception):
    """Base exception for notification handler."""
    pass


class ConfigError(NotificationError):
    """Configuration is invalid."""
    pass


class DeliveryError(NotificationError):
    """Notification delivery failed."""
    pass


@dataclass
class NotificationRequest:
    """Request to send a notification."""
    recipient: str
    channel: NotificationChannel
    template: str
    context: Dict = None
    priority: str = "normal"  # normal, high, urgent

    def __post_init__(self):
        if not self.recipient:
            raise ValueError("Recipient is required")
        if self.context is None:
            self.context = {}


@dataclass
class NotificationResponse:
    """Response from notification delivery."""
    notification_id: str
    recipient: str
    channel: str
    status: str  # sent, failed, queued
    message: Optional[str] = None
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow()


class NotificationHandler:
    """Handle notification requests across multiple channels."""

    def __init__(self, config: Dict):
        self.config = config
        self._validate_config()
        self._init_channels()
        logger.info("NotificationHandler initialized")

    def _validate_config(self) -> None:
        """Validate required configuration."""
        required_keys = {'channels', 'templates_dir', 'retry_config'}
        missing = required_keys - set(self.config.keys())
        if missing:
            raise ConfigError(f"Missing required config: {missing}")

        # Validate channel config
        for channel, ch_config in self.config['channels'].items():
            if 'enabled' not in ch_config:
                raise ConfigError(f"Channel {channel} missing 'enabled' field")

    def _init_channels(self) -> None:
        """Initialize channel-specific clients."""
        self.channels = {}

        if self.config['channels'].get('email', {}).get('enabled'):
            self.channels['email'] = EmailChannel(
                self.config['channels']['email']
            )

        if self.config['channels'].get('slack', {}).get('enabled'):
            self.channels['slack'] = SlackChannel(
                self.config['channels']['slack']
            )

        if self.config['channels'].get('sms', {}).get('enabled'):
            self.channels['sms'] = SMSChannel(
                self.config['channels']['sms']
            )

    async def send(self, request: NotificationRequest) -> NotificationResponse:
        """Send a notification."""
        try:
            logger.info(
                f"Processing notification for {request.recipient} "
                f"via {request.channel}"
            )

            # Validate channel is enabled
            if request.channel.value not in self.channels:
                raise DeliveryError(f"Channel {request.channel} is not enabled")

            # Get appropriate channel
            channel = self.channels[request.channel.value]

            # Send notification
            notification_id = await channel.send(request)

            logger.info(f"Notification {notification_id} sent successfully")
            return NotificationResponse(
                notification_id=notification_id,
                recipient=request.recipient,
                channel=request.channel.value,
                status='sent'
            )

        except DeliveryError as e:
            logger.error(f"Delivery failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            raise DeliveryError(f"Failed to send notification: {e}") from e

    async def send_batch(
        self, requests: List[NotificationRequest]
    ) -> List[NotificationResponse]:
        """Send multiple notifications concurrently."""
        logger.info(f"Sending batch of {len(requests)} notifications")

        tasks = [self.send(req) for req in requests]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        responses = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch item {i} failed: {result}")
                responses.append(NotificationResponse(
                    notification_id=f"failed-{i}",
                    recipient=requests[i].recipient,
                    channel=requests[i].channel.value,
                    status='failed',
                    message=str(result)
                ))
            else:
                responses.append(result)

        return responses


class EmailChannel:
    """Handle email notifications."""

    def __init__(self, config: Dict):
        self.config = config
        self.provider = config.get('provider', 'sendgrid')
        self.api_key = config.get('api_key')

        if not self.api_key:
            raise ConfigError("Email channel requires api_key")

    async def send(self, request: NotificationRequest) -> str:
        """Send email notification."""
        logger.debug(f"Sending email to {request.recipient}")

        # In real implementation, compose from template
        subject = f"[{request.template.upper()}] Notification"
        body = f"Template: {request.template}\nContext: {request.context}"

        # Call email service API (mocked here)
        try:
            # In real code: sendgrid_client.send(...)
            message_id = f"email-{hash(request.recipient)}"
            logger.debug(f"Email sent with ID: {message_id}")
            return message_id
        except Exception as e:
            raise DeliveryError(f"Email delivery failed: {e}") from e


class SlackChannel:
    """Handle Slack notifications."""

    def __init__(self, config: Dict):
        self.config = config
        self.bot_token = config.get('bot_token')
        self.channel_id = config.get('channel_id')

        if not self.bot_token:
            raise ConfigError("Slack channel requires bot_token")

    async def send(self, request: NotificationRequest) -> str:
        """Send Slack notification."""
        logger.debug(f"Sending Slack message to {request.recipient}")

        # Format message for Slack
        message = f":bell: {request.template}\n{request.context}"

        try:
            # In real code: slack_client.chat.postMessage(...)
            ts = "1234567890.123456"  # Slack timestamp
            logger.debug(f"Slack message sent with ts: {ts}")
            return ts
        except Exception as e:
            raise DeliveryError(f"Slack delivery failed: {e}") from e


class SMSChannel:
    """Handle SMS notifications."""

    def __init__(self, config: Dict):
        self.config = config
        self.api_key = config.get('api_key')
        self.from_number = config.get('from_number')

        if not self.api_key or not self.from_number:
            raise ConfigError("SMS channel requires api_key and from_number")

    async def send(self, request: NotificationRequest) -> str:
        """Send SMS notification."""
        logger.debug(f"Sending SMS to {request.recipient}")

        message = f"{request.template}: {request.context}"

        try:
            # In real code: twilio_client.messages.create(...)
            message_id = f"sms-{hash(request.recipient)}"
            logger.debug(f"SMS sent with ID: {message_id}")
            return message_id
        except Exception as e:
            raise DeliveryError(f"SMS delivery failed: {e}") from e


# --- Example usage ---

async def main():
    """Example: Using the notification handler."""

    # Configuration
    config = {
        'channels': {
            'email': {
                'enabled': True,
                'provider': 'sendgrid',
                'api_key': 'your-sendgrid-key'
            },
            'slack': {
                'enabled': True,
                'bot_token': 'xoxb-your-token',
                'channel_id': 'C0XXXXX'
            },
            'sms': {
                'enabled': False,
                'api_key': 'your-twilio-key',
                'from_number': '+1234567890'
            }
        },
        'templates_dir': './templates',
        'retry_config': {
            'max_retries': 3,
            'backoff_base': 2
        }
    }

    # Initialize handler
    handler = NotificationHandler(config)

    # Send single notification
    email_request = NotificationRequest(
        recipient='user@example.com',
        channel=NotificationChannel.EMAIL,
        template='welcome',
        context={'name': 'John', 'signup_date': '2024-01-15'}
    )

    try:
        response = await handler.send(email_request)
        print(f"✓ {response.notification_id}: {response.status}")
    except DeliveryError as e:
        print(f"✗ Failed: {e}")

    # Send batch notifications
    requests = [
        NotificationRequest(
            recipient='user1@example.com',
            channel=NotificationChannel.EMAIL,
            template='daily_digest',
            context={'count': 5}
        ),
        NotificationRequest(
            recipient='user2@example.com',
            channel=NotificationChannel.SLACK,
            template='alert',
            context={'severity': 'high', 'message': 'API latency spike'}
        ),
    ]

    responses = await handler.send_batch(requests)
    for resp in responses:
        status_icon = "✓" if resp.status == 'sent' else "✗"
        print(f"{status_icon} {resp.recipient} ({resp.channel}): {resp.status}")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
