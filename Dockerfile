# Multi-stage Python Dockerfile for Coolify deployment
FROM python:3.11-slim as builder

# Set working directory for build stage
WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim as runtime

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy Python packages from builder stage
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Set working directory
WORKDIR /app

# Create data directory for persistent files
RUN mkdir -p /app/data && \
    chown -R app:app /app

# Copy application code
COPY main.py .
COPY .env.example .

# Ensure data directory has proper permissions
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys, os; sys.exit(0 if os.path.exists('/app/data') else 1)"

# Command to run the application
CMD ["python", "main.py"]
