# Use Python 3.11 slim image for better compatibility and smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for potential ML packages and Azure compatibility
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user for security (Azure Container Apps requirement)
RUN adduser --disabled-password --gecos '' --uid 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Set environment variables for production
ENV FLASK_APP=startup:app
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create data directory for vector storage (with proper permissions)
RUN mkdir -p /app/data/chroma && \
    chmod 755 /app/data

# Azure Container Apps uses port 8080 internally and maps to 443 externally
EXPOSE 8080

# Health check for Azure Container Apps
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8080/api/health || exit 1

# Use Gunicorn for production deployment (Azure Container Apps compatible)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--worker-class", "gthread", "--threads", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info", "--preload", "startup:app"]
