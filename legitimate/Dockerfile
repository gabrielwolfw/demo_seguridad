FROM python:3.11-slim
WORKDIR /app
RUN pip install flask pyotp
COPY . .
CMD ["python", "app.py"]
