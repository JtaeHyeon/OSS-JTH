from datetime import date
from typing import Optional

class DailySummary:
    def __init__(self, summary_date: date, user: "User"):
        if not isinstance(summary_date, date):
            raise ValueError("Summary date must be a datetime.date object.")
        self.summary_date: date = summary_date
        self.user: "User" = user
        self.generated_string: Optional[str] = None

    def generate(self) -> str:
        summary_parts = [f"Daily Summary for {self.summary_date.strftime('%Y-%m-%d')} for {self.user.nickname}:"]

        daily_routines = [r for r in self.user.routines if r.deadline == self.summary_date]
        if daily_routines:
            completed_routines = [r.title for r in daily_routines if r.is_complete]
            pending_routines = [r.title for r in daily_routines if not r.is_complete]
            routine_summary = f"  - Routines ({len(daily_routines)}): "
            if completed_routines:
                routine_summary += f"Completed: {', '.join(completed_routines)}. "
            if pending_routines:
                routine_summary += f"Pending: {', '.join(pending_routines)}."
            summary_parts.append(routine_summary.strip())

        daily_thoughts = [t for t in self.user.thoughts if t.created_at.date() == self.summary_date]
        if daily_thoughts:
            thoughts_content = [f"'{t.content[:50]}...'" if len(t.content) > 50 else f"'{t.content}'" for t in daily_thoughts]
            summary_parts.append(f"  - Thoughts ({len(daily_thoughts)}): {'; '.join(thoughts_content)}")

        daily_emotions = [e for e in self.user.emotions if e.date.date() == self.summary_date]
        if daily_emotions:
            emotions_str = [f'{e.emotion_type} (level {e.level})' for e in daily_emotions]
            summary_parts.append(f"  - Emotions ({len(daily_emotions)}): {', '.join(emotions_str)}")

        daily_goals = [g for g in self.user.goals if g.deadline == self.summary_date]
        if daily_goals:
            goals_summary = [f"'{g.title}' (Progress: {g.progress*100:.0f}%)" for g in daily_goals]
            summary_parts.append(f"  - Goals with Deadline Today ({len(daily_goals)}): {'; '.join(goals_summary)}")

        self.generated_string = "\n".join(summary_parts)
        return self.generated_string

    def __repr__(self) -> str:
        return f"<DailySummary(date='{self.summary_date.strftime('%Y-%m-%d')}', user='{self.user.username}')>"
