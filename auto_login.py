# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "009F03CBF3934D8B34238A2B38735523DB1E863D8330551CC50E2AC19A7B33F1EB36921BB987BC6DA535B81C0C4DC9A3A76ABFE1AB7EEA798E734F7BF59945969A4A40C8A69E3E7C2FBEA6AB523B6B02F626FBD6487C715544D49B5FAB84CA4873CC5CC4EDCDAE3B46E61EF581DDD1591F655EF266AF0DDAF686C8D183B56B0B94767A9408F1D41C6DC88167EC012C88F9C61FE4D4F165C69AD1FB0A2E2F252CCB58E3962C26DBA9F7DD8CA12AA2FA3B3817AE20FCEADE2F0A5A7A3C5DA3801D735DF4F49EFBB0D6EC1C66C27EBFB0FFB41CF30EE900950095E11069D62C08459C13DE75652712176EAD234392B66210501FD0713B81A399DFF8B032101663317DEDB5F7CCC9C48142E1611FBD6005DAF351D04B407467A6CB59A94EFAB2BF9159D78B00C55FE66E9A8B2076B9C8F20CE7751F2B660A280E1E2E41D97AEB6117F95A340FB24B05010F071E2B981A83A316D6383ECF4F07D5673376147BA78D88F3"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
