from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def citrin_cooperman(driver, url):
    driver.get(url)
    try:
        # Wait up to 20 seconds for the job listings container to appear.
        wait = WebDriverWait(driver, 20)
        results_container = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul#results"))
        )
        
        # Now locate all job listing elements on the current page.
        job_listings = results_container.find_elements(By.CSS_SELECTOR, "li.jobInfo.JobListing")
        
        print(f"Found {len(job_listings)} job listings on the current page.")
        
        # Loop over each job listing and extract the relevant details.
        for job in job_listings:
            try:
                title = job.find_element(By.CSS_SELECTOR, "span.jobInfoLine.jobTitle").text
            except Exception:
                title = ""
            try:
                location = job.find_element(By.CSS_SELECTOR, "span.jobInfoLine.jobLocation").text
            except Exception:
                location = ""
            try:
                description = job.find_element(By.CSS_SELECTOR, "span.jobInfoLine.jobDescription").text
            except Exception:
                description = ""
            
            print("Job Title:", title)
            print("Location:", location)
            print("Description:", description)
            print("-" * 40)
    except Exception as e:
        print("An error occurred:", e)

