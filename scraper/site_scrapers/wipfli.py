from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def wipfli(browser, url):
    """
    Extract all job posting details from the given URL using the provided Selenium browser.
    The function navigates through all pages of job postings.
    
    Each job posting is expected to have:
      - a job title (in a <h3 class="job_title"> tag)
      - a URL (from the <a> tag wrapping the title or the "See More" link)
      - location(s) (each contained in a <span class="badge"> under a <li> with "Location:")
      - job type (contained in a <span class="badge"> under a <li> with "Job Type:")
    
    Returns a list of dictionaries, each containing the job information.
    """
    job_list = []
    wait = WebDriverWait(browser, 10)
    
    # Load the first page
    browser.get(url)
    
    while True:
        # Wait until job postings are present on the page
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.jobs div.job")))
        time.sleep(1)  # small sleep to ensure content is fully rendered
        
        # Find all job posting elements on the page
        jobs = browser.find_elements(By.CSS_SELECTOR, "div.jobs div.job")
        
        for job in jobs:
            # Initialize a dictionary to store job details
            job_data = {}
            
            # Extract job title (from the <h3 class="job_title"> tag)
            try:
                title_elem = job.find_element(By.CSS_SELECTOR, "h3.job_title")
                job_data["title"] = title_elem.text.strip()
            except Exception:
                job_data["title"] = None
            
            # Extract the job URL (from the <a> element that wraps the title)
            try:
                link_elem = job.find_element(By.CSS_SELECTOR, "a")
                job_data["url"] = link_elem.get_attribute("href")
            except Exception:
                job_data["url"] = None
            
            # Extract the locations: look for the <li> that contains "Location:"
            try:
                location_li = job.find_element(By.XPATH, ".//li[contains(., 'Location:')]")
                location_badges = location_li.find_elements(By.CSS_SELECTOR, "span.badge")
                # Create a list of location names
                job_data["location"] = [badge.text.strip() for badge in location_badges].join(", ")
            except Exception:
                job_data["location"] = None
            
            # # Extract the job type: look for the <li> that contains "Job Type:"
            # try:
            #     jobtype_li = job.find_element(By.XPATH, ".//li[contains(., 'Job Type:')]")
            #     jobtype_badge = jobtype_li.find_element(By.CSS_SELECTOR, "span.badge")
            #     job_data["job_type"] = jobtype_badge.text.strip()
            # except Exception:
            #     job_data["job_type"] = None
            
            job_list.append(job_data)
        
        # Attempt to go to the next page.
        # Here we look for an <a> element with aria-label "Go to next page".
        try:
            next_button = browser.find_element(By.XPATH, "//a[@aria-label='Go to next page']")
            # If the parent <li> has a "disabled" class, then no further pages exist.
            parent_li = next_button.find_element(By.XPATH, "./..")
            if "disabled" in parent_li.get_attribute("class"):
                break  # exit the loop if next page is disabled
            else:
                next_button.click()
                # Wait a short time for the new page to load; adjust if necessary.
                time.sleep(2)
        except Exception:
            # If the next button is not found, exit the loop.
            break
    
    return job_list
