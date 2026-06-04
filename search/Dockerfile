FROM python:3.11-slim

WORKDIR /app

COPY app.py /app/app.py
COPY templates /app/templates

RUN pip install --no-cache-dir Flask

EXPOSE 5002

CMD ["python", "app.py"]
