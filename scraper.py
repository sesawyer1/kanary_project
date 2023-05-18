# working with a dynamic website – focusing on headless mode

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from bs4 import BeautifulSoup

# Setup
chromedriver_path = "C:/Users/sarahsawyer/Downloads/chromedriver.exe"
url = 'https://golookup.com/'


first_name = input('Enter target first name: ')
last_name = input('Enter target last name: ')

chrome_options = Options()
chrome_options.add_argument("--headless") 

service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 17)
driver.get(url)

# Name input

first_name_element = driver.find_element(By.CSS_SELECTOR, 'input[name="firstName"]')
last_name_element = driver.find_element(By.CSS_SELECTOR, 'input[name="lastName"]')
first_name_element.send_keys(first_name)
last_name_element.send_keys(last_name)

# State selector
loc_element = driver.find_element(By.CSS_SELECTOR, 'select[name="state"]')
location_select = Select(loc_element)
location_options = [option.text for option in location_select.options]

selected_state = input('Enter state code: ')
state = selected_state.upper()

# error
if state not in location_options:
    print('Not a valid state')
    driver.quit()
    exit()

location_select.select_by_value(state)

# Submit button
search_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
search_button.click()

# wait for results page to load
wait = WebDriverWait(driver, 60)

try:
    results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#results')))
except TimeoutException:
    print("There are no search results")
    driver.quit()
    exit()

# print results
for res in results: 
    sub_results = res.find_elements(By.CSS_SELECTOR, '[data-age], [data-location]')
    for sub_res in sub_results:
        print(sub_res.text)
        print()

    print() 

driver.quit()
exit()

# next steps:
# decode the addresses so you can see full address
# filter results? 
# potentially add more search fields for user