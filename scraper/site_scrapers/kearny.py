from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def kearny(browser, url):
    """
    Given a Selenium browser and a starting URL for job search results,
    this function extracts all job postings (across all pages). For each
    posting it grabs the title, req id, location, categories, and the URL
    to the job detail page.
    
    Returns:
        A list of dictionaries, each representing one job posting.
    """
    job_postings = []
    browser.get(url)
    
    while True:
        # Wait until at least one job card is present.
        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "mat-expansion-panel.search-result-item"))
            )
        except Exception as e:
            print("No job postings found on this page:", e)
            break
        
        # Grab all job posting elements on the page.
        job_cards = browser.find_elements(By.CSS_SELECTOR, "mat-expansion-panel.search-result-item")
        for card in job_cards:
            # Get job title and URL.
            try:
                title_elem = card.find_element(By.CSS_SELECTOR, "p.job-title a.job-title-link")
                title = title_elem.text.strip()
                job_url = title_elem.get_attribute("href")
            except Exception:
                title = ""
                job_url = ""
            
            # Get Req ID.
            try:
                req_elem = card.find_element(By.CSS_SELECTOR, "p.req-id span")
                req_id = req_elem.text.strip()
            except Exception:
                req_id = ""
            
            # Get Location.
            try:
                loc_elem = card.find_element(By.CSS_SELECTOR, ".job-result__location .label-value")
                location = loc_elem.text.strip()
            except Exception:
                location = ""
            
            # Get Categories.
            try:
                cat_elem = card.find_element(By.CSS_SELECTOR, ".job-result__categories .label-value")
                categories = cat_elem.text.strip()
            except Exception:
                categories = ""
            
            job_postings.append({
                "title": title,
                # "req_id": req_id,
                "location": location,
                # "categories": categories,
                "url": job_url,
            })
        
        # Before clicking next, check for and hide the cookie consent overlay.
        try:
            cookie_banner = browser.find_element(By.ID, "pixel-consent-container")
            # Use JavaScript to hide the overlay.
            browser.execute_script("arguments[0].style.display = 'none';", cookie_banner)
            # Alternatively, if there is an accept/close button, you could click it:
            # consent_button = cookie_banner.find_element(By.CSS_SELECTOR, "button.accept")
            # consent_button.click()
        except Exception:
            # If the cookie banner is not present, do nothing.
            pass
        
        # Attempt to locate and click the "Next" button.
        try:
            next_button = browser.find_element(By.CSS_SELECTOR, "button.mat-paginator-navigation-next")
            # If the "disabled" attribute is present, then we're on the last page.
            if next_button.get_attribute("disabled"):
                break
            else:
                # Scroll the next button into view if needed.
                browser.execute_script("arguments[0].scrollIntoView(true);", next_button)
                next_button.click()
                # Wait until the previous job cards become stale.
                WebDriverWait(browser, 10).until(EC.staleness_of(job_cards[0]))
                # Give the new page a moment to settle.
                time.sleep(1)
        except Exception as e:
            print("No next button found or an error occurred:", e)
            break

    return job_postings
