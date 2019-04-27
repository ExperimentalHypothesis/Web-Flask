from selenium import webdriver

browser = webdriver.Firefox(executable_path="/home/nirvikalpa/Documents/python/repos/web_flask/__seltest/geckodriver")
browser.get('http://www.lynx.cz')
element = browser.find_element_by_tag_name('h1')
assert element.text == 'Example Domains'
browser.quit()