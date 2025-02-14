import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException

from custom_selenium_utils import *

def cohn_reznick(browser, url):
    """
    Navigates to the provided URL using the browser, extracts job listings,
    and returns a list of dictionaries with job details.
    
    Parameters:
      browser: A Selenium WebDriver instance.
      url: The URL of the job listings page.
    
    Returns:
      A list of dictionaries, each containing:
        - title
        - id
        - function
        - location
        - url (link to the job post)
    """
    
    def get_job_details(job_element):
        """
        Extracts job details from a job listing element.
        Details include:
        - title
        - id
        - function
        - location
        - url (link to the job post)
        """
        try:
            title_elem = job_element.find_element(By.XPATH, './/a[@id="title"]')
            title = title_elem.text.strip()
            job_url = title_elem.get_attribute("href")
        except Exception:
            title = ""
            job_url = ""
        try:
            job_id = job_element.find_element(By.XPATH, './/p[@id="id"]').text.strip()
        except Exception:
            job_id = ""
        try:
            job_function = job_element.find_element(By.XPATH, './/p[@id="function"]').text.strip()
        except Exception:
            job_function = ""
        try:
            location = job_element.find_element(By.XPATH, './/p[@id="location"]').text.strip()
        except Exception:
            location = ""
        
        return {
            "title": job_function + ' / ' + title,
            "location": location,
            # "id": job_id,
            # "function": job_function,
            "url": job_url
        }

    def safe_click(browser, element):
        """
        Attempts to click an element. If the click is intercepted,
        it scrolls the element into view and uses JavaScript or ActionChains as a fallback.
        """
        try:
            element.click()
        except ElementClickInterceptedException:
            # Scroll the element into view
            browser.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            try:
                # Attempt JavaScript click
                browser.execute_script("arguments[0].click();", element)
            except Exception:
                # Fallback to ActionChains
                ActionChains(browser).move_to_element(element).click().perform()

    
    # Navigate to the site
    browser.get(url)
    
    wait = WebDriverWait(browser, 10)
    
    # Wait until the job list is present on the page
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.job-listing-careers__list")))
    
    # Extract total pages from the pagination text.
    # Expected text format: "1 of 11 pages"
    pagination_text = browser.find_element(By.CSS_SELECTOR, "p.job-list-pagination-result span").text
    total_pages = int(pagination_text.split("of")[1].split()[0])
    print(f"Total pages found: {total_pages}")
    
    all_jobs = []
    
    # Loop through each page (pages are zero-indexed in the onclick call)
    for page_index in range(total_pages):
        if page_index > 0:
            # Build the XPath for the pagination link
            pagination_xpath = f"//a[@onclick='initializeJobsList({page_index})']"
            try:
                # Wait for the pagination element to be present
                pagination_link = wait.until(EC.presence_of_element_located((By.XPATH, pagination_xpath)))
                # Scroll it into view and then wait for it to become clickable
                browser.execute_script("arguments[0].scrollIntoView(true);", pagination_link)
                pagination_link = wait.until(EC.element_to_be_clickable((By.XPATH, pagination_xpath)))
            except TimeoutException:
                print(f"Timeout waiting for pagination link for page index {page_index}. Skipping this page.")
                continue
            
            # Use the safe_click function to click the pagination link
            safe_click(browser, pagination_link)
            # Wait a short time for the new page content to load (adjust as needed)
            time.sleep(2)
        
        # Find all job listing elements on the current page
        job_items = browser.find_elements(By.CSS_SELECTOR, "ul.job-listing-careers__list li.job-listing-careers__item")
        for job in job_items:
            details = get_job_details(job)
            all_jobs.append(details)
    
    return all_jobs