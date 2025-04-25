cd /opt/render/project/src
source .venv/bin/activate
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port $PORT