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

from failed_posts_downloader import download_failed_posts
from download_saved_posts import download_saved_posts

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
        return ["",""]


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
            #look_for_audio = True
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
        #print(e)
        return ["", ""]
        #quit()

    if len(visual_video_links_highquality) == len(audio_video_links_highquality):

        return [visual_video_links_highquality, audio_video_links_highquality]

        #print(len(visual_video_links_highquality))
        #print(len(audio_video_links_highquality))

        #return [visual_video_links_lowquality, audio_video_links_lowquality]


    #print(len(visual_video_links_highquality))
    #print(len(audio_video_links_highquality))


    return ["", ""]


def download_profile(driver,profile_url, username, password, list_of_video_types, list_of_audio_types,
                     number_posts_to_download):

    error_logs = []
    profile_name = None
    page_loading_time = 7.5
    scroll_timeout = 0.5
    video_render_sleep = 1.25
    video_render_sleep_single = 2


    driver.get(profile_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft"]'))
    )

    username_element = driver.find_element(by=By.XPATH,
                                           value='//*[@class="x1lliihq x193iq5w x6ikm8r x10wlt62 xlyipyv xuxw1ft"]')
    profile_name = username_element.text

    profile_info = driver.find_elements(by=By.XPATH,
                                        value='//*[@class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu '
                                              'x4uap5 x18d9i69 xkhd6sd'
                                              ' x1hl2dhg x16tdsg8 x1vvkbs"]')
    number_of_posts = int(profile_info[0].text.replace(",", ""))
    print("\nTotal number of user posts: " + str(number_of_posts), end='\n\n')

    final_picture_set = set()
    final_video_set = set()

    posts_visited = 0
    current_file_number = 0
    number_posts_downloaded = 0
    WebDriverWait(driver, 10).until( #MAIN content holder pane, with each post element inside
        EC.presence_of_element_located((By.XPATH, '//*[@style="display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;"]'))
    )
    post_holding_field = driver.find_element(by=By.XPATH,
                                             value='//*[@style="display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;"]')

    instagram_posts = post_holding_field.find_elements(by=By.XPATH,
                                                       value='.//*[@class="x1i10hfl xjbqb8w x1ejq31n xd10rxx'
                                                             ' x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n'
                                                             ' x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm'
                                                             ' xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd'
                                                             ' x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]')
    driver.execute_script("window.performance.clearResourceTimings();")
    driver.execute_script("arguments[0].click();", instagram_posts[0])

    current_user = getpass.getuser()
    directory = "C:\\users\\" + str(current_user) + "\\desktop\\" + profile_name + "\\"
    current_directory = os.getcwd()

    if not os.path.exists(directory):
        os.makedirs(directory)
    failed_visual_videos = set()
    failed_audio_videos = set()
    post_url_set = set()
    main_loop = 1
    loop_count = 0

    while main_loop:
        files_from_current_post = []
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # time.sleep(scroll_timeout)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                        '//*[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh xl56j7k"]')))

        post_container = None
        try:
            post_container = driver.find_element(by=By.XPATH,
                                                 value='//*[@class="_aatk _aatl"]')
        except NoSuchElementException:
            post_container = driver.find_element(by=By.XPATH,
                                                 value='//*[@class="_aatk _aatl _aatm"]')

        next_button_visible = True
        next_button_clicked = False
        next_button = None

        time.sleep(video_render_sleep_single)
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

                    time.sleep(video_render_sleep)

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
                    #print(video_link)
                    worked = True
                    if video_link == ["", ""]:
                        # failed_visual_videos.add(video_link[0][i])
                        # failed_audio_videos.add(video_link[1][i])
                        post_url_set.add(driver.current_url)
                        worked = False
                    else:
                        for i in range(len(video_link[0])):

                            if (download_insta_video(profile_name, -1, video_link[0][i], current_directory) == "" and
                                download_insta_video(profile_name, -2, video_link[1][i], current_directory)) == "":
                                current_date_time = datetime.now()
                                current_date = current_date_time.date()
                                file_name = profile_name + "_" + str(current_file_number) + "_" + str(
                                    current_date) + ".mp4"
                                #print("video link: " + video_link[0][i], "Audio link: " + video_link[1][i])

                                # next_button_visible = False
                                """elif video_link[1][i] == "":
                                    failed_visual_videos.add(video_link[1][i])
                                    post_url_set.add(driver.current_url)
                                    if_worked = False
                                    # next_button_visible = False
                                elif video_link[1][i] == "":
                                    failed_audio_videos.add(video_link[1][i])
                                    # post_url_set.add(driver.current_url)
                                    # next_button_visible = False
                                    # if_worked = False"""

                                if worked:
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
                                        worked = False
                                        break

                            else:
                                for j in video_link:
                                    print("Unexpected program error, exiting.")
                                    driver.quit()
                                    quit()
                                    # print("URL: " + video_link[i] + "Failed to print")
                except Exception as e:
                    print(e)

        buttons = None
        next_post = None
        try:
            buttons = driver.find_elements(by=By.XPATH, value='//*[@class="_abl-"]')
            button_exists = False
            for i in buttons:
                try:
                    next_post = i.find_element(by=By.XPATH,
                                               value='.//*[@style="display: inline-block; transform: rotate(90deg);"]')
                    driver.execute_script("window.performance.clearResourceTimings();")
                    time.sleep(video_render_sleep_single)
                    driver.execute_script("arguments[0].click();", i)
                    button_exists = True
                    loop_count += 1
                    break
                except NoSuchElementException:
                    pass
            if number_posts_to_download == 'all':
                if not button_exists:
                    main_loop = 0
            else:
                if loop_count == number_posts_to_download:
                    main_loop = 0
        except Exception as e:
            print("Critical Program error while going to next post")
            driver.quit()
            quit()

        number_posts_downloaded += 1
        sys.stdout.write("\rDownloaded posts:  " + str(number_posts_downloaded) + "/" + str(number_of_posts) + "\n")
        sys.stdout.flush()
        print()
        posts_visited += 1

    failed_video_downloads = set()
    failed_image_downloads = set()

    if len(post_url_set) >= 1:

        filename = 'Failed.txt'
        with open(filename, 'w') as file:
            for line in post_url_set:
                file.write(line+'\n')
        driver.execute_script("window.performance.clearResourceTimings();")
        print("Downloading Posts That did not Download Earlier")
        download_failed_posts(driver,list_of_video_types, list_of_audio_types,directory)
    else:
        for i in post_url_set:
            print("Failed this post: " + i)


    print("Downloads Completed!!")

