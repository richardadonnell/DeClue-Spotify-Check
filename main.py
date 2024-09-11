import json
import logging
import os
from datetime import datetime
from urllib.parse import urlparse

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

# File to store the last checked episode
LAST_EPISODE_FILE = os.getenv('LAST_EPISODE_FILE')

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

def get_latest_episode(token):
    logging.debug(f"Fetching latest episode for show ID: {SHOW_ID}")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'https://api.spotify.com/v1/shows/{SHOW_ID}/episodes', headers=headers)
    episodes = response.json()['items']
    if episodes:
        latest_episode = episodes[0]
        logging.debug(f"Latest episode found: {latest_episode['name']}")
        return latest_episode
    else:
        logging.warning("No episodes found")
        return None

def save_last_episode(episode):
    logging.debug(f"Saving last episode: {episode['name']}")
    with open(LAST_EPISODE_FILE, 'w') as f:
        json.dump({
            'id': episode['id'],
            'name': episode['name'],
            'release_date': episode['release_date']
        }, f)

def load_last_episode():
    logging.debug("Loading last checked episode")
    if os.path.exists(LAST_EPISODE_FILE):
        with open(LAST_EPISODE_FILE, 'r') as f:
            episode = json.load(f)
            logging.debug(f"Last checked episode: {episode['name']}")
            return episode
    logging.debug("No last checked episode found")
    return None

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def trigger_webhook(episode):
    logging.debug(f"Triggering webhook for episode: {episode['name']}")
    payload = {
        'text': f"New episode of DeClue Equine: {episode['name']}",
        'episode_data': episode  # Pass the entire episode data
    }
    if not is_valid_url(WEBHOOK_URL):
        logging.error(f"Invalid webhook URL: {WEBHOOK_URL}")
        return False
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        logging.debug("Webhook triggered successfully")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to trigger webhook: {str(e)}")
        return False

def main():
    logging.info("Script started")
    try:
        token = get_spotify_token()
        latest_episode = get_latest_episode(token)
        
        if not latest_episode:
            logging.info("No episodes found.")
            return

        last_checked_episode = load_last_episode()

        if not last_checked_episode or latest_episode['id'] != last_checked_episode['id']:
            logging.info(f"New episode found: {latest_episode['name']}")
            if trigger_webhook(latest_episode):
                save_last_episode(latest_episode)
            else:
                logging.warning("Failed to trigger webhook, not saving last episode")
        else:
            logging.info("No new episodes.")
    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")
    finally:
        logging.info("Script completed")

if __name__ == "__main__":
    main()