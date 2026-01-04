import httpx
from typing import Annotated
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()
class VerifyRequest(BaseModel):
    name: str
    phonenumber: str
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This allows 'null' (local files) and all domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/verify")
async def verify(data: VerifyRequest):
    print(f"DEBUG: API 1 received JSON for {data.name} and {data.phonenumber}")
    async with httpx.AsyncClient() as client:
        try:
            # Note: 127.0.0.1 is more reliable than 'localhost' in code
            response = await client.post(
                "http://127.0.0.1:8001/details", 
                json=data.dict()
            )
            return response.json()
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"API 2 Connection Error: {e}")