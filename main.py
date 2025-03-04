from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time

tiermakerurl = input("Url to the tiermaker live? (https://live.tiermaker.com/abcdef): ")
itera = input("How often to vote: ")
imgsrc = input("Who to vote for? (image src url): ")
whattovote = input("RGB of the option to vote for (seperated with comma, e.g. '255, 127, 128'): ")
for i in range(itera):
    # Set up the Edge driver in no gpu mode
    service = Service(EdgeChromiumDriverManager().install())
    options = webdriver.EdgeOptions()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Edge(service=service, options=options)

    start_time = time.time()

    # Open the website
    driver.get(tiermakerurl)

    # Click the button with specified classes
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.fc-button.fc-cta-consent.fc-primary-button"))
    ).click()

    # Click the image with the specified src, using JavaScript click
    image = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//img[@src='{imgsrc}']"))
    )
    driver.execute_script("arguments[0].click();", image)

    # Click the div with class "vote-square" and specific background color
    vote_square = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'vote-square') and contains(@style, 'background-color: rgb({whattovote})')]"))
    )
    driver.execute_script("arguments[0].click();", vote_square)
    time.sleep(2)

    # Close the browser
    driver.quit()

    end_time = time.time()
    print(f"Script completed in {end_time - start_time:.2f} seconds")
