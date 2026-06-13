#!/usr/bin/env python3
"""
Maya Memory System - Learns from interactions and improves responses
Remembers questions, tracks patterns, and provides smarter replies over time
"""

import json
import os
from datetime import datetime
from collections import Counter

class MayaMemory:
    """Intelligent memory system that learns from user interactions"""

    def __init__(self, memory_file=None):
        self.memory_file = memory_file or os.path.expanduser("~/.maya_memory.json")
        self.interactions = []
        self.learned_patterns = {}
        self.response_ratings = {}
        self.user_preferences = {}
        self.load_memory()

    def load_memory(self):
        """Load existing memory from file"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    data = json.load(f)
                    self.interactions = data.get('interactions', [])
                    self.learned_patterns = data.get('patterns', {})
                    self.response_ratings = data.get('ratings', {})
                    self.user_preferences = data.get('preferences', {})
            except Exception as e:
                print(f"[Memory] Error loading memory: {e}")
                self.interactions = []

    def save_memory(self):
        """Save memory to file"""
        try:
            data = {
                'interactions': self.interactions[-100:],  # Keep last 100 interactions
                'patterns': self.learned_patterns,
                'ratings': self.response_ratings,
                'preferences': self.user_preferences
            }
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"[Memory] Error saving memory: {e}")

    def remember_interaction(self, question, response, category=None, quality=None):
        """Remember a question-response pair"""
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'question': question,
            'response': response,
            'category': category,
            'quality': quality,  # Can be 'good', 'bad', 'neutral'
        }
        self.interactions.append(interaction)

        # Learn from the interaction
        self._learn_from_interaction(question, response, category, quality)
        self.save_memory()

    def _learn_from_interaction(self, question, response, category, quality):
        """Extract patterns from interactions"""
        # Track question patterns
        q_lower = question.lower()
        keywords = q_lower.split()

        for keyword in keywords:
            if keyword not in self.learned_patterns:
                self.learned_patterns[keyword] = []
            self.learned_patterns[keyword].append({
                'question': question,
                'response': response,
                'quality': quality,
                'count': len([i for i in self.interactions if keyword in i['question'].lower()])
            })

        # Track response quality
        if response not in self.response_ratings:
            self.response_ratings[response] = {'good': 0, 'bad': 0, 'neutral': 0}

        if quality:
            self.response_ratings[response][quality] += 1

    def get_similar_questions(self, question, limit=3):
        """Find similar questions from history"""
        q_lower = question.lower()
        keywords = set(q_lower.split())

        similar = []
        for interaction in self.interactions:
            inter_keywords = set(interaction['question'].lower().split())
            # Calculate similarity
            common = len(keywords & inter_keywords)
            if common >= 2:  # At least 2 keywords match
                similar.append({
                    'question': interaction['question'],
                    'response': interaction['response'],
                    'similarity': common / len(keywords | inter_keywords),
                    'quality': interaction.get('quality')
                })

        # Sort by similarity and return best matches
        similar.sort(key=lambda x: x['similarity'], reverse=True)
        return similar[:limit]

    def suggest_better_response(self, question, current_response):
        """Suggest a better response based on learned patterns"""
        # Check if we've answered similar questions
        similar = self.get_similar_questions(question)

        if similar:
            # Find the best rated response
            best_response = None
            best_quality = None

            for sim in similar:
                if sim['quality'] == 'good':
                    return sim['response']
                elif best_quality != 'good' and sim['quality'] is not None:
                    best_response = sim['response']
                    best_quality = sim['quality']

            if best_response:
                return best_response

        return None

    def rate_response(self, response, quality):
        """Rate a response to improve future answers"""
        if response in self.response_ratings:
            self.response_ratings[response][quality] += 1
            self.save_memory()
            return f"Thanks! I've noted that response as '{quality}' to improve."
        return None

    def get_statistics(self):
        """Get learning statistics"""
        total_interactions = len(self.interactions)
        good_responses = sum(1 for resp in self.response_ratings.values() if resp['good'] > 0)
        bad_responses = sum(1 for resp in self.response_ratings.values() if resp['bad'] > 0)

        return {
            'total_interactions': total_interactions,
            'good_responses': good_responses,
            'bad_responses': bad_responses,
            'learned_patterns': len(self.learned_patterns),
            'improvement_rate': f"{(good_responses / max(1, total_interactions) * 100):.1f}%"
        }

    def get_learning_report(self):
        """Get a report of what Maya has learned"""
        stats = self.get_statistics()

        report = f"""
═══════════════════════════════════════════════════════
📚 MAYA LEARNING REPORT
═══════════════════════════════════════════════════════

Total Interactions: {stats['total_interactions']}
Good Responses: {stats['good_responses']}
Bad Responses: {stats['bad_responses']}
Learned Patterns: {stats['learned_patterns']}
Improvement Rate: {stats['improvement_rate']}

════════════════════════════════════════════════════════
Maya is getting smarter with every interaction!
════════════════════════════════════════════════════════
"""
        return report

    def reset_memory(self):
        """Clear all memory (start fresh)"""
        self.interactions = []
        self.learned_patterns = {}
        self.response_ratings = {}
        self.user_preferences = {}
        self.save_memory()

    def get_top_questions(self, limit=5):
        """Get most frequently asked questions"""
        questions = [i['question'] for i in self.interactions]
        question_counts = Counter(questions)
        return question_counts.most_common(limit)

    def get_improvement_suggestions(self):
        """Get suggestions for how Maya could improve"""
        # Find questions with mostly bad responses
        bad_questions = []
        for response, ratings in self.response_ratings.items():
            if ratings['bad'] > ratings['good']:
                # Find which questions led to this bad response
                for interaction in self.interactions:
                    if interaction['response'] == response and interaction.get('quality') == 'bad':
                        bad_questions.append(interaction['question'])

        return bad_questions[:5]

# Global memory instance
_maya_memory = MayaMemory()

def remember(question, response, category=None, quality=None):
    """Remember an interaction"""
    _maya_memory.remember_interaction(question, response, category, quality)

def rate_last_response(quality):
    """Rate the last response (good/bad/neutral)"""
    if _maya_memory.interactions:
        last = _maya_memory.interactions[-1]
        return _maya_memory.rate_response(last['response'], quality)

def get_memory_stats():
    """Get memory statistics"""
    return _maya_memory.get_statistics()

def get_memory_report():
    """Get full learning report"""
    return _maya_memory.get_learning_report()

def suggest_better_response(question, current_response):
    """Get suggestion for better response"""
    return _maya_memory.suggest_better_response(question, current_response)

def get_similar_questions(question):
    """Find similar questions from history"""
    return _maya_memory.get_similar_questions(question)
