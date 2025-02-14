import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from custom_selenium_utils import *

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

def hutchinson_and_bloodgood(browser, url):
    browser.get(url)
    
    time.sleep(random.uniform(3, 5))
    
    view_all_button_xpath = '//*[@id="recruitment_careerCenter_showAllJobs"]'
    click_button(browser, view_all_button_xpath)
    
    openings_list_xpath = '//*[@id="recruitment_content"]/div/div[1]/div/div[3]/div'
    openings_list = browser.find_elements(By.XPATH, openings_list_xpath)[0].find_elements(By.XPATH, "./*")
    
    num_openings = len(openings_list)
    
    # print(f"Found {num_openings} listings")
    
    jobs = []
    
    for i in range(num_openings):
        opening = browser.find_elements(By.XPATH, openings_list_xpath)[0].find_elements(By.XPATH, "./*")[i].find_elements(By.XPATH, "./*")[0]
        children = opening.find_elements(By.XPATH, "./*")
        
        title = children[0].text
        location = children[1].text
        date = children[2].text
        
        children[0].click()
        
        time.sleep(2)
        job_url = browser.current_url
        click_button(browser, '//*[@id="recruitment_jobDescription_back"]')

        jobs.append({
            "title": title,
            "location": location,
            "posted_date": date,
            "url": job_url
        })
        # print(title, ' | ', location, ' | ', date)
        # print(job_url)
        # print()
    
    return jobs