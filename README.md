# DeClue-Spotify-Check

This project is an automated system that checks for new episodes of the DeClue Equine podcast on Spotify and sends notifications via a webhook when new episodes are found.

## Project Description

The DeClue-Spotify-Check script performs the following tasks:

1. Authenticates with the Spotify API using client credentials.
2. Retrieves all episodes of the DeClue Equine podcast from Spotify.
3. Compares the retrieved episodes with a locally stored list of previously checked episodes.
4. Identifies any new episodes that have been published since the last check.
5. If new episodes are found, it sends a notification with episode details to a specified webhook.
6. Updates the local storage with the current list of episodes.

This automation allows for easy monitoring of new podcast episodes without manual checking, enabling quick notifications and potential further actions through the webhook integration.

## Key Features

- Spotify API Integration: Utilizes Spotify's API to fetch podcast episode data.
- Webhook Notifications: Sends notifications about new episodes to a specified webhook URL.
- Local State Management: Maintains a local JSON file to keep track of previously checked episodes.
- Pagination Handling: Capable of retrieving all episodes, even if they span multiple pages in the Spotify API response.
- Error Handling and Logging: Implements comprehensive error handling and logging for easy debugging and monitoring.
- Log Rotation: Automatically manages the debug log file, keeping only the last week of logs to prevent excessive file growth.

## Configuration

The project uses environment variables for configuration, which should be set in a `.env` file:

- `SPOTIFY_CLIENT_ID`: Your Spotify API client ID
- `SPOTIFY_CLIENT_SECRET`: Your Spotify API client secret
- `WEBHOOK_URL`: The URL of the webhook to send notifications to
- `SHOW_ID`: The Spotify ID of the DeClue Equine podcast

## Usage

To use this script:

1. Ensure all required Python packages are installed (see `requirements.txt`).
2. Set up the `.env` file with the necessary configuration.
3. Run the script using Python: `python main.py`

The script can be scheduled to run periodically (e.g., using cron jobs) to regularly check for new episodes.

## Files

- `main.py`: The main Python script that performs the Spotify checking and webhook notification.
- `.env`: Configuration file for environment variables (not tracked in git).
- `last_episodes.json`: JSON file storing information about previously checked episodes (not tracked in git).
- `debug.log`: Log file for debugging information (not tracked in git).

## Dependencies

- Python 3.x
- requests
- python-dotenv

## Note

Ensure that your Spotify API credentials and webhook URL are kept secure and not shared publicly.
