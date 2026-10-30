from fastapi import APIRouter, Depends
from schemas.schemas import CreateUrl, Response 
from core.database import get_db 
from sqlalchemy.orm import Session 
from models.models import WebhookSubscription, WebhookEventLog

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"]) 

@router.post("/", response_model = Response)
async def create_data(data:CreateUrl, db: Session = Depends(get_db)): 
    new_request = WebhookSubscription(url=data.url, secret_token=data.secret_token) 
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    return new_request
    



@router.get("/", response_model = list[Response])
async def get_data(db: Session = Depends(get_db)): 
    subscriptions = db.query(WebhookEventLog).all()
    return subscriptions
