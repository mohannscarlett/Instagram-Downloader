#Instagram Profile Downloader
#Mohann Scarlett 11/27/2023
import requests
import os
import sys

import getpass
from datetime import datetime

def download_insta_image(profile_name, current_file_number, URL):

    current_user = getpass.getuser()
    directory = "C:\\users\\" + str(current_user) + "\\desktop\\" + profile_name + "\\"
    current_date_time = datetime.now()
    current_date = current_date_time.date()
    file_number = None
    file_name = profile_name + "_" + str(current_file_number) + "_" + str(current_date)
    failed_download = ""

    try:
        response = requests.get(URL)
        if response.status_code == 200:
            with open(directory+file_name+'.jpg', 'wb') as img_file:
                img_file.write(response.content)
        else:
            failed_download = URL
    except Exception:
            failed_download = URL

    return failed_download