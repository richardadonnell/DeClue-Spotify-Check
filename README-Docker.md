# Docker Deployment Guide

## Overview

This guide explains how to deploy the DeClue-Spotify-Check application using Docker and Docker Compose.

## Prerequisites

- Docker and Docker Compose installed
- Access to required environment variables
- Network access to Spotify API and webhook endpoints

## Local Development

### 1. Build the Docker Image

```bash
docker build -t declue-spotify-check .
```

### 2. Run with Docker Compose

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your actual values
# Then run:
docker-compose up -d
```

### 3. Check Logs

```bash
docker-compose logs -f declue-spotify-check
```

### 4. Check Container Health

```bash
docker-compose ps
```

## Environment Variables

Create a `.env` file with the following variables:

```bash
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
WEBHOOK_URL=your_webhook_url
SHOW_ID=spotify_show_id
SMTP_SERVER=your_smtp_server
SMTP_PORT=587
SMTP_USERNAME=your_email@example.com
SMTP_PASSWORD=your_email_password
EMAIL_RECIPIENT=notifications@example.com
```

## Data Persistence

The application stores data in the `/app/data` directory inside the container, which is mounted as a named volume `app_data`. This ensures:

- `last_episodes.json` persists between container restarts
- `debug.log` is retained for troubleshooting
- Application state is maintained across deployments

## Health Checks

The container includes health checks that verify:
- Python runtime is functional
- Data directory is accessible
- Container is ready to process requests

## Testing

### Test the Application

```bash
# Test with limited episodes
docker-compose exec declue-spotify-check python main.py --test 2

# Test email configuration
docker-compose exec declue-spotify-check python main.py --test-email
```

### Debug Issues

```bash
# Access container shell
docker-compose exec declue-spotify-check bash

# Check logs
docker-compose logs declue-spotify-check

# Check volume contents
docker volume inspect declue-spotify-check_app_data
```

## Production Deployment

For production deployment, consider:

1. **Resource Limits**: Add memory and CPU limits to docker-compose.yml
2. **Restart Policies**: Already configured with `unless-stopped`
3. **Monitoring**: Use container monitoring tools
4. **Backup**: Regular backup of the `app_data` volume
5. **Security**: Run with non-root user (already configured)

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure the app user has access to mounted volumes
2. **Network Issues**: Check container can reach Spotify API and webhook URLs
3. **Environment Variables**: Verify all required variables are set
4. **Log File Issues**: Check data directory permissions

### Container Won't Start

```bash
# Check container status
docker-compose ps

# View startup logs
docker-compose logs declue-spotify-check

# Check image build
docker build -t declue-spotify-check .
```

### Application Errors

```bash
# Check application logs
docker-compose exec declue-spotify-check cat /app/data/debug.log

# Verify environment variables
docker-compose exec declue-spotify-check env | grep SPOTIFY
```
