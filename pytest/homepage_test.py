# from selenium import webdriver

# browser = webdriver.Firefox()
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions
from pytest.page_object import homepage

opts = FirefoxOptions()
opts.add_argument("--headless")

binary = FirefoxBinary('/usr/bin/firefox')
browser = webdriver.Firefox(firefox_binary=binary, firefox_options=opts)

def on_homepage(browser):
    homepage = Homepage(browser) #var to refer to the import; easier to refer to
    assert homepage.get_title() == 'National Treasures!'