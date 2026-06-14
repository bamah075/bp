#!/usr/bin/env python3
"""
Maya Web UI Server - Serves the HTML interface and connects to Python backend
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from Brain.smart_brain import _smart_brain
from TextToSpeech.Fast_DF_TTS import speak
from Brain.maya_memory import get_memory_stats
import os
import json

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

@app.route('/')
def index():
    """Serve the main Maya web interface"""
    return open('maya_web_ui.html', 'r').read()

@app.route('/api/command', methods=['POST'])
def process_command():
    """Process voice/text commands and return Maya's response"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()

        if not user_input:
            return jsonify({'error': 'Empty message'}), 400

        # Process command through Maya's brain
        response = _smart_brain.process_command(user_input)

        # Optionally speak the response
        if data.get('speak', False):
            try:
                speak(response)
            except Exception as e:
                print(f"TTS Error: {e}")

        return jsonify({
            'success': True,
            'response': response,
            'timestamp': str(datetime.now())
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get system status"""
    try:
        memory_stats = get_memory_stats()
        return jsonify({
            'success': True,
            'voice': 'ready',
            'network': 'online',
            'memory': memory_stats,
            'apis': {
                'openrouter': True,
                'firecrawl': True,
                'kie_ai': True,
                'openweather': True
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/memory', methods=['GET'])
def get_memory():
    """Get memory statistics"""
    try:
        from Brain.maya_memory import _maya_memory
        return jsonify({
            'success': True,
            'stats': get_memory_stats(),
            'interactions': len(_maya_memory.interactions),
            'patterns': len(_maya_memory.learned_patterns)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Maya AI Assistant',
        'version': '1.0.0',
        'mode': 'web'
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🌟 MAYA WEB SERVER STARTING 🌟")
    print("="*60)
    print("\n📱 Web Interface: http://localhost:5000")
    print("🔌 API Endpoint: http://localhost:5000/api")
    print("\n✨ Opening in browser...\n")

    import webbrowser
    import time
    from datetime import datetime

    # Give server time to start before opening browser
    import threading
    def open_browser():
        time.sleep(1)
        try:
            webbrowser.open('http://localhost:5000')
        except:
            print("⚠️  Could not auto-open browser. Visit http://localhost:5000 manually")

    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()

    # Run Flask server
    try:
        app.run(
            host='localhost',
            port=5000,
            debug=False,
            use_reloader=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Maya Web Server shutting down...")
        print("Goodbye! 👋")
