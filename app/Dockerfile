FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV APP_INSIGHTS_INSTRUMENTATION_KEY=${APP_INSIGHTS_INSTRUMENTATION_KEY}

CMD ["python", "app/app.py"]
