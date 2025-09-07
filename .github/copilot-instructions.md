# DeClue-Spotify-Check Copilot Instructions

## Project Overview
This is a Python-based automation script that monitors the "DeClue Equine" podcast on Spotify for new episodes and sends webhook notifications when new content is detected. The system runs via cron jobs and maintains persistent state between executions.

## Core Architecture

### State Management Pattern
- **Persistent state**: `last_episodes.json` stores episode metadata (id, name, release_date) between runs
- **Comparison logic**: New episodes are detected by comparing current Spotify API response against stored episode IDs
- **Atomic updates**: Episodes are only saved to state file after successful webhook delivery (except in test mode)

### API Integration Flow
1. **Spotify OAuth**: Uses client credentials flow (`get_spotify_token()`) - no user authentication required
2. **Pagination handling**: `get_all_episodes()` automatically follows `next` URLs to fetch complete episode list
3. **Webhook payload**: Sends structured JSON with episode count and full episode details array

### Environment Configuration
All sensitive data is managed via `.env` file (not in git):
```
SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET  # Spotify API credentials
WEBHOOK_URL                               # Notification endpoint
SHOW_ID                                   # Spotify podcast identifier
SMTP_*                                    # Email settings for error notifications
```

## Development Workflows

### Testing Commands
```bash
# Test with limited episodes (doesn't update state)
python main.py --test 2

# Test email configuration
python main.py --test-email
```

### Virtual Environment Setup
- Project uses `env/` virtual environment (standard venv, not conda)
- **Critical**: Always activate before running: `source env/bin/activate` (Linux) or `.\env\Scripts\Activate.ps1` (Windows)
- Dependencies are minimal: `python-dotenv`, `requests` only

### Deployment Pattern
- **Production**: Runs via `run_script.sh` cron job every hour (`0 * * * *`)
- **Logging**: Dual logging system - `debug.log` (application) + `cron.log` (cron output)
- **Log rotation**: `rotate_log_file()` automatically purges entries older than 7 days

## Code Patterns & Conventions

### Error Handling Strategy
- **Graceful degradation**: Script continues on non-critical errors but logs extensively
- **Email alerting**: Automatic error emails sent via SMTP when exceptions occur in main()
- **Webhook validation**: URL validation before POST requests (`is_valid_url()`)

### Logging Philosophy
- **Debug-first**: All operations logged at DEBUG level to `debug.log`
- **Production safety**: No sensitive data (tokens, credentials) in logs
- **Timestamp preservation**: Log rotation maintains chronological order

### Data Structures
- Episode objects are simplified to essential fields: `{id, name, release_date}`
- Webhook payload structure: `{text: summary, episodes: [episode_array]}`
- State persistence uses direct JSON serialization (no ORM/database)

## Key Dependencies & Integrations

### Spotify API Specifics
- **Endpoint**: Uses `/v1/shows/{id}/episodes` with 50-item pagination
- **Rate limiting**: No explicit handling (relies on stable cron scheduling)
- **Token management**: Fresh token obtained on each run (no caching/refresh logic)

### Cross-Platform Considerations
- Shell script paths are Linux-specific (`/home/richa/python-projects/...`)
- Windows users should adapt paths in `run_script.sh` or run directly via Python

## Common Maintenance Tasks

### Adding New Notification Channels
- Extend `trigger_webhook()` function for additional endpoints
- Consider adding similar validation patterns as `is_valid_url()`

### State Recovery
- If `last_episodes.json` is corrupted/missing, script treats all episodes as "new"
- Use `--test` mode to verify behavior before production runs

### Debugging Integration Issues
- Check `debug.log` for API response details and webhook status codes
- Verify `.env` file presence and variable names (script will fail silently on missing vars)
- Test Spotify API connectivity: token acquisition is the first failure point
