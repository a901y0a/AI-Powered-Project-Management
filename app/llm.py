# import os
# import psycopg2
# from openai import AzureOpenAI
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# # Azure OpenAI client setup
# client = AzureOpenAI(
#     api_key=os.getenv("AZURE_OPENAI_API_KEY"),
#     azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
#     api_version="2024-02-01"
# )

# # PostgreSQL connection
# def get_pg_connection():
#     return psycopg2.connect(
#         host=os.getenv("PG_HOST"),
#         database=os.getenv("PG_DB"),
#         user=os.getenv("PG_USER"),
#         password=os.getenv("PG_PASSWORD")
#     )

# # Dynamically extract schema from PostgreSQL
# def get_schema_context():
#     conn = get_pg_connection()
#     cur = conn.cursor()

#     schema_context = ""
#     cur.execute("""
#         SELECT table_name FROM information_schema.tables
#         WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
#     """)
#     tables = cur.fetchall()

#     for table in tables:
#         table_name = table[0]
#         schema_context += f"\nTable: {table_name}\nColumns:\n"

#         cur.execute("""
#             SELECT column_name, data_type
#             FROM information_schema.columns
#             WHERE table_name = %s;
#         """, (table_name,))
#         columns = cur.fetchall()

#         for col_name, col_type in columns:
#             schema_context += f"- {col_name} ({col_type})\n"

#     cur.close()
#     conn.close()
#     return schema_context

# # Convert user natural language question to SQL
# def convert_to_sql(nl_query):
#     schema_context = get_schema_context()

#     messages = [
#         {"role": "system", "content": f"You are a helpful assistant that converts natural language to SQL for a PostgreSQL database.\n\nContext:\n{schema_context}"},
#         {"role": "user", "content": f"Write only the PostgreSQL SQL query for the following user question. Do not explain anything or add extra formatting.\n\nUser: {nl_query}"}
#     ]

#     response = client.chat.completions.create(
#         model=os.getenv("AZURE_DEPLOYMENT_NAME"),
#         messages=messages,
#         temperature=0.3,
#         max_tokens=150
#     )
#     return response.choices[0].message.content.strip()

# # Convert SQL output to human-readable chatbot-style response
# def convert_sql_result_to_nl(sql_query, rows, colnames):
#     # Format rows into readable text
#     formatted_result = "\n".join(str(dict(zip(colnames, row))) for row in rows)

#     messages = [
#         {"role": "system", "content": "You are a helpful assistant summarizing SQL query results into clear and professional natural language for HR-related chatbot queries."},
#         {"role": "user", "content": f"The executed SQL query was:\n{sql_query}\n\nThe returned result is:\n{formatted_result}\n\nNow summarize this result as a helpful chatbot message."}
#     ]

#     response = client.chat.completions.create(
#         model=os.getenv("AZURE_DEPLOYMENT_NAME"),
#         messages=messages,
#         temperature=0.5,
#         max_tokens=200
#     )

#     return response.choices[0].message.content.strip()

import os
import psycopg2
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version="2024-02-01"
)

def get_pg_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST"),
        database=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD")
    )

def get_schema_context():
    conn = get_pg_connection()
    cur = conn.cursor()

    schema_context = ""
    cur.execute("""
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    """)
    tables = cur.fetchall()

    for table in tables:
        table_name = table[0]
        schema_context += f"\nTable: {table_name}\nColumns:\n"

        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s;
        """, (table_name,))
        columns = cur.fetchall()

        for col_name, col_type in columns:
            schema_context += f"- {col_name} ({col_type})\n"

    cur.close()
    conn.close()
    return schema_context

def convert_to_sql(nl_query):
    schema_context = get_schema_context()

    messages = [
        {"role": "system", "content": f"You are a helpful assistant that converts natural language to SQL for a PostgreSQL database.\n\nContext:\n{schema_context}"},
        {"role": "user", "content": f"Write only the PostgreSQL SQL query for the following user question. Do not explain anything or add extra formatting.\n\nUser: {nl_query}"}
    ]

    response = client.chat.completions.create(
        model=os.getenv("AZURE_DEPLOYMENT_NAME"),
        messages=messages,
        temperature=0.3,
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def convert_sql_result_to_nl(sql_query, rows, colnames):
    formatted_result = "\n".join(str(dict(zip(colnames, row))) for row in rows)

    messages = [
        {"role": "system", "content": "You are a helpful assistant summarizing SQL query results into clear and professional natural language for HR-related chatbot queries."},
        {"role": "user", "content": f"The executed SQL query was:\n{sql_query}\n\nThe returned result is:\n{formatted_result}\n\nNow summarize this result as a helpful chatbot message."}
    ]

    response = client.chat.completions.create(
        model=os.getenv("AZURE_DEPLOYMENT_NAME"),
        messages=messages,
        temperature=0.5,
        max_tokens=200
    )

    return response.choices[0].message.content.strip()
