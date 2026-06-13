#!/usr/bin/env python3
"""
Smart JARVIS Brain - Intelligent conversational AI
Provides varied responses, multiple capabilities, and natural interactions
"""

import random
import datetime
import platform
import socket
import subprocess
from datetime import datetime as dt
from .reddit_scraper import _reddit_scraper

class SmartBrain:
    def __init__(self):
        self.conversation_history = []
        self.user_name = "Sir"
        self.last_response = None
        self.response_pool = {}
        self.initialize_responses()

    def initialize_responses(self):
        """Initialize diverse response pools"""
        self.response_pool = {
            "greeting": [
                "Hello! I'm JARVIS, your AI assistant. How can I help you today?",
                "Good to see you! What would you like me to help with?",
                "Greetings! I'm ready to assist you.",
                "Hi there! What can I do for you?",
                "Hello! Ready to help. What do you need?",
            ],
            "capabilities": [
                "I can help with system information, check the weather, tell you jokes, provide facts, manage your time, and automate tasks.",
                "My capabilities include: system monitoring, time management, information retrieval, entertainment, and automation assistance.",
                "I can get system info, tell jokes, provide weather updates, manage reminders, and help with various automated tasks.",
                "I'm capable of: checking system status, retrieving information, entertainment through jokes and facts, and task automation.",
                "I can assist with: system diagnostics, time/date info, web searches, humor, facts, and automation routines.",
            ],
            "system_info": [
                f"You're running {platform.system()} {platform.release()} on a {platform.machine()} processor.",
                f"System: {platform.system()} {platform.release()} - Architecture: {platform.machine()}",
                f"Platform: {platform.system()} - Processor: {platform.machine()} - Version: {platform.release()}",
            ],
            "thanks": [
                "You're welcome! Happy to help.",
                "Glad I could assist!",
                "Anytime! Anything else?",
                "My pleasure! Let me know if you need anything else.",
                "That's what I'm here for!",
            ],
            "help": [
                "I can help you with many things. Ask me about: system info, time, jokes, weather, facts, or say 'what can you do' to learn more.",
                "Need help? I can do: system checks, time queries, jokes, facts, weather info, or any automation tasks.",
                "I'm here to help! You can ask me about system status, current time, jokes, interesting facts, and more.",
                "Ask me for: system information, current time, jokes, facts, weather, or automation help.",
            ],
            "time": [
                f"The current time is {dt.now().strftime('%I:%M %p')}.",
                f"It's currently {dt.now().strftime('%I:%M %p and %A, %B %d')}.",
                f"The time right now is {dt.now().strftime('%H:%M:%S')}.",
                f"Current time: {dt.now().strftime('%I:%M %p')} on {dt.now().strftime('%A')}.",
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
                "I'm not quite sure what you mean. Could you rephrase that?",
                "I didn't catch that. Can you say it differently?",
                "That's not something I fully understand. Can you clarify?",
                "I'm not sure about that one. Can you provide more details?",
                "That's unclear to me. Could you explain further?",
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
        }

    def get_random_response(self, key):
        """Get a random response from a pool, avoiding repeats"""
        if key not in self.response_pool:
            return None

        responses = self.response_pool[key]
        # Filter out the last response to avoid immediate repeats
        available = [r for r in responses if r != self.last_response]
        if not available:
            available = responses

        response = random.choice(available)
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
        return response

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

# Global instance
_smart_brain = SmartBrain()

def Main_Brain(text):
    """Backward compatible function"""
    return _smart_brain.process_command(text)
