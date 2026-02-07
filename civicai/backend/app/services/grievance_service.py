from datetime import datetime
from sqlalchemy.orm import Session

from app.models.entities import Complaint, Feedback, Log, Ticket
from app.services.ai_engine import HybridAIEngine, build_tracking_id


class GrievanceService:
    def __init__(self, ai: HybridAIEngine):
        self.ai = ai

    def process_chat(self, db: Session, user_id: str, message: str, location: str):
        match = self.ai.match(message)
        similar = self.ai.top_similar(message)
        severity = self.ai.predict_severity(message)
        level = 1 if match.confidence >= 0.32 else 2
        tracking_id = None
        if level == 2:
            tracking_id = self.create_ticket(db, user_id, message, match.category, location, severity, match.department)
        reply = (
            f"Department: {match.department}\n"
            f"Solution: {match.solution}\n"
            f"Expected time: 48h\n"
            f"Helpline: 1533\n"
            f"Confidence: {match.confidence:.2f}"
        )
        if level == 2:
            reply += f"\nEscalated to Level-2. Tracking ID: {tracking_id}"
        return reply, level, match.confidence, similar, tracking_id

    def create_ticket(self, db: Session, user_id: str, text: str, category: str, location: str, severity: float, authority: str):
        complaint = Complaint(user_id=user_id, text=text, category=category, location=location, severity=severity, level=2)
        db.add(complaint)
        db.flush()
        tracking_id = build_tracking_id()
        ticket = Ticket(tracking_id=tracking_id, complaint_id=complaint.id, authority=authority, escalated=True, status="OPEN")
        db.add(ticket)
        db.add(Log(tracking_id=tracking_id, message="Day1: Ticket created"))
        db.commit()
        return tracking_id

    def add_feedback(self, db: Session, user_id: str, tracking_id: str, rating: int, comment: str):
        db.add(Feedback(user_id=user_id, tracking_id=tracking_id, rating=rating, comment=comment))
        db.commit()

    def follow_up(self, db: Session, ticket: Ticket):
        age = (datetime.utcnow() - ticket.created_at).days
        if age >= 5:
            msg = "Day5: Public alert"
        elif age >= 3:
            msg = "Day3: Escalated to Level-2 authority"
        elif age >= 2:
            msg = "Day2: Reminder sent"
        else:
            msg = "Day1: Ticket created"
        db.add(Log(tracking_id=ticket.tracking_id, message=msg))
        db.commit()
