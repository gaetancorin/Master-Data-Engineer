from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()  # Remplacez par webdriver.Firefox() si vous utilisez Firefox
driver.get("https://www.etoro.com/login")
print(driver.title)

# username_input = driver.find_element(By.ID, "username")

# username_input.send_keys("picpognon")

time.sleep(250)

driver.quit()