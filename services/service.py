# services.py
import httpx
from core.database import SessionLocal
from models.models import WebhookEventLog

def send_single_webhook(event_id: int, url: str, payload: dict, secret_token: str):
    """
    Отправляет вебхук на указанный URL и обновляет статус в базе данных.
    Выполняется в фоне после ответа клиенту.
    """

    db = SessionLocal()
    
    try:
        
        with httpx.Client(timeout=5.0) as client:
            response = client.post(
                url, 
                json=payload, 
                headers={"X-Webhook-Secret": secret_token}
            )
        
        
        event_log = db.query(WebhookEventLog).filter(WebhookEventLog.id == event_id).first()
        
        if event_log:
            if 200 <= response.status_code < 300:
                event_log.status = "success"
            else:
                event_log.status = "failed"
                event_log.retry_count += 1
            
           
            db.commit()
            
    except Exception as e:
        print(f"Failed to send webhook to {url}: {e}")
        
        # Если упала сеть или сработал таймаут, тоже фиксируем неудачу
        event_log = db.query(WebhookEventLog).filter(WebhookEventLog.id == event_id).first()
        if event_log:
            event_log.status = "failed"
            event_log.retry_count += 1
            db.commit()
            
    finally:
        db.close()