FROM python:3.11-alpine

WORKDIR /app 

RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    python3-dev 


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]