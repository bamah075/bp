#!/usr/bin/env python3
"""
Calendar & Reminders Manager - Manage appointments and to-do lists
"""

from datetime import datetime, timedelta
from typing import List, Dict
import json

class CalendarManager:
    def __init__(self):
        self.appointments = []
        self.todo_items = []
        self.reminders = []

    def add_appointment(self, title: str, date: str, time: str, duration: str = "1 hour", description: str = None):
        """Add an appointment to calendar"""
        appointment = {
            'id': len(self.appointments) + 1,
            'title': title,
            'date': date,
            'time': time,
            'duration': duration,
            'description': description or '',
            'created': datetime.now().isoformat(),
            'completed': False
        }
        self.appointments.append(appointment)
        return f"✓ Appointment scheduled: {title} on {date} at {time}"

    def add_todo(self, task: str, priority: str = "medium", due_date: str = None, category: str = None):
        """Add a to-do item"""
        todo = {
            'id': len(self.todo_items) + 1,
            'task': task,
            'priority': priority.lower(),
            'due_date': due_date or 'No due date',
            'category': category or 'General',
            'created': datetime.now().isoformat(),
            'completed': False
        }
        self.todo_items.append(todo)
        priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority.lower(), '⚪')
        return f"{priority_emoji} To-do added: {task} (Due: {due_date or 'Not set'})"

    def complete_todo(self, task_id: int):
        """Mark a to-do as complete"""
        for todo in self.todo_items:
            if todo['id'] == task_id:
                todo['completed'] = True
                return f"✓ Completed: {todo['task']}"
        return f"Task {task_id} not found"

    def complete_appointment(self, appointment_id: int):
        """Mark an appointment as complete"""
        for appt in self.appointments:
            if appt['id'] == appointment_id:
                appt['completed'] = True
                return f"✓ Completed: {appt['title']}"
        return f"Appointment {appointment_id} not found"

    def set_reminder(self, message: str, remind_date: str, remind_time: str):
        """Set a reminder for a specific date/time"""
        reminder = {
            'id': len(self.reminders) + 1,
            'message': message,
            'date': remind_date,
            'time': remind_time,
            'created': datetime.now().isoformat(),
            'sent': False
        }
        self.reminders.append(reminder)
        return f"🔔 Reminder set: {message} on {remind_date} at {remind_time}"

    def get_today_schedule(self) -> str:
        """Get today's schedule"""
        today = datetime.now().strftime("%Y-%m-%d")

        today_appointments = [a for a in self.appointments if a['date'] == today and not a['completed']]
        today_todos = [t for t in self.todo_items if not t['completed']]

        schedule = f"📅 Today's Schedule ({today})\n\n"

        if today_appointments:
            schedule += "Appointments:\n"
            for appt in sorted(today_appointments, key=lambda x: x['time']):
                schedule += f"  • {appt['time']} - {appt['title']} ({appt['duration']})\n"
            schedule += "\n"

        if today_todos:
            schedule += "To-Do Items:\n"
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            sorted_todos = sorted(today_todos, key=lambda x: priority_order.get(x['priority'], 3))
            for todo in sorted_todos[:5]:
                emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(todo['priority'], '⚪')
                schedule += f"  {emoji} {todo['task']} (Due: {todo['due_date']})\n"

        if not today_appointments and not today_todos:
            schedule += "No appointments or tasks scheduled for today. You're all set! ✨"

        return schedule.strip()

    def get_week_summary(self) -> str:
        """Get summary of the week"""
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_end = week_start + timedelta(days=7)

        week_appts = [a for a in self.appointments
                      if week_start.date() <= datetime.fromisoformat(a['date']).date() < week_end.date()
                      and not a['completed']]

        incomplete_todos = [t for t in self.todo_items if not t['completed']]

        summary = f"📊 Week Summary ({week_start.strftime('%b %d')} - {week_end.strftime('%b %d')})\n\n"
        summary += f"Upcoming Appointments: {len(week_appts)}\n"
        summary += f"Pending To-Do Items: {len(incomplete_todos)}\n\n"

        if week_appts:
            summary += "Key Appointments:\n"
            for appt in week_appts[:5]:
                summary += f"  • {appt['date']} at {appt['time']}: {appt['title']}\n"
            summary += "\n"

        if incomplete_todos:
            summary += "Top Priorities:\n"
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            sorted_todos = sorted(incomplete_todos, key=lambda x: priority_order.get(x['priority'], 3))
            for todo in sorted_todos[:5]:
                emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(todo['priority'], '⚪')
                summary += f"  {emoji} {todo['task']}\n"

        return summary.strip()

    def get_upcoming_reminders(self, days: int = 7) -> List[Dict]:
        """Get upcoming reminders"""
        now = datetime.now()
        future = now + timedelta(days=days)

        upcoming = [r for r in self.reminders
                   if not r['sent'] and
                   datetime.fromisoformat(r['date'] + ' ' + r['time']) <= future]

        return sorted(upcoming, key=lambda x: x['date'] + ' ' + x['time'])

    def list_todos(self, filter_by: str = None) -> str:
        """List all to-dos, optionally filtered"""
        incomplete = [t for t in self.todo_items if not t['completed']]

        if filter_by:
            incomplete = [t for t in incomplete if t['category'].lower() == filter_by.lower()]

        if not incomplete:
            return f"No pending to-dos{f' in {filter_by}' if filter_by else ''}. Great job! ✨"

        result = f"📋 To-Do Items{f' ({filter_by})' if filter_by else ''}:\n\n"

        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        sorted_todos = sorted(incomplete, key=lambda x: priority_order.get(x['priority'], 3))

        for i, todo in enumerate(sorted_todos, 1):
            emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(todo['priority'], '⚪')
            result += f"{i}. {emoji} {todo['task']} (Due: {todo['due_date']}, Category: {todo['category']})\n"

        return result.strip()

    def update_todo_status(self, task_id: int) -> str:
        """Toggle to-do completion status"""
        for todo in self.todo_items:
            if todo['id'] == task_id:
                todo['completed'] = not todo['completed']
                status = "✓ Completed" if todo['completed'] else "↩ Reopened"
                return f"{status}: {todo['task']}"
        return f"Task {task_id} not found"

# Global instance
_calendar = CalendarManager()

def add_appointment(title: str, date: str, time: str, duration: str = "1 hour", description: str = None):
    return _calendar.add_appointment(title, date, time, duration, description)

def add_todo(task: str, priority: str = "medium", due_date: str = None, category: str = None):
    return _calendar.add_todo(task, priority, due_date, category)

def get_today_schedule():
    return _calendar.get_today_schedule()

def get_week_summary():
    return _calendar.get_week_summary()

def list_todos(filter_by: str = None):
    return _calendar.list_todos(filter_by)

def set_reminder(message: str, remind_date: str, remind_time: str):
    return _calendar.set_reminder(message, remind_date, remind_time)
