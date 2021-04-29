# from selenium import webdriver

# browser = webdriver.Firefox()
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions
from .page_object.homepage import Homepage

opts = FirefoxOptions()
opts.add_argument("--headless")

# binary = FirefoxBinary('/usr/bin/firefox')
browser = webdriver.Firefox(options=opts)

def test_on_homepage():
    homepage = Homepage(browser) #var to refer to the import; easier to refer to
    assert homepage.get_title() != 'National Treasures!'

