import re
from fastapi.responses import JSONResponse 
from fastapi import FastAPI,HTTPException,Request
from pydantic import BaseModel
from ..repositorylayer import create_db_and_tables, get_user

app = FastAPI()

class VerifyRequest(BaseModel):
    name: str
    phonenumber: str
    
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request ,exc: Exception):
    status_code=500
    message="An internal server error occured."
    # If we manually 'raised' an error, use that status and message
    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        message = exc.detail
    
    return JSONResponse(
        status_code=status_code,
        content={"error": message, "status": "fail"}
    )

@app.post("/details")
async def get_details(data: VerifyRequest):
    # Fetch from repository
    user = get_user(data.name.strip())
    
    # --- ERROR 404 ---
    if not user:
        raise HTTPException(status_code=404, detail="User not found in MySQL")

    # Clean numbers for comparison
    clean_db = re.sub(r'\D', '', user.phonenumber)
    clean_input = re.sub(r'\D', '', data.phonenumber)
    
    # --- ERROR 401 ---
    if clean_db != clean_input:
        raise HTTPException(status_code=401, detail="Phone number does not match")
        
    # --- SUCCESS 200 ---
    return user