#!/usr/bin/env python3
"""
Smart Maya Brain - Intelligent conversational AI
Provides varied responses, multiple capabilities, and natural interactions
"""

import random
import datetime
import platform
import socket
import subprocess
from datetime import datetime as dt
from .reddit_scraper import _reddit_scraper
from .meeting_notes import _meeting_notes
from .calendar_manager import _calendar
from .automation_helper import _automation_helper
from .smart_employee import _smart_employee
from .maya_memory import _maya_memory

class SmartBrain:
    def __init__(self, user_name="bamah"):
        self.conversation_history = []
        self.user_name = user_name
        self.last_response = None
        self.last_responses = {}  # Track last response per category
        self.response_pool = {}
        self.initialize_responses()

    def initialize_responses(self):
        """Initialize diverse response pools"""
        self.response_pool = {
            "greeting": [
                f"Hey bamah!",
                f"Hi bamah!",
                f"Hello!",
                f"What's up?",
                f"Ready to help!",
            ],
            "capabilities": [
                "Meetings, tasks, calendar, automation, planning, analysis, brainstorming, research.",
                "I do: meetings, calendar, tasks, automation guides, planning, analysis, brainstorming.",
                "Meeting management, task/calendar tracking, automation help, planning, analysis.",
                "Meetings, tasks, automation, planning, brainstorming, analysis, research.",
                "Calendar, meetings, tasks, automation, planning, analysis, brainstorming.",
            ],
            "system_info": [
                f"You're running {platform.system()} {platform.release()} on a {platform.machine()} processor.",
                f"System: {platform.system()} {platform.release()} - Architecture: {platform.machine()}",
                f"Platform: {platform.system()} - Processor: {platform.machine()} - Version: {platform.release()}",
            ],
            "thanks": [
                "Welcome!",
                "Got it!",
                "Anytime!",
                "Happy to help!",
                "No problem!",
            ],
            "help": [
                "Ask me about: meetings, tasks, calendar, automation, planning, analysis, brainstorming.",
                "I can help with meetings, tasks, calendar, automation, planning, research.",
                "Ask for: tasks, calendar, meetings, automation, planning, analysis.",
                "I help with: meetings, calendar, tasks, automation, planning, research.",
            ],
            "time": [
                lambda: f"The current time is {dt.now().strftime('%I:%M %p')}.",
                lambda: f"It's {dt.now().strftime('%I:%M %p')} on {dt.now().strftime('%A, %B %d')}.",
                lambda: f"Right now it's {dt.now().strftime('%H:%M:%S')} ({dt.now().strftime('%A')}).",
                lambda: f"Current time: {dt.now().strftime('%I:%M %p')} - {dt.now().strftime('%A')}.",
                lambda: f"The time is {dt.now().strftime('%I:%M %p')} on this {dt.now().strftime('%A')}.",
            ],
            "joke": [
                "Why did the AI go to school? To improve its neural network!",
                "What do you call an AI that tells jokes? A funny algorithm!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
                "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
                "Why do Java developers wear glasses? Because they don't C#!",
                "A SQL query walks into a bar, walks up to two tables and asks... 'Can I join you?'",
                "Why did the developer go broke? Because he used up all his cache!",
                "How do you know if there's a programmer in your office? They complain about the wifi instead of the coffee!",
            ],
            "fact": [
                "Did you know? Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs that was still edible!",
                "Fun fact: A group of flamingos is called a 'flamboyance'!",
                "Did you know? Octopuses have three hearts - two pump blood to the gills, one pumps it to the rest of the body!",
                "Fun fact: Bananas are berries, but strawberries aren't - botanically speaking!",
                "Did you know? Your nose can remember 50,000 different scents!",
                "Fun fact: The heart of a blue whale is the size of a small car!",
                "Did you know? Cleopatra lived closer to the invention of the iPhone than to the building of the Great Pyramid!",
            ],
            "affirmative": [
                "Understood!",
                "Got it!",
                "Will do!",
                "Right away!",
                "Absolutely!",
            ],
            "confused": [
                "Not sure. Can you rephrase?",
                "Didn't catch that. Try again?",
                "Unclear. What do you mean?",
                "Say that differently?",
                "I don't get it. More details?",
            ],
            "reddit_search": [
                "Let me search Reddit for that information.",
                "I'll look that up on Reddit for you.",
                "Searching Reddit for relevant discussions...",
                "Let me find what people are discussing about that.",
            ],
            "reddit_small_business": [
                "Searching for Australian small business automation topics on Reddit...",
                "Looking up small business pain points and automation solutions...",
                "Fetching relevant discussions from the Australian subreddit...",
            ],
            "meeting_start": [
                "Starting a new meeting. Ready to capture notes.",
                "Let's begin the meeting. I'll track notes and action items.",
                "Meeting initialized. You can now add notes and decisions.",
            ],
            "meeting_end": [
                "Meeting concluded. Here's your summary:",
                "Meeting finished. Summary prepared:",
                "All done! Here's what we covered:",
            ],
            "calendar_check": [
                "Checking your schedule...",
                "Pulling up your calendar...",
                "Let me show you what's on your plate...",
            ],
            "automation_help": [
                "Let me help you automate that.",
                "I can guide you through the automation setup.",
                "Let's figure out the best way to automate this.",
            ],
            "employee_assist": [
                "Happy to help with that task.",
                "I'm here to assist. Let me break this down for you.",
                "Let's work through this together.",
            ],
        }

    def get_random_response(self, key):
        """Get a random response from a pool, NEVER repeating the last one"""
        if key not in self.response_pool:
            return None

        responses = self.response_pool[key]
        if not responses or len(responses) < 2:
            selected = random.choice(responses) if responses else None
            return selected() if callable(selected) else selected

        # Get the last response template used for this category
        last_response_template = self.last_responses.get(key, None)

        # Filter out the last used response template
        available = [r for r in responses if r != last_response_template]

        # If all filtered out, use all options
        if not available:
            available = responses

        # Pick a random response template
        response_template = random.choice(available)

        # Store the template (not the generated response)
        self.last_responses[key] = response_template

        # Generate the actual response (handle callables for dynamic content)
        response = response_template() if callable(response_template) else response_template
        self.last_response = response

        return response

    def get_system_info(self):
        """Get detailed system information"""
        try:
            info = {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "hostname": socket.gethostname(),
            }
            return f"System: {info['system']} {info['release']} | Machine: {info['machine']} | Hostname: {info['hostname']}"
        except:
            return self.get_random_response("system_info")

    def get_network_info(self):
        """Get network information"""
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            return f"Your hostname is {hostname} and your IP address is {ip_address}."
        except:
            return "I'm unable to retrieve network information at the moment."

    def get_time_info(self):
        """Get current time with more details"""
        now = dt.now()
        day_name = now.strftime("%A")
        date_str = now.strftime("%B %d, %Y")
        time_str = now.strftime("%I:%M %p")
        return f"It's {time_str} on {day_name}, {date_str}."

    def process_command(self, text):
        """Process voice command and return intelligent response"""
        text_lower = text.lower().strip()

        # Add to conversation history
        self.conversation_history.append(("user", text))

        # Determine category for learning
        category = self._determine_category(text_lower)

        # Greeting patterns
        if any(word in text_lower for word in ["hello", "hi", "hey", "greetings"]):
            response = self.get_random_response("greeting")

        # Capability queries
        elif any(word in text_lower for word in ["what can you do", "capabilities", "what are you capable of", "features"]):
            response = self.get_random_response("capabilities")

        # System info queries
        elif any(word in text_lower for word in ["what system", "what os", "what platform", "system info", "operating system"]):
            response = self.get_system_info()

        # Network/IP queries
        elif any(word in text_lower for word in ["ip address", "network", "hostname", "ip"]):
            response = self.get_network_info()

        # Time queries
        elif any(word in text_lower for word in ["what time", "current time", "time", "what's the time", "date"]):
            response = self.get_time_info()

        # Tell me a joke
        elif any(word in text_lower for word in ["joke", "funny", "make me laugh", "tell joke", "humor"]):
            response = f"Here's one: {self.get_random_response('joke')}"

        # Tell me a fact
        elif any(word in text_lower for word in ["fact", "interesting", "did you know", "tell me something"]):
            response = f"Here's an interesting fact: {self.get_random_response('fact')}"

        # Help
        elif any(word in text_lower for word in ["help", "assist", "guide", "how do i"]):
            response = self.get_random_response("help")

        # Thank you
        elif any(word in text_lower for word in ["thank", "thanks", "appreciate", "thankyou"]):
            response = self.get_random_response("thanks")

        # Affirmations
        elif any(word in text_lower for word in ["yes", "sure", "okay", "ok", "yes please"]):
            response = self.get_random_response("affirmative")

        # Meeting notes management
        elif any(phrase in text_lower for phrase in ["start meeting", "begin meeting", "new meeting"]):
            response = self.get_random_response("meeting_start")
            _meeting_notes.start_meeting()

        elif any(phrase in text_lower for phrase in ["end meeting", "stop meeting", "finish meeting", "meeting summary"]):
            response = self.get_random_response("meeting_end")
            summary = _meeting_notes.end_meeting()
            if isinstance(summary, dict) and 'summary_text' in summary:
                response = f"{response}\n\n{summary['summary_text']}"
            else:
                response += "\n\nNo active meeting to end."

        elif any(phrase in text_lower for phrase in ["add note", "note that", "write down", "remember this", "we discussed", "noted"]):
            # Extract note content - be smarter about it
            note_text = text_lower
            for phrase in ["add note", "note that", "write down", "remember this"]:
                note_text = note_text.replace(phrase, "").strip()
            response = _meeting_notes.add_note(note_text or text)

        elif any(phrase in text_lower for phrase in ["action item", "assign task", "who does"]):
            response = _meeting_notes.get_active_meeting_status()

        # Calendar and reminders - CHECK VIEW FIRST
        elif any(phrase in text_lower for phrase in ["what's my schedule", "show my schedule", "today's schedule", "what do i have today", "my appointments"]):
            response = self.get_random_response("calendar_check")
            response = f"{response}\n\n{_calendar.get_today_schedule()}"

        elif any(phrase in text_lower for phrase in ["week summary", "what's this week", "weekly overview"]):
            response = f"Let me show you your week:\n\n{_calendar.get_week_summary()}"

        elif any(phrase in text_lower for phrase in ["my tasks", "to-do", "todo list", "what tasks do i have"]):
            response = _calendar.list_todos()

        elif any(phrase in text_lower for phrase in ["add appointment", "book meeting", "schedule appointment", "add appointment"]):
            response = f"I can help you schedule that. Please provide: title, date (YYYY-MM-DD), and time (HH:MM)"

        elif any(phrase in text_lower for phrase in ["add task", "add todo", "add to my list", "new task"]):
            task_text = text_lower.replace("add task", "").replace("add todo", "").replace("add to my list", "").replace("new task", "").strip()
            response = _calendar.add_todo(task_text or "Untitled task", priority="medium")

        elif any(phrase in text_lower for phrase in ["set reminder", "remind me", "schedule reminder"]):
            response = "I can set a reminder. Please provide: message, date (YYYY-MM-DD), and time (HH:MM)"

        # Automation help
        elif any(phrase in text_lower for phrase in ["automate", "automation", "zapier", "goHighLevel", "ghl", "copilot", "workflow"]):
            response = self.get_random_response("automation_help")
            # Extract the automation request
            automation_request = text_lower
            suggestion = _automation_helper.get_automation_suggestion(automation_request)
            response = f"{response}\n\n{suggestion}"

        # Smart Employee assistance
        elif any(phrase in text_lower for phrase in ["help with", "assist with", "help me", "can you help", "i need help", "draft email", "write email"]):
            response = self.get_random_response("employee_assist")

            if any(word in text_lower for word in ["email", "draft", "write"]):
                response = "I can help draft an email. Please provide: recipient name, subject, and purpose."
            elif any(word in text_lower for word in ["plan", "goal", "objective"]):
                goal = text_lower.replace("help with", "").replace("plan", "").strip()
                plan = _smart_employee.create_action_plan(goal or "your goal")
                response = f"{response}\n\n{plan}"
            elif any(word in text_lower for word in ["analyze", "data"]):
                response = f"{response}\n\n{_smart_employee.analyze_data('your data')}"
            elif any(word in text_lower for word in ["problem", "issue", "trouble"]):
                problem = text_lower.replace("help with", "").strip()
                response = f"{response}\n\n{_smart_employee.problem_solver(problem or 'this problem')}"
            elif any(word in text_lower for word in ["brainstorm", "ideas", "creative"]):
                topic = text_lower.replace("brainstorm", "").replace("ideas", "").strip()
                response = f"{response}\n\n{_smart_employee.brainstorm_ideas(topic or 'your topic')}"
            else:
                task = text_lower.replace("help with", "").replace("assist with", "").strip()
                response = f"{response}\n\n{_smart_employee.help_with_task(task or 'this task')}"

        # Reddit searches - small business automation
        elif any(phrase in text_lower for phrase in ["reddit", "search reddit", "small business", "automation pain", "australian small business"]):
            response = self.get_random_response("reddit_small_business")
            # Fetch actual Reddit data
            try:
                reddit_results = _reddit_scraper.get_formatted_results(
                    "small business automation Australia",
                    limit=3
                )
                response = f"{response}\n\n{reddit_results}"
            except Exception as e:
                response += "\n\nI found some discussions on Reddit about small business automation in Australia, though I'm having trouble fetching the latest posts at the moment."

        # Default - confused
        else:
            response = self.get_random_response("confused")

        # Add to history
        self.conversation_history.append(("jarvis", response))

        # Remember this interaction for learning
        try:
            _maya_memory.remember_interaction(text, response, category=category)
        except Exception as e:
            pass  # Memory system is optional

        return response

    def _determine_category(self, text_lower):
        """Determine the category of the question for learning"""
        if any(word in text_lower for word in ["meeting", "note", "action"]):
            return "meeting"
        elif any(word in text_lower for word in ["task", "schedule", "calendar", "appointment"]):
            return "calendar"
        elif any(word in text_lower for word in ["automate", "zapier", "workflow"]):
            return "automation"
        elif any(word in text_lower for word in ["help", "plan", "analyze", "draft"]):
            return "smart_employee"
        elif any(word in text_lower for word in ["joke", "funny", "laugh"]):
            return "entertainment"
        elif any(word in text_lower for word in ["fact", "interesting", "know"]):
            return "facts"
        elif any(word in text_lower for word in ["time", "date", "when"]):
            return "time"
        elif any(word in text_lower for word in ["system", "platform", "machine"]):
            return "system_info"
        else:
            return "general"

    def get_conversation_summary(self):
        """Get summary of conversation"""
        return len(self.conversation_history)

    def reset(self):
        """Reset conversation history"""
        self.conversation_history = []
        self.last_response = None

def process_command(text):
    """Global function for backward compatibility"""
    brain = SmartBrain()
    return brain.process_command(text)

# Global instance with user name
_smart_brain = SmartBrain(user_name="bamah")

def Main_Brain(text):
    """Backward compatible function"""
    return _smart_brain.process_command(text)
