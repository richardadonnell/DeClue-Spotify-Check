# Coolify Environment Setup Guide

## Overview

This guide provides detailed instructions for configuring environment variables and settings in the Coolify dashboard for the DeClue-Spotify-Check application.

## Environment Variables Configuration

### Access Environment Variables

1. Log into your Coolify dashboard
2. Navigate to your project
3. Select the DeClue-Spotify-Check application
4. Go to **Environment Variables** tab

### Required Environment Variables

#### Spotify API Configuration

**SPOTIFY_CLIENT_ID**
- **Type**: Standard
- **Value**: Your Spotify application client ID
- **Description**: Public identifier for your Spotify app
- **Required**: Yes

**SPOTIFY_CLIENT_SECRET**
- **Type**: Secret (mark as sensitive)
- **Value**: Your Spotify application client secret
- **Description**: Private key for Spotify API authentication
- **Required**: Yes

**SHOW_ID**
- **Type**: Standard
- **Value**: Spotify podcast ID for DeClue Equine
- **Description**: Unique identifier for the podcast to monitor
- **Required**: Yes

#### Webhook Configuration

**WEBHOOK_URL**
- **Type**: Standard (or Secret if sensitive)
- **Value**: Complete URL for webhook notifications
- **Example**: `https://hooks.slack.com/services/...` or `https://discord.com/api/webhooks/...`
- **Description**: Endpoint for receiving new episode notifications
- **Required**: Yes

#### Email Configuration

**SMTP_SERVER**
- **Type**: Standard
- **Value**: SMTP server hostname
- **Examples**: `smtp.gmail.com`, `smtp.outlook.com`, `smtp.company.com`
- **Description**: SMTP server for sending error notifications
- **Required**: Yes

**SMTP_PORT**
- **Type**: Standard
- **Value**: SMTP server port number
- **Common Values**: `587` (STARTTLS), `465` (SSL), `25` (plain)
- **Default**: 587
- **Required**: Yes

**SMTP_USERNAME**
- **Type**: Standard
- **Value**: Email account username
- **Description**: Username for SMTP authentication
- **Required**: Yes

**SMTP_PASSWORD**
- **Type**: Secret (mark as sensitive)
- **Value**: Email account password or app password
- **Description**: Password for SMTP authentication
- **Required**: Yes

**EMAIL_RECIPIENT**
- **Type**: Standard
- **Value**: Email address for notifications
- **Description**: Where to send error alerts and notifications
- **Required**: Yes

### Optional Environment Variables

**DATA_DIR**
- **Type**: Standard
- **Value**: `/app/data` (default)
- **Description**: Container path for persistent data storage
- **Required**: No

## Coolify Configuration Steps

### 1. Basic Application Settings

1. **Application Name**: `declue-spotify-check`
2. **Build Pack**: Docker
3. **Docker Compose**: Enable
4. **Port**: Leave empty (no web interface)
5. **Domain**: Not required

### 2. Git Repository Settings

1. **Repository URL**: Your git repository
2. **Branch**: `prep-for-coolify`
3. **Build Context**: Root directory
4. **Dockerfile Path**: `./Dockerfile`
5. **Docker Compose Path**: `./docker-compose.yml`

### 3. Build Configuration

1. **Build Command**: Not required (Docker handles build)
2. **Install Command**: Not required
3. **Start Command**: Defined in docker-compose.yml

### 4. Volume Configuration

#### Persistent Data Volume

1. Go to **Volumes** section
2. Click **Add Volume**
3. Configure:
   - **Name**: `app_data`
   - **Mount Path**: `/app/data`
   - **Type**: Named Volume
   - **Backup**: Enable for data safety

#### Benefits of Volume Configuration

- **Data Persistence**: State survives container restarts
- **Backup Integration**: Coolify can backup volume data
- **Performance**: Better I/O performance than bind mounts
- **Portability**: Easy to migrate between servers

### 5. Network Configuration

Since this application doesn't serve web traffic:

1. **Port Mapping**: Not required
2. **Domain**: Not needed
3. **SSL Certificate**: Not applicable
4. **Reverse Proxy**: Disabled

### 6. Health Check Configuration

Health checks are defined in docker-compose.yml:

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import os; exit(0 if os.path.exists('/app/data') else 1)"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

Benefits:
- **Automatic Recovery**: Coolify restarts unhealthy containers
- **Monitoring**: Dashboard shows health status
- **Alerting**: Notifications for persistent failures

## Security Best Practices

### Secret Management

1. **Mark Sensitive Variables**: Always mark passwords, API keys, and tokens as secrets
2. **Environment Separation**: Use different values for development/production
3. **Access Control**: Limit who can view/edit environment variables
4. **Rotation**: Regularly rotate API keys and passwords

### Container Security

1. **Non-Root User**: Application runs as 'app' user (configured in Dockerfile)
2. **Read-Only Filesystem**: Only /app/data is writable
3. **Resource Limits**: Configure CPU and memory limits
4. **Network Isolation**: Container only accesses required external services

## Testing Environment Configuration

### Development Environment

Create a separate Coolify application for testing:

1. **Name**: `declue-spotify-check-dev`
2. **Branch**: Development branch
3. **Environment Variables**: Test values
4. **Schedule**: Less frequent (for testing)

### Validation Steps

1. **Deploy Application**: Ensure successful deployment
2. **Check Logs**: Verify no configuration errors
3. **Test Execution**: Run with `--test` flag
4. **Test Email**: Use `--test-email` command
5. **Monitor Health**: Verify health checks pass

## Monitoring and Alerts

### Coolify Monitoring Features

1. **Container Health**: Real-time health status
2. **Resource Usage**: CPU, memory, disk monitoring
3. **Logs**: Centralized log aggregation
4. **Deployment History**: Track deployment success/failure

### Alert Configuration

1. **Email Notifications**: Configure for deployment failures
2. **Webhook Alerts**: Integration with external monitoring
3. **Health Check Failures**: Automatic notifications
4. **Resource Limits**: Alerts for high resource usage

## Troubleshooting

### Common Environment Issues

1. **Missing Variables**: Check all required variables are set
2. **Incorrect Values**: Verify variable values are correct
3. **Secret Access**: Ensure secrets are properly configured
4. **Type Mismatch**: Check variable types (string, number, boolean)

### Debug Commands

Access container terminal in Coolify:

```bash
# Check environment variables
env | grep SPOTIFY
env | grep SMTP

# Test directory access
ls -la /app/data/

# Test Python imports
python -c "import os; print(os.environ.get('SPOTIFY_CLIENT_ID', 'NOT SET'))"
```

### Environment Variable Validation

```bash
# Check all required variables
python -c "
import os
required = ['SPOTIFY_CLIENT_ID', 'SPOTIFY_CLIENT_SECRET', 'WEBHOOK_URL', 'SHOW_ID']
missing = [var for var in required if not os.environ.get(var)]
print('Missing variables:', missing if missing else 'None')
"
```

## Maintenance

### Regular Tasks

1. **Variable Review**: Quarterly review of environment variables
2. **Secret Rotation**: Regular rotation of sensitive credentials
3. **Health Monitoring**: Monitor application health and performance
4. **Backup Verification**: Ensure volume backups are working

### Updates and Changes

1. **Variable Updates**: Use Coolify interface for changes
2. **Deployment**: Redeploy after environment changes
3. **Testing**: Verify changes in development environment first
4. **Documentation**: Keep this guide updated with changes
