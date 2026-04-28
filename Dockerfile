FROM python:3.11-slim as requirements-stage

WORKDIR /tmp

# Install PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies, creating wheels for faster builds
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /tmp/wheels -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

# Install runtime PostgreSQL dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=requirements-stage /tmp/wheels /wheels
COPY --from=requirements-stage /tmp/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY . .

# Ensure the alembic folder and other configs are accessible
# Usually you would run migrations here or at container entrypoint

EXPOSE 8000

# Start server (run migrations first so tables exist on fresh deployments)
CMD ["sh", "-c", "python scripts/fix_alembic.py && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
