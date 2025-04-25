cd /opt/render/project/src
.venv/bin/python -c "from alembic import command; from alembic.config import Config; command.upgrade(Config('alembic.ini'), 'head')"
# Start the FastAPI application
.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port $PORT