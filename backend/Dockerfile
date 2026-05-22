FROM python:3.11-slim

LABEL org.opencontainers.image.title="EmploySight Backend"
LABEL org.opencontainers.image.version="4.0.1"
LABEL org.opencontainers.image.description="FastAPI backend with local fallback, optional OpenRouter AI insights, and admin audit security"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV AI_ENABLED=true
ENV AI_BASE_URL=https://openrouter.ai/api/v1
ENV AI_MODEL=openai/gpt-oss-120b:free
ENV OPENROUTER_APP_NAME=EmploySight
ENV AI_TIMEOUT_SECONDS=20

WORKDIR /app

COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

COPY backend/app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
