#Instagram Profile Downloader
#Mohann Scarlett 11/27/2023
import time
import sys
import getpass
from datetime import datetime
import os
import logging
import hashlib
import subprocess
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from video_downloader import download_insta_video
from image_downloader import download_insta_image

from moviepy.editor import VideoFileClip, AudioFileClip

from pymediainfo import MediaInfo

from mutagen.mp4 import MP4, MP4Cover

def calculate_file_hash(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        hash_value = hashlib.md5(content).hexdigest()
    return hash_value


def check_video_stream(file_path):
    file_path = os.path.abspath(file_path)
    fileInfo = MediaInfo.parse(file_path)
    for track in fileInfo.tracks:
        if track.track_type == "Video":
            print("Audio file has video")
            return True
        else:
            print("Audio file has NO video")
            return False
    # success!


def set_mp4_comment(file_path, new_comment):
    # Open the MP4 file for editing
    mp4_file = MP4(file_path)

    # Set the new comment metadata
    mp4_file['\xa9cmt'] = [new_comment]

    # Save the changes
    mp4_file.save()


def combine_video_audio(video_path, audio_path, output_filename, driver):
    # Load video and audio clips
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Set video clip's audio
    video_clip = video_clip.set_audio(audio_clip)
    # Save the combined video
    try:
        video_clip.write_videofile(output_filename, codec='libx264', audio_codec='aac')
    except Exception as e:
        print("Error while merging video and audio, will continue without downloading this file +\n " + str(
            driver.current_url))
        video_clip.close()
        audio_clip.close()
        return

    set_mp4_comment(output_filename, driver.current_url)
    # Close clips
    video_clip.close()
    audio_clip.close()


def get_image_link(driver, post_container, picture_set, mode):
    try:
        post_images = post_container.find_elements(by=By.XPATH,
                                                   value='.//*[@class="x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o '
                                                         'xh8yej3"]')
        for i in post_images:
            image_URL = i.get_attribute("src")
            if image_URL not in picture_set or mode == 1:
                return image_URL
    except NoSuchElementException as e:
        return False


def get_image_link(driver, post_container, picture_set, mode):
    try:
        post_images = post_container.find_elements(by=By.XPATH,
                                                   value='.//*[@class="x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o '
                                                         'xh8yej3"]')
        for i in post_images:
            image_URL = i.get_attribute("src")
            if image_URL not in picture_set or mode == 1:
                return image_URL
    except NoSuchElementException as e:
        return False


def get_video_link(driver, list_of_video_types, list_of_audio_types):
    substring_to_find = ".mp4"

    link_found = False
    video_links_filtered = []
    video_links_raw = []

    stuck_in_loop = 0
    #rint("List of links")
    while not link_found:
        if stuck_in_loop > 5:
            #print("System error logger:\nNew video ssid to document")
            for entry in network_data:
                video_link = entry.get('name')
                #print(video_link)
            break
        network_data = driver.execute_script("return window.performance.getEntries();")
        for entry in network_data:
            if substring_to_find in entry['name']:
                video_link = entry.get('name')
                #print(video_link)
                # Find the index of '&bytestart'
                index = video_link.find('&bytestart')
                if index != -1:  # Check if '&bytestart' is found in the URL
                    video_links_raw.append(video_link)
                    video_link = video_link[:index]  # Extract the portion before '&bytestart'
                else:
                    pass
                    #print("&bytestart not in URL")
                video_links_filtered.append(video_link)
                link_found = True

        stuck_in_loop += 1
    visual_video_link = ""
    audio_video_link = ""

    found = False
    try:
        found = False
        for i in video_links_raw:
            if found == True:
                break
            for j in list_of_video_types:
                if j in i and "&bytestart=0&byteend=" in i:
                    # print("here")
                    index = i.find('&bytestart')
                    if index != -1:  # Check if '&bytestart' is found in the URL
                        visual_video_link = i[:index]
                    found = True
                    break
        if found == False:
            raise NoSuchElementException("Error 306")
    except NoSuchElementException as e:
        # print(e)
        temp_video_list = []
        for i in video_links_filtered:
            for j in list_of_video_types:
                if j in i:
                    temp_video_list.append(i)

        if int(len(temp_video_list) / 2) != 0:
            visual_video_link = temp_video_list[int(len(temp_video_list) / 2)]
        else:
            for i in video_links_filtered:
                for j in list_of_video_types:
                    if (j in i):
                        visual_video_link = i

        for i in video_links_filtered:
            if list_of_video_types[2] in i:
                visual_video_link = i
                for j in video_links_filtered:
                    if "_n.mp4" in j:
                        audio_video_link = j
                        break

    for i in video_links_filtered:
        for j in list_of_audio_types:
            if j in i:
                audio_video_link = i

    return [visual_video_link, audio_video_link]


def get_video_link_scrolling(driver, list_of_video_types, list_of_audio_types):
    substring_to_find = ".mp4"

    link_found = False
    video_links_filtered = []
    video_links_raw = []

    stuck_in_loop = 0
    #print("List of links")
    while not link_found:
        if stuck_in_loop > 5:
            #print("System error logger:\nNew video ssid to document")
            for entry in network_data:
                video_link = entry.get('name')
                #print(video_link)
            break
        network_data = driver.execute_script("return window.performance.getEntries();")

        for entry in network_data:
            if substring_to_find in entry['name']:
                video_link = entry.get('name')
                #print(video_link)
                # Find the index of '&bytestart'
                index = video_link.find('&bytestart')
                if index != -1:  # Check if '&bytestart' is found in the URL
                    if video_link not in video_links_raw:
                        video_links_raw.append(video_link)
                    video_link = video_link[:index]  # Extract the portion before '&bytestart'
                else:
                    pass
                    #print("&bytestart not in URL")
                if video_link not in video_links_filtered:
                    video_links_filtered.append(video_link)
                link_found = True

        stuck_in_loop += 1
    visual_video_link = ""
    audio_video_link = ""

    visual_video_links_highquality = []
    audio_video_links_highquality = []

    visual_video_links_lowquality = []
    audio_video_links_lowquality = []

    video_byte_ends = []
    audio_byte_ends = []

    found = False
    try:
        found = False
        for position, i in enumerate(video_links_raw):
            # look_for_audio = True
            for j in list_of_video_types:
                if j in i and "&bytestart=0&byteend=" in i:

                    # print("here")
                    index = i.find('&bytestart')
                    if index != -1:  # Check if '&bytestart' is found in the URL
                        visual_video_links_highquality.append(i[:index])

                        byte_end_index = i.find('&byteend=')
                        if byte_end_index != -1:  # Check if '&bytestart' is found in the URL
                            video_byte_ends.append(int(i[byte_end_index + len('&byteend='):]))


                    found = True



            for j in list_of_audio_types:
                if j in i and "&bytestart=0&byteend=" in i:

                    index = i.find('&bytestart')
                    if index != -1:  # Check if '&bytestart' is found in the URL
                        audio_video_links_highquality.append(i[:index])


                    found = True
        if found == False:
            raise NoSuchElementException("Error 306")
    except NoSuchElementException as e:
        print(e)
        return ["", ""]
        # quit()

    if len(visual_video_links_highquality) == len(audio_video_links_highquality):

        return [visual_video_links_highquality, audio_video_links_highquality]


    return ["", ""]


def download_failed_posts(driver,list_of_video_types, list_of_audio_types,parent_directory):

    error_logs = []
    #try:
    profile_name = "Failed_posts"
    page_loading_time = 7.5
    scroll_timeout = 0.5
    video_render_sleep = 1.25
    video_render_sleep_single = 1.25

    final_picture_set = set()
    final_video_set = set()

    posts_visited = 0
    current_file_number = 0
    number_posts_downloaded = 0

    current_user = getpass.getuser()
    directory = parent_directory + profile_name + "\\"
    current_directory = os.getcwd()

    if not os.path.exists(directory):
        os.makedirs(directory)

    post_links = set()
    file_path = os.path.abspath("Failed.txt")
    with open(file_path, 'r') as file:
        # Iterate through each line in the file
        for line in file:
            post_links.add(line)

    print(len(post_links))
    number_of_posts = int(len(post_links))
    print("\nTotal Number of Failed Posts to Retry: " + str(number_of_posts), end='\n\n')
    
    failed_visual_videos = set()
    failed_audio_videos = set()
    post_url_set = set()


    for i in post_links:
        files_from_current_post = []
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # time.sleep(scroll_timeout)
        driver.get(i)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                        '//*[@class="x1yvgwvq x1dqoszc x1ixjvfu xhk4uv x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x178xt8z xm81vs4 xso031l xy80clv x78zum5 x1q0g3np xh8yej3"]')))

        post_container = None
        try:
            post_container = driver.find_element(by=By.XPATH,
                                                 value='//*[@class="x1ey2m1c x9f619 xds687c x10l6tqk x17qophe x13vifvy x1ypdohk"]')
        except NoSuchElementException:
            post_container = driver.find_element(by=By.XPATH,
                                                 value='//*[@class="_aatk _aatl"]')

        next_button_visible = True
        next_button_clicked = False
        next_button = None

        time.sleep(video_render_sleep)
        if_worked = True

        single_content = True
        try:
            test_button = post_container.find_element(by=By.XPATH, value='.//*[@class=" _afxw _al46 _al47"]')
            single_content = False
        except NoSuchElementException:
            # is a stand alone video
            pass

        image_found = get_image_link(driver, post_container, final_picture_set, 0)
        if isinstance(image_found, str) and image_found not in final_picture_set:
            final_picture_set.add(image_found)
            failed_image_downloads = download_insta_image(profile_name, current_file_number, image_found)
            current_file_number += 1
        else:
            if single_content:
                video_link = get_video_link(driver, list_of_video_types, list_of_audio_types)
                if (download_insta_video(profile_name, -1, video_link[0], current_directory)  == "" and
                            download_insta_video(profile_name, -2, video_link[1], current_directory)) == "":
                    current_date_time = datetime.now()
                    current_date = current_date_time.date()
                    file_name = profile_name + "_" + str(current_file_number) + "_" + str(current_date) + ".mp4"

                    #print("video link: " + video_link[0], "Audio link: " + video_link[1])

                    if video_link[0] == "" and video_link[1] == "":
                        failed_visual_videos.add(video_link[0])
                        failed_audio_videos.add(video_link[1])
                        post_url_set.add(driver.current_url)
                        if_worked = False
                        #next_button_visible = False
                    elif video_link[0] == "":
                        failed_visual_videos.add(video_link[0])
                        post_url_set.add(driver.current_url)
                        if_worked = False
                        #next_button_visible = False
                    elif video_link[1] == "":
                        failed_audio_videos.add(video_link[1])
                        post_url_set.add(driver.current_url)
                        #next_button_visible = False
                        if_worked = False

                    if if_worked:
                        video_file_hash = calculate_file_hash("temporary_visual_video.mp4")
                        video_audio_hash = calculate_file_hash("temporary_audio_video.mp4")
                        if video_file_hash != video_audio_hash:
                            combine_video_audio("temporary_visual_video.mp4", "temporary_audio_video.mp4",
                                                directory + file_name, driver)
                            files_from_current_post.append(directory + file_name)
                            current_file_number += 1
                        else:
                            post_url_set.add(driver.current_url)
                            #next_button_visible = False
                            if_worked = False

                else:
                    for i in video_link:
                        print("URL: " + video_link[i] + "Failed to print")

        ##Remember toadd LEGACYY
        if not next_button_visible:
            print("i am here")
            for i in files_from_current_post:
                try:
                    os.remove(i)
                    print(f"{i} has been deleted because post failed to download.")
                except FileNotFoundError:
                    print(f"{i} not found.")
                    quit()
                except PermissionError:
                    print(f"Permission denied to delete {i}.")
                    quit()
                except Exception as e:
                    print(f"An error occurred: {e}")

        if if_worked == True and not single_content:
            instance_of_video = 0
            while next_button_visible:
                try:
                    next_button = post_container.find_element(by=By.XPATH, value='.//*[@class=" _afxw _al46 _al47"]')
                    driver.execute_script("arguments[0].click();", next_button)

                    next_button_clicked = True

                    time.sleep(video_render_sleep_single)

                    image_found = get_image_link(driver, post_container, final_picture_set, 0)
                    if isinstance(image_found, str) and image_found not in final_picture_set:
                        final_picture_set.add(image_found)
                        failed_image_downloads = download_insta_image(profile_name, current_file_number, image_found)
                        current_file_number += 1
                        time.sleep(video_render_sleep)
                    else:
                        instance_of_video += 1
                        time.sleep(video_render_sleep)

                except NoSuchElementException:
                    break

            if instance_of_video >= 1:
                try:
                    video_link = get_video_link_scrolling(driver, list_of_video_types, list_of_audio_types)
                    print(video_link)
                    for i in range (len(video_link[0])):
                        if (download_insta_video(profile_name, -1, video_link[0][i], current_directory) == "" and
                            download_insta_video(profile_name, -2, video_link[1][i], current_directory)) == "":
                            current_date_time = datetime.now()
                            current_date = current_date_time.date()
                            file_name = profile_name + "_" + str(current_file_number) + "_" + str(current_date) + ".mp4"
                            print("video link: " + video_link[0][i], "Audio link: " + video_link[1][i])

                            if_worked = True
                            if video_link[0][i] == "" and video_link[1][i] == "":
                                failed_visual_videos.add(video_link[0][i])
                                failed_audio_videos.add(video_link[1][i])
                                post_url_set.add(driver.current_url)
                                if_worked = False
                                break
                                # next_button_visible = False
                            elif video_link[1][i] == "":
                                failed_visual_videos.add(video_link[1][i])
                                post_url_set.add(driver.current_url)
                                if_worked = False
                                # next_button_visible = False
                            elif video_link[1][i] == "":
                                failed_audio_videos.add(video_link[1][i])
                                # post_url_set.add(driver.current_url)
                                # next_button_visible = False
                                # if_worked = False

                            if if_worked:
                                video_file_hash = calculate_file_hash("temporary_visual_video.mp4")
                                video_audio_hash = calculate_file_hash("temporary_audio_video.mp4")
                                if video_file_hash != video_audio_hash:
                                    combine_video_audio("temporary_visual_video.mp4", "temporary_audio_video.mp4",
                                                        directory + file_name, driver)
                                    files_from_current_post.append(directory + file_name)
                                    current_file_number += 1
                                else:
                                    post_url_set.add(driver.current_url)
                                    # next_button_visible = False
                                    if_worked = False
                                    break

                        else:
                            for i in video_link:
                                print("Unsure of why this executes, testing")
                                quit()
                                #print("URL: " + video_link[i] + "Failed to print")
                except Exception as e:
                    print(e)

        buttons = None
        next_post = None
        try:
            buttons = driver.find_elements(by=By.XPATH, value='//*[@class="_abl-"]')
            for i in buttons:
                try:
                    next_post = i.find_element(by=By.XPATH,
                                               value='.//*[@style="display: inline-block; transform: rotate(90deg);"]')
                    driver.execute_script("arguments[0].click();", i)

                    break
                except NoSuchElementException:
                    pass
            driver.execute_script("window.performance.clearResourceTimings();")
        except Exception:
            print("Program error")
            quit()


        number_posts_downloaded += 1
        sys.stdout.write("\rDownloaded posts:  " + str(number_posts_downloaded) + "/" + str(number_of_posts) + "\n")
        sys.stdout.flush()
        posts_visited += 1

    print()
    failed_video_downloads = set()
    failed_image_downloads = set()

    with open("Failed.txt", 'w'):
        pass
    for i in post_url_set:
        print("Failed this post: " + i)
    print("Finished Trying to Download Missed Posts but the Above were Missed!!")




