#!/usr/bin/env python3
"""
Automation Helper - Integration with Claude, GitHub Copilot, GoHighLevel, Zapier
"""

import requests
import os
from typing import Dict, List

class AutomationHelper:
    def __init__(self):
        self.claude_api_key = os.getenv('CLAUDE_API_KEY', None)
        self.copilot_api_key = os.getenv('COPILOT_API_KEY', None)
        self.ghl_api_key = os.getenv('GHL_API_KEY', None)
        self.zapier_webhook = os.getenv('ZAPIER_WEBHOOK', None)

        self.automation_templates = {
            'email_automation': {
                'description': 'Automate email sending and follow-ups',
                'platforms': ['Zapier', 'GoHighLevel'],
                'steps': ['Define trigger', 'Create email template', 'Set conditions', 'Deploy']
            },
            'lead_capture': {
                'description': 'Capture and qualify leads automatically',
                'platforms': ['GoHighLevel', 'Zapier'],
                'steps': ['Setup form', 'Define qualification', 'Auto-response', 'CRM integration']
            },
            'workflow_automation': {
                'description': 'Automate repetitive business workflows',
                'platforms': ['Zapier', 'Make'],
                'steps': ['Map workflow', 'Identify triggers', 'Create actions', 'Test']
            },
            'data_sync': {
                'description': 'Keep data synchronized across platforms',
                'platforms': ['Zapier'],
                'steps': ['Connect apps', 'Map fields', 'Set sync frequency', 'Monitor']
            },
            'code_automation': {
                'description': 'Generate and suggest code improvements',
                'platforms': ['GitHub Copilot', 'Claude'],
                'steps': ['Write prompt', 'Get suggestions', 'Review code', 'Apply']
            }
        }

    def get_automation_suggestion(self, task_description: str) -> str:
        """Get automation suggestion for a task"""
        response = f"🤖 Automation Suggestion for: {task_description}\n\n"

        matching_templates = self._find_matching_templates(task_description)

        if matching_templates:
            for template_name, template in matching_templates:
                response += f"📌 {template_name.replace('_', ' ').title()}\n"
                response += f"   Description: {template['description']}\n"
                response += f"   Platforms: {', '.join(template['platforms'])}\n"
                response += f"   Steps:\n"
                for i, step in enumerate(template['steps'], 1):
                    response += f"     {i}. {step}\n"
                response += "\n"
        else:
            response += "I can help automate this! Describe the specific workflow you want to automate, and I'll guide you through the setup.\n\n"
            response += "Available automation types:\n"
            for name in self.automation_templates.keys():
                response += f"  • {name.replace('_', ' ').title()}\n"

        return response.strip()

    def _find_matching_templates(self, description: str) -> List[tuple]:
        """Find matching automation templates"""
        description_lower = description.lower()
        matches = []

        keywords = {
            'email_automation': ['email', 'send', 'newsletter', 'campaign'],
            'lead_capture': ['lead', 'capture', 'form', 'qualify'],
            'workflow_automation': ['workflow', 'process', 'automate', 'task'],
            'data_sync': ['sync', 'data', 'integrate', 'connect'],
            'code_automation': ['code', 'generate', 'script', 'function']
        }

        for template_name, keywords_list in keywords.items():
            if any(keyword in description_lower for keyword in keywords_list):
                matches.append((template_name, self.automation_templates[template_name]))

        return matches

    def claude_automation_help(self, prompt: str) -> str:
        """Get help from Claude for automation"""
        if not self.claude_api_key:
            return "⚠️ Claude API key not configured. Set CLAUDE_API_KEY environment variable.\n\nDespite this, here's my suggestion for your automation request:\n" + self._provide_local_guidance(prompt)

        try:
            # This is a placeholder - actual Claude API integration would go here
            response = f"🤖 Claude's Automation Advice:\n\n{self._provide_local_guidance(prompt)}"
            return response
        except Exception as e:
            return f"Error contacting Claude: {str(e)}\n\nLocal suggestion: {self._provide_local_guidance(prompt)}"

    def copilot_code_help(self, code_snippet: str, task: str) -> str:
        """Get code suggestions from GitHub Copilot"""
        response = f"💡 Code Automation Suggestion for: {task}\n\n"

        if not self.copilot_api_key:
            response += "⚠️ Copilot API key not configured.\n\n"

        response += "Here's an approach to automate this:\n\n"
        response += "1. **Analyze the pattern**: Identify repetitive code blocks\n"
        response += "2. **Extract to function**: Create reusable functions\n"
        response += "3. **Use loops/conditions**: Replace repetition with logic\n"
        response += "4. **Consider libraries**: Use existing automation libraries\n"
        response += "5. **Test thoroughly**: Ensure automated solution works correctly\n\n"
        response += "Common automation techniques:\n"
        response += "  • Generators and iterators\n"
        response += "  • Decorators for repeated logic\n"
        response += "  • Abstract base classes\n"
        response += "  • Context managers\n"

        return response

    def ghl_automation(self, automation_type: str) -> str:
        """Get GoHighLevel automation setup"""
        ghl_automations = {
            'lead_scoring': {
                'steps': [
                    'Set up custom fields for lead attributes',
                    'Create automation workflow in GHL',
                    'Define scoring rules (contact, engagement, purchase)',
                    'Set threshold for qualified leads',
                    'Auto-assign to sales team'
                ]
            },
            'email_sequences': {
                'steps': [
                    'Create email templates',
                    'Define trigger events',
                    'Set timing between emails',
                    'Add personalization tokens',
                    'Monitor performance'
                ]
            },
            'appointment_automation': {
                'steps': [
                    'Setup calendar integration',
                    'Create appointment booking flows',
                    'Set availability rules',
                    'Configure reminders',
                    'Enable automated follow-ups'
                ]
            },
            'sms_campaigns': {
                'steps': [
                    'Create SMS templates',
                    'Define subscriber segments',
                    'Set send times',
                    'Enable two-way messaging',
                    'Track engagement metrics'
                ]
            }
        }

        if automation_type.lower() in ghl_automations:
            automation = ghl_automations[automation_type.lower()]
            response = f"🚀 GoHighLevel: {automation_type.replace('_', ' ').title()}\n\n"
            response += "Setup Steps:\n"
            for i, step in enumerate(automation['steps'], 1):
                response += f"  {i}. {step}\n"
            return response
        else:
            available = list(ghl_automations.keys())
            return f"Available GHL automations: {', '.join([a.replace('_', ' ').title() for a in available])}"

    def zapier_automation_guide(self, from_app: str, to_app: str, action: str) -> str:
        """Guide for Zapier automation"""
        response = f"⚡ Zapier Automation: {from_app} → {to_app}\n\n"
        response += f"Action: {action}\n\n"
        response += "Setup Steps:\n"
        response += "  1. Create Zap in Zapier.com\n"
        response += f"  2. Select trigger: {from_app}\n"
        response += "  3. Connect your account and choose event\n"
        response += f"  4. Select action app: {to_app}\n"
        response += f"  5. Configure action: {action}\n"
        response += "  6. Map fields between apps\n"
        response += "  7. Test the Zap\n"
        response += "  8. Turn on and monitor\n\n"
        response += "💡 Tips:\n"
        response += "  • Use Zapier formatter for data transformation\n"
        response += "  • Test with sample data first\n"
        response += "  • Set up error notifications\n"
        response += "  • Monitor usage for plan limits\n"

        return response

    def _provide_local_guidance(self, prompt: str) -> str:
        """Provide local guidance without API"""
        return """Automation Strategy:

1. **Identify the bottleneck**: What's slowing you down?
2. **Map the workflow**: Document each step
3. **Find integration points**: Where can automation help?
4. **Choose the right tool**:
   - Simple tasks → Zapier
   - CRM workflows → GoHighLevel
   - Code generation → GitHub Copilot
   - Complex logic → Claude AI
5. **Test in stages**: Implement gradually
6. **Monitor results**: Track automation metrics

Would you like specific guidance on any of these areas?"""

    def get_automation_status(self) -> str:
        """Get status of configured automations"""
        status = "🔧 Automation Status:\n\n"

        apis = {
            'Claude API': self.claude_api_key,
            'GitHub Copilot': self.copilot_api_key,
            'GoHighLevel': self.ghl_api_key,
            'Zapier': self.zapier_webhook
        }

        for api_name, key in apis.items():
            status_icon = "✓" if key else "✗"
            status += f"  {status_icon} {api_name}: {'Configured' if key else 'Not configured'}\n"

        return status

# Global instance
_automation_helper = AutomationHelper()

def get_automation_suggestion(task: str):
    return _automation_helper.get_automation_suggestion(task)

def claude_help(prompt: str):
    return _automation_helper.claude_automation_help(prompt)

def copilot_help(code: str, task: str):
    return _automation_helper.copilot_code_help(code, task)

def ghl_setup(automation_type: str):
    return _automation_helper.ghl_automation(automation_type)

def zapier_setup(from_app: str, to_app: str, action: str):
    return _automation_helper.zapier_automation_guide(from_app, to_app, action)
