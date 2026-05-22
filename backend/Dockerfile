FROM python:3.11-slim

LABEL org.opencontainers.image.title="EmploySight Backend"
LABEL org.opencontainers.image.version="3.0.3"
LABEL org.opencontainers.image.description="FastAPI backend with local fallback and optional ZenMux/Gemini AI insights"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV AI_ENABLED=true
ENV ZENMUX_BASE_URL=https://zenmux.ai/api/v1
ENV ZENMUX_MODEL=google/gemini-3.5-flash-free
ENV AI_TIMEOUT_SECONDS=20

WORKDIR /app

COPY backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /tmp/requirements.txt

COPY backend/app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
