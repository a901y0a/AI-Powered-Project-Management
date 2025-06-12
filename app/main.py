from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.llm import convert_to_sql, convert_sql_result_to_nl
from app.db import get_pg_connection
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from app.schemas import LoginRequest, Token
from passlib.hash import bcrypt
from app.utils.auth import create_access_token

app = FastAPI()

# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chatbot NL Query Route
class QueryInput(BaseModel):
    query: str

@app.post("/api/run")
def run_query(input: QueryInput):
    nl_query = input.query.strip()

    if nl_query.lower() in ['exit', 'quit']:
        return {"response": "👋 Exiting."}

    try:
        conversational_response = convert_to_sql(nl_query)
        sql_query = conversational_response.strip().strip("```sql").strip("```")

        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()

        if not rows:
            return {"response": "⚠ No results found."}

        chatbot_message = convert_sql_result_to_nl(sql_query, rows, colnames)
        return {"response": chatbot_message}

    except Exception as e:
        return {"response": f"❌ Error: {str(e)}"}

# Auth route for login
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/auth/login", response_model=Token)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not bcrypt.verify(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username, "role": user.role})
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }
