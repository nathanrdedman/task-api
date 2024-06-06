FROM python:3.10-slim

ARG SQLALCHEMY_DATABASE_URL
ENV SQLALCHEMY_DATABASE_URL=$SQLALCHEMY_DATABASE_URL

COPY . /opt/
WORKDIR /opt/

RUN apt-get update \
    && apt-get install \    
    -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY deploy/run.sh /run.sh
RUN chmod +x  /start.sh
CMD ["/run.sh"]