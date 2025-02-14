from selenium.webdriver.common.by import By

def gursey(browser, url):
    """
    Navigates to the given URL using the provided Selenium WebDriver instance,
    extracts job posting details from the page, and returns them as a list of
    dictionaries. Each dictionary contains the job title, location, and a link
    to the job page.
    
    Parameters:
        browser: Selenium WebDriver instance.
        url (str): The URL of the job listings page.
    
    Returns:
        list of dict: Each dict has keys 'title', 'location', and 'link'.
    """
    # Navigate to the URL.
    browser.get(url)
    
    # Find all job posting containers using the new By syntax.
    job_elements = browser.find_elements(By.CSS_SELECTOR, "div.grid-item.post-item")
    
    jobs = []
    for element in job_elements:
        # Extract the job title and the corresponding link from the <h3> anchor.
        title_anchor = element.find_element(By.CSS_SELECTOR, "h3 a")
        title = title_anchor.text.strip()
        job_link = title_anchor.get_attribute("href")
        
        # Extract the job location from the <h4> element.
        location = element.find_element(By.CSS_SELECTOR, "h4").text.strip()
        
        jobs.append({
            "title": title,
            "location": location,
            "url": job_link
        })
    
    return jobs