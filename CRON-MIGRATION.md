# Cron Scheduling Migration Guide

## Overview

This guide documents the migration from system cron jobs on Raspberry Pi to Coolify's built-in cron scheduling for the DeClue-Spotify-Check application.

## Current System (Raspberry Pi)

### Existing Cron Configuration

```bash
# Current crontab entry
0 * * * * /home/richa/python-projects/DeClue-Spotify-Check/run_script.sh >> /home/richa/python-projects/DeClue-Spotify-Check/cron.log 2>&1
```

**Schedule**: Every hour at minute 0
**Script**: `run_script.sh`
**Logging**: Redirected to `cron.log`

### Current Script Execution Flow

1. **Environment Activation**: Sources Python virtual environment
2. **Directory Change**: Changes to project directory
3. **Python Execution**: Runs `main.py`
4. **Log Output**: Captures both stdout and stderr

```bash
#!/bin/bash
cd /home/richa/python-projects/DeClue-Spotify-Check
source env/bin/activate
python main.py
```

## Coolify Cron Scheduling

### Access Cron Configuration

1. Open Coolify dashboard
2. Navigate to your application: `declue-spotify-check`
3. Go to **Configuration** > **Scheduled Tasks**
4. Click **Add Scheduled Task**

### Cron Schedule Configuration

#### Basic Settings

**Task Name**: `spotify-episode-check`

**Schedule Expression**: `0 * * * *`
- **Format**: Standard cron format
- **Frequency**: Every hour at minute 0
- **Same as**: Current Raspberry Pi schedule

#### Command Configuration

**Container**: `declue-spotify-check` (your main application container)

**Command**: `python main.py`
- **Working Directory**: `/app` (container working directory)
- **Environment**: Inherits all environment variables
- **User**: `app` (non-root user from Dockerfile)

#### Advanced Options

**Timeout**: `300` seconds (5 minutes)
- **Purpose**: Prevents hanging processes
- **Recommendation**: Generous timeout for API calls

**Restart Policy**: `never`
- **Reason**: Cron jobs should complete and exit
- **Behavior**: Failed jobs don't restart automatically

**Resource Limits**:
- **Memory**: `128MB` (sufficient for Python script)
- **CPU**: `0.1` CPU cores

### Schedule Expression Examples

#### Current Schedule

```bash
0 * * * *    # Every hour at minute 0
```

#### Alternative Schedules

```bash
*/30 * * * *  # Every 30 minutes
0 */2 * * *   # Every 2 hours
0 8,20 * * *  # Twice daily (8 AM and 8 PM)
0 9 * * 1-5   # Weekdays at 9 AM
```

### Benefits of Coolify Cron

#### Advantages Over System Cron

1. **Container Integration**: Runs in same environment as application
2. **Centralized Management**: All configuration in Coolify dashboard
3. **Logging Integration**: Logs available in Coolify interface
4. **Resource Management**: CPU and memory limits
5. **Monitoring**: Built-in execution tracking
6. **Scalability**: Easy to modify schedule without server access

#### Monitoring Features

- **Execution History**: Track successful and failed runs
- **Duration Tracking**: Monitor execution time
- **Resource Usage**: CPU and memory consumption
- **Alert Integration**: Notifications for failures

## Migration Process

### Step 1: Prepare Application

Ensure the containerized application is working:

```bash
# Test container locally
docker-compose up --build
```

### Step 2: Deploy to Coolify

1. Deploy the Docker application to Coolify
2. Verify environment variables are configured
3. Test manual execution through Coolify terminal

### Step 3: Configure Cron Schedule

1. Add the scheduled task in Coolify dashboard
2. Use identical schedule: `0 * * * *`
3. Set command to: `python main.py`
4. Configure timeout and resource limits

### Step 4: Test Cron Execution

1. **Wait for Next Hour**: Allow natural execution
2. **Manual Trigger**: Use Coolify's manual trigger option
3. **Check Logs**: Verify execution in Coolify logs
4. **Validate Output**: Confirm webhook and email functionality

### Step 5: Disable Raspberry Pi Cron

Once Coolify cron is confirmed working:

```bash
# Remove old crontab entry
crontab -e
# Comment out or delete the line:
# 0 * * * * /home/richa/python-projects/DeClue-Spotify-Check/run_script.sh >> /home/richa/python-projects/DeClue-Spotify-Check/cron.log 2>&1
```

### Step 6: Archive Raspberry Pi Setup

1. **Backup Current Data**: Copy `last_episodes.json` and logs
2. **Document Configuration**: Save current environment variables
3. **Transfer State**: Import existing state to Coolify deployment

## Logging Comparison

### Raspberry Pi Logging

```bash
# Cron logs to file
/home/richa/python-projects/DeClue-Spotify-Check/cron.log

# Application logs to file
/home/richa/python-projects/DeClue-Spotify-Check/debug.log
```

### Coolify Logging

#### Cron Execution Logs

- **Location**: Coolify dashboard > Application > Scheduled Tasks > Execution History
- **Content**: Command output, exit codes, execution duration
- **Retention**: Configurable retention period

#### Application Logs

- **Location**: Coolify dashboard > Application > Logs
- **Content**: Container stdout/stderr, including debug.log output
- **Features**: Real-time streaming, search, filtering

#### Log Configuration

Update logging in containerized application:

```python
# Enhanced logging for container environment
import logging
import sys

# Configure dual logging: file + stdout
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/data/debug.log'),
        logging.StreamHandler(sys.stdout)  # Coolify captures this
    ]
)
```

## Monitoring and Alerts

### Coolify Monitoring Features

#### Execution Tracking

- **Success Rate**: Percentage of successful executions
- **Average Duration**: Typical execution time
- **Resource Usage**: CPU and memory consumption
- **Failure Patterns**: Common failure reasons

#### Alert Configuration

1. **Email Alerts**: Configure for cron failures
2. **Webhook Integration**: External monitoring systems
3. **Dashboard Notifications**: In-app alerts
4. **Threshold Alerts**: For execution duration or resource usage

### Application-Level Monitoring

The application includes built-in email notifications for errors:

```python
# Email alerts are sent when exceptions occur
def send_error_email(error_message):
    # SMTP configuration from environment variables
    # Automatic email alerts for application failures
```

## Troubleshooting

### Common Issues

#### Schedule Not Executing

1. **Check Schedule Format**: Verify cron expression syntax
2. **Container Status**: Ensure main application is running
3. **Resource Limits**: Check if resource constraints are blocking execution
4. **Permissions**: Verify container user has necessary permissions

#### Command Failures

1. **Environment Variables**: Ensure all required variables are set
2. **Working Directory**: Verify command runs from correct directory
3. **Dependencies**: Check all Python packages are available
4. **File Permissions**: Ensure data directory is writable

#### Log Access Issues

1. **Log Retention**: Check Coolify log retention settings
2. **Log Volume**: Ensure log volume is properly mounted
3. **Application Logging**: Verify application writes to expected locations

### Debug Commands

Access container through Coolify terminal:

```bash
# Test manual execution
python main.py --test 1

# Check environment
env | grep -E "(SPOTIFY|SMTP|WEBHOOK)"

# Verify file access
ls -la /app/data/

# Test cron schedule parsing
python -c "import os; print('Container ready for cron')"
```

### Schedule Validation

```bash
# Test cron expression (if available in container)
# Note: This depends on system tools being available
echo "0 * * * *" | crontab -
crontab -l
```

## Performance Considerations

### Resource Optimization

#### Memory Usage

- **Container Limit**: 128MB (generous for Python script)
- **Application Usage**: ~50MB typical
- **Monitoring**: Track actual usage in Coolify

#### CPU Usage

- **Container Limit**: 0.1 CPU cores
- **Application Usage**: Minimal (I/O bound)
- **Considerations**: API calls may cause brief spikes

#### Network Usage

- **Spotify API**: Minimal data transfer
- **Webhook Calls**: Small JSON payloads
- **Email Notifications**: Only on errors

### Scaling Considerations

#### Multiple Instances

- **Current Need**: Single instance sufficient
- **Future Scaling**: Easy to add multiple schedules
- **Conflict Prevention**: State file locking may be needed

#### Geographic Distribution

- **Current Setup**: Single server deployment
- **Future Options**: Multiple Coolify servers
- **Data Sync**: Consider state synchronization

## Best Practices

### Schedule Management

1. **Consistent Timing**: Keep same schedule as Raspberry Pi initially
2. **Gradual Changes**: Test schedule changes in development
3. **Documentation**: Document any schedule modifications
4. **Monitoring**: Watch for execution patterns

### Maintenance

1. **Regular Review**: Monthly review of execution logs
2. **Performance Monitoring**: Track execution duration trends
3. **Error Analysis**: Investigate any execution failures
4. **Schedule Optimization**: Adjust timing based on actual needs

### Backup Strategy

1. **State Files**: Regular backup of application state
2. **Configuration**: Backup Coolify configuration
3. **Log Archives**: Periodic log archival
4. **Recovery Testing**: Test restore procedures

## Migration Checklist

- [ ] Deploy containerized application to Coolify
- [ ] Configure all environment variables
- [ ] Test manual application execution
- [ ] Create scheduled task with `0 * * * *` schedule
- [ ] Set command to `python main.py`
- [ ] Configure resource limits and timeout
- [ ] Test manual cron trigger
- [ ] Monitor first automatic execution
- [ ] Verify logs are accessible
- [ ] Confirm webhook and email functionality
- [ ] Transfer existing state data
- [ ] Disable Raspberry Pi cron job
- [ ] Archive old configuration
- [ ] Document new monitoring procedures
