from behave import given, when, then, step
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def get_jobs(driver):
    result_content = driver.find_elements(By.XPATH, "//td[@class='resultContent']")
    found = []
    for i in range(len(result_content)):
        job_title = result_content[i].find_element(By.XPATH, "./div/h2/a").text
        job_href = result_content[i].find_element(By.XPATH, "./div/h2/a").get_attribute('href')
        job_company = result_content[i].find_element(By.XPATH, "./div/div/span[@class='companyName']").text
        found.append([job_company, job_title, job_href])
    return found


@step('Indeed: Find "{title}" in location "{location}" within "{radius}" miles for the last "{date_posted}" days')
def open_url(context, title, location, radius, date_posted):
    assert radius in ['0', '5', '10', '15', '25', '35', '50',
                      '100', 'any'], f"The miles should be one of '0', '5', '10', '15', '25', '35', '50', '100' or 'any'."
    assert date_posted in ['1', '3', '7', '14', 'any'], f"The days should be one of '1', '3', '7', '14' or 'any'."

    context.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    wait_time = 10
    context.driver.implicitly_wait(wait_time)
    wait = WebDriverWait(context.driver, wait_time)

    title = title.replace(' ', '%20')
    location = location.replace(' ', '%20').replace(',', '%2C')

    url_base = f"https://www.indeed.com/jobs?q={title}&l={location}"
    url_ext = f"&radius={radius}&sort=date&fromage={date_posted}&start=0"

    if radius == 'any':
        url_ext = f"&sort=date&fromage={date_posted}&start=0"
    elif date_posted == 'any':
        url_ext = f"&radius={radius}&sort=date&start=0"
    elif radius == 'any' and date_posted == 'any':
        url_ext = f"&sort=date&start=0"

    url_indeed = url_base + url_ext

    found_jobs = []

    context.driver.get(url_indeed)
    for i in range(100):
        new_found_jobs = get_jobs(context.driver)
        found_jobs.extend(new_found_jobs)
        pagination = context.driver.find_elements(By.XPATH, "//a[@data-testid='pagination-page-next']")
        if len(pagination) > 0:
            pagination[0].click()
            continue
        else:
            break

    context.indeed = found_jobs
    context.indeed_days = date_posted
    context.indeed_location = location
    context.indeed_radius = radius
