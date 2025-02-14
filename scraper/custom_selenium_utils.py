import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

def create_chrome_stealth_browser(isHeadless=False):
    options = Options()
    
    # Connect to Selenium running in the Docker container
    selenium_url = os.getenv("SELENIUM_REMOTE_URL", "http://selenium:4444")
    
    # Core options
    if isHeadless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")

    # Set a non-headless user agent
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36")
    options.add_argument(f'user-agent={user_agent}')
    
    # Disable automation flags
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    # Preferences
    prefs = {
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_settings.popups': 0,
        'profile.password_manager_enabled': False,
        'credentials_enable_service': False,
        'intl.accept_languages': 'en-US,en',
    }
    options.add_experimental_option('prefs', prefs)

    # Initialize the remote browser
    browser = webdriver.Remote(
        command_executor=selenium_url,
        options=options
    )
    
    return browser

def random_scrolling(browser):
    for _ in range(random.randint(3, 7)):
        browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(random.uniform(1, 3))
        
def get_element_by_xpath(browser, xpath):
    try:
        element = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        return element

    except Exception as e:
        print("Error: Could not find element", e)
    

def click_button(browser, xpath):
    try:
        button = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        button.click()
        # print("Button clicked successfully!")

        time.sleep(random.uniform(2, 5))

    except Exception as e:
        print("Error: Button not found or not clickable", e)
        
def type_into_field(browser, xpath, text):
    try:
        input_field = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        
        input_field.click()
        input_field.clear()

        # Simulate human-like typing
        for char in text:
            input_field.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))

        # print("Typing successful!")
        
        time.sleep(random.uniform(2, 5))

    except Exception as e:
        print("Error: Input field not found", e)
        
def get_siblings_of_element_by_id(browser, id):
    try:
        target_div = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.ID, id))
        )

        parent_element = target_div.find_element(By.XPATH, "..")
        sibling_elements = parent_element.find_elements(By.XPATH, "./*")
        return sibling_elements
            
    except Exception as e:
        print("Error:", e)
        return None
        
def get_children_recursively(root, xpath):
    return root.find_elements(By.XPATH, xpath)

def login(browser, url, username_xpath, username, password_xpath, password, submit_xpath):
    browser.get(url)
    time.sleep(random.uniform(5, 10))
    
    type_into_field(browser, username_xpath, username)
    time.sleep(random.uniform(2, 5))

    type_into_field(browser, password_xpath, password)
    time.sleep(random.uniform(2, 5))
    
    click_button(browser, submit_xpath)