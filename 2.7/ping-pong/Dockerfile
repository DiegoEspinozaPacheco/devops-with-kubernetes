FROM python:3.12-alpine

WORKDIR /app
RUN apk add --no-cache postgresql-dev gcc musl-dev
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .

ENV PORT=3002
CMD ["python", "main.py"]