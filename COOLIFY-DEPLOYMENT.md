# Coolify Deployment Guide

## Overview

This guide explains how to deploy the DeClue-Spotify-Check application on Coolify VPS using Docker.

## Prerequisites

- Coolify instance running on your VPS
- Git repository access (GitHub, GitLab, etc.)
- Required environment variables and secrets

## Deployment Steps

### 1. Connect Your Repository

1. In Coolify dashboard, go to **Projects** → **New Project**
2. Choose **Git Repository** as the source
3. Connect your GitHub/GitLab account
4. Select the `DeClue-Spotify-Check` repository
5. Choose the `prep-for-coolify` branch

### 2. Configure Application Settings

1. **Application Type**: Select "Docker Compose"
2. **Build Pack**: Select "Docker"
3. **Port**: Leave empty (no web interface)
4. **Domain**: Not required for this application

### 3. Set Environment Variables

In the Coolify dashboard, navigate to **Environment Variables** and add:

```
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

**Important**: Mark sensitive variables (passwords, API keys) as **Secret** in Coolify.

### 4. Configure Persistent Storage

1. Go to **Volumes** section
2. Add volume mapping: `app_data:/app/data`
3. This ensures data persistence across deployments

### 5. Deploy the Application

1. Click **Deploy** to start the initial deployment
2. Monitor the build logs in the Coolify interface
3. Wait for the deployment to complete successfully

### 6. Set Up Cron Scheduling

Since this application needs to run periodically (hourly), configure scheduling in Coolify:

1. Go to **Scheduled Tasks** in your application
2. Add a new scheduled task:
   - **Name**: "Check for new episodes"
   - **Command**: `python main.py`
   - **Schedule**: `0 * * * *` (every hour)
   - **Container**: Select your application container

### 7. Verify Deployment

1. Check application logs in Coolify dashboard
2. Verify the container is healthy
3. Test the application:
   ```bash
   # Through Coolify terminal
   python main.py --test 2
   python main.py --test-email
   ```

## Environment Variable Details

### Required Variables

- **SPOTIFY_CLIENT_ID**: Your Spotify API client ID
- **SPOTIFY_CLIENT_SECRET**: Your Spotify API client secret (mark as secret)
- **WEBHOOK_URL**: URL for webhook notifications
- **SHOW_ID**: Spotify podcast ID for DeClue Equine

### Email Configuration

- **SMTP_SERVER**: Your SMTP server hostname
- **SMTP_PORT**: SMTP port (usually 587 or 465)
- **SMTP_USERNAME**: Email account username
- **SMTP_PASSWORD**: Email account password (mark as secret)
- **EMAIL_RECIPIENT**: Email address for error notifications

### Optional Variables

- **DATA_DIR**: Data directory path (defaults to `/app/data`)

## Coolify Features Used

### Auto-Deployment

- **Git Integration**: Automatic deployments on git push
- **Webhook Support**: GitHub/GitLab webhooks for instant deployment
- **Branch Protection**: Deploy only from specific branches

### Monitoring

- **Health Checks**: Automatic container health monitoring
- **Logs**: Centralized log viewing and searching
- **Alerts**: Email notifications for deployment failures

### Security

- **Secret Management**: Encrypted storage of sensitive variables
- **Container Isolation**: Applications run in isolated containers
- **SSL/TLS**: Automatic HTTPS certificates (if domain configured)

## Migration from Existing Cron Setup

### 1. Backup Current Data

Before migration, backup your current setup:

```bash
# On your current server
sudo cp /home/richa/python-projects/DeClue-Spotify-Check/last_episodes.json /backup/
sudo cp /home/richa/python-projects/DeClue-Spotify-Check/debug.log /backup/
```

### 2. Disable Current Cron Job

```bash
# Remove from crontab
crontab -e
# Comment out or remove the DeClue line: 0 * * * * /home/richa/python-projects/DeClue-Spotify-Check/run_script.sh
```

### 3. Transfer Data to Coolify

After successful Coolify deployment:

1. Access Coolify container terminal
2. Upload backed up `last_episodes.json` to `/app/data/`
3. Verify the application can read the existing state

### 4. Test New Setup

1. Run a test execution in Coolify
2. Verify webhook notifications work
3. Check email alerts function correctly
4. Monitor logs for any issues

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check Docker syntax in Dockerfile
   - Verify all files are committed to git
   - Check Coolify build logs

2. **Runtime Errors**
   - Verify environment variables are set correctly
   - Check network connectivity to Spotify API
   - Review application logs in Coolify

3. **Scheduling Issues**
   - Confirm cron expression syntax
   - Check scheduled task logs in Coolify
   - Verify container is running

### Debug Commands

```bash
# Check container status
docker ps

# View application logs
docker logs <container_name>

# Access container
docker exec -it <container_name> bash

# Check data persistence
ls -la /app/data/
```

### Support Resources

- [Coolify Documentation](https://coolify.io/docs)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Spotify API Documentation](https://developer.spotify.com/documentation/web-api/)

## Post-Deployment

### Monitoring

1. **Set up Monitoring**: Configure Coolify alerts
2. **Log Rotation**: Monitor log file sizes
3. **Health Checks**: Verify container health regularly
4. **Performance**: Monitor resource usage

### Maintenance

1. **Updates**: Use Coolify's git integration for updates
2. **Backups**: Regular backup of persistent data
3. **Security**: Keep base images updated
4. **Scaling**: Monitor and adjust resources as needed
