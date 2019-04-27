from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys


driver = webdriver.Firefox(executable_path="/home/nirvikalpa/Documents/python/repos/web_flask/__seltest/geckodriver")

driver.get("http://127.0.0.1:5000/")



driver.find_element_by_link_text("Home").click()
driver.find_element_by_link_text("About").click()
driver.find_element_by_link_text("Systems").click()
driver.find_element_by_link_text("Login").click()




def pass_match():
    driver.find_element_by_id("name").send_keys("name")
    driver.find_element_by_id("email").send_keys("email@email.com")
    driver.find_element_by_id("username").send_keys("username")
    driver.find_element_by_id("password").send_keys("pass")
    driver.find_element_by_id("confirm").send_keys("pass")
    driver.find_element_by_xpath("//input[@type='submit' and @value='Submit']").click()

def pass_mismatch():
    driver.find_element_by_link_text("Login").click()
    driver.find_element_by_id("name").send_keys("name")
    driver.find_element_by_id("email").send_keys("email@email.com")
    driver.find_element_by_id("username").send_keys("username")
    driver.find_element_by_id("password").send_keys("pass")
    driver.find_element_by_id("confirm").send_keys("xxxx")
    driver.find_element_by_xpath("//input[@type='submit' and @value='Submit']").click()

pass_match()
pass_mismatch()



time.sleep(4)

driver.quit()

