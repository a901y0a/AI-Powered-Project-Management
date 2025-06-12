# from fastapi import APIRouter, HTTPException, Request
# from pydantic import BaseModel
# from db import get_pg_connection
# from app.llm import convert_to_sql, convert_sql_result_to_nl

# router = APIRouter()

# class QueryInput(BaseModel):
#     query: str

# @router.post("/query")
# def chatbot_query(data: QueryInput, request: Request):
#     nl_query = data.query.strip()
#     if nl_query.lower() in ['exit', 'quit']:
#         return {"response": "👋 Exiting."}

#     try:
#         # Convert natural language to SQL
#         conversational_response = convert_to_sql(nl_query)
#         sql_query = conversational_response.strip().strip("```sql").strip("```")

#         conn = get_pg_connection()
#         cur = conn.cursor()
#         cur.execute(sql_query)
#         rows = cur.fetchall()
#         colnames = [desc[0] for desc in cur.description]
#         cur.close()
#         conn.close()

#         if not rows:
#             return {"response": "⚠ No results found."}

#         # Convert SQL result to NL summary
#         chatbot_message = convert_sql_result_to_nl(sql_query, rows, colnames)
#         return {"response": chatbot_message}

#     except Exception as e:
#         return {"response": f"❌ Error: {str(e)}"}

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from app.db import get_pg_connection
from app.llm import convert_to_sql, convert_sql_result_to_nl

router = APIRouter()

class QueryInput(BaseModel):
    query: str

@router.post("/query")
def chatbot_query(data: QueryInput, request: Request):
    nl_query = data.query.strip()

    if nl_query.lower() in ['exit', 'quit']:
        return {"response": "👋 Exiting."}

    try:
        # Convert natural language to SQL
        conversational_response = convert_to_sql(nl_query)
        sql_query = conversational_response.strip().strip("```sql").strip("```")

        # Execute SQL query
        conn = get_pg_connection()
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]
        cur.close()
        conn.close()

        if not rows:
            return {"response": "⚠ No results found."}

        # Convert SQL result to human-readable response
        chatbot_message = convert_sql_result_to_nl(sql_query, rows, colnames)
        return {"response": chatbot_message}

    except Exception as e:
        return {"response": f"❌ Error: {str(e)}"}
