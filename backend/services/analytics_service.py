"""
Analytics Service
=================
Privacy-focused analytics for tracking application usage.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict
import json


class AnalyticsService:
    """Collect and analyze application usage metrics"""

    def __init__(self):
        self.events: List[Dict] = []
        self.daily_stats: Dict[str, Dict] = defaultdict(lambda: {
            "active_users": set(),
            "verse_lookups": 0,
            "lexicon_lookups": 0,
            "chat_messages": 0,
            "conversations_created": 0,
            "api_calls": defaultdict(int),
        })

    def track_event(
        self,
        event_type: str,
        user_id: Optional[int] = None,
        metadata: Optional[Dict] = None
    ):
        """Track an analytics event"""
        event = {
            "type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "metadata": metadata or {}
        }
        self.events.append(event)

        # Keep only last 10,000 events
        if len(self.events) > 10000:
            self.events = self.events[-10000:]

        # Update daily stats
        date_key = datetime.utcnow().strftime("%Y-%m-%d")
        if user_id:
            self.daily_stats[date_key]["active_users"].add(user_id)

        # Update event-specific counters
        if event_type == "verse_lookup":
            self.daily_stats[date_key]["verse_lookups"] += 1
        elif event_type == "lexicon_lookup":
            self.daily_stats[date_key]["lexicon_lookups"] += 1
        elif event_type == "chat_message":
            self.daily_stats[date_key]["chat_messages"] += 1
        elif event_type == "conversation_created":
            self.daily_stats[date_key]["conversations_created"] += 1

    def track_api_call(self, endpoint: str, user_id: Optional[int] = None):
        """Track API endpoint usage"""
        date_key = datetime.utcnow().strftime("%Y-%m-%d")
        self.daily_stats[date_key]["api_calls"][endpoint] += 1

        if user_id:
            self.daily_stats[date_key]["active_users"].add(user_id)

    def get_daily_stats(self, date: Optional[str] = None) -> Dict:
        """Get statistics for a specific date"""
        if date is None:
            date = datetime.utcnow().strftime("%Y-%m-%d")

        stats = dict(self.daily_stats[date])
        # Convert set to count
        if "active_users" in stats:
            stats["active_users"] = len(stats["active_users"])
        # Convert defaultdict to dict
        if "api_calls" in stats:
            stats["api_calls"] = dict(stats["api_calls"])

        return stats

    def get_weekly_stats(self) -> List[Dict]:
        """Get statistics for the last 7 days"""
        stats = []
        for i in range(7):
            date = (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d")
            day_stats = self.get_daily_stats(date)
            day_stats["date"] = date
            stats.append(day_stats)
        return sorted(stats, key=lambda x: x["date"])

    def get_summary(self) -> Dict:
        """Get overall summary statistics"""
        weekly = self.get_weekly_stats()

        return {
            "total_events": len(self.events),
            "last_7_days": {
                "active_users": sum(s.get("active_users", 0) for s in weekly),
                "verse_lookups": sum(s.get("verse_lookups", 0) for s in weekly),
                "lexicon_lookups": sum(s.get("lexicon_lookups", 0) for s in weekly),
                "chat_messages": sum(s.get("chat_messages", 0) for s in weekly),
                "conversations": sum(s.get("conversations_created", 0) for s in weekly),
            },
            "daily_breakdown": weekly
        }

    def get_popular_verses(self, limit: int = 10) -> List[Dict]:
        """Get most frequently looked up verses"""
        verse_counts = defaultdict(int)

        for event in self.events:
            if event["type"] == "verse_lookup" and event.get("metadata"):
                reference = event["metadata"].get("reference")
                if reference:
                    verse_counts[reference] += 1

        sorted_verses = sorted(
            verse_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {"reference": ref, "count": count}
            for ref, count in sorted_verses[:limit]
        ]

    def get_popular_words(self, limit: int = 10) -> List[Dict]:
        """Get most frequently looked up Greek words"""
        word_counts = defaultdict(int)

        for event in self.events:
            if event["type"] == "lexicon_lookup" and event.get("metadata"):
                word = event["metadata"].get("word")
                if word:
                    word_counts[word] += 1

        sorted_words = sorted(
            word_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [
            {"word": word, "count": count}
            for word, count in sorted_words[:limit]
        ]


# Global analytics instance
analytics = AnalyticsService()
