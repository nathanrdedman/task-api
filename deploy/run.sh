#!/bin/bash
set -e


alembic upgrade head
uvicorn main:app --app-dir src --loop asyncio --log-config ${UVICORN_LOG_CONFIG}
