#Instagram Profile Downloader
#Mohann Scarlett 11/27/2023
import requests
import os
import sys

from bs4 import BeautifulSoup
import getpass
from datetime import datetime


def download_insta_video(profile_name, content_set):
    current_user = getpass.getuser()
    directory = "C:\\users\\"+str(current_user)+"\\desktop\\"+profile_name

    current_date_time = datetime.now()
    current_date = current_date_time.date()
    file_number = 0
    file_name = profile_name + "_" + str(file_number) + "_" + str(current_date)

    if not os.path.exists(directory):
           os.makedirs(directory)

    failed_download = set()
    counter = 1
    for i in content_set:
        sys.stdout.write("\rVideo " + str(counter) + "/" + str(len(content_set)))
        sys.stdout.flush()

        try:
            video_request = requests.get(i)
            if video_request.status_code == 200:
                with open(directory+'\\'+file_name+'.mp4', 'wb') as f:
                    f.write(video_request.content)
            else:
                failed_download.add(i)
        except Exception:
            failed_download.add(i)
        file_number += 1
        file_name = profile_name + "_" + str(file_number) + "_" + str(current_date)
        counter += 1
    print()
    return failed_download
