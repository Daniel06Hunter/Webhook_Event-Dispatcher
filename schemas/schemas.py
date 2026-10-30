from pydantic import BaseModel 
from sqlalchemy.orm import Config 

class CreateUrl(BaseModel): 
    url :str 
    secret_token: str 
    
class Response(CreateUrl): 
    id:int
    is_active: bool 
    
    class Config: 
        from_attributes = True
        
class EventCreate(BaseModel): 
    event_type:str 
    payload:dict 

    

