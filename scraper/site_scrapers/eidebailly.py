from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def eidebailly(browser, url):
    """
    Given a Selenium browser instance and a URL for a jobs page,
    extract all job posting information from all pages. Each job posting
    includes the title, req id, location, categories, and the job page URL.
    
    Returns a list of dictionaries.
    """
    jobs = []
    browser.get(url)
    wait = WebDriverWait(browser, 10)

    def dismiss_cookie_consent():
        """If a cookie consent container is visible, dismiss it."""
        try:
            cookie = browser.find_element(By.ID, "pixel-consent-container")
            if cookie.is_displayed():
                # If an "Accept" button exists inside the container, click it.
                try:
                    accept_btn = cookie.find_element(By.XPATH, ".//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'accept')]")
                    accept_btn.click()
                except Exception:
                    # Otherwise remove the element via JavaScript.
                    browser.execute_script("arguments[0].remove();", cookie)
                # Pause briefly to allow the UI to update.
                time.sleep(1)
        except Exception:
            pass

    # Dismiss cookie consent if it appears on the first load.
    dismiss_cookie_consent()

    while True:
        try:
            # Wait for job posting panels to load.
            wait.until(EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "mat-expansion-panel.search-result-item")
            ))
        except Exception:
            print("No job postings found on the page.")
            break

        postings = browser.find_elements(By.CSS_SELECTOR, "mat-expansion-panel.search-result-item")
        for post in postings:
            # Extract the job title.
            try:
                title_elem = post.find_element(By.CSS_SELECTOR, "a.job-title-link span")
                title = title_elem.text.strip()
            except Exception:
                title = ""
            # Extract the Req ID.
            try:
                req_elem = post.find_element(By.CSS_SELECTOR, "p.req-id span")
                req_id = req_elem.text.strip()
            except Exception:
                req_id = ""
            # Extract the location.
            try:
                loc_elem = post.find_element(By.CSS_SELECTOR, "div.job-card-result-container.job-result__location span.label-value.location")
                location = loc_elem.text.strip()
            except Exception:
                location = ""
            # Extract the categories.
            try:
                cat_elem = post.find_element(By.CSS_SELECTOR, "div.job-card-result-container.job-result__categories span.categories.label-value")
                categories = cat_elem.text.strip()
            except Exception:
                categories = ""
            # Extract the job URL.
            try:
                job_link_elem = post.find_element(By.CSS_SELECTOR, "a.job-title-link")
                job_url = job_link_elem.get_attribute("href")
            except Exception:
                job_url = ""
                
            jobs.append({
                "title": title,
                # "req_id": req_id,
                "location": location,
                # "categories": categories,
                "url": job_url
            })
        
        # Before clicking the next button, dismiss the cookie consent popup if needed.
        dismiss_cookie_consent()

        # Try to locate the "Next" page button.
        try:
            next_button = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button.mat-paginator-navigation-next"))
            )
            # Check if the next button appears to be disabled.
            classes = next_button.get_attribute("class")
            disabled = next_button.get_attribute("disabled")
            if ("mat-button-disabled" in classes) or disabled:
                # No more pages.
                break
            # Scroll the button into view.
            browser.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(0.5)
            # Force click the next button using JavaScript.
            browser.execute_script("arguments[0].click();", next_button)
            # Pause briefly to allow the next page to load.
            time.sleep(2)
        except Exception as e:
            print("No next page button found or an error occurred:", e)
            break

    return jobs
