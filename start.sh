python -m alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port $DB_PORT