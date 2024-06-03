FROM python:3.10-slim

WORKDIR /opt/app

COPY . /opt/app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["uvicorn", "task-api.main:app", "--host", "0.0.0.0", "--port", "80"]