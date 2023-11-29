#Instagram Profile Downloader
#Mohann Scarlett 11/27/2023
import requests
import os
import sys

import getpass
from datetime import datetime

def download_image(profile_name, content_set, file_number_marker):
    current_user = getpass.getuser()
    directory = "C:\\users\\" + str(current_user) + "\\desktop\\" + profile_name

    current_date_time = datetime.now()
    current_date = current_date_time.date()
    file_number = file_number_marker + 1
    file_name = profile_name + "_" + str(file_number) + "_" + str(current_date)

    failed_download = set()
    counter = 1

    for i in content_set:
        sys.stdout.write("\rImage " + str(counter) + "/" + str(len(content_set)))
        sys.stdout.flush()
        try:
            response = requests.get(i)
            if response.status_code == 200:
                with open(directory+'\\'+file_name+'.jpg', 'wb') as img_file:
                    img_file.write(response.content)
            else:
                failed_download.add(i)
        except Exception:
            failed_download.add(i)
        file_number += 1
        file_name = profile_name + "_" + str(file_number) + "_" + str(current_date)
        counter += 1
    print()
    return failed_download