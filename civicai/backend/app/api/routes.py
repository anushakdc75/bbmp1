from collections import Counter
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.entities import Complaint, Feedback, Log, Ticket
from app.schemas.contracts import ChatRequest, ChatResponse, ComplaintRequest, ComplaintResponse, FeedbackRequest
from app.services.ai_engine import HybridAIEngine
from app.services.grievance_service import GrievanceService

router = APIRouter()
ai_engine = HybridAIEngine(settings.data_file)
service = GrievanceService(ai_engine)


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, db: Session = Depends(get_db)):
    reply, level, conf, similar, tracking_id = service.process_chat(db, payload.user_id, payload.message, payload.location)
    return ChatResponse(reply=reply, level=level, confidence=conf, similar_cases=similar, tracking_id=tracking_id)


@router.post("/complaint", response_model=ComplaintResponse)
def complaint(payload: ComplaintRequest, db: Session = Depends(get_db)):
    match = ai_engine.match(payload.text)
    severity = ai_engine.predict_severity(payload.text)
    tracking = service.create_ticket(db, payload.user_id, payload.text, match.category, payload.location, severity, match.department)
    return ComplaintResponse(tracking_id=tracking, level=2, authority=match.department, status="OPEN")


@router.get("/status/{ticket_id}")
def status(ticket_id: str, db: Session = Depends(get_db)):
    ticket = db.scalar(select(Ticket).where(Ticket.tracking_id == ticket_id))
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    logs = db.scalars(select(Log).where(Log.tracking_id == ticket_id)).all()
    return {"tracking_id": ticket_id, "status": ticket.status, "authority": ticket.authority, "logs": [l.message for l in logs]}


@router.get("/history/{user_id}")
def history(user_id: str, db: Session = Depends(get_db)):
    items = db.scalars(select(Complaint).where(Complaint.user_id == user_id)).all()
    return [{"text": c.text, "category": c.category, "location": c.location, "level": c.level} for c in items]


@router.post("/feedback")
def feedback(payload: FeedbackRequest, db: Session = Depends(get_db)):
    service.add_feedback(db, payload.user_id, payload.tracking_id, payload.rating, payload.comment)
    return {"ok": True}


@router.get("/analytics")
def analytics(db: Session = Depends(get_db)):
    complaints = db.scalars(select(Complaint)).all()
    tickets = db.scalars(select(Ticket)).all()
    by_category = Counter(c.category for c in complaints)
    by_area = Counter(c.location for c in complaints)
    sla_open = sum(1 for t in tickets if t.status != "RESOLVED")
    return {"total_complaints": len(complaints), "total_tickets": len(tickets), "by_category": by_category, "by_area": by_area, "sla_open": sla_open}
