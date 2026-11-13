import os
from pathlib import Path

import psycopg
from psycopg import sql

# Connection details for your local PostgreSQL server.
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = "travel_planner"

if not DB_PASSWORD:
    raise ValueError(
        "Please set your PostgreSQL password in the terminal first."
    )

# Connect to the existing PostgreSQL maintenance database.
with psycopg.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname="postgres",
    autocommit=True,
) as connection:
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (DB_NAME,),
        )

        if cursor.fetchone():
            print(f"Database '{DB_NAME}' already exists.")
        else:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(DB_NAME)
                )
            )
            print(f"Database '{DB_NAME}' created.")

# Connect to the Travel Planner database and create the tables.
schema_file = Path(__file__).with_name("schema.sql")
schema_sql = schema_file.read_text(encoding="utf-8")

with psycopg.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    dbname=DB_NAME,
) as connection:
    with connection.cursor() as cursor:
        cursor.execute(schema_sql)

print("Tables created successfully!")