# NEBULA Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install build dependencies for C-compilation (required by REBOUND)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python scientific dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Default port
EXPOSE 8000

# Environment variables
ENV ENVIRONMENT=production \
    PYTHONUNBUFFERED=1 \
    DATABASE_URL=sqlite:///./nebula.db

# Launch production server via run.py / uvicorn
CMD ["python", "run.py"]
