#!/bin/bash

# Log start time to cron.log
echo "Script started at $(date)" >> /home/richa/python-projects/DeClue-Spotify-Check/cron.log

# Change to the project directory
cd /home/richa/python-projects/DeClue-Spotify-Check || exit

# Activate the virtual environment
source env/bin/activate

# Run the Python script
python main.py

# Log completion time
echo "Script completed at $(date)" >> /home/richa/python-projects/DeClue-Spotify-Check/cron.log

# Optional: Explicitly exit the script
exit 0
