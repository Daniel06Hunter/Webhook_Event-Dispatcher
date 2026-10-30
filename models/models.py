from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Text, DateTime, func
from core.database import Base 

class WebhookSubscription(Base): 
    __tablename__ = "webhook_subscriptions" 
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    url: Mapped[str] = mapped_column(String(300))
    secret_token: Mapped[str] = mapped_column(String(300))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
class WebhookEventLog(Base): 
    __tablename__ = "webhook_event_logs" 
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True) 
    event_type: Mapped[str] = mapped_column(String(100))
    payload: Mapped[str] = mapped_column(Text)  
    status: Mapped[str] = mapped_column(String(50), default="pending") 
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())