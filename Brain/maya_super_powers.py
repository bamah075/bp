#!/usr/bin/env python3
"""
Maya Super Powers - Advanced API Integration
Connects to OpenRouter, Firecrawl, Kie.ai, and OpenWeather
"""

import os
import requests
from typing import Dict, List, Optional

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

class MayaSuperPowers:
    """Advanced capabilities using external APIs"""

    def __init__(self):
        self.openrouter_key = os.getenv('OPENROUTER_API_KEY')
        self.firecrawl_key = os.getenv('FIRECRAWL_API_KEY')
        self.kie_key = os.getenv('KIE_API_KEY')
        self.weather_key = os.getenv('OPENWEATHER_API_KEY')

        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.firecrawl_url = "https://api.firecrawl.dev/v0"
        self.weather_url = "https://api.openweathermap.org/data/2.5"

    # ==================== OPENROUTER - Advanced AI ====================

    def advanced_reasoning(self, question: str, context: str = None) -> str:
        """Use OpenRouter for advanced AI reasoning"""
        if not self.openrouter_key:
            return "⚠️ OpenRouter not configured. Set OPENROUTER_API_KEY."

        try:
            prompt = f"{context}\n\nQuestion: {question}" if context else question

            response = requests.post(
                self.openrouter_url,
                headers={
                    "Authorization": f"Bearer {self.openrouter_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/gpt-4-turbo",
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                timeout=30
            )

            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return f"Error: {response.status_code} - {response.text[:100]}"

        except Exception as e:
            return f"Error: {str(e)}"

    # ==================== FIRECRAWL - Web Scraping ====================

    def scrape_website(self, url: str) -> Dict:
        """Scrape website content using Firecrawl"""
        if not self.firecrawl_key:
            return {"error": "Firecrawl not configured. Set FIRECRAWL_API_KEY."}

        try:
            response = requests.post(
                f"{self.firecrawl_url}/scrape",
                headers={
                    "Authorization": f"Bearer {self.firecrawl_key}",
                    "Content-Type": "application/json",
                },
                json={"url": url},
                timeout=30
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}"}

        except Exception as e:
            return {"error": str(e)}

    def extract_data(self, url: str) -> Dict:
        """Extract structured data from website"""
        if not self.firecrawl_key:
            return {"error": "Firecrawl not configured"}

        try:
            response = requests.post(
                f"{self.firecrawl_url}/extract",
                headers={
                    "Authorization": f"Bearer {self.firecrawl_key}",
                },
                json={
                    "url": url,
                    "prompt": "Extract all structured data"
                },
                timeout=30
            )

            return response.json() if response.status_code == 200 else {"error": response.text}

        except Exception as e:
            return {"error": str(e)}

    # ==================== KIE.AI - Document Intelligence ====================

    def analyze_document(self, document_path: str) -> Dict:
        """Analyze document using Kie.ai"""
        if not self.kie_key:
            return {"error": "Kie.ai not configured. Set KIE_API_KEY."}

        try:
            with open(document_path, 'rb') as f:
                response = requests.post(
                    "https://api.kie.ai/v1/documents",
                    headers={"Authorization": f"Bearer {self.kie_key}"},
                    files={"document": f},
                    timeout=30
                )

            return response.json() if response.status_code == 200 else {"error": response.text}

        except Exception as e:
            return {"error": str(e)}

    # ==================== OPENWEATHER - Real Weather Data ====================

    def get_weather(self, city: str) -> str:
        """Get real weather data"""
        if not self.weather_key:
            return "⚠️ Weather API not configured. Set OPENWEATHER_API_KEY."

        try:
            response = requests.get(
                f"{self.weather_url}/weather",
                params={
                    "q": city,
                    "appid": self.weather_key,
                    "units": "metric"
                },
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                return f"Weather in {city}: {temp}°C, {description.title()}, {humidity}% humidity"
            else:
                return f"Could not get weather for {city}"

        except Exception as e:
            return f"Error: {str(e)}"

    def get_forecast(self, city: str, days: int = 5) -> str:
        """Get weather forecast"""
        if not self.weather_key:
            return "⚠️ Weather API not configured."

        try:
            # Get coordinates first
            geo_response = requests.get(
                "https://api.openweathermap.org/geo/1.0/direct",
                params={
                    "q": city,
                    "appid": self.weather_key,
                    "limit": 1
                },
                timeout=10
            )

            if not geo_response.json():
                return f"City '{city}' not found"

            lat, lon = geo_response.json()[0]['lat'], geo_response.json()[0]['lon']

            forecast_response = requests.get(
                f"{self.weather_url}/forecast",
                params={
                    "lat": lat,
                    "lon": lon,
                    "appid": self.weather_key,
                    "units": "metric"
                },
                timeout=10
            )

            if forecast_response.status_code == 200:
                data = forecast_response.json()
                forecast = "5-Day Forecast:\n"
                for item in data['list'][::8]:  # Every 24 hours
                    dt = item['dt_txt'].split()[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast += f"  {dt}: {temp}°C, {desc.title()}\n"
                return forecast
            else:
                return "Could not get forecast"

        except Exception as e:
            return f"Error: {str(e)}"

    # ==================== SUMMARY ====================

    def get_status(self) -> str:
        """Show which APIs are configured"""
        status = "🚀 MAYA SUPER POWERS STATUS:\n\n"

        status += f"OpenRouter (Advanced AI): {'✅' if self.openrouter_key else '❌'}\n"
        status += f"Firecrawl (Web Scraping): {'✅' if self.firecrawl_key else '❌'}\n"
        status += f"Kie.ai (Document AI): {'✅' if self.kie_key else '❌'}\n"
        status += f"OpenWeather (Real Weather): {'✅' if self.weather_key else '❌'}\n"

        return status

# Global instance
_maya_super = MayaSuperPowers()

def get_advanced_answer(question: str) -> str:
    """Get advanced answer using OpenRouter"""
    return _maya_super.advanced_reasoning(question)

def get_weather(city: str) -> str:
    """Get current weather"""
    return _maya_super.get_weather(city)

def get_forecast(city: str) -> str:
    """Get weather forecast"""
    return _maya_super.get_forecast(city)

def scrape_website(url: str) -> Dict:
    """Scrape a website"""
    return _maya_super.scrape_website(url)

def analyze_document(path: str) -> Dict:
    """Analyze a document"""
    return _maya_super.analyze_document(path)

def super_powers_status() -> str:
    """Check which super powers are enabled"""
    return _maya_super.get_status()
