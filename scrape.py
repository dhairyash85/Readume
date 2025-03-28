from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import pandas as pd

# Set up Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in background
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")

# Path to your ChromeDriver (Download the latest version from https://chromedriver.chromium.org/)
service = Service("chromedriver.exe")  # Change this to the correct path
driver = webdriver.Chrome(service=service, options=chrome_options)

# LinkedIn Jobs URL (Modify based on your filters)
job_search_url = "https://www.linkedin.com/jobs/search/?keywords=Machine%20Learning&location=Worldwide"
driver.get(job_search_url)

time.sleep(5)  # Let the page load

# Scroll down to load more jobs
for _ in range(3):  # Increase for more jobs
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
    time.sleep(3)

# Extract page source
soup = BeautifulSoup(driver.page_source, "html.parser")

# Extract job listings
jobs = soup.find_all("li", class_="job-result-card")

job_data = []
for job in jobs:
    try:
        title = job.find("h3", class_="base-search-card__title").text.strip()
        company = job.find("h4", class_="base-search-card__subtitle").text.strip()
        location = job.find("span", class_="job-result-card__location").text.strip()
        job_link = job.find("a", class_="base-card__full-link")["href"]
        
        # Open job details page
        driver.get(job_link)
        time.sleep(3)
        job_soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extract job description & required skills
        job_desc = job_soup.find("div", class_="description__text").text.strip()
        
        job_data.append({"Title": title, "Company": company, "Location": location, "Link": job_link, "Description": job_desc})
    
    except Exception as e:
        print(f"Error fetching job: {e}")

# Convert to DataFrame
df = pd.DataFrame(job_data)

# Save dataset
df.to_csv("linkedin_jobs.csv", index=False)

print("Job dataset saved!")
driver.quit()
