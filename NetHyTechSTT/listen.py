from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import sys

driver = None
website = "https://allorizenproject1.netlify.app/"

def _get_chrome_driver_path():
    cwd = os.getcwd()
    if sys.platform == "win32":
        return os.path.join(cwd, "chromedriver.exe")
    else:
        return os.path.join(cwd, "chromedriver")

def _get_recognition_file_path():
    return os.path.join(os.getcwd(), "input.txt")

def _initialize_driver():
    global driver
    if driver is not None:
        return driver

    chrome_options = Options()
    chrome_options.add_argument("--use-fake-ui-for-media-stream")
    chrome_options.add_argument("--headless=old")

    chrome_driver_path = _get_chrome_driver_path()
    service = Service(executable_path=chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(website)
    return driver

def listen():
    print("Support in Youtube @NetHyTech")
    global driver
    try:
        driver = _initialize_driver()
        recog_file = _get_recognition_file_path()

        start_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, 'startButton')))
        start_button.click()
        print("Listening...")
        output_text = ""
        is_second_click = False
        while True:
            output_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'output')))
            current_text = output_element.text.strip()
            if "Start Listening" in start_button.text and is_second_click:
                if output_text:
                    is_second_click = False
            elif "Listening..." in start_button.text:
                is_second_click = True
            if current_text != output_text:
                output_text = current_text
                with open(recog_file, "w") as file:
                    file.write(output_text.lower())
                    print("User:", output_text)
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        if driver is not None:
            driver.quit()
            driver = None