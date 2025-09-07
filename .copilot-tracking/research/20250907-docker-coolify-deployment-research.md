<!-- markdownlint-disable-file -->
# Task Research Notes: Docker Deployment for Coolify VPS

## Research Executed

### File Analysis
- main.py
  - Python script with Spotify API integration, webhook notifications, and cron-like execution
  - Uses environment variables for configuration via python-dotenv
  - Implements logging, error handling, and state persistence
  - Contains SMTP email functionality for error notifications

- requirements.txt
  - Minimal dependencies: python-dotenv==1.0.1, Requests==2.32.3
  - No complex dependency chains or system requirements

- run_script.sh
  - Linux-specific shell script for cron job execution
  - Hardcoded paths for Raspberry Pi environment
  - Activates virtual environment and runs Python script

- .env.example
  - Configuration template with Spotify credentials, webhook URL, and SMTP settings
  - Shows all required environment variables for the application

### Code Search Results
- Environment variable usage patterns
  - Found 8 environment variables used throughout main.py
  - All sensitive data properly externalized from code
- File I/O operations
  - last_episodes.json for state persistence
  - debug.log and cron.log for logging
  - All files use relative paths from working directory

### External Research
- #githubRepo:"coolify python docker deployment"
  - Coolify supports multiple deployment methods for Python applications
  - Can use Dockerfile-based deployments with custom Dockerfiles
  - Supports docker-compose.yml for complex multi-service applications
  - Built-in cron job scheduling through Coolify web interface
  - Environment variables managed through Coolify dashboard
  - Volume mounting supported for persistent data storage

- #githubRepo:"coollabsio/coolify docker python"
  - Coolify uses Docker Compose for application orchestration
  - Supports custom Docker run options for advanced configurations
  - Environment variables can be injected at runtime
  - Health checks supported for container monitoring
  - Automatic SSL certificate management through Let's Encrypt

- #fetch:https://coolify.io/docs/knowledge-base/docker/custom-commands
  - Custom Docker run options supported but limited
  - Some options may interfere with Coolify's automation
  - Examples include capability additions, device mounts, security options
  - Not all Docker run options are supported

### Project Conventions
- Standards referenced: Python virtual environment usage, environment variable configuration
- Instructions followed: Proper logging practices, error handling patterns

## Key Discoveries

### Project Structure
The application is a self-contained Python script that:
- Runs periodically to check for new podcast episodes
- Maintains persistent state between executions
- Sends webhook notifications when new content is found
- Includes comprehensive logging and error reporting

### Implementation Patterns
- Environment-based configuration (no hardcoded values)
- File-based state persistence (JSON format)
- Comprehensive error handling with email notifications
- Logging with automatic rotation
- Test modes for development and validation

### Complete Examples
```dockerfile
# Multi-stage Python Dockerfile for Coolify
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim as runtime
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
WORKDIR /app
COPY . .
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app
CMD ["python", "main.py"]
```

```yaml
# docker-compose.yml for Coolify deployment
version: '3.8'
services:
  declue-spotify-check:
    build: .
    restart: unless-stopped
    environment:
      - SPOTIFY_CLIENT_ID=${SPOTIFY_CLIENT_ID}
      - SPOTIFY_CLIENT_SECRET=${SPOTIFY_CLIENT_SECRET}
      - WEBHOOK_URL=${WEBHOOK_URL}
      - SHOW_ID=${SHOW_ID}
      - SMTP_SERVER=${SMTP_SERVER}
      - SMTP_PORT=${SMTP_PORT}
      - SMTP_USERNAME=${SMTP_USERNAME}
      - SMTP_PASSWORD=${SMTP_PASSWORD}
      - EMAIL_RECIPIENT=${EMAIL_RECIPIENT}
    volumes:
      - ./data:/app/data
    healthcheck:
      test: ["CMD", "python", "-c", "import os; print('Container healthy')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### API and Schema Documentation
Coolify deployment supports:
- **Dockerfile deployments**: Custom Dockerfile with build context
- **Docker Compose**: Full docker-compose.yml support
- **Git integration**: Automatic builds from Git repositories
- **Environment management**: Runtime environment variable injection
- **Volume mounting**: Persistent storage for application data
- **Cron scheduling**: Built-in cron job management through web UI

### Technical Requirements
- Python 3.9+ runtime environment
- Network access for Spotify API and webhook delivery
- Persistent storage for state files and logs
- Scheduled execution (hourly intervals)
- SMTP access for error notifications

## Recommended Approach
**Docker Compose with Coolify Cron Scheduling**

Primary deployment strategy using Coolify's native capabilities:
- Multi-stage Dockerfile for optimized image size
- Docker Compose for service definition and configuration
- Coolify web interface for cron job scheduling (replacing system cron)
- Environment variables managed through Coolify dashboard
- Named volumes for persistent data storage
- Health checks for container monitoring
- Automatic SSL certificate management

## Implementation Guidance
- **Objectives**: Containerize Python application for Coolify VPS deployment with automated scheduling
- **Key Tasks**: Create optimized Dockerfile, docker-compose.yml, configure Coolify environment variables, set up cron scheduling
- **Dependencies**: Coolify platform access, Docker runtime, environment variable configuration
- **Success Criteria**: Application runs successfully in container, cron scheduling works through Coolify UI, data persistence maintained
