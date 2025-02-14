from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
import time

def eisner(browser, url):
    """
    Scrape all job postings from the given URL using the provided Selenium browser instance.
    Each job posting dictionary contains:
      - job_title: The text of the job title.
      - job_url: The full URL to the job posting.
      - meta: A list of meta information (e.g. department, location).
      - job_id: (Optional) The job identifier from the data attribute.
      
    This function paginates through all pages until no "next" button is found.
    """
    jobs = []
    browser.get(url)

    while True:
        try:
            # Wait until at least one job card is present on the page.
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.card.card-job"))
            )
        except TimeoutException:
            print("No job cards found on the page.")
            break

        # Find all job cards on the current page
        job_cards = browser.find_elements(By.CSS_SELECTOR, "div.card.card-job")
        for card in job_cards:
            try:
                # The job title and URL come from the <a> element within the <h2>
                title_elem = card.find_element(By.CSS_SELECTOR, "h2.card-title a")
                job_title = title_elem.text.strip()
                job_url = title_elem.get_attribute("href")
            except Exception:
                job_title = ""
                job_url = ""
            
            # Collect meta information (like department, location, etc.)
            meta_items = card.find_elements(By.CSS_SELECTOR, "ul.job-meta li")
            meta = [item.text.strip() for item in meta_items]

            # Optionally, get the job id from the data attribute in the actions div.
            try:
                actions = card.find_element(By.CSS_SELECTOR, "div.card-job-actions.js-job")
                job_id = actions.get_attribute("data-id")
            except Exception:
                job_id = None

            jobs.append({
                "title": job_title,
                "url": job_url
                # "meta": meta,
                # "job_id": job_id,
            })

        # Attempt to find and click the "Next" page button.
        try:
            next_button = WebDriverWait(browser, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "li.next.page-item a"))
            )
            # Scroll the next button into view
            browser.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)  # slight pause to ensure any animations/overlays settle

            try:
                next_button.click()
            except ElementClickInterceptedException:
                # Fallback: use JavaScript click if normal click is intercepted.
                browser.execute_script("arguments[0].click();", next_button)
            
            # Wait until the previous page's job cards are stale (i.e. the new page is loading)
            WebDriverWait(browser, 10).until(EC.staleness_of(job_cards[0]))
            time.sleep(1)  # Optional: small pause for stability
        except (NoSuchElementException, TimeoutException, IndexError):
            # No next button found or page did not update, so exit the loop.
            break

    return jobs
