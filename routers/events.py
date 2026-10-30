from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from schemas.schemas import CreateUrl, Response, EventCreate
from core.database import get_db 
from sqlalchemy.orm import Session 
from models.models import WebhookSubscription, WebhookEventLog
from services.service import send_single_webhook

router = APIRouter(prefix="/events", tags = ["events"]) 

@router.post("/", response_model=Response) # Или схема ответа для события
async def create_event(event: EventCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)): 
  
    new_event = WebhookEventLog(**event.dict())
    db.add(new_event) 
    db.commit()
    db.refresh(new_event)
    
  
    active_subscriptions = db.query(WebhookSubscription).filter(WebhookSubscription.is_active == True).all()
    
    # 3. Для каждой подписки добавляем задачу в BackgroundTasks
    for sub in active_subscriptions:
        background_tasks.add_task(send_single_webhook, send_single_webhook, 
            event_id=new_event.id, 
            url=sub.url, 
            payload=event.payload, 
            secret_token=sub.secret_token)
    
    return new_event

