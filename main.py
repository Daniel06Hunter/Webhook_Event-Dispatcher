from fastapi import FastAPI
from routers import subscriptions, events


app = FastAPI(title="Webhook and Event-Dispatcher")
app.include_router(subscriptions.router)
app.include_router(events.router)

@app.get("(/)")
async def root(): 
    return {"message": "Welcome to the Webhook and Event-Dispatcher API"}
