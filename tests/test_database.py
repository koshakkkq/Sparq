# tests/test_db.py
import pytest
import asyncio
import asyncpg

DB_HOST = "localhost"
DB_NAME = "mydb"
DB_USER = "postgres"
DB_PASSWORD = "password"

@pytest.mark.asyncio
async def test_db_connection():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST
    )
    assert conn is not None
    await conn.close()

@pytest.mark.asyncio
async def test_insert_and_query():
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        host=DB_HOST
    )

    # Создаем тестовую таблицу (или можешь сделать миграцию заранее)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)

    # Очищаем перед тестом
    await conn.execute("TRUNCATE TABLE test_table RESTART IDENTITY;")

    # Вставляем данные
    await conn.execute("INSERT INTO test_table (name) VALUES ($1)", "Test name")

    # Делаем запрос
    row = await conn.fetchrow("SELECT id, name FROM test_table WHERE name = $1", "Test name")

    assert row is not None
    assert row["name"] == "Test name"

    await conn.close()
