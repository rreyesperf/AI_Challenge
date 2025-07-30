# Use Python 3.11 slim image for better compatibility and smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for potential ML packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --uid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Set environment variables for production
ENV FLASK_APP=routes:app
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create data directory for vector storage (with proper permissions)
RUN mkdir -p /app/data/chroma && \
    chmod 755 /app/data

# Expose port (Azure Container Apps will map this to 443)
EXPOSE 8080

# Health check for container orchestration
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/api/health')" || exit 1

# Use Gunicorn for production deployment instead of Flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "4", "--worker-class", "gthread", "--threads", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "--preload", "startup:app"]
