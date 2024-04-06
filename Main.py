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

from download_instagram_profile import download_profile
from download_saved_posts import download_saved_posts


if __name__ == '__main__':
    video_identifying_string_1 = "9a5d50&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNhcm91c2VsX2l0ZW0uYzItQzMuZGFzaF92cDll"
    video_identifying_string_2 = "9a5d50&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfdn"
    video_identifying_string_3 = "_video_dashinit.mp4"
    video_identifying_string_4 = "9a5d50&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfaGlna"
    video_identifying_string_5 = "9a5d50&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfcjJldmV2c"
    video_identifying_string_6 = (
        "eyJxZV9ncm91cHMiOlsiaWdfZXZlcnN0b3JlX3RvX29pbDppZ19kYXNoX2RlbGl2ZXJ5X292ZXJfb2lsX"
        "3VybF92Mjp0ZXN0Il0sInZlbmNvZGVfdGFnIjoiaWcteHB2ZHMuY2Fyb3VzZWxfaXRlbS5jMi1DMy5kYXNoX"
        "3ZwOWV")
    video_identifying_string_7 = (
        "eyJxZV9ncm91cHMiOlsiaWdfZXZlcnN0b3JlX3RvX29pbDppZ19kYXNoX2RlbGl2ZXJ5X292ZXJfb2lsX"
        "3VybF92Mjp0ZXN0Il0sInZlbmNvZGVfdGFnIjoiaWcteHB2ZHMuY2xpcHMuYzItQzMuZGFzaF9yMmV2")
    video_identifying_string_8 = ("efg=eyJxZV9ncm91cHMiOlsiaWdfZXZlcnN0b3JlX3RvX29pbDppZ19kYXNoX2RlbGl2ZXJ5X292ZXJfb2ls"
                                  "X3VybF92Mjp0ZXN0Il0sInZlbmNvZGVfdGFnIjoiaWcteHB2ZHMuY2xpcHMuYzItQzMuZGFzaF92cDll")

    video_identifying_string_9 = ("eyJxZV9ncm91cHMiOlsiaWdfZXZlcnN0b3JlX3RvX29pbDppZ19kYXNoX2RlbGl2ZXJ5X292ZXJfb2ls"
                                  "X3VybF92Mjp0ZXN0Il0sInZlbmNvZGVfdGFnIjoiaWcteHB2ZHMuY2Fyb3VzZWxfaXRlbS5jMi1DMy5kYXN"
                                  "oX2Jhc2VsaW5lXzF")
    video_identifying_string_10 = "eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfcjJldmV2c"
    video_identifying_string_11 = "9a5d50&efg=eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMxLUMzLmRhc2hfaGlna"
    video_identifying_string_12 = "eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNhcm91c2VsX2l0ZW0uYzItQzMuZGFzaF9oaW"
    video_identifying_string_13 = "eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfYmFzZWxpbmVfMV92MS"
    video_identifying_string_14 = "eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNhcm91c2VsX2l0ZW0uYzItQzMuZGFzaF9iYXNlbGluZV8"
    video_identifying_string_15 = "eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfYmFzZWxpbmVfMTA"

    audio_identifying_string_1 = "eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNhcm91c2VsX2l0ZW0uYzItQzMuZGFzaF9iYXNlbGluZV9"
    audio_identifying_string_2 = "eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfbG5"
    audio_identifying_string_3 = "eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMyLUMzLmRhc2hfYmFzZWxpbmVfYXVkaW9fdjEi"
    audio_identifying_string_4 = (
        "eyJxZV9ncm91cHMiOlsiaWdfZXZlcnN0b3JlX3RvX29pbDppZ19kYXNoX2RlbGl2ZXJ5X292ZXJfb2lsX3Vyb"
        "F92Mjp0ZXN0Il0sInZlbmNvZGVfdGFnIjoiaWcteHB2ZHMuY2Fyb3VzZWxfaXRlbS5jMi1DMy5kYXNoX2Jhc2V")
    audio_identifying_string_5 = ("efg=eyJxZV9ncm91cHMiOlsiaWdfZXZlcnN0b3JlX3RvX29pbDppZ19kYXNoX2RlbGl2ZXJ5X292ZXJfb2l"
                                  "sX3VybF92Mjp0ZXN0Il0sInZlbmNvZGVfdGFnIjoiaWcteHB2ZHMuY2Fyb3VzZWxfaXRlbS5jMi1DMy5kYXN"
                                  "oX2Jhc2VsaW5lX2F")
    audio_identifying_string_6 = "eyJ2ZW5jb2RlX3RhZyI6ImlnLXhwdmRzLmNsaXBzLmMxLUMzLmRhc2hfbG5"

    list_of_video_types = []
    list_of_video_types.append(video_identifying_string_1)
    list_of_video_types.append(video_identifying_string_2)
    list_of_video_types.append(video_identifying_string_3)
    list_of_video_types.append(video_identifying_string_4)
    list_of_video_types.append(video_identifying_string_5)
    list_of_video_types.append(video_identifying_string_6)
    list_of_video_types.append(video_identifying_string_7)
    list_of_video_types.append(video_identifying_string_8)
    list_of_video_types.append(video_identifying_string_9)
    list_of_video_types.append(video_identifying_string_10)
    list_of_video_types.append(video_identifying_string_11)
    list_of_video_types.append(video_identifying_string_12)
    list_of_video_types.append(video_identifying_string_13)
    list_of_video_types.append(video_identifying_string_14)
    list_of_video_types.append(video_identifying_string_15)


    list_of_audio_types = []
    list_of_audio_types.append(audio_identifying_string_1)
    list_of_audio_types.append(audio_identifying_string_2)
    list_of_audio_types.append(audio_identifying_string_3)
    list_of_audio_types.append(audio_identifying_string_4)
    list_of_audio_types.append(audio_identifying_string_5)
    list_of_audio_types.append(audio_identifying_string_6)

    print("Login is required to download posts from private profiles, and to download saved posts.")
    username = input("Your instagram account Email or Username: ").replace(" ", "").replace(" ", "")
    password = input("Your instagram account password: ")

    options = webdriver.FirefoxOptions()
    # Uncomment the following line if you want to run in headless mode
    options.add_argument("--headless")
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("dom.infobar.enabled", False)
    options.set_preference("browser.log.level", "error")
    options.set_preference("devtools.jsonview.enabled", False)

    service = Service(executable_path='geckodriver.exe')
    driver = webdriver.Firefox(service=service, options=options)
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
    time.sleep(2)
    driver.get("https://www.instagram.com")


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@class="_aa4b _add6 _ac4d _ap35"]'))
    )


    input_fields = driver.find_elements(by=By.XPATH, value='//*[@class="_aa4b _add6 _ac4d _ap35"]')
    input_fields[0].send_keys(username)
    input_fields[1].send_keys(password)
    login_button = driver.find_element(by=By.XPATH, value='//*[@class=" _acan _acap _acas _aj1- _ap30"]')

    try:
        login_button.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//*[@class="x9f619 xvbhtw8 x78zum5 x5ur3kl xopu45v x1bs97v6 xmo9t06 x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x178xt8z xm81vs4 xso031l xy80clv x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]'))
        )
    except Exception as e:
        print("Error Authenticating User, Please Ensure Credentials are Correct.")
        driver.quit()
        quit()

    print("Login successful!")
    while True:

        program_option = int(input("Choose an option:\nEnter '1' to Download All Instagram Posts From a Profile\n"
                               "Enter '2' to Download Saved Posts From Your Instagram Account\n"
                                   "Enter '3' to Exit Program\n"))
        if program_option == 1:
            print("")
            instagram_link = input(
                "Enter an instagram profile link\nAny other link will result in undetermined program behavior"
                "\nExample profile link: https://www.instagram.com/mrbeast/"
                "\nTo download from private accounts, the account you authenticate with must follow that user"
                "\nEnter link: ").replace(" ", "")

            download_profile(driver,instagram_link
                             , username
                             , password
                             , list_of_video_types
                             , list_of_audio_types)
        elif program_option == 2:
            print("")
            while True:
                saved_option = input("Enter 'all' to Download Every Saved Post\nEnter a Number to Download a Specific Amount Starting From the Top\n").lower()
                if saved_option == "all":
                    break
                else:
                    try:
                        saved_option = int(saved_option)
                        break
                    except Exception as e:
                        print("Please Enter a Valid Number")


            instagram_link = "https://www.instagram.com/" + username + "/saved/all-posts/"
            download_saved_posts(driver,instagram_link
                             , username
                             , password
                             , list_of_video_types
                             , list_of_audio_types,saved_option)

        elif program_option == 3:
            quit()