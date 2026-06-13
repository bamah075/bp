#!/usr/bin/env python3
"""
Smart Employee AI - General-purpose task assistant
"""

from datetime import datetime
from typing import Dict, List

class SmartEmployee:
    def __init__(self):
        self.capabilities = {
            'document_assistance': 'Help with writing, editing, and organizing documents',
            'data_analysis': 'Analyze data and provide insights',
            'project_management': 'Help plan and track projects',
            'communication': 'Draft emails, messages, and communications',
            'research': 'Help research topics and compile information',
            'planning': 'Create plans, schedules, and strategies',
            'problem_solving': 'Help solve technical and business problems',
            'learning': 'Explain concepts and help with learning',
            'brainstorming': 'Generate ideas and creative solutions',
            'reporting': 'Create reports and summaries'
        }

        self.task_history = []
        self.completed_tasks = []

    def help_with_task(self, task_description: str) -> str:
        """Provide assistance with a task"""
        response = f"🎯 Task: {task_description}\n\n"

        # Analyze task and suggest approach
        approach = self._suggest_approach(task_description)
        response += f"📋 Suggested Approach:\n{approach}\n\n"

        # Suggest relevant capabilities
        relevant = self._find_relevant_capabilities(task_description)
        if relevant:
            response += "💡 Relevant Assistance Types:\n"
            for capability in relevant:
                description = self.capabilities.get(capability, '')
                response += f"  • {capability.replace('_', ' ').title()}: {description}\n"

        return response.strip()

    def draft_email(self, recipient: str, subject: str, purpose: str) -> str:
        """Draft an email"""
        response = f"📧 Email Draft\n\n"
        response += f"To: {recipient}\n"
        response += f"Subject: {subject}\n"
        response += f"─" * 40 + "\n\n"

        # Generate professional email
        email_body = self._generate_email_template(purpose, recipient)
        response += email_body

        return response

    def _generate_email_template(self, purpose: str, recipient: str) -> str:
        """Generate email template based on purpose"""
        templates = {
            'introduction': f"""Dear {recipient},

I hope this message finds you well. I'm reaching out to introduce myself and discuss potential opportunities for collaboration.

[Your specific message here]

I'd welcome the opportunity to discuss this further at your convenience.

Best regards,
[Your Name]""",

            'follow_up': f"""Hi {recipient},

Thank you for taking the time to [previous meeting/call]. I wanted to follow up on the points we discussed:

1. [Point 1]
2. [Point 2]
3. [Point 3]

Please let me know your thoughts on these action items.

Best regards,
[Your Name]""",

            'proposal': f"""Dear {recipient},

I'm writing to present a proposal that I believe will benefit your organization:

**Proposal Overview:**
[Summary of what you're proposing]

**Key Benefits:**
• [Benefit 1]
• [Benefit 2]
• [Benefit 3]

**Timeline:**
[When you plan to implement]

**Investment:**
[Cost/resource requirements]

I'd like to schedule a time to discuss this in detail.

Best regards,
[Your Name]""",

            'status_update': f"""Hi {recipient},

Here's a quick status update on [project/task]:

**Current Status:** On track
**Completed:** [What's done]
**In Progress:** [What's being worked on]
**Next Steps:** [What comes next]

Please let me know if you need any additional information.

Best regards,
[Your Name]"""
        }

        # Return generic professional template if purpose not recognized
        purpose_lower = purpose.lower()
        for key in templates:
            if key in purpose_lower:
                return templates[key]

        return templates['follow_up']

    def create_action_plan(self, goal: str) -> str:
        """Create an action plan for a goal"""
        response = f"🎯 Action Plan: {goal}\n\n"
        response += f"Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        response += "Phase 1: Planning (Week 1)\n"
        response += "  1. Define clear objectives\n"
        response += "  2. Identify resources needed\n"
        response += "  3. Create detailed timeline\n"
        response += "  4. Assign responsibilities\n\n"

        response += "Phase 2: Implementation (Week 2-4)\n"
        response += "  1. Execute planned tasks\n"
        response += "  2. Monitor progress\n"
        response += "  3. Address obstacles\n"
        response += "  4. Maintain communication\n\n"

        response += "Phase 3: Review & Adjust (Week 5)\n"
        response += "  1. Measure results\n"
        response += "  2. Gather feedback\n"
        response += "  3. Make adjustments\n"
        response += "  4. Plan next steps\n\n"

        response += "📊 Success Metrics:\n"
        response += "  ☐ Objective 1: [Measure]\n"
        response += "  ☐ Objective 2: [Measure]\n"
        response += "  ☐ Objective 3: [Measure]\n"

        return response.strip()

    def analyze_data(self, data_description: str) -> str:
        """Provide data analysis guidance"""
        response = f"📊 Data Analysis: {data_description}\n\n"

        response += "Analysis Framework:\n\n"

        response += "1. **Data Collection**\n"
        response += "   • What data do you have?\n"
        response += "   • What format is it in?\n"
        response += "   • Is the data complete?\n\n"

        response += "2. **Data Cleaning**\n"
        response += "   • Remove duplicates\n"
        response += "   • Handle missing values\n"
        response += "   • Standardize formats\n\n"

        response += "3. **Exploratory Analysis**\n"
        response += "   • Summary statistics\n"
        response += "   • Identify patterns\n"
        response += "   • Find outliers\n\n"

        response += "4. **Key Insights**\n"
        response += "   • What stands out?\n"
        response += "   • What correlations exist?\n"
        response += "   • What's the story in the data?\n\n"

        response += "5. **Recommendations**\n"
        response += "   • Action items based on insights\n"
        response += "   • Further investigation needed?\n"

        return response.strip()

    def brainstorm_ideas(self, topic: str, context: str = None) -> str:
        """Generate ideas for a topic"""
        response = f"💡 Brainstorm: {topic}\n\n"

        response += "Creative Approaches:\n\n"

        response += "1. **Traditional Method**\n"
        response += "   • Follow proven approaches\n"
        response += "   • Build on existing success\n\n"

        response += "2. **Innovative Approach**\n"
        response += "   • Challenge assumptions\n"
        response += "   • Combine unexpected elements\n\n"

        response += "3. **Collaborative Approach**\n"
        response += "   • Involve different perspectives\n"
        response += "   • Cross-functional ideas\n\n"

        response += "4. **Gradual Approach**\n"
        response += "   • Pilot test ideas\n"
        response += "   • Iterate and improve\n\n"

        response += "5. **Bold Approach**\n"
        response += "   • Think big\n"
        response += "   • Consider future possibilities\n\n"

        response += "🎯 Evaluation Criteria:\n"
        response += "  • Feasibility\n"
        response += "  • Impact\n"
        response += "  • Resources needed\n"
        response += "  • Timeline\n"
        response += "  • Risk level\n"

        return response.strip()

    def problem_solver(self, problem: str) -> str:
        """Help solve a problem"""
        response = f"🔧 Problem Solving: {problem}\n\n"

        response += "Problem-Solving Framework:\n\n"

        response += "1. **Understand the Problem**\n"
        response += "   • What exactly is happening?\n"
        response += "   • What are the symptoms?\n"
        response += "   • What's the impact?\n\n"

        response += "2. **Root Cause Analysis**\n"
        response += "   • Why is this happening?\n"
        response += "   • What triggered it?\n"
        response += "   • Are there related issues?\n\n"

        response += "3. **Generate Solutions**\n"
        response += "   • Quick fixes\n"
        response += "   • Long-term solutions\n"
        response += "   • Prevention measures\n\n"

        response += "4. **Evaluate Options**\n"
        response += "   • Pros and cons\n"
        response += "   • Resource requirements\n"
        response += "   • Timeline\n\n"

        response += "5. **Implement Solution**\n"
        response += "   • Create action plan\n"
        response += "   • Assign responsibilities\n"
        response += "   • Monitor results\n"

        return response.strip()

    def _suggest_approach(self, task: str) -> str:
        """Suggest an approach for a task"""
        return """1. Break the task into smaller components
2. Identify the primary objective
3. Determine required resources
4. Create a timeline
5. Identify potential challenges
6. Plan mitigation strategies
7. Execute step by step
8. Monitor and adjust"""

    def _find_relevant_capabilities(self, description: str) -> List[str]:
        """Find relevant capabilities for a task"""
        description_lower = description.lower()
        relevant = []

        keywords = {
            'document_assistance': ['write', 'email', 'letter', 'document', 'edit'],
            'data_analysis': ['analyze', 'data', 'statistics', 'metrics', 'report'],
            'project_management': ['project', 'plan', 'schedule', 'timeline', 'track'],
            'communication': ['communicate', 'message', 'email', 'present', 'speak'],
            'research': ['research', 'find', 'investigate', 'learn', 'study'],
            'planning': ['plan', 'strategy', 'schedule', 'organize'],
            'problem_solving': ['problem', 'issue', 'solve', 'fix', 'troubleshoot'],
            'brainstorming': ['idea', 'brainstorm', 'creative', 'innovative'],
        }

        for capability, keywords_list in keywords.items():
            if any(kw in description_lower for kw in keywords_list):
                relevant.append(capability)

        return relevant[:3]  # Return top 3

# Global instance
_smart_employee = SmartEmployee()

def help_with(task: str):
    return _smart_employee.help_with_task(task)

def draft_email(recipient: str, subject: str, purpose: str):
    return _smart_employee.draft_email(recipient, subject, purpose)

def create_plan(goal: str):
    return _smart_employee.create_action_plan(goal)

def analyze(data_description: str):
    return _smart_employee.analyze_data(data_description)

def brainstorm(topic: str, context: str = None):
    return _smart_employee.brainstorm_ideas(topic, context)

def solve_problem(problem: str):
    return _smart_employee.problem_solver(problem)
