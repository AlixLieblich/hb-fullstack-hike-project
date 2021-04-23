from selenium.webdriver.common.by import By

class Homepage:
  HOMEPAGE_TITLE = (By.CSS_SELECTOR, 'h3')

@classmethod
def __init__(self, browser):
    self.browser = browser #define browser
            
            # Wait implicitly for elements to be ready before attempting interactions
    driver.implicitly_wait(10)
  
        # Return the driver object at the end of setup
    yield driver
        
        # For cleanup, quit the driver
    driver.quit()
        
    def get_title(self):
        browser.get('http://localhost:5001')
        homepage_title = self.browser.find_element(*self.HOMEPAGE_TITLE)
        return homepage_title.get_text()    #get_text is method that belongs to Class element (so when homepage title is defined as an element - pytest all have the same methods available)
