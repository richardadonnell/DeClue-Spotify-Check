import json
import logging
import os
import argparse
from datetime import datetime, timedelta
from urllib.parse import urlparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(filename='debug.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Spotify API credentials
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')

# Webhook URL
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

# Show ID for DeClue Equine
SHOW_ID = os.getenv('SHOW_ID')

# File to store the last checked episodes
LAST_EPISODES_FILE = 'last_episodes.json'

# SMTP settings
SMTP_SERVER = os.getenv('SMTP_SERVER')
SMTP_PORT = int(os.getenv('SMTP_PORT'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
EMAIL_RECIPIENT = os.getenv('EMAIL_RECIPIENT')

def get_spotify_token():
    logging.debug("Attempting to get Spotify token")
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })
    auth_response_data = auth_response.json()
    logging.debug("Spotify token obtained successfully")
    return auth_response_data['access_token']

def get_all_episodes(token):
    logging.debug(f"Fetching all episodes for show ID: {SHOW_ID}")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    episodes = []
    url = f'https://api.spotify.com/v1/shows/{SHOW_ID}/episodes?limit=50'
    
    while url:
        response = requests.get(url, headers=headers)
        data = response.json()
        episodes.extend(data['items'])
        url = data['next']
    
    logging.debug(f"Fetched {len(episodes)} episodes")
    return episodes

def save_episodes(episodes):
    logging.debug(f"Saving {len(episodes)} episodes")
    with open(LAST_EPISODES_FILE, 'w') as f:
        json.dump([{
            'id': episode['id'],
            'name': episode['name'],
            'release_date': episode['release_date']
        } for episode in episodes], f)

def load_last_episodes():
    logging.debug("Loading last checked episodes")
    if os.path.exists(LAST_EPISODES_FILE):
        with open(LAST_EPISODES_FILE, 'r') as f:
            episodes = json.load(f)
            logging.debug(f"Loaded {len(episodes)} last checked episodes")
            return episodes
    logging.debug("No last checked episodes found")
    return []

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def trigger_webhook(new_episodes, test_limit=None):
    if test_limit:
        new_episodes = new_episodes[:test_limit]
    
    logging.debug(f"Triggering webhook for {len(new_episodes)} new episodes")
    payload = {
        'text': f"New episodes of DeClue Equine: {len(new_episodes)} found",
        'episodes': new_episodes
    }
    if not is_valid_url(WEBHOOK_URL):
        logging.error(f"Invalid webhook URL: {WEBHOOK_URL}")
        return False
    try:
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(WEBHOOK_URL, json=payload, headers=headers)
        response.raise_for_status()
        logging.debug(f"Webhook triggered successfully. Response: {response.text}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to trigger webhook: {str(e)}")
        if hasattr(e.response, 'text'):
            logging.error(f"Response content: {e.response.text}")
        return False

def rotate_log_file():
    logging.debug("Rotating log file")
    if os.path.exists('debug.log'):
        with open('debug.log', 'r') as f:
            lines = f.readlines()
        
        one_week_ago = datetime.now() - timedelta(days=7)
        new_lines = []
        for line in lines:
            try:
                log_date = datetime.strptime(line.split(' - ')[0], '%Y-%m-%d %H:%M:%S,%f')
                if log_date >= one_week_ago:
                    new_lines.append(line)
            except ValueError:
                # If we can't parse the date, keep the line
                new_lines.append(line)
        
        with open('debug.log', 'w') as f:
            f.writelines(new_lines)
        
        logging.debug(f"Removed {len(lines) - len(new_lines)} old log entries")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Check for new DeClue Equine podcast episodes and send notifications.')
    parser.add_argument('--test', type=int, help='Number of episodes to send for testing purposes')
    parser.add_argument('--test-email', action='store_true', help='Send a test email to verify SMTP settings')
    return parser.parse_args()

def send_test_email():
    try:
        message = MIMEMultipart()
        message['From'] = SMTP_USERNAME
        message['To'] = EMAIL_RECIPIENT
        message['Subject'] = 'DeClue Equine Script Test Email'

        body = "This is a test email to verify the SMTP settings for the DeClue Equine script."
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
            logging.info("Test email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send test email: {str(e)}")

def send_error_email(error_message):
    try:
        message = MIMEMultipart()
        message['From'] = SMTP_USERNAME
        message['To'] = EMAIL_RECIPIENT
        message['Subject'] = 'DeClue Equine Script Error'

        body = f"An error occurred while running the DeClue Equine script:\n\n{error_message}"
        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
            logging.debug("Error email sent successfully")
    except Exception as e:
        logging.error(f"Failed to send error email: {str(e)}")

def main():
    args = parse_arguments()
    rotate_log_file()
    logging.info("Script started")

    if args.test_email:
        send_test_email()
        return

    try:
        token = get_spotify_token()
        current_episodes = get_all_episodes(token)
        
        if not current_episodes:
            logging.info("No episodes found.")
            return

        last_episodes = load_last_episodes()
        last_episode_ids = set(episode['id'] for episode in last_episodes)

        new_episodes = [episode for episode in current_episodes if episode['id'] not in last_episode_ids]

        if new_episodes:
            logging.info(f"Found {len(new_episodes)} new episodes")
            if trigger_webhook(new_episodes, args.test):
                if not args.test:  # Only save episodes if not in test mode
                    save_episodes(current_episodes)
            else:
                logging.warning("Failed to trigger webhook, not saving current episodes")
        else:
            logging.info("No new episodes. Webhook not triggered.")
    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")
        send_error_email(str(e))
    finally:
        logging.info("Script completed")

if __name__ == "__main__":
    main()