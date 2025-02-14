from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def armanino(browser, url):
    """
    Given a Selenium browser instance and a starting URL,
    extract all job postings across all pages.
    
    Each job posting is expected to include:
      - Title (text from the <a> with data-automation-id="jobTitle")
      - Link (the href attribute from that same <a>)
      - Location (text in the <dd> inside the element with data-automation-id="locations")
      - Posted On (text in the <dd> inside the element with data-automation-id="postedOn")
      - Job ID (text in the <li> inside the <ul data-automation-id="subtitle">)
    
    Returns a list of dictionaries.
    """
    jobs = []
    browser.get(url)
    wait = WebDriverWait(browser, 10)

    while True:
        # Wait for the job results section to load.
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "section[data-automation-id='jobResults']")))
        # (Optional) short sleep for extra stability.
        time.sleep(1)

        # Find all job posting elements (each <li> with the given class)
        postings = browser.find_elements(By.CSS_SELECTOR, "li.css-1q2dra3")
        for post in postings:
            # Extract job title and its URL
            try:
                title_elem = post.find_element(By.CSS_SELECTOR, "a[data-automation-id='jobTitle']")
                title = title_elem.text.strip()
                link = title_elem.get_attribute("href")
            except Exception:
                title, link = "", ""
            # Extract location text
            try:
                location = post.find_element(By.CSS_SELECTOR, "div[data-automation-id='locations'] dd").text.strip()
            except Exception:
                location = ""
            # Extract posted on text
            try:
                posted_on = post.find_element(By.CSS_SELECTOR, "div[data-automation-id='postedOn'] dd").text.strip()
            except Exception:
                posted_on = ""
            # Extract job id (from the subtitle list)
            try:
                job_id = post.find_element(By.CSS_SELECTOR, "ul[data-automation-id='subtitle'] li").text.strip()
            except Exception:
                job_id = ""
            
            jobs.append({
                "title": title,
                "location": location,
                "posted_date": posted_on,
                "url": link,
                # "job_id": job_id
            })

        # Try to click the "next" pagination button.
        try:
            # The next button is identified by aria-label="next"
            next_button = browser.find_element(By.CSS_SELECTOR, "button[aria-label='next']")
            # If the button is enabled, click it.
            if next_button.is_enabled():
                next_button.click()
                # Wait until the previous postings become stale (i.e. page changes)
                wait.until(EC.staleness_of(postings[0]))
                time.sleep(1)  # Optional pause to let the new page settle
            else:
                break  # next button exists but is disabled → last page reached.
        except Exception:
            # Either the next button was not found or another issue arose:
            break

    return jobs
