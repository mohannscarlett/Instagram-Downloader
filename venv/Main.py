#Instagram Profile Downloader
#Mohann Scarlett 11/27/2023
import time
import sys
import getpass
from datetime import datetime
import os
import logging

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from video_downloader import download_insta_video
from image_downloader import download_insta_image

from moviepy.editor import VideoFileClip, AudioFileClip

def combine_video_audio(video_path, audio_path, output_filename):
    # Load video and audio clips
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    # Set video clip's audio
    video_clip = video_clip.set_audio(audio_clip)

    # Save the combined video
    video_clip.write_videofile(output_filename, codec='libx264', audio_codec='aac')

    # Close clips
    video_clip.close()
    audio_clip.close()


def get_image_link(driver, post_container, picture_set):
    try:
        post_images = post_container.find_elements(by=By.XPATH,
                                                   value='.//*[@class="x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o '
                                                         'xh8yej3"]')
        for i in post_images:
            image_URL = i.get_attribute("src")
            if image_URL not in picture_set:
                return image_URL
    except NoSuchElementException as e:
        return False


def get_video_link(driver):
    substring_to_find = ".mp4"
    video_identifying_string_1 = "9a5d50&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNhcm91c2VsX2l0ZW0uYzItQzMuZGFzaF92cDll"
    video_identifying_string_2 = "9a5d50&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfdn"
    video_identifying_string_3 = "_video_dashinit.mp4"
    audio_identifying_string_1 = "9a5d50&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNhcm91c2VsX2l0ZW0uYzItQzMuZGFzaF9iY"
    audio_identifying_string_2 = "9a5d50&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfbG5"
    link_found = False
    video_links = set()
    while not link_found:
        network_data = driver.execute_script("return window.performance.getEntries();")
        for entry in network_data:
            if substring_to_find in entry['name']:
                video_link = entry.get('name')

                # Find the index of '&bytestart'
                index = video_link.find('&bytestart')
                if index != -1:  # Check if '&bytestart' is found in the URL
                    video_link = video_link[:index]  # Extract the portion before '&bytestart'
                else:
                    print("&bytestart not in URL")
                video_links.add(video_link)
                link_found = True
    visual_video_link = ""
    audio_video_link = ""
    for i in video_links:
        if video_identifying_string_3 in i:
            visual_video_link = i
            for j in video_links:
                if "_n.mp4" in j:
                    audio_video_link = j

    for i in video_links:
        if video_identifying_string_1 in i or video_identifying_string_2 in i:
            visual_video_link = i
            break

    for i in video_links:
        if audio_identifying_string_1 in i or audio_identifying_string_2 in i:
            audio_video_link = i
            break

    return [visual_video_link, audio_video_link]


def download_profile(profile_url, username, password):

    error_logs = []
    try:
        profile_name = None
        page_loading_time = 7.5
        scroll_timeout = 0.5
        video_render_sleep = 0.5

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Additional options
        prefs = {
            "profile.default_content_setting_values.notifications": 2  # Disable notifications
        }
        options.add_experimental_option("prefs", prefs)

        service = Service(executable_path='chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("window.performance.clearResourceTimings();")
        # Suppress console logs using JavaScript
        script = '''
        var console = {
            log: function() {},
            warn: function() {},
            error: function() {}
        };
        '''
        driver.execute_script(script)

        print("\nAuthenticating user... ", end='\n\n')
        driver.get("https://www.instagram.com")

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="_aa4b _add6 _ac4d _ap35"]'))
        )

        input_fields = driver.find_elements(by=By.XPATH, value='//*[@class="_aa4b _add6 _ac4d _ap35"]')
        input_fields[0].send_keys(username)
        input_fields[1].send_keys(password)
        login_button = driver.find_element(by=By.XPATH, value='//*[@class=" _acan _acap _acas _aj1- _ap30"]')
        login_button.click()
        print("\nLoading target profile data... ", end='\n\n')
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="x9f619 xvbhtw8 x78zum5 x5ur3kl xopu45v x1bs97v6 xmo9t06 x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x178xt8z xm81vs4 xso031l xy80clv x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]'))
        )
        driver.get(profile_url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli '
                                                      'x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i '
                                                      'x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x10wh9bi '
                                                      'x1wdrske x8viiok x18hxmgj"]'))
        )

        username_element = driver.find_element(by=By.XPATH,
                                               value='//*[@class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli '
                                                     'x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i '
                                                     'x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x10wh9bi '
                                                     'x1wdrske x8viiok x18hxmgj"]')
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

        post_holding_field = driver.find_element(by=By.XPATH,
                                                 value='//*[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr '
                                                       'xo71vjh x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli '
                                                       'xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]')
        instagram_posts = post_holding_field.find_elements(by=By.XPATH,
                                                           value='.//*[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd '
                                                                 'xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx '
                                                                 'xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 '
                                                                 'x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz '
                                                                 '_a6hd"]')
        instagram_posts[0].click()

        current_user = getpass.getuser()
        directory = "C:\\users\\" + str(current_user) + "\\desktop\\" + profile_name + "\\"
        current_directory = os.getcwd()

        if not os.path.exists(directory):
            os.makedirs(directory)

        while posts_visited != number_of_posts:
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

            image_found = get_image_link(driver, post_container, final_picture_set)
            if isinstance(image_found, str) and image_found not in final_picture_set:
                final_picture_set.add(image_found)
                failed_image_downloads = download_insta_image(profile_name, current_file_number, image_found)
                current_file_number += 1
            else:
                video_link = get_video_link(driver)
                if (download_insta_video(profile_name, -1, video_link[0], current_directory)  == "" and
                            download_insta_video(profile_name, -2, video_link[1], current_directory)) == "":
                    current_date_time = datetime.now()
                    current_date = current_date_time.date()
                    file_name = profile_name + "_" + str(current_file_number) + "_" + str(current_date) + ".mp4"
                    combine_video_audio("temporary_visual_video.mp4","temporary_audio_video.mp4",directory+file_name)
                    current_file_number += 1

                else:
                    for i in video_link:
                        print("URL: " + video_link[i] + "Failed to print")

            next_button_visible = True
            next_button_clicked = False
            next_button = None
            while next_button_visible:
                try:
                    next_button = post_container.find_element(by=By.XPATH, value='.//*[@class=" _afxw _al46 _al47"]')
                    driver.execute_script("window.performance.clearResourceTimings();")
                    next_button.click()
                    time.sleep(video_render_sleep)
                    next_button_clicked = True

                    image_found = get_image_link(driver, post_container, final_picture_set)
                    if isinstance(image_found, str) and image_found not in final_picture_set:
                        final_picture_set.add(image_found)
                        failed_image_downloads = download_insta_image(profile_name, current_file_number, image_found)
                        current_file_number += 1
                    else:
                        video_link = get_video_link(driver)
                        if (download_insta_video(profile_name, -1, video_link[0], current_directory) == "" and
                            download_insta_video(profile_name, -2, video_link[1], current_directory)) == "":
                            current_date_time = datetime.now()
                            current_date = current_date_time.date()
                            file_name = profile_name + "_" + str(current_file_number) + "_" + str(current_date) + ".mp4"
                            combine_video_audio("temporary_visual_video.mp4", "temporary_audio_video.mp4",
                                                directory + file_name)
                            current_file_number += 1

                        else:
                            for i in video_link:
                                print("URL: " + video_link[i] + "Failed to print")

                except NoSuchElementException:
                    break

            buttons = None
            next_post = None
            try:
                buttons = driver.find_elements(by=By.XPATH, value='//*[@class="_abl-"]')
                for i in buttons:
                    try:
                        next_post = i.find_element(by=By.XPATH,
                                                   value='.//*[@style="display: inline-block; transform: rotate(90deg);"]')
                        driver.execute_script("window.performance.clearResourceTimings();")
                        i.click()
                        break
                    except NoSuchElementException:
                        pass
            except NoSuchElementException:
                print("Program error")
                quit()


            number_posts_downloaded += 1
            sys.stdout.write("\rDownloaded posts:  " + str(number_posts_downloaded) + "/" + str(number_of_posts) + "\n")
            sys.stdout.flush()
            posts_visited += 1

        print()
        failed_video_downloads = set()
        failed_image_downloads = set()
        """
        if len(failed_video_downloads) > 0:
            print("Attempting to download videos that failed to download...", end='\n\n')
            # failed_video_downloads = download_insta_video(profile_name, failed_video_downloads)
            if len(failed_video_downloads) > 0:
                print("Cannot download these videos:", end='\n\n')
                for i in failed_video_downloads:
                    print(i + " :Video")

        if len(failed_image_downloads) > 0:
            print("Attempting to download images that failed to download...", end='\n\n')
            # failed_image_downloads = download_insta_video(profile_name, failed_image_downloads)
            if len(failed_image_downloads) > 0:
                print("Cannot download these images:", end='\n\n')
                for i in failed_image_downloads:
                    print(i + " :Image")
        """
        driver.quit()
        print("Downloads Completed!!")

    except ModuleNotFoundError as e:
        print(e)
        print(
            "\nCritial program error, likely causes:\nWifi issues\nInvalid Profile link\nPrivate profile\nWrong username or password")


if __name__ == '__main__':
    instagram_link = input(
        "Enter an instagram profile link\nAny other link will result in undetermined program behavior"
        "\nExample profile link: https://www.instagram.com/mrbeast/"
        "\nTo download from private accounts, the account you authenticate with must follow that user"
        "\nEnter link: ").replace(" ", "")
    username = input("Your instagram account username: ").replace(" ", "").replace(" ", "")
    password = input("Your instagram account password: ")
    download_profile(instagram_link
                     , username
                     , password)
