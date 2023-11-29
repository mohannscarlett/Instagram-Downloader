#Instagram Profile Downloader
#Mohann Scarlett 11/27/2023
import time
import sys

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from video_downloader import download_insta_video
from image_downloader import download_image


def main(profile_url, username, password):
    try:
        profile_name = None
        page_loading_time = 7.5
        scroll_timeout = 0.5

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

        service = Service(executable_path='Resources/chromedriver.exe')
        driver = webdriver.Chrome(service=service, options=options)

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
        time.sleep(page_loading_time)
        driver.get(profile_url)
        time.sleep(page_loading_time)

        username_element = driver.find_element(by=By.XPATH, value='//*[@class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye x1ms8i2q xo1l8bm x5n08af x10wh9bi x1wdrske x8viiok x18hxmgj"]')
        profile_name = username_element.text

        profile_info = driver.find_elements(by=By.XPATH, value='//*[@class="html-span xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd'
                                                               ' x1hl2dhg x16tdsg8 x1vvkbs"]')
        number_of_posts = int(profile_info[0].text.replace(",",""))
        print("\nTotal number of user posts: "+ str(number_of_posts), end='\n\n')
        post_links = set()

        print("Compiling a list of all the users posts...", end='\n\n')
        while len(post_links) != number_of_posts:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(scroll_timeout)

            post_holding_field = driver.find_element(by=By.XPATH, value='//*[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1n2onr6 x1plvlek xryxfnj x1iyjqo2 x2lwn1j xeuugli xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]')
            instagram_posts = post_holding_field.find_elements(by=By.XPATH, value='.//*[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz _a6hd"]')

            for i in instagram_posts:
                post_links.add(i.get_attribute("href"))
                sys.stdout.write("\rNumber of posts compiled:  " + str(len(post_links)) + "/" + str(number_of_posts))
                sys.stdout.flush()

        print()
        print()
        print("List of posts retrieved.", end='\n\n')
        driver.delete_all_cookies()
        picture_set = set()
        video_set = set()
        for i in post_links:
            sys.stdout.write("\rNumber of video links gotten from profile: " +str(len(video_set)) +
                             " | Number of picture links gotten from profile: "+ str(len(picture_set)))
            sys.stdout.flush()
            driver.get(i)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@class="_aatk _aatn"]'))
            )

            next_button_visible = True
            while next_button_visible:
                number_of_fails = 0
                post_container = driver.find_element(by=By.XPATH, value='//*[@class="_aatk _aatn"]')
                try:
                    photo_posts = post_container.find_elements(by=By.XPATH, value='.//*[@class="x5yr21d xu96u03 x10l6tqk x13vifvy x87ps6o xh8yej3"]')
                    for i in photo_posts:
                        picture_set.add(i.get_attribute("src"))
                except NoSuchElementException:
                    print("Failed to get an image link", end='\n\n')
                    number_of_fails += 1
                try:
                     video_posts = driver.find_elements(by=By.XPATH, value='.//*[@class="x1lliihq x5yr21d xh8yej3"]')
                     for i in video_posts:
                         video_set.add(i.get_attribute("src"))
                except NoSuchElementException:
                    print("Failed to get a video link", end='\n\n')
                    number_of_fails += 1
                if(number_of_fails >= 2):
                    print("Terminal program error, ending program")
                    quit()

                try:
                    next_button = driver.find_element(by=By.XPATH, value='.//*[@class="_afxw _al46 _al47"]')
                except NoSuchElementException:
                    next_button_visible = False
                    break

                next_button.click()
                #time.sleep(2)

        print()
        failed_video_downloads = set()
        failed_image_downloads = set()

        print("Downloading videos...", end='\n\n')
        failed_video_downloads = download_insta_video(profile_name,video_set)
        print("Downloading images...", end='\n\n')
        failed_image_downloads = download_image(profile_name, picture_set, len(failed_video_downloads))

        if len(failed_video_downloads) > 0:
            print("Attempting to download videos that failed to download...", end='\n\n')
            failed_video_downloads = download_insta_video(profile_name, failed_video_downloads)
            if len(failed_video_downloads) > 0:
                print("Cannot download these videos:", end='\n\n')
                for i in failed_video_downloads:
                    print(i + " :Video")

        print("")
        if len(failed_image_downloads) > 0:
            print("Attempting to download images that failed to download...", end='\n\n')
            failed_image_downloads = download_insta_video(profile_name, failed_image_downloads)
            if len(failed_image_downloads) > 0:
                print("Cannot download these images:", end='\n\n')
                for i in failed_image_downloads:
                    print(i + " :Image")

        driver.quit()
        print("Downloads Completed!!")

    except Exception as e:
        print("\nCritial program error, likely causes:\nWifi issues\nInvalid Profile link\nPrivate profile\nWrong username or password")



if __name__ == '__main__':
    instagram_link = input("Enter an instagram profile link\nAny other link will result in undetermined program behavior"
                           "\nOnly works with public accounts"
                           "\nExample: https://www.instagram.com/mrbeast/\n").replace(" ", "")
    username = input("Your instagram account username: ").replace(" ", "")
    password = input("Your instagram account password: ")
    main(instagram_link
         ,username
         ,password)