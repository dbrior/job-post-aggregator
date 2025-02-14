from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def andersen(browser, url):
    """
    Navigates to the given URL and extracts job posting information across all pages.
    Returns a list of dictionaries containing details like title, job_url, description, posted_date, and location.
    """
    jobs = []
    browser.get(url)
    
    # Optionally: If the page uses an iframe, switch into it.
    # wait = WebDriverWait(browser, 20)
    # iframe = wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
    # browser.switch_to.frame(iframe)
    
    # Increase the wait timeout and use a specific selector.
    wait = WebDriverWait(browser, 20)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.container-fluid.iCIMS_JobsTable")))
    except Exception as e:
        print("Timeout waiting for the job listings container. Here is a snippet of the page source:")
        print(browser.page_source[:1000])
        raise e

    while True:
        time.sleep(1)  # Allow extra time for dynamic content.
        
        # Find all job posting blocks; they are contained in rows.
        job_elements = browser.find_elements(By.CSS_SELECTOR, "div.container-fluid.iCIMS_JobsTable > div.row")
        
        for job in job_elements:
            try:
                title_elem = job.find_element(By.CSS_SELECTOR, "div.title a h3")
            except Exception:
                continue  # Skip non-job rows.
            
            title = title_elem.text.strip()
            
            try:
                url_elem = job.find_element(By.CSS_SELECTOR, "div.title a")
                job_url = url_elem.get_attribute("href")
            except Exception:
                job_url = None
            
            try:
                description_elem = job.find_element(By.CSS_SELECTOR, "div.description")
                description = description_elem.text.strip()
            except Exception:
                description = None
            
            try:
                date_elem = job.find_element(By.CSS_SELECTOR, "div.header.right span")
                posted_date = date_elem.get_attribute("title") or date_elem.text.strip()
            except Exception:
                posted_date = None
            
            location = None
            try:
                additional_elem = job.find_element(By.CSS_SELECTOR, "div.additionalFields")
                location_elem = additional_elem.find_element(By.XPATH, ".//dt[contains(., 'Location')]/following-sibling::dd")
                location = location_elem.text.strip()
            except Exception:
                pass
            
            jobs.append({
                "title": title,
                "location": location,
                "posted_date": posted_date,
                "url": job_url,
                # "description": description,
            })

        # Try to click the "Next page" button.
        try:
            next_page = browser.find_element(By.XPATH, "//a[.//span[@title='Next page of results']]")
            next_page.click()
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.container-fluid.iCIMS_JobsTable")))
        except Exception:
            # No next button found; break the pagination loop.
            break

    # If you switched into an iframe, switch back to the default content.
    # browser.switch_to.default_content()
    
    return jobs
