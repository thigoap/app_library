#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação
# poetry run uvicorn --host 0.0.0.0 --port 8000 fast.app:app
poetry run fastapi run fast/app.py --host 0.0.0.0