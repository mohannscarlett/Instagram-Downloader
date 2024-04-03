# Instagram Profile Downloader
# Mohann Scarlett 11/27/2023
import requests
import os
import sys

from bs4 import BeautifulSoup
import getpass
from datetime import datetime


def download_insta_video(profile_name, current_file_number, URL, directory):
    current_date_time = datetime.now()
    current_date = current_date_time.date()
    file_number = None
    file_name = None
    if current_file_number == -1:
        temp_file_name = "temporary_visual_video"
        file_name = temp_file_name
    elif current_file_number == -2:
        temp_file_name = "temporary_audio_video"
        file_name = temp_file_name

    failed_download = ""

    try:
        video_request = requests.get(URL)
        if video_request.status_code == 200:
            with open(file_name + '.mp4', 'wb') as f:
                f.write(video_request.content)
        else:
            failed_download = URL
    except Exception:
        failed_download = URL

    return failed_download
