#!/usr/bin/env python3
"""
Meeting Notes Module - Capture, transcribe, summarize meetings
"""

import json
from datetime import datetime
from typing import List, Dict

class MeetingNotes:
    def __init__(self):
        self.current_meeting = None
        self.meetings_history = []
        self.meeting_started = False

    def start_meeting(self, title: str = None, attendees: List[str] = None):
        """Start capturing a new meeting"""
        self.current_meeting = {
            'title': title or f"Meeting {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            'start_time': datetime.now().isoformat(),
            'attendees': attendees or [],
            'notes': [],
            'action_items': [],
            'decisions': [],
        }
        self.meeting_started = True
        return f"Meeting '{self.current_meeting['title']}' started. Ready to capture notes."

    def add_note(self, note: str):
        """Add a note to the current meeting"""
        if not self.meeting_started:
            return "No active meeting. Start a meeting first with 'start meeting'"

        self.current_meeting['notes'].append({
            'text': note,
            'timestamp': datetime.now().isoformat()
        })
        return f"Note added: {note}"

    def add_action_item(self, action: str, owner: str = None, due_date: str = None):
        """Add an action item to the current meeting"""
        if not self.meeting_started:
            return "No active meeting. Start a meeting first."

        self.current_meeting['action_items'].append({
            'action': action,
            'owner': owner or 'Unassigned',
            'due_date': due_date or 'Not specified',
            'status': 'open',
            'created': datetime.now().isoformat()
        })
        return f"Action item added: {action} (Owner: {owner or 'Unassigned'})"

    def add_decision(self, decision: str):
        """Add a decision made during the meeting"""
        if not self.meeting_started:
            return "No active meeting."

        self.current_meeting['decisions'].append({
            'decision': decision,
            'timestamp': datetime.now().isoformat()
        })
        return f"Decision recorded: {decision}"

    def end_meeting(self) -> Dict:
        """End the current meeting and return summary"""
        if not self.meeting_started:
            return {'error': 'No active meeting to end'}

        # Save to history
        self.meetings_history.append(self.current_meeting)

        summary = self._generate_summary(self.current_meeting)
        self.meeting_started = False
        return summary

    def _generate_summary(self, meeting: Dict) -> Dict:
        """Generate a summary of the meeting"""
        summary = {
            'title': meeting['title'],
            'date': meeting['start_time'],
            'attendees': meeting['attendees'],
            'notes_count': len(meeting['notes']),
            'action_items': meeting['action_items'],
            'decisions': meeting['decisions'],
            'summary_text': self._create_summary_text(meeting)
        }
        return summary

    def _create_summary_text(self, meeting: Dict) -> str:
        """Create readable summary text"""
        text = f"Meeting: {meeting['title']}\n"
        text += f"Date: {meeting['start_time']}\n\n"

        if meeting['attendees']:
            text += f"Attendees: {', '.join(meeting['attendees'])}\n\n"

        if meeting['notes']:
            text += "Key Notes:\n"
            for i, note in enumerate(meeting['notes'], 1):
                text += f"  {i}. {note['text']}\n"
            text += "\n"

        if meeting['decisions']:
            text += "Decisions Made:\n"
            for i, decision in enumerate(meeting['decisions'], 1):
                text += f"  {i}. {decision['decision']}\n"
            text += "\n"

        if meeting['action_items']:
            text += "Action Items:\n"
            for i, item in enumerate(meeting['action_items'], 1):
                text += f"  {i}. {item['action']} (Owner: {item['owner']}, Due: {item['due_date']})\n"

        return text.strip()

    def get_active_meeting_status(self) -> str:
        """Get status of active meeting"""
        if not self.meeting_started:
            return "No active meeting"

        notes_count = len(self.current_meeting['notes'])
        actions_count = len(self.current_meeting['action_items'])
        decisions_count = len(self.current_meeting['decisions'])

        return f"Meeting: {self.current_meeting['title']} | Notes: {notes_count} | Actions: {actions_count} | Decisions: {decisions_count}"

    def get_meeting_history(self, limit: int = 5) -> List[Dict]:
        """Get recent meetings"""
        return self.meetings_history[-limit:]

    def export_meeting(self, meeting_index: int = -1) -> str:
        """Export a meeting as formatted text"""
        if not self.meetings_history:
            return "No meetings to export"

        meeting = self.meetings_history[meeting_index]
        return self._create_summary_text(meeting)

# Global instance
_meeting_notes = MeetingNotes()

def start_meeting(title: str = None, attendees: List[str] = None):
    """Start a new meeting"""
    return _meeting_notes.start_meeting(title, attendees)

def add_note(note: str):
    """Add a note"""
    return _meeting_notes.add_note(note)

def add_action_item(action: str, owner: str = None, due_date: str = None):
    """Add an action item"""
    return _meeting_notes.add_action_item(action, owner, due_date)

def end_meeting():
    """End meeting and get summary"""
    return _meeting_notes.end_meeting()
